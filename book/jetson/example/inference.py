import tensorflow as tf
import os
import glob


class ModelInference:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)

    # def preprocess_input(self, input_data):
    #     # Implement preprocessing logic
    #     return preprocessed_data

    def __call__(self, input_data, training=False):
        # preprocessed_data = self.preprocess_input(input_data)
        # Use training=False to ensure layers like BatchNormalization behave correctly
        predictions = self.model(input_data, training=training)
        return predictions


def load_images(image_directory: str):
    image_files = []
    image_extensions = [
        "*.jpg",
        "*.jpeg",
        "*.png",
        "*.gif",
        "*.bmp",
    ]  # Add more extensions if needed
    for ext in image_extensions:
        image_files = glob.glob(os.path.join(image_directory, ext))
        input_data_list.extend(image_files)

    return image_files


inference = ModelInference("../../dnn/cat-dog/cat-dog-tuned")

input_data_list = load_images("../../dnn/cat-dog/img")

for input_data in input_data_list:
    predictions = inference(input_data)
    print(predictions)
