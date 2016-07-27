Title: Tensorflow
Date: 2016-01-28 21:00
Status: draft

TensorFlow is a Deep learning library now release from google which has been open sourced
I think it's current limitation is that it's limited to running on a single host, although that may change in time with the open source version

Looks like for windows there isn't a native pip install available yet
https://www.tensorflow.org/versions/master/get_started/os_setup.html

TODO
1. Try building on a windows enviroment
2. If all else fails using docker is one way around it apparantly
http://stackoverflow.com/questions/33616094/tensorflow-is-it-or-will-it-sometime-soon-be-compatible-with-a-windows-work

also currently it's only setup for Cuda support with Nvidia cards
for AMD cards this will require a future update to include OpenCL support
https://github.com/tensorflow/tensorflow/issues/22

TODO look into rCUDA
https://en.wikipedia.org/wiki/RCUDA
