# Final: GPIO Checkpoint

For this checkpoint, you must prove that you can trigger an action **in Docker** by driving a GPIO pin to digital HIGH.

## Deliverables

1. Conduct a BLERP analysis for voice recording and transcription.
2. Prove that you can use the GPIO to trigger a simple action in Docker running Python, such as printing to the screen.

```{hint}
1. Check the GPIO on the Jetson host, with Bash, and with no Docker
2. Then do the Python in Docker
```

## Jetson GPIO with Bash

*Before* you try to do anything with Docker and Python, make sure your 40-pin GPIO header works.

TLDR:

Put $0V$ on **pin 29** then run this line in the terminal:

```bash
# With 0V on pin 29
# Will print 0 to terminal, for digital LOW
gpioget gpiochip0 105
```

Now put $3.3V$ on **pin 29** then run the line again

```bash
# With 3.3V on pin 29
# Will print 1 to terminal, for digital HIGH
gpioget gpiochip0 105
```

### Explanation

Your Jetson has two headers. The one we care about is named **`gpiochip0`**, which is the 40-pin vertical header.

According to [JetsonHacks: NVIDIA Jetson Orin Nano GPIO Header Pinout](https://jetsonhacks.com/nvidia-jetson-orin-nano-gpio-header-pinout/),
pin `#29` on is named `GPIO01`.
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

Now we can read the digital value on the pin!

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

## Jetson.GPIO in Docker

We can use the Python https://github.com/NVIDIA/jetson-gpio library in combination with [libgpiod](https://libgpiod.readthedocs.io/en/stable/) to
access the Jetson's GPIO in Python.

```{important}
When you run a container that you want to access the GPIO you **must** allow it to access the device, so add this flag after `docker run`

~~~bash
--device=/dev/gpiochip0
~~~
```

### Setup

You can do this interactively with a running container, but you can (and should) bake it into a Dockerfile!

First install `gpiod` (this provides the command line tools such as `gpioget`)

```bash
apt install gpiod
```

Next, install the Jetson GPIO Python library.

```bash
pip install Jetson.GPIO
```

Tell the library which Jetson model it's running via an environment variable:

```bash
# In terminal
export JETSON_MODEL_NAME=JETSON_ORIN_NANO
```

or

```Dockerfile
# In Dockerfile
ENV JETSON_MODEL_NAME=JETSON_ORIN_NANO
```

### Run Test Script

Once setup, run Python.

```python
'''Prints 'UP' or 'DOWN' based on edges on Jetson pin #29'''
import Jetson.GPIO as GPIO

# Init as digital input
my_pin = 29
GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
GPIO.setup(my_pin, GPIO.IN)  # digital input

print('Starting Demo! Move pin 29 between 0V and 3.3V')

while True:
    GPIO.wait_for_edge(my_pin, GPIO.RISING)
    print('UP!')
    GPIO.wait_for_edge(my_pin, GPIO.FALLING)
    print('down')
```
