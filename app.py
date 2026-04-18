import tensorflow as tf
import numpy as np
from flask import Flask, request, render_template
from tensorflow.keras.preprocessing import image
import os
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# 🔥 FIX: Increase upload size (camera issue)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Load model
model = tf.keras.models.load_model("papaya_model.h5")

# Classes
class_names = [
    "Bacterial_Blight",
    "Carica_Insect_Hole",
    "Healthy",
    "Yellow_Necrotic_Spots_Holes"
]

# Disease info
disease_info = {
    "Bacterial_Blight": {
        "description": "A bacterial infection affecting papaya leaves.",
        "symptoms": "Dark spots, yellow halos.",
        "solution": "Use copper fungicide and remove infected leaves."
    },
    "Carica_Insect_Hole": {
        "description": "Damage caused by insects.",
        "symptoms": "Holes and damaged edges.",
        "solution": "Use insecticide spray."
    },
    "Healthy": {
        "description": "Leaf is healthy.",
        "symptoms": "Green and fresh.",
        "solution": "No action needed."
    },
    "Yellow_Necrotic_Spots_Holes": {
        "description": "Fungal disease.",
        "symptoms": "Yellow spots and dry areas.",
        "solution": "Apply fungicide."
    }
}

def local_ai_response(question, detected_disease=None):
    q = question.lower()

    # 🌿 General structured responses
    def format_response(title, causes, symptoms, solution, prevention):
        return f"""
🔍 {title}

🦠 Causes:
{causes}

⚠ Symptoms:
{symptoms}

💊 Treatment:
{solution}

🛡 Prevention:
{prevention}
"""

    # 🧠 Disease-specific answers
    if "bacterial" in q or (detected_disease == "Bacterial_Blight"):
        return format_response(
            "Bacterial Blight in Papaya",
            "- Caused by bacteria due to humid conditions and poor sanitation.",
            "- Water-soaked spots\n- Yellow halos\n- Leaf damage",
            "- Use copper-based fungicides\n- Remove infected leaves immediately",
            "- Avoid overwatering\n- Ensure proper air circulation"
        )

    elif "insect" in q or "pest" in q or (detected_disease == "Carica_Insect_Hole"):
        return format_response(
            "Insect Damage (Carica Insect Hole)",
            "- Caused by pests feeding on leaves.",
            "- Small holes in leaves\n- Irregular leaf edges",
            "- Use organic or chemical insecticides\n- Clean affected leaves",
            "- Regular inspection\n- Maintain plant hygiene"
        )

    elif "fungal" in q or "yellow" in q or (detected_disease == "Yellow_Necrotic_Spots_Holes"):
        return format_response(
            "Fungal Disease in Papaya",
            "- Caused by fungal infection in moist conditions.",
            "- Yellow spots\n- Dry patches\n- Leaf holes",
            "- Apply fungicides\n- Remove infected parts",
            "- Avoid excess moisture\n- Improve drainage"
        )

    elif "healthy" in q or (detected_disease == "Healthy"):
        return format_response(
            "Healthy Plant Condition",
            "- No disease detected.",
            "- Green and fresh leaves\n- No damage",
            "- No treatment required",
            "- Maintain regular watering and sunlight"
        )

    # 🌱 General agriculture questions
    elif "prevent" in q or "avoid" in q:
        return """
🛡 General Disease Prevention Tips:

- Maintain proper plant hygiene
- Avoid overwatering
- Ensure good sunlight exposure
- Use quality fertilizers
- Regularly inspect leaves
"""

    elif "fertilizer" in q or "nutrient" in q:
        return """
🌱 Fertilizer Advice:

- Use balanced NPK fertilizer
- Organic compost improves soil health
- Apply fertilizer every 2–3 weeks
"""

    elif "water" in q or "watering" in q:
        return """
💧 Watering Advice:

- Water regularly but avoid overwatering
- Ensure proper drainage
- Morning watering is best
"""

    elif "soil" in q:
        return """
🌍 Soil Tips:

- Use well-drained soil
- Maintain pH between 6–7
- Add organic compost for better growth
"""

    # 🤖 Smart fallback (this makes it feel like AI)
    else:
        return f"""
🤖 Smart Assistant Response:

Based on your question: "{question}"

👉 Here are some general recommendations:

- Monitor plant health regularly
- Remove infected or damaged leaves
- Maintain proper watering and sunlight
- Use fertilizers and pesticides when needed
- Keep surroundings clean to avoid disease spread

💡 Tip:
If you detected a disease, follow specific treatment guidelines for better results.
"""
# 🔥 STORE LAST RESULT
last_result = {
    "prediction": None,
    "info": None,
    "image_path": None,
    "confidence": None
}

@app.route("/", methods=["GET", "POST"])

def index():
    prediction = None
    info = None
    image_path = None
    confidence = None
    ai_answer = None

    if request.method == "POST":

        filepath = None

        # 📷 Camera input
        if "captured_image" in request.form and request.form["captured_image"]:
            data = request.form["captured_image"]
            image_data = base64.b64decode(data.split(',')[1])

            img = Image.open(BytesIO(image_data)).convert("RGB")
            filepath = "static/captured.jpg"
            img.save(filepath, "JPEG")

        # 📁 Upload input
        elif "file" in request.files and request.files["file"].filename != "":
            file = request.files["file"]
            filepath = os.path.join("static", file.filename)
            file.save(filepath)

        # 🔍 Prediction
        if filepath:
            img = image.load_img(filepath, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0) / 255.0

            pred = model.predict(img_array)
            pred_index = np.argmax(pred)

            confidence_val = float(np.max(pred))
            pred_index = np.argmax(pred)

            if confidence_val < 0.3:
                prediction = "Unknown"
                info = {
                    "description": "Not a papaya leaf or unclear image.",
                    "symptoms": "Model not confident.",
                    "solution": "Upload a clear papaya leaf image."
                }
            else:
                prediction = class_names[pred_index]
                info = disease_info[prediction]

            confidence = round(confidence_val * 100, 2)
            image_path = filepath

            # SAVE RESULT
            last_result["prediction"] = prediction
            last_result["info"] = info
            last_result["image_path"] = image_path
            last_result["confidence"] = confidence

        # 🤖 Offline AI (UPDATED)
        if "question" in request.form and request.form["question"]:
            ai_answer = local_ai_response(request.form["question"], last_result["prediction"])

    # Restore previous result if no new image
    if not prediction and last_result["prediction"]:
        prediction = last_result["prediction"]
        info = last_result["info"]
        image_path = last_result["image_path"]
        confidence = last_result["confidence"]

    return render_template(
        "index.html",
        prediction=prediction,
        info=info,
        image_path=image_path,
        confidence=confidence,
        ai_answer=ai_answer
    )

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)