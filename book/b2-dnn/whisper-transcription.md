# ICE: Whisper Transcription

In this ICE we will use [Distil-Whipser](https://huggingface.co/distil-whisper) to transcribe audio to text.

## Background

## Setup

Before you begin, make sure you have configured git on your Jetson Orin Nano.
This should include setting your email, username, and authenticating to GitHub.

1. Create a new GitHub repository, and name it something helpful.
2. Clone the repository to your Jetson and open it in VSCode.
3. Open a terminal in VSCode by pressing `Ctrl` + `Shift` + `\``
    or with the Terminal menu at the top of the window.

## Dockerfile

Create a Dockerfile

```bash
code Dockerfile
```

We want to use the [NVIDIA PyTorch Container](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch)
as our base image. You want the newest container that matches the version of CUDA installed on your Jetson.

As of December 2024, we are using JetPack 6.1, which includes CUDA 12.6.

Add this line to the start of your Dockerfile

```Dockerfile
FROM nvcr.io/nvidia/pytorch:24.11-py3-igpu
```

Next, set a working directory for the application.
If we don't do this the following command will just stick things in `/`, which causes problems.

```Dockerfile
WORKDIR /app
```

Next, install Python dependencies. According to the [distil-medium.en](https://huggingface.co/distil-whisper/distil-medium.en)
model card, you need t###### and a##### (up to you to find them!).

We will also need [Python SoundDevice](https://python-sounddevice.readthedocs.io/) to record audio.

Finally, to keep the size of our final image small we will use the `--no-cache-dir` option.
The `\` character allows us to break the command into multiple lines.
The `&&` chains commands; it will execute the second command if the first command executes successfully.
Replace the "#" with the right letters.

```Dockerfile
RUN pip install --upgrade --no-cache-dir pip && \
    pip install --no-cache-dir \
    t###### \
    a###### \
    sounddevice
```

Next, we need to copy our python script into the Dockerfile.
We can just copy the local file to the current working directory (that we set above with `WORKDIR`!) using `.`

```Dockerfile
COPY speech_recognition.py .
```

Finally, we tell our image where it should start to execute.
We can always override this; for example to get a shell use `--entrypoint=/bin/bash` as an option to `docker run`.

```Dockerfile
ENTRYPOINT ["python", "speech_recognition.py"]
```

### Build Docker Image

To build the image and name it `whisper` just execute this. The `.` sends the entire working directory to the builder.

```bash
docker buildx build . -t whisper
```

That likely failed! We need to create the `speech_recognition.py` script!

## Python Script

### CUDA Test

Before we do anything else, we should make sure CUDA is working. If it is, that means our container can access the GPU!

Create `speech_recognition.py`.

If you go back to [NVIDIA PyTorch Container](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch) you will see
an example of how to tell if CUDA is available. Find that and add these two lines to your script.

```python
import torch
# TODO: check if CUDA is available
```

Now, build the container again! (Hint: use the up-arrow in your terminal).

#### Run the container

Once it is built you can see your images with `docker image list`.

Assuming you see your image, you can run the following command:

```bash
docker run -it --rm --runtime nvidia mywhisper
```

If all goes well, this will print **True** to the terminal!

### Record Audio

First, import sounddevice:

```python
import sounddevice as sd
```

Then create the following function:

```python

```
