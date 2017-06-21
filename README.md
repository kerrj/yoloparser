# Boxes Around Robots
This is the source code behind http://boxesaroundrobots.com, including all training images and processed annotations.
# Goals
The long-term goal of this project is to give FTC teams a relatively streamlined interface to use neural networks for object detection during competitions. Broken down, this means my intention is to enable teams to:
* Transplant a pre-trained network into their robots which already detects game elements like robots and balls
* Create their own training data and train a custom neural net object detector

FTC has been forging forward recently, giving teams access to more powerful processors, sensors, and most importantly a camera. I hope this project can keep expanding the tools in teams' toolboxes, as well as teach about an exciting recent development in computer science.
# Using Neural Nets for Object Detection
![](/samples/demo1.jpg?raw=true)
![](/samples/demo2.jpg?raw=true)

Example of a neural net detecting balls in adverse conditions using training data from this repository.

Let's start with a little background, If you've made it this far I'll assume you're at least a bit interested in pursuing neural nets for use this season. First I'll start by saying: neural nets sound awfully intimidating at first, but I assure you they aren't nearly as confusing as they may seem at first. Plus, I've done as much I can to simplify the process for beginners so you can do as little work as copy pasting some code into your app, or as much digging as you want if you find yourself hooked (like me).
## What are neural nets?
In short, neural nets are a computer scientist's attempt at mimicking the processes occuring inside a biological brain with math. Instead of using electrolytes, dendrites, synaptic gaps, and a whole slew of neurological jargon, neural nets are at their core simply multiplying and adding numbers in a structured way, sort of like a tree. They typically take one input and produce one output, with a bunch of neurons between. A neuron is simply a dot product: it takes the dot product of a vector of "weights" with the outputs from the previous layer, and sends that output downstream to all neurons in the next layer. The diagram below shows a simple single-input-single-output network with 2 hidden layers of 2 neurons.

Neural nets have been around since the later 1900's, but have only very recently (we're talking since 2012) taken off, largely due to the increased availability of training information, and faster processors. They have become very successful at classifying images, translation, object detection, and much more. We will only focus on object detection here.
