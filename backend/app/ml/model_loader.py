import random


# ============================================
# MOCK MODEL LOADER
# ============================================

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


def get_model():
    return None


def predict_disease(image_path):

    disease = random.choice(CLASS_NAMES)

    confidence = round(random.uniform(85, 99), 2)

    return {
        "disease_name": disease,
        "confidence": confidence
    }