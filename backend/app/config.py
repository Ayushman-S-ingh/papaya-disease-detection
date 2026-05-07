"""
app/config.py
All configuration settings loaded from environment variables
"""
import os
from datetime import timedelta


class Config:
    # Core
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

    # Database
    DATABASE_URL = "sqlite:///papaya.db"

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 300}

    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-change-in-production")
    JWT_ACCESS_TOKEN_EXPIRES  = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # CORS
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")

    # File uploads
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

    # ML Model
    MODEL_PATH = os.environ.get(
    "MODEL_PATH",
    "app/ml/papaya_model.h5"
)
    IMG_SIZE = (224, 224)
    CONFIDENCE_THRESHOLD = 0.60

    # Disease classes (must match training order)
    DISEASE_CLASSES = [
    "Anthracnose",
    "Bacterial Spot",
    "Curl",
    "Healthy",
    "Mealybug",
    "Mite Disease",
    "Mosaic",
    "Ringspot"
    ]

    # ReportLab / PDF
    REPORT_OUTPUT_DIR = os.environ.get("REPORT_DIR", "reports")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 10,
        "max_overflow": 20,
    }


config = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
    "default":     DevelopmentConfig,
}