# What is it?
The project is a python3 library based on the open NSFW developed by yahoo which is a convolutional machine learning model. Using this lib you'll be able to recognize what images have sexual content by a score of 0 to 1.

# How do I run it?

First, we need to meet some requirements:
- Linux
- numpy
- pillow
- caffe

After all the libraries and their dependencies are installed, we just need to call the Classifier in our python3 application as the example below:

```
from Classifier import *

classifier = Classifier(filePath)
sexualContent = classifier.getScore() >= 0.8
```
