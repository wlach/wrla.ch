    Title: Neural networks mystify me
    Date: 2023-04-15T10:33:52
    Tags: AI

Spent a good chunk of a week off (re)learning the basics of neural networks: forward propagation, gradient descent, loss functions.
It's taking some time, but gradually I feel some level of understanding is taking hold.
What kind of continues to amaze me is how simple it all is: you really only need a high-school level understanding of linear algebra and calculus to understand most of what's going on behind the scenes.
Best as I can tell, the recent innovations in the last few years (in particular transformer models behind things like ChatGPT) are just refinements on top of these basic concepts.

Neural networks (there really there is nothing "neural" about them) are really not new: I remember hearing about that as an undergraduate in the early 2000s (and I think they were rather old hat even then).
At the time, they were pretty much dismissed as a warmed-over model of [behaviorism](https://en.wikipedia.org/wiki/Behaviorism), unlikely to be useful anywhere except perhaps in a few simplistic applications.
Based on what I saw at the time, I agreed and basically bought into the idea that computers are mainly useful as an adjunct to human processes, systems and intuition.

Thus, I find the fact that these systems can produce something even mildly resembling novel or creative outputs (as is the case with things like ChatGPT and Midjourney) _surprising_ - as in it wasn't something I saw coming.
Yes, much of what has been built using these technologies is overhyped and arguably dangerous.
Still, I also don't want to lose the sense of wonder that this is possible at all.
If I was mistaken about this what else might I be missing?

I feel like the best response at this point is to take a step back, learn as much as I can, and _then_ develop an opinion.
I expect this process to take at least a year, probably longer.

In case it's helpful to others, here's some literature I've been working through on these topics.

Some theoretical but approachable material for understanding the basics:

- [Hacker's Guide to Neural Networks](http://karpathy.github.io/neuralnets/): Now dislcaimed by the author as out of date, I still found its explanation of neural networks as a circuit quite helpful for building my intuition.
- [Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com/index.html): Another introduction to the basics, more refined and comprehensive than the above.
- [How to trick a neural network into thinking a panda is a vulture](https://codewords.recurse.com/issues/five/why-do-neural-networks-think-a-panda-is-a-vulture): Often the best way of understanding something is to break it.

On the ethical side:

- [On the Dangers of Stochastic Parrots](https://dl.acm.org/doi/10.1145/3442188.3445922): Good antidote to some of the hype around LLMs, incorporating an understanding of how these systems may further perpetuate social harms. Much more nuanced and interesting than most of the critiques I've seen fly by in the last few months.
- [Resisting Determinstic Thinking](https://zephoria.medium.com/resisting-deterministic-thinking-52ef8d78248c): How can we think critically about AI without falling into the trap of black/white thinking ("this is all good" vs. "this is all bad")

And some articles on how to think about LLMs from a pragmatic perspective as a programmer:

- [Think of language models like ChatGPT as a “calculator for words”](https://simonwillison.net/2023/Apr/2/calculator-for-words/): This feels right to me based on my usage of OpenAI as a "tool for thought so far" (though I don't think I've yet been able to use ChatGPT as effectively as this person).
- [Cheating is all you need](https://about.sourcegraph.com/blog/cheating-is-all-you-need): Some speculative thinking about how this stuff might play out for those of us doing programming from the internet-famous Steve Yegge.
