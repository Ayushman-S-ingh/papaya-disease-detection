import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# ✅ Load exported model (folder)
model = tf.keras.models.load_model("papaya_model_export")

class_names = [
    "Bacterial_Blight",
    "Carica_Insect_Hole",
    "Healthy",
    "Yellow_Necrotic_Spots_Holes"
]

img_path = "test.jpg"

img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0) / 255.0

pred = model(img_array)

pred_index = np.argmax(pred)
confidence = np.max(pred)

print("Prediction:", class_names[pred_index])
print("Confidence:", round(float(confidence) * 100, 2), "%")