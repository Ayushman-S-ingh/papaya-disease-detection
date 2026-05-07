"""
app/ml/model_loader.py
Singleton model loader — loads EfficientNetB0 once, reuses across requests
"""
import os
import threading
import numpy as np

_model = None
_lock  = threading.Lock()


def get_model():
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                _model = _load_model()
    return _model


def _load_model():
    try:
        import tensorflow as tf
        from flask import current_app
        model_path = current_app.config.get("MODEL_PATH", "ml/models/efficientnetb0_papaya.h5")
        if os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
            current_app.logger.info(f"Model loaded from {model_path}")
            return model
        else:
            current_app.logger.warning(
                f"Model file not found at {model_path}. Using mock model for demo."
            )
            return _create_mock_model()
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {e}")


def _create_mock_model():
    """
    Placeholder — returns random probabilities.
    Replace with real model before deployment.
    """
    class MockModel:
        def predict(self, x):
            scores = np.random.dirichlet(np.ones(12)).reshape(1, 12)
            return scores
    return MockModel()


# ── Preprocessor ──────────────────────────────────────────────────────────────
"""
app/ml/preprocessor.py
Image loading and EfficientNetB0 preprocessing
"""
import numpy as np


def preprocess_image(filepath: str, img_size=(224, 224)) -> np.ndarray:
    """Load an image, resize, and apply EfficientNetB0 preprocessing."""
    try:
        from tensorflow.keras.preprocessing import image as keras_image
        from tensorflow.keras.applications.efficientnet import preprocess_input

        img     = keras_image.load_img(filepath, target_size=img_size)
        arr     = keras_image.img_to_array(img)
        arr     = np.expand_dims(arr, axis=0)
        arr     = preprocess_input(arr)
        return arr
    except ImportError:
        # Fallback using Pillow if TF not installed
        from PIL import Image
        img = Image.open(filepath).convert("RGB").resize(img_size)
        arr = np.array(img, dtype=np.float32) / 255.0
        arr = np.expand_dims(arr, axis=0)
        return arr