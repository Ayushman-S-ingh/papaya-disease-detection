import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

model = tf.keras.models.load_model("papaya_model.h5")

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

prediction = model.predict(img_array)

pred_index = np.argmax(prediction)
confidence = np.max(prediction)

print("Prediction:", class_names[pred_index])
print("Confidence:", round(float(confidence) * 100, 2), "%")