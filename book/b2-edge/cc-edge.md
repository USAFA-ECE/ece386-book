# C&C: Edge Inference

This is a **Clarify and Communicate** lesson.
The objective of a C&C is to:

1. *Clarify* any questions, perceptions, or misconceptions about the preceding lessons
2. *Communicate* what you have learned.

These classes are motivated by the harsh reality that because you've had a smidgen of AI experience,
people will now regard you as something of an expert and ask you all sorts of wild questions.

The lesson is broken into two parts:

First, an open forum for asking any question at all about the block.

Second, a closed-note written quiz. This quiz will typically have a question that requires a
written response, as well as a few multiple choice questions.
The written response is not formatted like a normal GR; rather, it may involve more role-play,
such as an email from your commander.

The C&C is graded based on your clarity of communication and your knowledge of the material.
In some cases, the answer may be "I need to go do some research and find that out" - if so,
specify where you'd look for the answer and approximately how long you think it would take.

## What to Study

This course is cumulative, but specifically this C&C will focus on...

### New content

- [Using machine learning to index text from billions of images](https://dropbox.tech/machine-learning/using-machine-learning-to-index-text-from-billions-of-images).
    This is one of my all-time favorite blog posts.

### Learning Outcomes

The specific outcomes in **bold** below will be emphasized for this C&C.

#### 1: Discuss the usage of machine prediction to aid in making risk-based decisions in an uncertain or adversarial environment

I can discuss Artificial Intelligence like a technical officer.

1. I can frame a problem in terms of Prediction, Judgement, Decision, Action, Feedback and effectively communicate it to senior leaders as a way of reducing risk.
2. **I can analyze the impact of trade-offs between latency and throughput during inference on the system's ability to solve the original problem.**
3. I can identify hidden factors in a dataset that may cause unintended discrimination or false confidence and make ethical recommendations on how to proceed.

#### 2: Design and construct a machine learning training pipeline using contemporary frameworks and tools

I can use the engineering method to go from an ill-defined problem to a working training pipeline in Jupyter Notebook.

1. **I can wrangle a dataset so that it can be used for training.**
2. I can identify an appropriate base model and loss function for a particular problem
3. I can perform transfer learning on open-source models using PyTorch and TensorFlow Keras.
4. I can assess model performance against test and validation datasets.

#### 3: Evaluate the engineering tradeoffs between devices when deploying models for inference

I can deploy a trained model to the right device and determine if it solves my problem.

1. **I can identify and apply the appropriate quantization techniques (e.g., linear quantization) and datatypes for specific hardware using PyTorch and TensorFlow Lite.**
2. I can evaluate the impact of quantization on model performance relative to the base model.
3. I can use Docker to build and publish container images for running AI inference.
4. **I can deploy a model to the appropriate hardware, considering throughput, latency, power, and bandwidth constraints, and determine if it effectively solves the problem.**

#### 4: Demonstrate the impact of computer architecture on AI computation

I can apply ECE 281 and 485 to AI.

1. **I can describe the common mathematical operations within a DNN and how they are executed on computer hardware.**
2. I can illustrate why GPU architecture enables higher throughput for certain operations, compared to a CPU.
3. **I can illustrate why the Cortex-M4 processor can provide better inference performance with quantized models, compared to float32 models.**
4. I can outline the geopolitical and defense consequences of chip manufacturing scarcity.
