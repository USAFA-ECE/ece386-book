# Prediction Machines and ML Workflow

> The current wave of advances in artificial intelligence doesn't actually bring us intelligence but instead a critical component of intelligence: prediction. ~ *Prediction Machines (4)*

## Pre-Reading

*TinyML*, Warden and Situnayake, 2019. [Chapter 3](https://learning.oreilly.com/library/view/tinyml/9781492052036/ch03.html#:-:text=Chapter%203.%20Getting%20Up%20to%20Speed%20on%20Machine%20Learning)

### Objectives

> I can frame a problem in terms of Prediction, Judgement, Decision, Action, Feedback and effectively communicate it to senior leaders as a way of reducing risk.

- Understand that AI is fundamentally prediction.
- Understand that prediction combines with human judgement to result in a decision.

---

## Prediction Machines

### Our role as commanders

Our role as commanders is to exercise judgment and make risk decisions in an uncertain and adversarial environment

#### From Doctrine

> It is a given in future conflicts that the joint force will be conducting operations in a contested environment. We must be prepared to execute in a degraded C2 environment where clearly delineated and forward thinking commander’s intent will be a requirement. It is imperative senior leaders provide our commanders with conditions-based authorities delegated to the lowest capable and competent level, and **empower command by negation to accept the appropriate level of risk, all while working toward moments of clear C2.** ~ General Charles Q. Brown, [AFPD-3-30](https://www.doctrine.af.mil/Portals/61/documents/AFDP_3-30/AFDP%203-30-Command-and-Control.pdf)

[AFPD 1](https://www.doctrine.af.mil/Portals/61/documents/AFDP_1/AFDP-1.pdf) core principle of *Mission Command:*

**Accept prudent risk**. All military operations contain uncertain, complex, and ambiguous elements. Commanders must analyze risks in collaboration with their subordinates to balance the tension between protecting the force and accepting and managing risks that must be taken to accomplish the mission.

### Making a Decision

> The following is derived from *Prediction Machines: The Simple Economics of Artificial Intelligence* by Agrawal, Gans, and Goldfarb, 2018.

A *decision* includes prediction, judgement, action, outcome, and data.

![Anatomy of a task](https://images.squarespace-cdn.com/content/v1/59d6456137c581acfcef3422/1541255026543-JS0Q6G7NY4O0TG8XL2ZA/Figure+7-1.png)

#### Prediction

> The machine learning algorithm builds a *model* of the system based on the data we provide, through a process we call *training*.
> The model is a type of computer program. We run data through this model to make predictions, in a process called *inference*. *~ TinyML*

AI only brings us a single critical component of intelligence: prediction

**Prediction** takes information you have, data, and uses it to generate information you don't have.

Machine learning reframes algorithmic problems as probabilistic prediction problems.

The Oakland A's identified what problem they were trying to solve: the impact of a player on team performance and capitalized on that; see *Moneyball*.

Jeff Hawkins argued that "The human cortex is an organ of prediction."

##### Accuracy of prediction

In contrast to machines, humans are sometimes extremely good at prediction with little data.
This is largely because of our broad context of the world.

As dimensionality grows, humans' ability to form accurate predictions diminishes.

Machines passed the human benchmark for image classification (5% error) in 2015.

Going from 85% to 90% accuracy means mistakes fall by one third.
Going from 98% to 99.9% means mistakes fall by a factor of twenty.
Better prediction leads to better outcomes.
At some point, accuracy hits a threshold where the prediction can become transformational.

Prediction machines are valuable because:

1. they often offer better, faster, cheaper predictions than humans can
2. prediction is a key ingredient to decision-making under uncertainty
3. decision-making is ubiquitous throughout our economic and social lives

#### Judgement

Computers made arithmetic cheap.
Internet made distribution, communication, and search cheap.
AI has made prediction cheap.

A drop in price of one thing can increase the price of its complements. For example, cheaper coffee means more expensive cream and sugar.

As the price of prediction drops, the price of judgement will increase.

Having better prediction raises the value of judgement.

Only humans can express relative rewards of one action over another.
The prediction may be handed to the machine but the human will still handle the judgment.

Objectives rarely have only a single dimension. Answering why you are doing something may be complicated.

Judging payoff requires time and effort. This slow decision-making has tradeoffs.
Judgement, whether by deliberation or experimentation, is costly (*especially in combat*).

In some cases, the judgment may be that the reward function engineering is clear enough to hand off the decision to the machine based only on the prediction.

Prediction will likely shift to machine by default and human by exception.

To make the most of prediction machines you need to rethink reward functions throughout your organization to better align with your true goals. This task is not easy.

Humans are critical to decision making where the goals are subjective.

Contracting out judgement is risky because they do not have the full context to resolve uncertainty in a strategic dilemma; you should keep judgement-focused workers in house.
(also, they are a big piece of your competitive advantage)

Judgement quality is hard to specify in a contract and difficult to monitor.

### Risk

A key task for a business leaders is to anticipate and manage various risks.

Risk exposure matters when a decision can change ones exposure to risk.

In the case of weather, an automated, decent prediction right now is preferable; the human only gets involved in extreme events.
Error rate increases for extended forecasts, so decision maker must decide when to decide.

Risk can be managed with **insurance**, where you take actions to reduce the *cost* associated with bad outcomes.
Or risk can be managed with **protection**, where you take actions to reduce the *probability* of a bad outcome.

When you use insurance to minimize waste, the waste is visible; by contrast, the waste may be difficult to see with protection.

Enhanced prediction increases returns by reducing the waste from unneeded insurance or protection.

Air Canada was able to predict how to fill underutilized capacity because it had:

1. Measurable waste
2. Wealth of data about the problem
3. A well-contained problem

Prediction machines will provide new and better methods for managing risk.

![Average payoff from taking or leaving an umbrella](https://images.squarespace-cdn.com/content/v1/59d6456137c581acfcef3422/1541255131938-N61GEXKOS0ON05RLXDSI/Figure+7-3.png)

#### Uncertainty

Perhaps the biggest weakness of prediction machines is the high confidence they can have in a wrong answer.

Uncertainty means you need judgement when the prediction turns out to be wrong, not just when it is correct.
Uncertainty increases the cost of judging a payoff for a given decision.

## Machine Learning Workflow

*TinyML* Chapter 3 presents the following [Deep Learning Workflow](https://learning.oreilly.com/library/view/tinyml/9781492052036/ch03.html#:-:text=The%20Deep%20Learning%20Workflow).
Sub-bullets are added.

1. Decide on a goal
2. Collect a dataset
    - and understand it
3. Design a model architecture
    - data input pipeline
    - the model itself
    - outputs that meet the goal
4. Train the model
    - initial model evaluation
5. Convert the model
    - considering where you will be deploying it
6. Run inference
7. Evaluate and troubleshoot
    - on-hardware performance
    - collect data for feedback

This workflow is an adaption of the Engineering Method!

Here is a similar visual representation:

![Microchip Basic Machine Learning Workflow - https://developerhelp.microchip.com/xwiki/bin/view/applications/machine-learning/basic-machine-learning-workflow/#Ibasic_ml_workflow.png](../img/basic_ml_workflow.png)

### ML Workflow into Prediction

Again,

$$
\text{prediction + judgement = decision}
$$

which leads to action!

![Anatomy of a task](https://images.squarespace-cdn.com/content/v1/59d6456137c581acfcef3422/1541255026543-JS0Q6G7NY4O0TG8XL2ZA/Figure+7-1.png)

## Closing thought from AFPD-1

> Airmen execute **mission command** through **centralized command**, **distributed
control**, and **decentralized execution**.

This is the new way in which we will fight wars.
