    Title: Training an autoclassifier
    Date: 2016-11-28T16:29:47
    Tags: Mozilla, Treeherder

Here at Mozilla, we've accepted that a certain amount of intermittent
failure in our automated testing of Firefox is to be expected. That
is, for every push, a subset of the tests that we run will fail for
reasons that have nothing to do with the quality (or lack thereof) of
the push itself.

On the main integration branches that developers commit code to, we
have dedicated staff and volunteers called sheriffs who attempt to
distinguish these expected failures from intermittents through a
manual classification process using [Treeherder](https://treeherder.mozilla.org). On any given
push, you can usually find some failed jobs that have stars beside them, this is
the work of the sheriffs, indicating that a job's failure is "nothing to worry
about":

<img src="/files/2016/11/treeherder-in-action.png"/>

This generally works pretty well, though unfortunately it doesn't help
developers who need to test their changes on Try, which have the
same sorts of failures but no sheriffs to watch them or interpret
the results. For this reason (and a few others which I won't go into
detail on here), there's been much interest in having Treeherder
autoclassify known failures.

We have a partially implemented version that attempts to do this
based on structured (failure line) information, but we've had some
difficulty creating a reasonable user interface to train it. Sheriffs
are used to being able to quickly tag many jobs with the same bug.
Having to go through each job's failure lines and manually
annotate each of them is much more time consuming, at least with the
approaches that have been tried so far.

<img src="/files/2016/11/treeherder-per-line-classification.png"/>

It's quite possible that this is a solvable problem, but I thought
it might be an interesting exercise to see how far we could get
training an autoclassifier with only the existing per-job
classifications as training data. With some recent work I've done
on refactoring Treeherder's database, getting a complete set of
per-job failure line information is only a small SQL query away:

```sql
select bjm.id, bjm.bug_id, tle.line from bug_job_map as bjm
  left join text_log_step as tls on tls.job_id = bjm.job_id
  left join text_log_error as tle on tle.step_id = tls.id
  where bjm.created > '2016-10-31' and bjm.created < '2016-11-24' and bjm.user_id is not NULL and bjm.bug_id is not NULL
  order by bjm.id, tle.step_id, tle.id;
```

Just to give some explanation of this query, the "bug_job_map"
provides a list of bugs that have been applied to jobs. The
"text_log_step" and "text_log_error" tables contain the actual
errors that Treeherder has extracted from the textual logs (to
explain the failure). From this raw list of mappings and errors,
we can construct a data structure incorporating the job, the assigned
bug and the textual errors inside it. For example:

```json
{
"bug_number": 1202623,
"lines": [
  "browser_private_clicktoplay.js Test timed out -",
  "browser_private_clicktoplay.js Found a tab after previous test timed out: http:/<number><number>:<number>/browser/browser/base/content/test/plugins/plugin_test.html -",
  "browser_private_clicktoplay.js Found a browser window after previous test timed out -",
  "browser_private_clicktoplay.js A promise chain failed to handle a rejection:  - at chrome://mochikit/content/browser-test.js:<number> - TypeError: this.SimpleTest.isExpectingUncaughtException is not a function",
  "browser_privatebrowsing_newtab_from_popup.js Test timed out -",
  "browser_privatebrowsing_newtab_from_popup.js Found a browser window after previous test timed out -",
  "browser_privatebrowsing_newtab_from_popup.js Found a browser window after previous test timed out -",
  "browser_privatebrowsing_newtab_from_popup.js Found a browser window
  after previous test timed out -"
  ]
}
```

Some quick google searching revealed that [scikit-learn](http://scikit-learn.org/) is a popular
tool for experimenting with text classifications. They even had a
[tutorial](http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html) on classifying newsgroup posts which seemed tantalizingly
close to what we needed to do here. In that example, they wanted
to predict which newsgroup a post belonged to based on its content.
In our case, we want to predict which existing bug a job failure
should belong to based on its error lines.

There are obviously some differences in our domain: test failures
are much more regular and structured. There are lots of numbers
in them which are mostly irrelevant to the classification (e.g.
the "expected 12 pixels different, got 10!" type errors in reftests).
Ordering of failures might matter. Still, some of the techniques
used on corpora of normal text documents for training a classifier
probably map nicely onto what we're trying to do here: it seems
plausible that weighting words which occur more frequently less
strongly against ones that are less common would be helpful, for
example, and that's one thing their default transformers does.

In any case, I built up a small little script to download a subset
of the downloaded data (from November 1st to November 23rd), used it
as training data for a classifier, then tested that against
another subset of test failures between November 24th and 28th.

```py
import os
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier


training_set = load_files('training')
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(training_set.data)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
clf = SGDClassifier(loss='hinge', penalty='l2',
                    alpha=1e-3, n_iter=5, random_state=42).fit(X_train_tfidf, training_set.target)

num_correct = 0
num_missed = 0

for (subdir, _, fnames) in os.walk('testing/'):
    if fnames:
        bugnum = os.path.basename(subdir)
        print bugnum, fnames
        for fname in fnames:
            doc = open(os.path.join(subdir, fname)).read()
            if not len(doc):
                print "--> (skipping, empty)"
            X_new_counts = count_vect.transform([doc])
            X_new_tfidf = tfidf_transformer.transform(X_new_counts)
            predicted_bugnum = training_set.target_names[clf.predict(X_new_tfidf)[0]]
            if bugnum == predicted_bugnum:
                num_correct += 1
                print "--> correct"
            else:
                num_missed += 1
                print "--> missed (%s)" % predicted_bugnum
print "Correct: %s Missed: %s Ratio: %s" % (num_correct, num_missed, num_correct / float(num_correct + num_missed))
```

With absolutely no tweaking whatsoever, I got an accuracy rate of 75%
on the test data. That is, the algorithm chose the correct
classification given the failure text 1312 times out of 1959. Not bad
for a first attempt!

After getting that working, I did some initial testing to see if I
could get better results by reusing some of the error ETL summary code
in Treeherder we use for bug suggestions, but the results were pretty much
the same.

So what's next? This seems like a wide open area to me, but some
initial areas that seem worth exploring, if we wanted to take this
idea further:

1. Investigate cases where the autoclassification failed or had a near
miss. Is there a pattern here? Is there something simple we could do,
either by tweaking the input data or using a better vectorizer/tokenizer?
2. Have a confidence threshold for using the autoclassifier's data.
It seems likely to me that many of the cases above where we got
the wrong were cases where the classifier itself wasn't that confident
in the result (vs. others). We can either present that in the user
interface or avoid classifications for these cases altogether (and
leave it up to a human being to make a decision on whether this is
an intermittent).
3. Using the structured log data inside the database as input to a
classifier. Structured log data here is much more regular and denser
than the free text that we're using. Even if it isn't explicitly
classified, we may well get better results by using it as our input
data.

If you'd like to experiment with the data and/or code, I've put it up on a
[github repository](https://github.com/wlach/treeherder-classifier).