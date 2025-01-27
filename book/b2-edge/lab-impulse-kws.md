# Lab 3: Edge Impulse KWS

In this lab we will make a "Hey, Siri" type device that continuously listens for a keyword.
When your device spots your keyword it will turn on an LED!

## Prelab

### Reading

Read Iodice's [*TinyML Cookbook, 2nd Ed*, Chapter 4: "Using Edge Impulse and the Arduino Nano to Control LEDs with Voice Commands"](https://learning.oreilly.com/library/view/tinyml-cookbook/9781837637362/Text/Chapter_04.xhtml). *Yes. You have to read it.**

### Data Collection

> Collecting a dataset is typically the most difficult, time-consuming, and expensive part of any edge AI project. It’s also the most likely place you will make terrible, hard-to-detect mistakes that can doom your project to failure. ~ [*AI at the Edge*](https://learning.oreilly.com/library/view/ai-at-the/9781098120191/ch07.html#:-:text=Collecting%20a%20dataset,project%20to%20failure.)

You need to think of a great keyword! It should be at least two syllabus, three ideally.
Examples (that you can't use) include 'Hey Siri', 'OK, Google', 'Alexa', 'Hello World'.

Once you think of your awesome keyword:

1. Create an [Edge Impulse](https://edgeimpulse.com/) account; I used my afacademy email.
2. Login, then **Create a new project** (top right of [projects page](https://studio.edgeimpulse.com/studio/profile/projects)). You can name it `kws_lab` or whatever you want.
3. Click **Data acquisition** in the left sidebar.
4. In the *Collect data** box, click the chip symbol in the top right; hovering says "connect a development board"
5. Scan the QR code to connect your phone.
6. Change the label to "keyword" or something helpful
7. Record 10 seconds of you saying your keyword in spaced intervals.

```{hint}
The Reading ^^ that you *definitely* did goes into detail for [collecting audio samples for KWS](https://learning.oreilly.com/library/view/tinyml-cookbook/9781837637362/Text/Chapter_04.xhtml#:-:text=Collecting%20audio%20samples%20for%20KWS).
```

Go back to your dashboard and make sure the samples look good. Once they do...

**Copy the QR Code** or **grab URL from the QR code**. Mine started with `https://smartphone.edgeimpulse.com/index.html?apiKey=` and had a 67-character API key.

Then...

**Share** with your friends and family!

Be sure to give them *very specific instructions** on how to record themselves saying your keyword.
Your goal is to get lots of different people saying your keyword so that you have a robust dataset.

Ideally, you have several minutes of audio prior to the lab starting... best of luck!

### Equipment Setup

Strictly speaking, you can wait to do equipment setup until during the lab...
up to you to decide which type of risk you want to accept, commander!

On your **Raspberry Pi** we will install edge-impulse-cli and arduino-cli.

Before doing anything, let's update the installed software.

```bash
sudo apt update && sudo apt upgrade -y
```

#### Edge Impulse CLI

Now do the relevant portions from the [Linux installation docs](https://docs.edgeimpulse.com/docs/tools/edge-impulse-cli/cli-installation#installation-linux-ubuntu-macos-and-raspbian-os).

Specifically,

- Install node
- Verify node version and path
- Install `edge-impulse-cli`

After installing you need to `exit` that terminal and open a new one.

Then verify it installed:

```bash
edge-impulse-daemon --version
```

#### Arduino CLI

Install `arduino-cli` according to [the docs](https://arduino.github.io/arduino-cli/1.1/installation/)

First, ensure `~/.local/bin` is on your PATH.

The environment variable `$PATH` is a list of directories that the OS will search for executables, *in order.*

```bash
# This shows your home directory, which uses the ~ symbol for short
# We expect it to be /home/pi/ by default, but it can be whatever!
echo $HOME

# This will print your current path.
# We expect to see ~/.local/bin/ towards the end,
# but instead of ~ it will be the result from the previous command
echo $PATH
```

We want to install the Arduino CLI to somewhere on our path. If we do `~/.local/bin` we don't need `sudo`.

```bash
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=~/.local/bin sh
```

Verify installation

```bash
arduino-cli version
```

#### Dialout Group

Lastly, we need to add your user to the Linux dialout group.

```{note}
It took Capt Yarbrough two entire afternoons to figure out that this needs to be done 🫠
```

The dialout group grants users permissions to access serial ports and modems.
Our Arduino board and daemon will connect to the serial port in such a way that we'll need this.

```bash
sudo usermod -aG dialout $USER
```

Then reboot.

```bash
sudo reboot
```

Once logged back in, user `pi` (or whoever you are) should be in dialout group.

```bash
grep dialout /etc/group
```

### Arduino Firmware

Follow the instructions to [connect edge impulse to the Arduino Nano 33 BLE Sense](https://docs.edgeimpulse.com/docs/edge-ai-hardware/mcu/arduino-nano-33-ble-sense#id-1.-connect-the-development-board-to-your-computer).

Specifically, you need to **connect the board** and **update firmware.**
You don't strictly need to do the "setting keys" part, but it might be helpful.

![RESET to launch bootloader](https://docs.edgeimpulse.com/~gitbook/image?url=https%3A%2F%2F3586622393-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FGEgcCk4PkS5Pa6uBabld%252Fuploads%252Fgit-blob-c47c9b3fde5e9a23528f23e997f35a51c1e3be3e%252Fb302301-out.gif%3Falt%3Dmedia&width=768&dpr=2&quality=100&sign=347037cf&sv=2)

If successful you should see a message like

> Flashed your Arduino Nano 33 BLE development board.

```{tip}
You *can* do all of this on Raspberry Pi or you *can* do all of this on Windows.
But I've found that:

1. Installing node and these things on Windows is a bad idea.
2. Folks like to be able to take their board and laptop out of the lab and still do work.
```

---

# Lab Workday

## Data Processing

At this point hopefully your friends and family have uploaded lots of samples of your **keyword** to your Edge Impulse project!

These samples were recorded on a phone microphone. However, we are going to be using our Arduino for real-world inference. As such, we will record some samples with the Nano's builtin microphone.

Once we do that, we'll need to process all this data so that it's ready to use!

### Collect Samples with Nano

> Building the dataset with recordings obtained with the mobile phone’s microphone is undoubtedly good enough for many applications. However, to prevent any potential loss in accuracy during the model’s deployment, we should also include audio clips recorded with the microphone used by the end application in the dataset. ~ *TinyML Cookbook*

To get started, you can connect your Arduino - with the Edge Impulse firmware already flashed - to your EdgeImpulse.com online project.

You can do this on your laptop, Pi, whatever; you *must* use Edge or Chrome.

1. Connect your Arduino to laptop with USB
2. Open your online project
3. Click on **Data acquisition** in the left sidebar
4. In the Collect data box, click the USB symbol in the top right.
5. Your browser will open a popup, select Nano 33.

![USB Data Acquisition](https://www.edgeimpulse.com/blog/content/images/je9uegn_gb6tafqvonescoqifgxo0eeuasl0nlvzgccgtxvftqffldoumu3ix_dcrfmbcdiixr0rjlozivgqty8hfbgawhjq4gv7jk0_xti5ap8a3gqn22e5yen7qn2aah3wyw6u.gif)

**Record about 50 samples of yourself saying the keyword, using your Nano microphone.**

### Split Samples

And now, for the fun, grueling, reality of machine learning: data processing!

Follow the guidance in *TinyML* combined with [Edge Impulse Tutorial: Responding to your voice](https://docs.edgeimpulse.com/docs/tutorials/end-to-end-tutorials/responding-to-your-voice) to:

1. Crop samples where your grandma said something that doesn't match the label
2. Split samples into 1 second samples

!['Split sample' automatically cuts out the interesting parts of an audio file.](https://docs.edgeimpulse.com/~gitbook/image?url=https%3A%2F%2F3586622393-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FGEgcCk4PkS5Pa6uBabld%252Fuploads%252Fgit-blob-91dbe818857626614de046667b0ad9f624afe655%252F83ae234-screenshot_2020-11-19_at_222215.png%3Falt%3Dmedia&width=768&dpr=1&quality=100&sign=4dd985db&sv=2)

### Download a dataset

Download the [keyword spotting dataset](https://cdn.edgeimpulse.com/datasets/Audio+Classification+-+Keyword+Spotting.zip)
and unzip it to your computer.

**Delete any file that starts with "helloworld"** since that's not a label we want.

We want *roughly* the same number of samples in each of our classes: noise, unknown, keyword.
There are about 300 files in the  the `testing/` directory, so just over two minutes of audio each for "noise" and "unknown."
**That's hopefully about how many "keyword" samples you have!**
The `training/` directory has many more samples... you probably don't need that many, so don't upload it.

If you don't have about two minutes of keyword samples, you need to either go get more data or upload less data to keep your classes balanced...

Upload unknown and noise samples to your project ([instructions here if needed](https://docs.edgeimpulse.com/docs/tutorials/end-to-end-tutorials/responding-to-your-voice#id-3.-building-your-dataset)).

### Test/Train Split

[Rebalance your dataset](https://docs.edgeimpulse.com/docs/tutorials/end-to-end-tutorials/responding-to-your-voice#rebalancing-your-dataset)
by **Perform test/train split.**

## Create Impulse
