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

While just having something on the TODO list worked for Shrek, we are going to have checkpoints
that help guide you to a working final product!

1. Design
2. LLM processing component
3. Edge AI component
4. Integration
5. Final demonstration

Information on each of these can be found in the specific heading below.

### Points

Each Gradescope assignment will have points associated with questions.
Here is the breakdown for functionality:

 ```{table} Implementation Points

| Component               | Functionality       | Portion of Component |
|-------------------------|---------------------|----------------------|
| Trigger voice recording | Key press           | 25                   |
| Trigger voice recording | Button on GPIO      | 60                   |
| Trigger voice recording | Keyword Spotting    | 15                   |
| Voice Transcription     | Voice-to-text       | 100                  |
| LLM query processing    | Return city         | 50                   |
| LLM query processing    | Return airport code | 25                   |
| LLM query processing    | Return location     | 25                   |
| Integration             | GET from wttr.in    | 15                   |
| Integration             | POST to LLM server  | 40                   |
| Integration             | GET local service   | 45                   |
| End-to-end              | Full functionality  | 100                  |
```

## Background Information

## Multi-Device Architectures: Voice Assistants

From [*AI at the Edge* Chapter 3, "The Hardware Edge of AI"](https://learning.oreilly.com/library/view/ai-at-the/9781098120191/ch03.html#:-:text=Multi-Device%20Architectures):

> Edge AI applications aren’t always implemented directly on the devices that host the actual sensors. Sometimes, it makes sense to use a multi-device architecture.
>
> A single device might contain multiple types of processors: for example, one for running application code and another for running ML algorithms. A complete system might be composed of many devices, some with multiple processors, that collect and process data at many different points depending on which BLERP benefits are needed. This type of solution can even involve cloud computation.
>
> A great example of this type of architecture is a smart speaker with a voice assistant. Typically, they have at least two processors. The first is a low-power, always-on chip that runs DSP and a machine learning model to listen for wake words without using too much energy.
>
> The second is an application processor, which is woken up by the always-on chip when the wake word is detected. The application processor might run a more sophisticated model to try to catch any false positives that got past the always-on chip. Together, these two processors can identify wake words without violating user privacy by streaming private conversations to the cloud.
>
> Once the wake word has been confirmed, the application processor streams the audio to a cloud server, which performs speech recognition and natural language processing in order to come up with an appropriate response. The general flow is shown in Figure 3-9.
>
>```{figure} ../img/voice-assistant-block.png
> The low-power processor aims to catch as many potential keywords as possible; the application processor wakes up to evaluate any possible matches and invokes the cloud web service if a match is confirmed
>```
>
> When designing a system, don’t be afraid to consider using multiple devices to tackle some of the trade-offs involved with different device types. Some common situations where it can be helpful are:
>
> - Monitoring large numbers of individual entities: this can get expensive if high-end AI-capable hardware is used on every entity.
> - Reducing energy use: sensors are battery powered and need to last a long time.
> - Protecting privacy: sending data directly to a large device or cloud server might violate privacy norms.
> - Integrating with legacy equipment: existing sensors or gateways might be supplemented with edge AI devices rather than being replaced.

We **are not** worried about revalidating the wake word, but we *are* interested in processing different pieces of the system on different hardware.

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

### DFEC AI Server

For the duration of the final project, the DFEC AI server will be running Ollama on `GPU:1`, serving [gemma3:27b](https://ollama.com/library/gemma3:27b) at:

```bash
10.1.69.214:11434
```

You must be connected to the ECE LAN to hit this private IP address.
You may also use the public URL, but must have an IPv6 address and it is blocked on USAFA's network...

`GPU:0`will be open and available for you to run your own containers on, but too many students attempting to use it at once may cause problems.

---

## Design Checkpoint

1. Identify what problem you are trying to solve.
2. Discuss the problem in terms of *Prediction Machines* "Anatomy of a Task".
3. Draw a **detailed** block diagram of your system.
4. Submit to Gradescope.

![Prediction Machines Anatomy of a Task](../img/anatomy-of-task.png)

![How neat is that](https://i.giphy.com/CWKcLd53mbw0o.webp)
