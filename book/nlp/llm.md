# Large Language Models

## Pre-Reading

- YouTube (0:00 - 8:35) [Transformers, explained: Understand the model behind GPT, BERT, and T5](https://youtu.be/SZorAJ4I-sA?si=NfWfV9U3TLAtccsh)

<iframe width="560" height="315" src="https://www.youtube.com/embed/SZorAJ4I-sA?si=VCrQ4ys7S7wsTbXW" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

- YouTube (0:00 - 3:03) [Transformers (how LLMs work) explained visually](https://www.youtube.com/watch?v=wjZofJX0v4M) -> watch more if you *really* want to see what's going on!

<iframe width="560" height="315" src="https://www.youtube.com/embed/wjZofJX0v4M?si=o-yIPL6_80LcBt4D" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

- Optional: [*Deep Learning with Python*, 11.4: The Transformer Architecture](https://learning.oreilly.com/library/view/deep-learning-with/9781617296864/Text/11.htm#:-:text=architecture)

### Objectives

- Understand why transformer architecture and GPUs make LLMs possible
- Describe how LLMs exhibit emergent behavior.
- Discuss ethical considerations with LLMs.

## Transformers

## Emergence

**Emergence** is when you combine relatively simple sets of rules and at some threshold a mind-blowing result manifests.

This is one of my all time favorite books.

![The Emergence of Everything book](https://global.oup.com/academic/covers/pop-up/9780195173314)

> **Emergence** is the the opposite of reduction. The latter tries to move from the whole to the parts. It has been enormously successful. The former tries to generate the properties of the whole from an understanding of the parts. Both approaches can he mutually self-consistent.

$$
sand + glass funnel = ?
$$

![Sand](https://images.unsplash.com/photo-1535631815644-2a104d57263b)

![Glass funnel](https://www.corning.com/catalog/cls/products/p/pyrexFunnelFluted60AngleShortStem/images/6180_A.jpg/_jcr_content/renditions/product.zoom.1200.jpg)

![Hourglass](https://images.unsplash.com/photo-1518281361980-b26bfd556770)

$$
sand + glass funnel = time keeping
$$

We take two simple objects, the force of gravity, and *the ability to measure the fourth dimension **emerges***.

### LLMs as an Emergent Phenomena

LLM Rules:

1. Use **self-attention** to compute relevancy between each word and every other word in the sentence.

```{figure} ../img/deep_learning_with_python-fig-11-06.png
Self-attention for **station** in the sentence "The train left the station on time."
~ *Deep Learning with Python, 2nd Ed.*, Fig. 11.6.
```

2.

### (Bonus) The Mind as an Emergent Phenomena

> **There are a wide variety of understandings of what is meant by mind.** The reductionist behaviorist tradition would argue that mind is an epiphenomenon of the activities of collections of neurons. They argue that minds do not in fact exist. At the opposite extreme, the idealist tradition going back to George Berkeley would argue that mind is all that exists, and matter is an epiphenomenon posited by minds for explanatory purposes. The Kantians would argue for the existence of both mind and matter, the latter being the ding an sich (thing in itself) that minds aspire to and cannot fully comprehend.
>
> **Our view is that all of the above is too simplistic.** The universe, whatever its ultimate character, unfolds in a large number of emergences, all of which must he considered. **The pruning rules of the emergences may go beyond the purely dynamic and exhibit a noetic character. It ultimately evolves into the mind, not as something that suddenly appears, but as a maturing character of an aging universe.** This is something that we are just beginning to understand and, frustrating as it may be to admit such a degree of ignorance, we move ahead. **That is our task as humans; some would call it knowing the mind of God and regard it as a vocation.**
> ~ [*The Emergence of Everything*, Harold J. Morowitz](https://www.goodreads.com/book/show/2301.The_Emergence_of_Everything)

## Ethics

Large Language Models are trained on large datasets of language!

Furthermore, *instruct* models are trained how to respond to queries.

Both of these steps have the potential to introduce bias into the model.
