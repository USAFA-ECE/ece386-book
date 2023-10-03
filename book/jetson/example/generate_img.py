from diffusers import AutoPipelineForText2Image
from fastapi import FastAPI
from fastapi.responses import Response
from io import BytesIO
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
    diffusion_model, use_safetensors=True, cache_dir="/app/models/"
).to(device)

# Create the FastAPI app
app = FastAPI()


@app.get("/generate_img")
async def generate_img(prompt: str):
    """Uses a diffusion model to generate and return an image based on the prompt."""

    # Generate the image based on the prompt
    image = pipeline(prompt, num_inference_steps=25).images[0]

    # Convert the PIL Image to bytes in memory
    image_bytes_io = BytesIO()
    image.save(image_bytes_io, format="JPEG")
    image_data = image_bytes_io.getvalue()

    # Indicate that you are returning a JPEG image
    headers = {
        "Content-Type": "image/jpeg",
    }

    # Return the image in a Response object
    # This works with a simple `curl -o myimage.jpg ...`
    return Response(content=image_data, headers=headers)
