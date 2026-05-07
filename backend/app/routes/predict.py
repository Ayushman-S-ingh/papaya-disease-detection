"""
app/routes/predict.py  —  Image upload + AI prediction endpoint
POST /api/predict
"""
import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from .. import db
from ..models.user import User
from ..models.prediction import Prediction, Disease
from ..ml.model_loader import get_model
from ..ml.preprocessor import preprocess_image
from ..services.prediction_service import (
    get_treatment_recommendation,
    get_severity,
    build_scores_dict,
)

predict_bp = Blueprint("predict", __name__)


def allowed_file(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


@predict_bp.route("/predict", methods=["POST"])
@jwt_required()
def predict():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Use PNG, JPG, JPEG, or WEBP"}), 400

    # Save uploaded file
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)
    ext       = file.filename.rsplit(".", 1)[-1].lower()
    filename  = f"{uuid.uuid4().hex}.{ext}"
    filepath  = os.path.join(upload_dir, filename)
    file.save(filepath)

    try:
        # Preprocess and run inference
        model       = get_model()
        img_array   = preprocess_image(filepath, current_app.config["IMG_SIZE"])
        raw_preds   = model.predict(img_array)           # shape (1, num_classes)
        class_names = current_app.config["DISEASE_CLASSES"]

        scores      = build_scores_dict(class_names, raw_preds[0])
        top_class   = max(scores, key=scores.get)
        confidence  = scores[top_class]
        severity    = get_severity(top_class, confidence)
        treatment   = get_treatment_recommendation(top_class)

        # Persist to DB
        record = Prediction(
            user_id        = user_id,
            image_filename = filename,
            image_url      = f"/api/uploads/{filename}",
            disease_name   = top_class,
            confidence     = confidence,
            severity       = severity,
            all_scores     = scores,
            treatment      = treatment,
            notes          = request.form.get("notes", ""),
        )
        db.session.add(record)
        db.session.commit()

        return jsonify({
            "prediction_id": record.id,
            "disease":        top_class,
            "confidence":     round(confidence * 100, 2),
            "severity":       severity,
            "all_scores":     {k: round(v * 100, 2) for k, v in scores.items()},
            "treatment":      treatment,
            "image_url":      record.image_url,
            "created_at":     record.created_at.isoformat(),
        }), 200

    except Exception as e:
        current_app.logger.error(f"Prediction error: {e}")
        # Clean up file on error
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"error": "Prediction failed. Please try again."}), 500