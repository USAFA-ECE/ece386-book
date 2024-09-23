# Live Inference 🐱 🐶

## Pre-Reading

- [Picamera2 Library Docs](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf) Chapter 1. Introduction
- [github.com/raspberrypi/picamera2/examples/tensorflow/real_time.py](https://github.com/raspberrypi/picamera2/blob/main/examples/tensorflow/real_time.py)

### Objectives

- Close the loop on the ML workflow with cats and dogs
- Conduct inference on real-life critters!

## The lab

We will have a live cat and dog for you to test your system on!

Recall that the machine learning workflow is:

1. Decide on a goal
2. Collect a dataset
    - Examine and understand the data
3. Design a model architecture
    - Consider the data input pipeline
4. Train the model
5. Convert the model
6. Run inference
7. Evaluate and troubleshoot

You have accomplished most of this in a sterile testing environment.
Now it's time to use a physical input pipeline and add in real-world chaos!

### Starting point

Complete the following code and get it to your Pi 4.

```python
# A script that uses TensorFlow Lite and Picamera
# to classify a Cat vs. Dog.
#
# Designed to use a pre-converted fine-tuned MobilenetV2 model.
```
