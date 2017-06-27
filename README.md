# Boxes Around Robots
This is the source code behind http://boxesaroundrobots.com, including all training images and processed annotations. It is also the name of a personal project to educate FTC teams in how to use neural nets for image processing.

### Webpage endpoints
* /: Main page for marking images
* /review: page for scrolling through annotated images and viewing their bounding boxes
* /getnumannotations: returns the number of annotated images
* /remaining: returns the number of images left to be annotated

# Goals
The long-term goal of this project is to give FTC teams a relatively streamlined interface to use neural networks for object detection during competitions. Broken down, this means my intention is to enable teams to:
* Transplant a pre-trained network into their robots which already detects game elements like robots and balls
* Create their own training data and train a custom neural net object detector

FTC has been forging forward recently, giving teams access to more powerful processors, sensors, and most importantly a camera. FTC has always tried to educate students about robotics, so I hope this project can not only expand the tools in teams' toolboxes, but also teach about an exciting recent development in computer science.

### Contents
* Should I use this?
* Background on neural nets
* Background on YOLO (neural net object detector)
* Using a pretrained neural net in an Android app
* Training your own neural net
* Resources

## Should I use neural nets for object detection?
The answer to this question is largely based on the specific team/person, since using them efficiently during competition would certainly take a lot of work, more so than just using color sensors and range meters. However, for teams/students who have the persistence to keep trying and the desire to challenge themselves and learn, using neural nets could certainly be a wonderful opportunity. I've summarized some of the pros and cons of using them in a strictly competition sense below:

### Pros
* Extremely accurate localization with few false positives compared to other vision processing techniques. Neural nets are state-of-the art technology which have recently been blowing all other techniques out of the water for vision processing.
* Able to detect as many types of objects as you want it to (any game element you want)
* See pictures below for examples
![](/samples/demo1.jpg?raw=true)
![](/samples/demo2.jpg?raw=true)
### Cons
* Currently, each frame takes about 700ms, which is pretty slow for vision processing. That said, Google has announced Tensorflow Lite coming in the next few months, which will tremendously increase the speed of processing by supporting phones' GPUs.
* Requires large amounts of data to train detection of new objects (code for the website is intended to help teams with this).


## Crash course in neural nets
Let's start with a little background, If you've made it this far I'll assume you're at least a bit interested in pursuing neural nets for use this season. First I'll start by saying: neural nets sound awfully intimidating at first, but I assure you they aren't nearly as confusing as they may seem at first. Plus, I've done as much I can to simplify the process for beginners so you can do as little work as copy pasting some code into your app, or as much digging as you want if you find yourself hooked (like me).

Neural nets are a computer scientist's attempt at mimicking the processes occuring inside a biological brain with math. Instead of using electrolytes, dendrites, synaptic gaps, and a whole slew of neurological jargon, neural nets are at their core simply multiplying and adding numbers in a structured way, sort of like a tree. They typically take one input and produce one output, with a bunch of neurons between. A neuron is simply a dot product: it takes the dot product of a vector of "weights" with the outputs from the previous layer, and sends that output downstream to all neurons in the next layer. The diagram below shows a simple single-input-single-output network with 2 hidden layers of 4 neurons each.
![](/net.jpeg?raw=true)

You might be asking, how does this network output anything meaningful? Right now, it doesn't, because all the weights are randomized to begin. Bear with me a second, let's imagine that the three input values to our network are *[temperature, humidity, time of day]*, and the output value is the number of people at Miami Beach. *Here's where the interesting part comes*: if we **train** the network with real life data, also called the "ground truth," or "training data" it can **learn** the correlation between temperature, humidity, time of day, and the number of people at Miami Beach. Through a process called "backpropagation," the neural net slowly adjusts the weights in every neuron based on the real life training data until it starts to more accurately predict the number of people. This can be a long process, but with a relatively small net it would probably only take a matter of minutes to train up. **After** training, you have a network which can **predict** the number of people at Miami Beach based on our 3 input parameters. That's the core concept behind neural networks.

This can be expanded to analyze many different types of input data, including images. The type of neural net used to process images is called a convolutional neural network (CNN), which have a slightly different structure from what we just discussed, but still have the same general principle of training neurons' weights with ground truth data.

If you'd like to *really* learn about neural networks, I've included several videos and other resources at the end of this document.

## YOLO
Neural nets have been around since the later 1900's, but have only very recently (we're talking since 2012) taken off, largely due to the increased availability of training information, and faster processors. They have become very successful at classifying images, translation, object detection, and much more. We will only focus on object detection here. The neural net we will use here is called "You Only Look Once" (yes YOLO). The link to the original paper as well as more resources are included at the bottom of this document. We won't spend much time on the architecture of this net, but it is important to understand a few things about it:
* **Size:** The version of YOLO we are using has roughly 45 million trainable parameters, and about 10 layers of neurons
* **I/O:** The input to the network is a 416x416 RGB image, and the output is a set of bounding box predictions
* **Training:** Training this network requires images with ground truth bounding boxes drawn, hence http://boxesaroundrobots.com

# Using a pretrained neural net in your Android app
(section under construction)
