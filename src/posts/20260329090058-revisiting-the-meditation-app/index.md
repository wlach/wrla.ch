---
tags: [meditation, apps]
---

# Revisiting the meditation app

In 2014, I [wrote a little HTML5 meditation app](https://archive.wrla.ch/blog/2014/08/a-new-meditation-app/).

For various reasons, I felt this was a concept worth resurrecting. I gave it some small updates for this iteration:

- Light/dark mode
- Trimmed background hiss on the original sound
- Uses modern web standards: service workers and [wake locks](https://developer.mozilla.org/en-US/docs/Web/API/Screen_Wake_Lock_API)
- Remove jQuery/iCanHaz.js dependencies (just uses raw DOM APIs)

No JavaScript build system, no frameworks, no business model, no gamification, no courses.
Just a timer.
Less than 300k: virtually of that a pleasant bell sound.
Free forever at [meditation.wrla.ch](https://meditation.wrla.ch) (and should keep working even if it goes down if you have a copy on your phone).

The only simpler timer is a stick of incense and a book of matches.
