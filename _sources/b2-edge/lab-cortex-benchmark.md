# Lab 2: Cortex DSP Benchmark

![Are you stealing those LCDs? Yeah but I'm doing it while my code compiles](https://imgs.xkcd.com/comics/compiling.png)

## Pre-Lab

Make a 1:45 to 2:00 minute video of yourself explaining how a basic CPU works.

See teams and Gradescope for more information.

## Lab

Run the following code on an Arduino Nano 33 BLE Sense.

Then write a technical explanation explaining what is going on.
Submit the report on Gradescope.

<script src="https://gist.github.com/byarbrough/9cda569df945c8817142c2d6b77d5037.js"></script>

```{tip}
If you click on [`dot_prod_dsp_bench.ino`](https://gist.github.com/byarbrough/9cda569df945c8817142c2d6b77d503) in the gist above you can clone the repository or access the raw file.
```

### Uno Comparison

*Optionally,* you may discuss the differences between the Nano's benchmarks and the same float and int benchmarks on the [Arduino Uno](https://docs.arduino.cc/hardware/uno-rev3/) shown in {numref}`uno-benchmark`:

```{table} Arduino Uno Dot Product Benchmark
:name: uno-benchmark
| Datatype | Time (microseconds) |
|----------|---------------------|
| int      | 5,600               |
| float    | 21,128              |
```

### Further guidance

- Your report should be well-written and highly technical, but take the tone of an executive summary.
- You can use or not use section headings to facilitate the flow, as you see fit.
- Assume your reader is a computer engineer who is familiar with Arduino, computer architecture, and dot products but has not run this particular benchmark.
- Your references need to be comprised of reputable sources, such as text books and ARM documentation.
- Include quantitative analysis of the results of the code run.
- Spend that majority of your effort explaining those results from a hardware and software standpoint.
- Conclude with a discussion of why this matters and how it may impact edge inference deployments.
- Do not exceed 3 pages.
- Ensure you include a Documentation statement.

```{hint}
This is primarily a **research** lab.

*The Designer's Guide to the Cortex-M Processor, 3rd Edition*, by Trevor Martin, [Chapter 9: Practical DSP for Cortex-M Microcontrollers](https://learning.oreilly.com/library/view/the-designers-guide/9780323854955/xhtml/Ch009_313-353_B9780323854948000103.xhtml) has some good info, but you will need several more resources.
```

#### Authorized resources

- Large Language Models (such as ChatGPT) are **not** authorized at all for this assignment.
- Other students in ECE 386 are **not** authorized.
- You are encouraged to work with the USAFA Writing Center to improve the quality of your writing!
- You are welcome to get help from cadets currently taking ECE 485 (but not ECE 386).
