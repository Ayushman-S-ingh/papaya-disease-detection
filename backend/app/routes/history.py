"""
app/routes/history.py  —  Prediction history CRUD
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import desc
from ..models.prediction import Prediction
from .. import db

history_bp = Blueprint("history", __name__)


@history_bp.route("/history", methods=["GET"])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    claims  = get_jwt()
    is_admin = claims.get("role") == "admin"

    page     = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    search   = request.args.get("search", "")
    severity = request.args.get("severity", "")
    sort     = request.args.get("sort", "newest")

    query = Prediction.query if is_admin else Prediction.query.filter_by(user_id=user_id)

    if search:
        query = query.filter(Prediction.disease_name.ilike(f"%{search}%"))
    if severity:
        query = query.filter(Prediction.severity == severity)

    if sort == "oldest":
        query = query.order_by(Prediction.created_at.asc())
    elif sort == "confidence_high":
        query = query.order_by(Prediction.confidence.desc())
    else:
        query = query.order_by(desc(Prediction.created_at))

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "predictions": [p.to_dict() for p in paginated.items],
        "total":       paginated.total,
        "pages":       paginated.pages,
        "current_page":page,
        "has_next":    paginated.has_next,
        "has_prev":    paginated.has_prev,
    }), 200


@history_bp.route("/history/<int:prediction_id>", methods=["GET"])
@jwt_required()
def get_single(prediction_id):
    user_id = get_jwt_identity()
    claims  = get_jwt()
    pred = Prediction.query.get_or_404(prediction_id)
    if pred.user_id != user_id and claims.get("role") != "admin":
        return jsonify({"error": "Access denied"}), 403
    return jsonify(pred.to_dict()), 200


@history_bp.route("/history/<int:prediction_id>", methods=["DELETE"])
@jwt_required()
def delete_prediction(prediction_id):
    user_id = get_jwt_identity()
    pred = Prediction.query.get_or_404(prediction_id)
    if pred.user_id != user_id:
        return jsonify({"error": "Access denied"}), 403
    db.session.delete(pred)
    db.session.commit()
    return jsonify({"message": "Prediction deleted"}), 200