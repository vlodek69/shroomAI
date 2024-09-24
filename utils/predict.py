from io import BytesIO

import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.preprocessing import image

mush_model = tf.keras.models.load_model("mushroom_classification_model.keras")


def preprocess_image(img_file, target_size=(110, 110)) -> np.ndarray:
    try:
        img_stream = BytesIO(img_file.read())
        img = Image.open(img_stream).convert("RGB")

        # Resize and preprocess image
        img = img.resize(target_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array /= 255.0
        return img_array
    except Exception as e:
        print(f"Error during preprocessing:", e)
        raise


def validate_image(img_file) -> None:
    file_extensions = ["jpg", "jpeg", "png", "gif"]
    img_file_extension = img_file.filename.rsplit(".", 1)[1].lower()
    if img_file_extension not in file_extensions:
        raise TypeError(f"Invalid file extension: {img_file_extension}")

    img_bytes = BytesIO(img_file.read())
    img_file.seek(0)
    if img_bytes.getbuffer().nbytes > 52428800:
        raise ValueError("Image too large, max size is 50mb")


def predict(img, model=mush_model) -> dict[str, str]:
    validate_image(img)
    try:
        preprocessed_img = preprocess_image(img)
        predictions = model.predict(preprocessed_img)

        predicted_class = np.argmax(predictions, axis=1)[0]
        probability = round(predictions[0, predicted_class] * 100, 2)

        return {"index": str(predicted_class), "probability": str(probability)}
    except Exception as e:
        print(f"Error during prediction:", e)
        raise
