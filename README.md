# Boxes Around Robots
Ever wonder if using neural nets for object detection in FTC is possible? This page leads you through how!

If you'd like to see immediate results download the app on the Google Play store titled "**FTC Neural Net Demo**".

If you'd like to spend some time learning about neural nets and how you can use them in FTC, read on!

This is also the source code behind http://boxesaroundrobots.com, a website for annotating training images. The dataset of images the example app was trained on is located <a href="https://github.com/kerrj/yolodata">here</a>

# Goals
* Teach teams how to train a custom neural net object detector for use during the season
* FTC has always tried to educate students about robotics, so I hope this project can not only expand the tools in teams' toolboxes, but also teach about an exciting recent development in computer science.
* Challenge teams to push the limits of what's possible with the Android hardware.

# Contents
* <a href="https://github.com/kerrj/yoloparser/blob/master/README.md#should-i-use-neural-nets-for-object-detection">Should I use this?</a>
* <a href="https://github.com/kerrj/yoloparser/blob/master/README.md#crash-course-in-neural-nets">Background on neural nets</a>
* <a href="https://github.com/kerrj/yoloparser/blob/master/README.md#yolo">Background on YOLO</a>
* <a href="https://github.com/kerrj/yoloparser/blob/master/README.md#using-a-pretrained-neural-net-in-your-android-app">Using a pretrained YOLO model in an Android app</a>
* <a href="https://github.com/kerrj/yoloparser/blob/master/README.md#how-can-i-train-yolo-on-custom-objects">Training your own neural net</a>
* <a href="https://github.com/kerrj/yoloparser/blob/master/README.md#resources">Resources</a>

# Should I use neural nets for object detection?
The answer to this question is largely based on the specific team/person, since using them efficiently during competition would certainly take a lot of work. However, for teams/students who have the persistence to keep trying and the desire to challenge themselves and learn, using neural nets could certainly be a powerful tool in competition as well as a wonderful opportunity to learn.

It's likely Relic Recovery will include some sort of find-and-retrieve action in the game, so this could prove very useful in locating game elements.
### Pros
* Extremely accurate localization with few false positives compared to other vision processing techniques. Neural nets are state-of-the art technology which have recently been blowing all other techniques out of the water for vision processing.
* Robust against lighting and environment variation
* Able to detect as many types of objects as you want it to (any game element you want)
* Able to detect abstract and complicated objects such as robots and people
* Size, position, pose, and distance invariant
* See pictures below for examples. Note how even in dark or clutttered conditions it can still find balls accurately.
<p align="center">
<img src="/static/demo1.jpg" width="250" >
<img src="/static/demo2.jpg" width="250" >
<img src="/static/demo3.jpg" width="250" >
<img src="/static/demo4.jpg" width="250" >
<img src="/static/demo5.jpg" width="250" >
<img src="/static/demo6.jpg" width="250" >
<img src="/static/demo7.jpg" width="250" >
<img src="/static/demo8.jpg" width="250" >
</p>

### Cons
* Currently, processing each frame takes about 700ms, which is pretty slow for vision processing. That said, Google has announced Tensorflow Lite coming in the next few months, which will tremendously increase the speed of processing by supporting phones' GPUs.
* Requires large amounts of data to train detection of new objects (code for the website is intended to help teams with this).


# Crash course in neural nets
Let's start with a little background, If you've made it this far I'll assume you're at least a bit interested in pursuing neural nets for use this season. First I'll start by saying: neural nets sound awfully intimidating at first, but I assure you they aren't nearly as confusing as they may seem at first. Plus, I've done as much I can to simplify the process for beginners so you can do as little work as copy pasting some code into your app, or as much digging as you want if you find yourself hooked (like me).

Neural nets are a computer scientist's attempt at mimicking the processes occuring inside a biological brain with math. Instead of using electrolytes, dendrites, synaptic gaps, and a whole slew of neurological jargon, neural nets are at their core simply multiplying and adding numbers in a structured way, sort of like a tree. They typically take one input and produce one output, with a bunch of neurons between. A neuron is simply a dot product: it takes the dot product of a vector of "weights" with the outputs from the previous layer, and sends that output downstream to all neurons in the next layer. The diagram below shows a simple single-input-single-output network with 2 hidden layers of 4 neurons each.

<p align="center"><img src="/net.jpeg"></p>

You might be asking, how does this network output anything meaningful? Right now, it doesn't, because all the weights are randomized to begin. Bear with me a second, let's imagine that the three input values to our network are *[temperature, humidity, time of day]*, and the output value is the number of people at Miami Beach. *Here's where the interesting part comes*: if we **train** the network with real life data, also called the "ground truth," or "training data" it can **learn** the correlation between temperature, humidity, time of day, and the number of people at Miami Beach. Through a process called "backpropagation," the neural net slowly adjusts the weights in every neuron based on the real life training data until it starts to more accurately predict the number of people. This can be a long process, but with a relatively small net it would probably only take a matter of minutes to train up. **After** training, you have a network which can **predict** the number of people at Miami Beach based on our 3 input parameters. That's the core concept behind neural networks.

This can be expanded to analyze many different types of input data, including images. The type of neural net used to process images is called a convolutional neural network (CNN), which have a slightly different structure from what we just discussed, but still have the same general principle of training neurons' weights with ground truth data.

If you'd like to *really* learn about neural networks, I've included several videos and other resources at the end of this document.

## YOLO
Neural nets have been around since the later 1900's, but have only very recently (we're talking since 2012) taken off, largely due to the increased availability of training information, and faster processors. They have become very successful at classifying images, translation, object detection, and much more. We will only focus on object detection here. The neural net we will use here is called "You Only Look Once" (yes YOLO). YOLO is a new (2016) architecture for single-pass object detection, meaning that the neural net does all the work, taking an image as input and outputting bounding boxes. It is one of the fastest options available, capable of running on a desktop GPU at hundreds of FPS, and so it is a good choice to use on phones which are much slower. The link to the original paper as well as more resources are included at the bottom of this document. We won't spend much time on the architecture of this net, but it is important to understand a few things about it:
* **Size:** The version of YOLO we are using has roughly 45 million trainable parameters, and about 10 layers of neurons. This may sound like an enormous amount, but it is actually pretty small as modern nets go, and indeed the version which runs on the phone is already a trimmed version of the full net. This sacrifices a bit of accuracy in return for speed.
* **I/O:** The input to the network is a 416x416 RGB image, and the output is a set of bounding box predictions
* **Training:** Training this network requires images with ground truth bounding boxes drawn, hence http://boxesaroundrobots.com

## Tensorflow
Tensorflow is a recently launched, quickly growing, open-source framework for neural nets developed by Google. You probably use Tensorflow on a daily basis, since it is the framework Google uses in their search engine for intelligent results and much more. It is what we will use to train and execute our neural net, both on desktops and on mobile devices.

# Using a pretrained YOLO model in your Android app
If you just want to see something work, download the full example app on the Google Play Store titled "**FTC Neural Net Demo**". All the source code is located <a href="http://github.com/kerrj/yoloexampleapp">here.</a>

**NOTE**:*This section and the example app currently use TensorflowInferenceInterface for exectuting the neural net. When Tensorflow Lite is released that will become obsolete, and this section will be updated.*

Using a pretrained YOLO network in your application is actually quite straightforward. The example app is ready-to-go and should compile onto a phone provided you have all SDK and NDK tools installed. However, **to use the framework in your own app, you need to do 3 things**:

1. Copy the following lines into your build.gradle. After that, you should be able to us TensorflowInferenceInterface freely.

```
//add these to the base of build.gradle
allprojects {
    repositories {
        jcenter()
    }
}

//add this to the dependencies of build.gradle
compile 'org.tensorflow:tensorflow-android:+'
```
*Do the following if you want to use the camera stream as well, not just the neural net*

2. Copy <a href="https://github.com/kerrj/yoloexampleapp/blob/master/app/CMakeLists.txt">CMakeLists.txt</a> into your /app directory.
3. Copy the entire <a href="https://github.com/kerrj/yoloexampleapp/blob/master/app/src/main/cpp">cpp directory</a> into your src/main directory.

The last two steps are necessary for converting image formats. They are native functions (written in C++) because they run much faster than Java, so expensive operations like image processing are much more efficient (20ms in native compared to 100+ in java).

## App structure
* The class which carries out detection is **TensorflowYoloDetector**. Simply call the recognizeImage() method in this class to retrieve a list of bounding boxes for a given input bitmap (must be 416x416 pixels).
* **MainActivity** is the class which initializes all relevant objects and processes frames from the camera. 
* **CameraInitializer** is responsible for setting up a camera stream and delivering frames
* **BitmapUtils** and **ImageUtils** are static classes which handle, among others, YUV->RGB conversion, bitmap resizing, and bitmap cropping.

# How can I train YOLO on custom objects?
This section leads you through training YOLO to detect a new object. It contains:
* Installation
* Collecting training data
* Training
* Deploying 

## Installation
Training YOLO to detect a new object is a bit more labor-intensive, but isn't particularly difficult. It requires installing a few components which can be frustrating sometimes. I will list the components you need installed below:
### Required
* <a href="https://www.python.org/downloads/release/python-353/">Python 3.5.3</a>
* <a href="https://www.tensorflow.org/install/">Tensorflow python</a> (pip installation is the easiest). **Note**: if you are on a windows or Linux machine with an NVIDIA GPU, I highly recommend following installation instructions for the GPU version of tensorflow, since it will drastically speed up training.
* <a href="https://github.com/thtrieu/darkflow">Clone Darkflow</a>. Follow installation instructions in the readme.

### Optional
*While not strictly required to function, the following allows greater control over your neural nets and has some optimization techniques which make execution faster on mobile devices.*
* Follow instructions for installing <a href="https://docs.bazel.build/versions/master/install.html">Bazel</a>. You can say no to all the options it asks for.
* Clone the <a href="https://github.com/tensorflow/tensorflow">Tensorflow repository</a>
* Run the "configure" executable which is in the parent directory of the repository, this initializes Bazel

## Collecting training data
One of the most important parts of developing a successful neural net is supplying high quality training data, and a lot of it. As a general rule of thumb, for simple objects like balls a diverse set of a few hundred training images of balls is sufficient. However, for more complex objects like robots that number should be at least a thousand. The pretrained neural net for detecting robots in the example app was trained on 1033 robots, about 300 red balls and 300 blue balls. Here are some good practices for collecting a training set:
* Include many different **poses** of the desired object(s)
* Include many different **backgrounds** and **lighting conditions** of the desired object(s)
* Include many different **sizes** of the desired object(s) if you want to detect it at many distances.
* Draw bounding boxes in a **consistent** way, for example try to leave the same margin around the object, instead of drawing some boxes close and some much further away.

This task is made easy with <a href="http://boxesaroundrobots.com">the website</a> since it handles all annotation parsing for you. All you have to do is:
* Upload all the images you want annotated to a (public) GitHub repo
* Go to <a href="http://boxesaroundrobots.com">boxesaroundrobots.com</a> and enter the GitHub username the repo is owned by, and the repo name. Also enter a list of objects you want to parse like "ball,robot,yogaball".
* Follow instructions to annotate images
* Download a zip of your annotations with the provided link.

## Training
After you've collected a set of training images and have .xml annotations for each, you can now train your model! The documentation at Darkflow does a good job explaining the process, so I won't detail it here. You are interested primarily in the section of the readme titled "Training new model".

Make sure you use the
```
--savepb
```
tag to save the output of training, this .pb file will be needed in the next step.

The loss of your model represents how well it is performing at the task, with larger numbers indicating worse performance. If you training set is working, the loss will quickly drop, then level off. A well performing model will typically bottom out around 1-2. If your loss doesn't fall, the data is probably corrupted somehow. If it drops but bottoms out at a large number like 15 your training set is probably too difficult, small, confusing, or erroneous.

## Deploying
*Finally!* You now have a trained model saved in a .pb file!
### Quickstart
To quickly deploy your neural net into your android app:
* Paste the .pb file into the assets folder of your app.
* Edit the constructor for TensorflowYoloClassifier to point to your file:
```
c = TensorFlowYoloDetector.create(getAssets(), "file:///your-file-name.pb", ...);
```
* Go to the TensorflowYoloDetector and change NUM_CLASSES to however many objects your net was trained to detect. 
* Edit the LABELS array to match the labels.txt your net was trained on

### Optimizing
This step requires the Tensorflow source code repository and Bazel from the optional installation instructions.
If you'd like to squeeze more speed out of your net, follow instructions for optimizing your graph <a href="https://github.com/tensorflow/tensorflow/tree/master/tensorflow/tools/graph_transforms/#optimizing-for-deployment">here</a>.
# Resources
### Websites
* <a href=https://github.com/thtrieu/darkflow>Darkflow GitHub, open-source method of training custom YOLO models</a>
* <a href=https://pjreddie.com/darknet/yolo/>YOLO website (includes research paper)</a>
* <a href=https://tensorflow.org>Tensorflow website</a>

### Videos
* <a href="https://www.ted.com/talks/fei_fei_li_how_we_re_teaching_computers_to_understand_pictures">TED talk in layman's terms on neural nets for image processing</a>
* <a href="https://www.youtube.com/watch?v=uXt8qF2Zzfo">Lecture on mathematics of neural nets, also watch 12.b</a>
* <a href="https://www.youtube.com/watch?v=u6aEYuemt0M">Talk on specifics of neural nets for image processing</a>
* <a href="https://www.youtube.com/watch?v=1L0TKZQcUtA">Survey of neural nets for learning, not specifically targeted for image processing</a>
* <a href="https://www.youtube.com/watch?v=AgkfIQ4IGaM">Fascinating demonstration "under the hood" of neural nets</a>
* <a href="https://www.youtube.com/watch?v=NM6lrxy0bxs">Presentation about YOLO</a>
