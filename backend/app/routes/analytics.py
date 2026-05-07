"""
app/routes/analytics.py  —  Disease statistics and trends
"""
from collections import Counter
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import func
from ..models.prediction import Prediction
from ..models.user import User
from .. import db

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/summary", methods=["GET"])
@jwt_required()
def summary():
    user_id  = get_jwt_identity()
    claims   = get_jwt()
    is_admin = claims.get("role") == "admin"

    base_q = Prediction.query if is_admin else Prediction.query.filter_by(user_id=user_id)

    total        = base_q.count()
    disease_dist = (
        db.session.query(Prediction.disease_name, func.count(Prediction.id))
        .filter(Prediction.user_id == user_id if not is_admin else True)
        .group_by(Prediction.disease_name)
        .all()
    )
    severity_dist = (
        db.session.query(Prediction.severity, func.count(Prediction.id))
        .filter(Prediction.user_id == user_id if not is_admin else True)
        .group_by(Prediction.severity)
        .all()
    )
    avg_conf = base_q.with_entities(func.avg(Prediction.confidence)).scalar() or 0

    return jsonify({
        "total_predictions": total,
        "avg_confidence":    round(float(avg_conf) * 100, 1),
        "disease_distribution": {d: c for d, c in disease_dist},
        "severity_distribution": {s: c for s, c in severity_dist},
    }), 200


@analytics_bp.route("/trends", methods=["GET"])
@jwt_required()
def trends():
    user_id  = get_jwt_identity()
    claims   = get_jwt()
    is_admin = claims.get("role") == "admin"
    days     = request.args.get("days", 30, type=int)

    since = datetime.utcnow() - timedelta(days=days)
    query = Prediction.query.filter(Prediction.created_at >= since)
    if not is_admin:
        query = query.filter_by(user_id=user_id)

    preds = query.all()
    # Group by date
    by_date: dict = {}
    for p in preds:
        key = p.created_at.strftime("%Y-%m-%d")
        by_date.setdefault(key, []).append(p.disease_name)

    trend_data = [
        {"date": k, "count": len(v), "diseases": dict(Counter(v))}
        for k, v in sorted(by_date.items())
    ]
    return jsonify({"trends": trend_data, "days": days}), 200


# ── Report route ──────────────────────────────────────────────────────────────
from flask import Blueprint as _B
report_bp = _B("report", __name__)


@report_bp.route("/pdf/<int:prediction_id>", methods=["GET"])
@jwt_required()
def download_pdf(prediction_id):
    """Generate and return a PDF report for a prediction."""
    from flask import make_response
    from ..services.report_service import generate_pdf_report
    from ..models.prediction import Prediction as P
    from ..models.user import User as U

    user_id = get_jwt_identity()
    pred    = P.query.get_or_404(prediction_id)
    if pred.user_id != user_id:
        return jsonify({"error": "Access denied"}), 403

    user   = U.query.get(user_id)
    pdf_bytes = generate_pdf_report(pred, user)

    response = make_response(pdf_bytes)
    response.headers["Content-Type"]        = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename=report_{prediction_id}.pdf"
    return response