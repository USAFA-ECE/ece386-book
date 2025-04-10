# Final Project

![Risks](https://pbs.twimg.com/media/EbJXUC4X0AEXhlD?format=jpg)

For the final project you will build an end-to-end personal voice assistant that tells you the weather!

## Overview

**Goal** Design and construct a voice assistant that listens for a wake word; records a sentence asking for weather at a city, airport, or location; returns the weather at that spot.

### Objectives

- Demonstrate dependency management while deploying a model.
- Target model deployment to the appropriate hardware.
- Facilitate edge and cloud AI interactions.
- Build a realistic, complex system!

**Every** project must:

1. Utilize multiple AI models running on appropriate hardware for that use case.
2. Be pushed to a public GitHub repository with a README that describes usage.
3. Manage dependencies with a `Dockerfile` or Python `requirements.txt`, as appropriate.
4. Be well-designed and adhere to engineering best practices.

### Grading

Consider this approach:

> **Princess Fiona:** You didn't slay the dragon?
>
> **Shrek:** It's on my "to do" list. Now come on.
>
> **Princess Fiona:** But this isn't right! You're meant to charge in, sword drawn, banner flying-that's what all the other knights did.
>
> **Shrek:** Yeah, right before they burst into flame!

While it worked for Shrek, we are going to have checkpoints
that help guide you to a working final product!

1. Design
2. Edge AI component
3. LLM processing component
4. Networking component
5. Final demonstration

## Background Information

### Jetson GPIO

According to [JetsonHacks: NVIDIA Jetson Orin Nano GPIO Header Pinout](https://jetsonhacks.com/nvidia-jetson-orin-nano-gpio-header-pinout/),
pin #29 is named `GPIO01`.
*However*, the OS uses the Sysfs lines that map to the system on a chip (SoC) spec.
So `GPIO01` is actually referred to as **line 105**.

On your Jetson you can run this to get the SoC name for line 105, which is GPIO01, which is pin #29 🤪

```bash
# Find name for GPIO01
gpioinfo | grep 105
# line 105: "PQ.05" unused input active-high
```

Cool, so we will simply call pin #29 line `105` but we now know it's configured as active-high input to the SoC port "PQ.05".

```{note}
This is actually super similar to the `.xdc` constraints file for the Basys3 board in ECE 281!
```

Now we can read the digial value on the pin!

```bash
# Should print 0 or 1 to the terminal
gpioget gpiochip0 105
```

I typed `gpio` and then pressed tab, tab to find `gpiomon`.

```bash
gpiomon --help
```

Looks like there are some flags to process something on the first rising edge. Nice!

```bash
# Run echo on rising edge
gpiomon -r -n 1 gpiochip0 105 | while read line; do echo "event $line"; done
```

*Disclaimer:* I never would have figured this out without ChatGPT https://chatgpt.com/share/67d4a6d8-5920-8003-a93a-67c68b6acc8c
**but notice how much research I did first in order to ask the right questions!** Also, not all the files it pointed me towards exist.

### wttr.in

[wttr.in (GitHub)](https://github.com/chubin/wttr.in) is "the right way to ~~check~~ curl the weather!"

It is a free API that allows you to check the weather for:

- city
- 3-letter airport codes
- geographic location (prefixed with a `~`)

```bash
$ curl wttr.in/Colorado+Springs
Weather report: Colorado+Springs

      \   /     Clear
       .-.      55 °F
    ― (   ) ―   ↘ 4 mph
       `-’      9 mi
      /   \     0.0 in
                                                       ┌─────────────┐
┌──────────────────────────────┬───────────────────────┤  Wed 09 Apr ├───────────────────────┬──────────────────────────────┐
│            Morning           │             Noon      └──────┬──────┘     Evening           │             Night            │
├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│     \   /     Sunny          │     \   /     Sunny          │     \   /     Sunny          │     \   /     Clear          │
│      .-.      +51(50) °F     │      .-.      66 °F          │      .-.      66 °F          │      .-.      +51(48) °F     │
│   ― (   ) ―   ↗ 4 mph        │   ― (   ) ―   ↑ 8-9 mph      │   ― (   ) ―   ↘ 6-7 mph      │   ― (   ) ―   → 4-9 mph      │
│      `-’      6 mi           │      `-’      6 mi           │      `-’      6 mi           │      `-’      6 mi           │
│     /   \     0.0 in | 0%    │     /   \     0.0 in | 0%    │     /   \     0.0 in | 0%    │     /   \     0.0 in | 0%    │
└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘
                                                       ┌─────────────┐
┌──────────────────────────────┬───────────────────────┤  Thu 10 Apr ├───────────────────────┬──────────────────────────────┐
│            Morning           │             Noon      └──────┬──────┘     Evening           │             Night            │
├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│     \   /     Sunny          │     \   /     Sunny          │     \   /     Sunny          │               Overcast       │
│      .-.      +50(46) °F     │      .-.      +60(59) °F     │      .-.      57 °F          │      .--.     +48(44) °F     │
│   ― (   ) ―   ↓ 4-5 mph      │   ― (   ) ―   ↖ 9-10 mph     │   ― (   ) ―   ↖ 8-9 mph      │   .-(    ).   ↑ 7-14 mph     │
│      `-’      6 mi           │      `-’      6 mi           │      `-’      6 mi           │  (___.__)__)  6 mi           │
│     /   \     0.0 in | 0%    │     /   \     0.0 in | 0%    │     /   \     0.0 in | 0%    │               0.0 in | 0%    │
└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘
                                                       ┌─────────────┐
┌──────────────────────────────┬───────────────────────┤  Fri 11 Apr ├───────────────────────┬──────────────────────────────┐
│            Morning           │             Noon      └──────┬──────┘     Evening           │             Night            │
├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤
│     \   /     Sunny          │     \   /     Sunny          │     \   /     Sunny          │     \   /     Clear          │
│      .-.      +57(55) °F     │      .-.      +71(69) °F     │      .-.      66 °F          │      .-.      +55(53) °F     │
│   ― (   ) ―   ↖ 0 mph        │   ― (   ) ―   ↖ 5-6 mph      │   ― (   ) ―   ↖ 11-13 mph    │   ― (   ) ―   ↑ 6-13 mph     │
│      `-’      6 mi           │      `-’      6 mi           │      `-’      6 mi           │      `-’      6 mi           │
│     /   \     0.0 in | 0%    │     /   \     0.0 in | 0%    │     /   \     0.0 in | 0%    │     /   \     0.0 in | 0%    │
└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘
Location: Colorado Springs, El Paso County, Colorado, United States of America [38.8339578,-104.8253485]

Follow @igor_chubin for wttr.in updates
```

---

# Design

1. Identify what problem you are trying to solve.
2. Discuss the problem in the context of prediction, judgement, and decision.
3. Elaborate on the steps of the engineering method/ ML Workflow that you will take to reach your goal.
4. Identify a class of models that you think will be helpful in achieving your end state.

![Prediction Machines Anatomy of a Task](../img/anatomy-of-task.png)

### Datasets and Models

You must do one of the following

- Use transfer learning **or**
- Compare performance of several pre-canned models **or**
- Use advanced quantization

1. If you will be conducting transfer learning, identify a dataset that fits your needs.
2. Identify at least one, but ideally multiple, base models that you will use.

### Model Implementation

Get the model working!

### Model Application

Wrap your working model with some logic that makes the results of the prediction available to the user.
This should work towards the goal you described in the first checkpoint.

### Final Demonstration

- Demonstrate your application to the class
- Push code to GitHub

![How neat is that](https://i.giphy.com/CWKcLd53mbw0o.webp)

---

# Final Project Workday 2

# Final Project Workday 3

# Final Project Workday 4
