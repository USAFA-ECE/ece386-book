# ICE 3: Whisper Transcription

In this ICE we will use [Distil-Whipser](https://huggingface.co/distil-whisper) to transcribe audio to text.
Transcription will run inside a Docker container on our NVIDIA Jetson Orin Nano.

## Background

OpenAI's **Whisper** models are cutting-edge speech processing models. They can do voice-to-text as well as translate between languages!

Here is the abstract from their paper:

> We study the capabilities of speech processing systems trained simply to predict large amounts of transcripts of audio on the internet. When scaled to 680,000 hours of multilingual and multitask supervision, the resulting models generalize well to standard benchmarks and are often competitive with prior fully supervised results but in a zeroshot transfer setting without the need for any finetuning. When compared to humans, the models approach their accuracy and robustness. We are releasing models and inference code to serve as a foundation for further work on robust speech processing.

Hugging Face 🤗 provides the **Transformers** library (backed by PyTorch) that allows you to
[run whisper models in 4 lines of code](https://huggingface.co/docs/transformers/model_doc/whisper)!

They also released [**Distil-Whisper**](https://huggingface.co/distil-whisper).

> Distil-Whisper is a distilled version of Whisper that is 6 times faster, 49% smaller, and performs within 1% word error rate (WER) on out-of-distribution evaluation sets.

For this lab we will be primarily using [distil-whisper/distil-medium.en](https://huggingface.co/distil-whisper/distil-medium.en)
because it has the fastest throughput of the distilled models.

```{note}
We will be asking questions about the paper [*Distil-Whisper: Robust Knowledge Distillation via Large-Scale Pseudo Labelling*](https://arxiv.org/abs/2311.00430)
during the end of block Clarify & Communicate.

Abstract:

> As the size of pre-trained speech recognition models increases, running these large models in low-latency or resource-constrained environments becomes challenging. In this work, we leverage pseudo-labelling to assemble a large-scale open-source dataset which we use to distill the Whisper model into a smaller variant, called Distil-Whisper. Using a simple word error rate (WER) heuristic, we select only the highest quality pseudo-labels for training. The distilled model is 5.8 times faster with 51% fewer parameters, while performing to within 1% WER on out-of-distribution test data in a zero-shot transfer setting. Distil-Whisper maintains the robustness of the Whisper model to difficult acoustic conditions, while being less prone to hallucination errors on long-form audio. Distil-Whisper is designed to be paired with Whisper for speculative decoding, yielding a 2 times speed-up while mathematically ensuring the same outputs as the original model. To facilitate further research in this domain, we make our training code, inference code and models publicly accessible.
```

## Setup

Before you begin, make sure you have configured Git on your Jetson Orin Nano.
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

As of March 2025, we are using JetPack 6.2, which includes CUDA 12.6.

```{tip}
You can check your CUDA version on the Jetson by running `nvidia-smi` in the terminal.
```

Add this line to the start of your Dockerfile

```Dockerfile
# Compatible with Jetpack 6.2
FROM nvcr.io/nvidia/pytorch:25.02-py3-igpu
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

Next, we will change the [HuggingFace Cache Directory](https://huggingface.co/docs/datasets/cache#cache-directory)
by setting an environment variable. This will allow us to not have to re-download the models each time we run the container.

```Dockerfile
ENV HF_HOME="/huggingface/"
```

Finally, we tell our image where it should start to execute.
We can always override this; for example to get a shell use `--entrypoint=/bin/bash` as an option to `docker run`.

```Dockerfile
ENTRYPOINT ["python", "speech_recognition.py"]
```

### Build Docker Image

To build the image and name it `whisper` just execute this. The `.` sends the entire working directory to the builder.

```bash
# This will fail; read on to find out why.
docker buildx build . -t whisper
```

The failure is because we need to create the `speech_recognition.py` script!

## Python Script

### CUDA Test

Before we do anything else, we should make sure CUDA is working. If it is, that means our container can access the GPU!

Create `speech_recognition.py`.

If you go back to [NVIDIA PyTorch Container](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch) you will see
an example of how to tell if CUDA is available. Find that and add these two lines to your script.

```python
import torch

print(f"CUDA available? {torch.cuda.is_available()}")
```

Now, build the container again! (*Hint: use the up-arrow in your terminal*).

#### Run the container

Once it is built you can see your images with `docker image list`.

Assuming you see your image, you can run the following command.

```{note}
See [docker run](https://docs.docker.com/reference/cli/docker/container/run/#options) for option docs.

- `-it` allocates a new interactive terminal
- `--rm` removes the container after it exits
- `--runtime=nvidia` allows the container to access the Jetson GPU
```

```bash
docker run -it --rm --runtime=nvidia whisper
```

If all goes well, this will print **True** to the terminal!

```{important}
After you verify that CUDA is working in your container, **commit** your code and push to GitHub!

Then delete the two lines from `speech_recognition.py`.
```

### Record Audio

First, import SoundDevice and NumPy:

```python
import sounddevice as sd
import numpy as np
import numpy.typing as npt
```

Then create the following function:

```python
def record_audio(duration_seconds: int = 10) -> npt.NDArray:
    """Record duration_seconds of audio from default microphone.
    Return a single channel numpy array."""
    sample_rate = 16000  # Hz
    samples = int(duration_seconds * sample_rate)
    # Will use default microphone; on Jetson this is likely a USB WebCam
    audio = sd.rec(samples, samplerate=sample_rate, channels=1, dtype=np.float32)
    # Blocks until recording complete
    sd.wait()
    # Model expects single axis
    return np.squeeze(audio, axis=1)
```

Next, create a chunk of code that will be executed whenever this file is directly run by Python,
`python speech_recognition.py`, exactly as our **ENTRYPOINT** is doing above!

```python
if __name__ == "__main__":

    print("Recording...")
    audio = record_audio()
    print("Done")

    print(audio) # Temporary line
```

**Build your image again.**

Here is the updated command to run the container.
We are letting the container access the webcam microphone with `--device /dev/snd`.

```bash
docker run -it --rm --device=/dev/snd --runtime=nvidia  whisper
```

*This should still fail!*

It turns out Python SoundDevice is a python binding for a C/C++ library...

Search online to find what you need to install with `apt` and then add this to the Dockerfile.
Make sure you add it **after** `WORKDIR /app` and **before** the `RUN pip...` command.

```Dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    # PUT APT LIBRARY HERE \
    && rm -rf /var/lib/apt/lists/
```

```{tip}
Docker builds images in layers and keeps those layers in a **cache**.
If you invalidate a layer of the image during `docker buildx`,
Docker rebuilds that layer and all subsequent layers.

As a result, you typically want to construct your Dockerfile so that the most frequently changed
things are at the bottom! In our case WORKDIR > RUN apt > RUN pip > COPY.

Of course, this isn't perfect, but it **will save you a ton of time** while iterating.
```

Now, re-build and re-run!
You should see some numbers printed out in an array 🎤

### 🤗 Pipeline

Hugging Face transformers pipelines can do [all sorts of cool tasks!](https://huggingface.co/docs/transformers/task_summary)

Add this method to your `speech_recognition.py` script.
It is extracted from the Distil-Whisper model card [short-form transcription](https://huggingface.co/distil-whisper/distil-medium.en#short-form-transcription).

```python
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, Pipeline, pipeline
```

```python
def build_pipeline(
    model_id: str, torch_dtype: torch.dtype, device: str
) -> Pipeline:
    """Creates a Hugging Face automatic-speech-recognition pipeline on the given device."""
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True,
    )
    model.to(device)
    processor = AutoProcessor.from_pretrained(model_id)
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        torch_dtype=torch_dtype,
        device=device,
    )
    return pipe
```

At this point you should have several imports and two methods!

### The `__main__`

Time to make those methods actually do something for us!

You need one more import:

```python
import sys
import time
```

`sys` will allow us to pass arguments to the script.
For us, that means you can do something like `python speech_recognition.py distil-whisper/distil-large-v3`
and get multi-lingual transcription!

The following code should go at the very bottom of your script.

```python
if __name__ == "__main__":
    # Get model as argument, default to "distil-whisper/distil-medium.en" if not given
    model_id = sys.argv[1] if len(sys.argv) > 1 else "distil-whisper/distil-medium.en"
    print("Using model_id {model_id}")
    # Use GPU if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    print(f"Using device {device}.")

    print("Building model pipeline...")
    pipe = build_pipeline(model_id, torch_dtype, device)
    print(type(pipe))
    print("Done")

    print("Recording...")
    audio = record_audio()
    print("Done")

    print("Transcribing...")
    start_time = time.time_ns()
    speech = pipe(audio)
    end_time = time.time_ns()
    print("Done")

    print(speech)
    print(f"Transcription took {(end_time-start_time)/1000000000} seconds")
```

#### Black

You should *almost always* run [Black](https://black.readthedocs.io/) on any Python script **before** you try and execute it!

> "Any color you like."

If you have not already done so, install Black with:

```bash
pipx install black
```

```{tip}
**pipx** allows you to install and run Python applications in isolated environments.
~~~bash
sudo apt update
sudo apt install pipx
pipx ensurepath # Then must restart terminal
~~~
```

Run black against your code to

1. Check your code for common errors and bugs (known as linting).
2. Reformat the code so it is easier to read. This style is opinionated - as you could guess - but it is extremely helpful once you get used to it.

```bash
black speech_recognition.py
```

Once Black exits cleanly, **commit your code and push to GitHub.**

```{note}
Our method declarations have **type hints** in the parameters and returns.
You *could* use **PyRight** to verify these, and usually you *should*;
however, this requires a virtual environment with all the same imports installed,
which is beyond the scope of this ICE.

Just take the instructors word for it that it passes:

~~~bash
$ pyright speech_recognition.py
0 errors, 0 warnings, 0 informations
~~~
```

## Running

At this point you should have a Dockerfile and Python script that you are pretty sure will work.

**Build your image one more time.**

### Volumes

The Hugging Face models can be quite large, so we don't want to have to download them every single time we restart a container.
We could bake them in to the image, but that would just bloat the image and reduce flexibility.

Instead, we are going to use [docker volumes](https://docs.docker.com/engine/storage/volumes/)!

Create a volume named `huggingface`. You can think of this as a folder managed by docker.

```bash
docker volume create huggingface
```

You can see your current volumes with `docker volume ls`.

We can tell a container to mount this volume by passing the `-v` flag to `docker run`.
The syntax is `named_volume:path_in_container` (you can also pass read/write permissions, which we aren't going to).

Recall that we used `ENV HF_HOME="/huggingface/"` inside our Dockerfile above to tell
HuggingFace transformers to use `/huggingface/` for the cache.

### The real deal

Our final run command will have a few more tweaks:

- `--ipc=host` increases the shared memory that the container is allowed to use
- `-v` for the volume mount, as discussed above

```bash
docker run -it --rm --device=/dev/snd --runtime=nvidia --ipc=host -v huggingface:/huggingface/ whisper
```

Be sure to recite from your Contrails while recording, and then see it printed to the screen!

## Conclusion

In this ICE you learned how to use a 🤗 transformer pipeline to run Distil-Whisper in a Docker container on your NVIDIA Jetson Orin Nano.

We would typically use `docker push` to publish your built image to someplace like DockerHub so that other people can use it.
But, seeing as it's several gigabytes, it isn't worth the upload time. That's ok though because it can always be rebuilt from the Dockerfile!

### Deliverables

To complete this ICE,

1. Commit all your code and push to GitHub
2. Complete the associated Gradescope ICE assignment.

```{tip}
You will need to use this ICE for your final project!
```
