# Machine Learning Workflow

## Pre-Reading

*TinyML* Chapter 3: The Deep Learning Workflow

### Objectives

- Describe the ML workflow for embedded systems
- Apply the ML workflow for embedded systems

## The Machine Learning Workflow for Embedded Devices

There are several variations of this workflow.

This list combines the workflow presented in *TinyML* Chapter 3 with
[TensorFlow Tutorial: Transfer learning and fine-tuning](https://www.tensorflow.org/tutorials/images/transfer_learning).

1. Decide on a goal
2. Collect and understand a dataset
3. Design a model architecture
    - Design the data input pipeline
    - Design the model itself
    - Design outputs that meet the goal
4. Train the model
5. Evaluate the model
6. Convert the model
7. Run inference
8. Iterate
    - Troubleshoot
    - Evaluate on-hardware performance
    - Collect data for feedback

Here is a simplified visual interpretation
yoinked from [this post](https://microchipdeveloper.com/harmony3:basic-machine-learning-workflow).

![Basic ML workflow](https://microchipdeveloper.com/local--files/harmony3:basic-machine-learning-workflow/basic_ml_workflow.png)

## Merging workflows

Recall from the [Prediction Machines lesson](prediction-machines.md) that:

> prediction + judgement = decision

![Anatomy of a task](https://images.squarespace-cdn.com/content/v1/59d6456137c581acfcef3422/1541255026543-JS0Q6G7NY4O0TG8XL2ZA/Figure+7-1.png)

### Exercise

Choose one of these or come up with your own. Then complete the jobs below.

#### Sample topics

- **Drone swarm range**: A quadcopter is deployed for search and reconnaissance missions in a remote and challenging environment, such as a disaster-stricken area, a forest, or a remote monitoring site. The quadcopter's primary task is to gather important information, capture images, or perform sensor-based measurements to aid in decision-making or situational awareness. However, it operates on a limited battery capacity - which means its flight time is restricted - and it is difficult to determine when a drone should return home to charge.
- **5G modem deployment**: 5G modems, IoT devices, cellular phones  communicate wirelessly to manage traffic, monitor environmental conditions, and optimize energy usage. However, the wireless communication channels are susceptible to interference and congestion. A company is trying to determine where and at what density to deploy its 5G modems to ensure efficient and reliable data transmission.
- **Ocean Restoration**: A coastal region has been hit by a devastating oil spill, severely affecting the marine ecosystem. The challenge is to determine the most effective locations for deploying cleanup efforts and restoration strategies. This involves making decisions about which areas to prioritize for different restoration methods, such as biological remediation or physical cleaning techniques.
- **Traffic routing**: A fleet of autonomous vehicles is navigating a city. There are enough of these vehicles that if they all choose similar routes they will cause excessive traffic. The team wants to determine if some vehicles can be routed to slightly sub-optimal routes for the benefit of the entire system.
- **Personalized mental health intervention**: A mobile application is designed to provide personalized mental health interventions to users based on their daily activities, emotions, and behaviors. The application aims to support users in managing stress, anxiety, and other mental health concerns. However, each user's response to different intervention strategies can vary significantly.

### Job 1

How does the Machine Learning Workflow for Embedded Devices above integrate as part of the overall task?

> **Sketch your interpretation of these two workflows nested together.**

### Job 2

Here is an example from *Prediction Machines* on planning a task.

![AI Canvas example](https://images.squarespace-cdn.com/content/v1/59d6456137c581acfcef3422/1541255133378-TJQW3O8I0HWHRPYEGNBU/Figure+13-3.png)

> **Complete an AI canvas for how you might approach the problem.**
>
> 1. Map this to your sketched workflow.
> 2. Also include a payoff decision tree.

![AI Canvas blank](https://images.squarespace-cdn.com/content/v1/59d6456137c581acfcef3422/1541255132827-ASC0MHNPAJLUP6YBFA33/Figure+13-1.png)
