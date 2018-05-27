    Title: Some thoughts on opinion polling in the Ontario 2018 election
    Date: 2018-05-27T12:57:30
    Tags: Polling, Statistics

Like many, I've been a bit worried about the Ontario election, and
have been rather obsessively checking a site called the [Ontario Poll
Tracker](https://newsinteractives.cbc.ca/onvotes/poll-tracker/).

<center>
  <img style="width:400px" srcset="/files/2018/05/CBC-poll-tracker-main.png 2x"/>
</center>

It has nice and shiny graphs and uses authoritative language and purports to
provide a scientific analysis which predicts the election.  Despite this, it's
my assertion that this kind of predictive modelling is nothing more than snake
oil. I keep on reminding myself that I shouldn't take it too seriously, but
haven't been too successful so far. This blog post is a reminder to myself on
why I should stop reloading that site so much, but maybe it will be helpful to
others as well. As a warning, it's not going to say anything particularly
novel. If you have any kind of background in statistics at all, this is
probably going to be quite boring.

First, a story. Way back when I had just graduated from university in 2003, I
worked briefly at an "opinion research company", telephoning people for
various opinion surveys. It was easily the worst job I ever had, horrible for
both the people doing the calling and those who were being called.

The work was mind-numbingly repetitive. Get assigned a poll. Telephone people
using an autodialer, work through the script using the DOS-based software the
call center was using where they would answer multiple-choice questions.
Repeat as many times as you can over the course of an hour. The topics were
varied, but roughly 50/50 political parties doing private polling and
businesses trying to get marketing data. In either case, the questions were
definitely of the "lowest common denominator" type question (i.e. "Which
products are you likely to buy in the next 12 months", "If an election were
held today, would you vote for party A, B, or C?")

One of the few benefits of tedious jobs is that they give you time
to think about things. In this case, one of my distinct experiential
take aways as that the results that we were getting were incredibly
unrepresentative.

For a poll to be valid it is supposed to be "reasonably" reflective of
the general population. Over the quantities that we're talking about,
that means anywhere from hundreds of thousands to millions of
people. If we were able to truly randomly sample a small number
from this group, the results are likely to be "representative of the
whole" (within some confidence interval). Let's write up a small
python script to confirm this intuition:

```py
# 100,000 random numbers between 0 and 1
>>> full_population_size = 100000
>>> full_sample = [random.random() for i in range(full_population_size)]

# average over entire result
>>> sum(full_sample) / full_population_size
0.501036568906331

# pull out 100 randomly selected values from the full sample and
# get their average
>>> random_subset_size = 100
>>> random_subset = [full_sample[i] for i in [int(random.random()*100000) for j in
                     range(random_subset_size)]]
>>> sum(random_subset) / random_subset_size
0.4924555517866068
```

Only a small fraction of the total population, but a result within 1%
of the true value. Expressing it this way makes random sampling almost
like a tautology. You probably learned this in high school. Great right?

Unfortunately, real life always comes in to disturb these assumptions, as it
always does.  You see, there were all sorts of factors that would affect who
we would be talking to and thus get datapoints from. At that time, most of the
population still had a land-line telephone but there were a wealth of other
factors that meant that we weren't getting a truly randoms sample of data. Men
(at least men under 60 or so) were much less likely to answer a telephone
survey than women.  For general opinion surveys, we were calling at a specific
time of day when *most* people were likely to be available -- but that
certainly wouldn't apply to everyone. Some people would work night shifts,
etc., etc. In our example above, this would be like taking out half the
results over (say) 0.75 from our sample -- the end result would tend to skew
much lower than the true value.

Just for fun, let's try doing that and see how it affects the results:

```py
# if we take away approximately half the results with a value of
# >0.75, the population we are sampling from is reduced proportionally
>>> full_sample_with_half75_removed = [v for v in full_sample if v <= 0.75 or random.random() < 0.5]
>>> len(full_sample_with_half75_removed)
87607

# the sampled value is then proportionally skewed downwards (because
# a large percentage of the high values are no longer available)
>>> random_subset = [full_sample_with_half75_removed[i] for i in
                     [int(random.random()*len(full_sample_with_half75_removed)) for j in
                      range(random_subset_size)]
                    ]
>>> sum(random_subset)/random_subset_size
0.4585241853943395
```

To try and get around this problem, the opinion polling company would try to
demographically restrict who we were surveying past a certain point, so that
the overall sample of the poll would reasonably reflect the characteristics of
the population.  This probably helped, but there's only so much you can do
here. For example, if you correct for the fact that men aged 20 to 60 are less
likely to answer an opinion survey, your sample is going to now consist of
those weird men who *do* answer opinion surveys. Who knows what effect that's
going to have on your results?

I want to be clear here: this is a methodological problem. Running
more opinion polls doesn't help. Probably some samples will be more
affected by errors than others, but the problem remains regardless.
Actually, let's show this trivially for our small example:

```py
>>> skewed_averages = []
>>> for i in range(10):
...   full_sample_with_half75_removed = [v for v in full_sample if v <= 0.75 or
                                         random.random() < 0.5]
...   random_subset = [full_sample_with_half75_removed[i] for i in
          [int(random.random()*len(full_sample_with_half75_removed)) for j in
           range(random_subset_size)]]
...   skewed_averages += [sum(random_subset)/len(random_subset)]
...
>>> skewed_averages
[0.4585241853943395, 0.4271412530288919, 0.46414511969024697, 0.4360740890986547,
 0.4779021127791633, 0.38419133106708714, 0.48688298744651576, 0.41076028280889915,
 0.47975630795860363, 0.4381467970818846]
```

Each time we resampled from the main population and got a different
result, but the end result was still one which was *far* off from what
we know in this case was the true value (0.5). Sampling from bad data
doesn't make up for these problems, it just gives you more bad results.

Now, flash forward to 2018. Almost no one under 50 has a land-line anymore,
people who have cell phones most often don't answer to unknown callers. And
don't even get me started on how to find a representative set of people to
participate in an "online panel".  What validity do polls have under these
circumstances? I would say very little and probably more importantly we
don't even have a clear idea of *how* our modern polls are skewed.

There has been no shortage of thinking on how to correct for these problems
but in my opinion it's all just speculative and largely invalid. You
can't definitively solve the kind of uncertainty we're talking about here by
coming up with "just so" stories about how you've corrected for it. We might have
some ideas about how our data is biased, but short of sampling the entire
population and then seeing how our sampling method falls into that superset
(which is impossible) there is no way of confirming that our efforts to
correct for that bias were effective.

With respect to the Ontario election which I alluded to above, the one thing
that I am getting from the data is that support for the NDP (across the highly
unrepresentative sample used in the polls) is increasing precipitously and
that for the PC's is decreasing almost as sharply. That seems to be a real
phenomenon.  We don't know whether that crosses over to the general population
but it doesn't seem unreasonable to think it does. Exactly how is
another question, and I make no assertions there.

<center>
  <img style="width:400px" srcset="/files/2018/05/CBC-poll-tracker-trend.png 2x"/>
</center>

tl;dr If you don't like the idea of [Doug
Ford](https://www.theguardian.com/world/2018/apr/30/doug-ford-ontario-conservative-trump-comparison-canada)
in power, there is no reason to panic based on sites like the Ontario Poll
Tracker. Spend your time doing something more productive, like convincing your
friends and relatives to vote for someone who is not Conservative.
