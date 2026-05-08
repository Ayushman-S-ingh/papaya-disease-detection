import os
import numpy as np
import tensorflow as tf

from tensorflow.keras.models import load_model
from tensorflow.keras.layers import BatchNormalization
from PIL import Image


# ==========================================
# CUSTOM BATCH NORMALIZATION FIX
# ==========================================
class CustomBatchNormalization(BatchNormalization):
    def __init__(self, *args, **kwargs):

        kwargs.pop("renorm", None)
        kwargs.pop("renorm_clipping", None)
        kwargs.pop("renorm_momentum", None)
        kwargs.pop("synchronized", None)

        super().__init__(*args, **kwargs)


# ==========================================
# MODEL PATH
# ==========================================
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "papaya_model.h5"
)


# ==========================================
# LOAD MODEL
# ==========================================
model = load_model(
    MODEL_PATH,
    custom_objects={
        "CustomBatchNormalization": CustomBatchNormalization
    },
    compile=False
)


# ==========================================
# CLASS NAMES
# ==========================================
CLASS_NAMES = [
    "Healthy",
    "Leaf Curl",
    "Mosaic",
    "Anthracnose",
    "Powdery Mildew",
    "Black Spot",
    "Brown Spot",
    "Downy Mildew"
]


# ==========================================
# PREPROCESS IMAGE
# ==========================================
def preprocess_image(image_path):

    image = Image.open(image_path).convert("RGB")

    image = image.resize((224, 224))

    image = np.array(image) / 255.0

    image = np.expand_dims(image, axis=0)

    return image


# ==========================================
# PREDICT
# ==========================================
def predict_disease(image_path):

    processed_image = preprocess_image(image_path)

    predictions = model.predict(processed_image)

    predicted_class = np.argmax(predictions[0])

    confidence = float(np.max(predictions[0]) * 100)

    disease_name = CLASS_NAMES[predicted_class]

    return {
        "disease_name": disease_name,
        "confidence": round(confidence, 2)
    }