    Title: Lightweight dashboards and reports with Irydium and surge.sh
    Date: 2021-08-03T11:37:35
    Tags: Irydium, Recurse

One of my main goals with [Irydium] is to allow it to be a part of as many possible data science and engineering workflows
(including ones I haven't thought of).
Yes, like [Iodide] and other products, I am (slowly) building a web-based interface for building and sharing dashboards, reports, and similar things.
However, I also want to fully support local and command-line based workflows.
Beyond the obvious utility of being able to use your favorite text-editor to create documents, this also opens up the possibility of combining Irydium with other tools and workflows.
For a slightly longer exposition on why this is desirable, I would highly recommend reading Ryan Harter's post on the subject: [Don't make me code in your text box].

## Using the irydium template

To make getting started easier, I just created an [irydium-template]: a simple GitHub repository which contains a minimal markdown document (a [big mac index] visualization) which you can use as a base, as well as a bit of npm scaffolding to get you up and running quickly.
To check it out via the console, I recommend using [degit] (the tool of choice for such things in the Svelte community):

```bash
npx degit git@github.com:irydium/irydium-template.git my-notebook
npm install
npm run dev
```

This will create a webserver which renders the document (index.md) at port 3000, along with some debugging options.
As you edit and save the document, the site should update automatically.

## Publishing your work

When you're happy with the results, you can create a static version of the site (an `index.html` file) by running `npm run build`.
You can publish this via whatever you like: GitHub pages, Netlify / Vercel or... my new favorite service, [surge.sh].
Surge provides a really simple hosting service for hosting static sites and works great with Irydium.
Installing _and_ running it locally is two commands:

```bash
npm install -g surge
surge
```

Surge will prompt you for an email and a password, then will automatically publish your site at a unique URL.
As an example, I published a site for the above template: [few-blade.surge.sh](https://few-blade.surge.sh)

Interested in chatting more about this? Feel free to reach out on the [Irydium Gitter chat].

[irydium]: https://irydium.dev
[iodide]: https://alpha.iodide.io
[don't make me code in your text box]: https://blog.harterrt.com/coding_in_textboxes.html
[irydium-template]: https://github.com/irydium/irydium-template
[big mac index]: https://www.economist.com/big-mac-index
[degit]: https://github.com/Rich-Harris/degit
[surge.sh]: https://surge.sh
[irydium gitter chat]: https://gitter.im/irydium/community
