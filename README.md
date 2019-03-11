# modeling-link-aggregators

Python code to submit rotated images to the Microsoft Computer Vision API + R code for visualizing it. This repository was used to create [this animation](https://twitter.com/minimaxir/status/1103676561809539072). 

The code here has been forked from Max Woolf (@minimaxir) original repo: https://github.com/minimaxir/optillusion-animation which contains the code to leverage Google's Cloud Vision API.  

All tools used:

* Python to rotate the image and get predictions from the API for each rotation.
* R, ggplot2, gganimate for building the animations.
* ffmpeg to render the animations.
* A video editor to stitch all the animations together.

**Disclaimer**: This was my first time working with gganimate (and working around a few bugs which surfaced), as a result my R code is messier than my typical R code.

## Maintaner

Fatos Ismali ([@bytebiscuit](http://www.thinkgradient.com))

## License

MIT