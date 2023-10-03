# Diffusion Image Generation

## Pre-reading

- [Stable Diffusion v1-5 Model Card](https://huggingface.co/runwayml/stable-diffusion-v1-5)

### Objectives

- Apply lessons-learned from containerization.
- Get a diffusion text to image model working on Jetson.
- Use ChatGPT to serve working model as API.

## Image generation

**My goal** is to serve a text-to-image model on the Jetson Orin Nano.

### The tutorial

I first read [Does Stable Diffusion run on NVIDIA Jetson AGX Xavier Developer Kit with CUDA?](https://iomz.github.io/how-to/docker-diffusers-jetson/) and thought this might be possible!

Following the tutorial under **Run Diffusers on Docker**,
I quickly came to this command:

```bash
git clone https://huggingface.co/runwayml/stable-diffusion-v1-5
```

Even with `git-lfs` installed, this was taking *forever*...
I pulled the plug after 25 GB came down with dozens more promised.

Going to take a different approach, but noting the
[Dockerfile](https://github.com/iomz/docker-diffusers-jetson/blob/main/Dockerfile)
for later reference, even though I can tell this person is *not* a docker expert.

### The documentation

The Hugging Face Diffusers Documentation has the suggestion:
[Choose an AutoPipeline for your task](https://huggingface.co/docs/diffusers/tutorials/autopipeline#choose-an-autopipeline-for-your-task) 🙏🏼

```python
from diffusers import AutoPipelineForText2Image
import torch

pipeline = AutoPipelineForText2Image.from_pretrained(
    "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16, use_safetensors=True
).to("cuda")
prompt = "peasant and dragon combat, wood cutting style, viking era, bevel with rune"

image = pipeline(prompt, num_inference_steps=25).images[0]
```

> Under the hood, AutoPipelineForText2Image:
>
> 1. automatically detects a "stable-diffusion" class from the model_index.json file
> 2. loads the corresponding text-to-image StableDiffusionPipline based on the "stable-diffusion" class name.

**Let's run that!**... on my Intel NUC.

### Try it on the NUC

I do not have an NVIDIA GPU on this device.
So, a quick DuckDuckGo search (ChatGPT actually got this one wrong)
tells me about `torch.cuda.is_available()`. So I write:

```python
from torch import cuda

# Use GPU if available; otherwise, cpu
if cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

```

Then I just replace `to.("cuda")` with `to.(device)`.

Install dependencies:

```bash
pip install torch  diffusers[torch] transformers
```

Then run it: great success! (After about **3:20**, yikes!)

Here's how to display your image:

```python
# Explore what this image even is
type(image)
# Oh, it's a PIL! We can just
image.show()
```

### Add the API

I want this thing to be served. Let's try ChatGPT.

Time for some **prompt engineering.**

First, I know I need to be specific about what I want
as well as the steps I want the LLM to take.

I've heard FastAPI is a good choice, but have never used it before.

#### Prompt 1

Here is what I try first

```markdown
I want to adapt the following code to serve a REST API where the user
passes a prompt with `prompt` and a JPEG is returned.

~~~python
from diffusers import AutoPipelineForText2Image
from torch import cuda

# https://huggingface.co/runwayml/stable-diffusion-v1-5
diffusion_model: str = "runwayml/stable-diffusion-v1-5"

# Use GPU if available; otherwise, cpu
if cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

# The auto pipeline automatically detects and loads the model
# https://huggingface.co/docs/diffusers/tutorials/autopipeline#choose-an-autopipeline-for-your-task
# Use_safetensors enables a NSFW filter.
pipeline = AutoPipelineForText2Image.from_pretrained(
    diffusion_model, use_safetensors=True
).to(device)

# Generate the image based on the prompt
prompt = "A falcon flying over mountains"
image = pipeline(prompt, num_inference_steps=25).images[0]
~~~

1. Create the FastAPI function `generate_img`
2. Use the `prompt` and `pipeline` to make the image
3. Convert the image to JPEG in memory
4. Return the image

I also want you to talk about how to serve this API and how to call it
using `curl -o`.
```

Ok, tbh this is totally not how I did it.
I walked the dog with individual prompts, starting from a basic example.
I would run those, search some things or ask for clarification, and iterate.

This prompt will *probably* give you working code, but it also will
almost certainly be way too complex.

For example, I ended up with a GET method doing it bit-by-bit but
the prompt above gave me a POST method. Maybe that's better, in truth.

At minimum, you should

1. Have `@app.post` or `@app.get` macro
2. Run the app with [uvicorn](https://www.uvicorn.org/)
3. Be able to `curl` the port and save the image. At this point, single word prompts with no whitespace are fine.

## Containerize the app

Here is a Dockerfile to get you started:

```Dockerfile
FROM nvcr.io/nvidia/pytorch:23.09-py3

EXPOSE 5858

WORKDIR /app
COPY ./generate_img.py /app

# Ideally, pin to versions you know work.
RUN pip install --no-cache-dir \

# TODO

```

1. Switch from the generic **nvidia/pytorch** base to the one designed for the Jetson.
2. Finish writing `generate_img.py` and make sure it is in the same directory as your Dockerfile.
3. Finish installing dependencies with pip.
4. Write the `CMD` layer.
5. Figure out the `docker run` command.
    - You should use a `-v` [volume](https://docs.docker.com/storage/volumes/) to reuse the model cache
    - You need to bind the correct port

After all that, you should be able to curl your container and get a generated image!
