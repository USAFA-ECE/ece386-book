import tflite_runtime.interpreter as tflite
import numpy as np
from picamera2 import Picamera2, Preview
from time import sleep

# How many pixe
capture_shape = (1280, 720)


def tflite_infer(interpreter, input_details, input_data):
    # Reserve a spot for the result
    interpreter.set_tensor(input_details[0]["index"], input_data)
    # Conduct inference
    interpreter.invoke()
    # Save results of inference
    output_data = interpreter.get_tensor(output_details[0]["index"])
    # Trim off extra dimensions from result
    return np.squeeze(output_data)


# Create the tflite Interpreter
model_path = "cat-dog.tflite"
interpreter = tflite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Initialize and start the camera
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(
    main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores"
)
picam2.configure(camera_config)
# Pop up a preview window
picam2.start_preview(Preview.QTGL)

# Turn on the camera
picam2.start()

# Pause for preview
sleep(2)

# Take a picture
np_pic = picam2.capture_array()
print("np size", np_pic.shape)
# Stop the camera
picam2.stop()

# Resize picture to be dimensions the TF model expects
resized_pic = np.resize(np_pic, input_details[0]["shape"])
resized_pic = resized_pic.astype(np.float32, copy=False)

# Conduct inference
infer_result = tflite_infer(interpreter, input_details, resized_pic)

print("Inference result:", infer_result)
