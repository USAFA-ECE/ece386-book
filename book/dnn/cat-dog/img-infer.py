import tflite_runtime.interpreter as tflite
import numpy as np
from PIL import Image
from picamera2 import Picamera2

# How many pixe
capture_shape = (720, 1280)


def resize_and_rescale_image(image_path, input_shape):
    # Load the image using PIL
    # image = Image.frombuffer("L", capture_shape, image_buffer)
    image = Image.open(image_path)
    # Resize the image to match what the model was trained on
    resized_image = image.resize((input_shape[1], input_shape[2]))
    input_data = np.array(resized_image, dtype=np.float32)
    input_data = np.expand_dims(input_data, axis=0)  # Create a batch of size 1

    return input_data


def tflite_infer(interpreter, input_details, input_data):
    interpreter.set_tensor(input_details[0]["index"], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]["index"])
    return np.squeeze(output_data)


# Create the tflite Interpreter
model_path = "cat-dog.tflite"
interpreter = tflite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Initialize the camera
# image_buffer = BytesIO()
picam2 = Picamera2()
picam_config = picam2.create_still_configuration(main={"size": capture_shape})
picam2.configure(picam_config)
# picam2.start()

# Take a picture
# image_buffer = picam2.capture_buffer()
# resized_image = resize_and_rescale_image(image_buffer, input_details[0]["shape"])
image_path = "mypic.jpg"
picam2.start_and_capture_file(image_path, show_preview=False)
resized_image = resize_and_rescale_image(image_path, input_details[0]["shape"])

# Conduct inference
infer_result = tflite_infer(interpreter, input_details, resized_image)

print("Inference result:", infer_result)
