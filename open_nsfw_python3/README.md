# `latest version 0.0.5` 

# What is this?
The open_nsfw_python3 is a python3 library based on the open NSFW developed by yahoo which is a convolutional machine learning model. Using this lib you'll be able to recognize images which have sexual content by a score from 0 to 1.

## Requirements
- caffe

## Installing
```
pip install open-nsfw-python3
```

We are going to need to install the caffe lib. This repository has a Dockerfile which can tell you how to build a Linux environment with caffe step by step.

After all the libraries and their dependencies are installed, you just need to import the NSFWClassifier class in your python3, create a new instance of the class, and start to predict!

## Using Example:
```
from open_nsfw_python3 import NSFWClassifier

classifier = NSFWClassifier()
score = classifier.get_score('image.jpg')

print(score)
0.8041712045669556
```

Copyright 2016, Yahoo Inc.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
