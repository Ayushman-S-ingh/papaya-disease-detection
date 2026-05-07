import tensorflow as tf
from flask import current_app

model = None

def get_model():

    global model

    if model is None:

        model_path = "app/ml/papaya_model.h5"

        model = tf.keras.models.load_model(model_path)

        current_app.logger.info("REAL PAPAYA AI MODEL LOADED")

    return model