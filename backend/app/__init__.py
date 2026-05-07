"""
app/__init__.py
Flask application factory with all extensions initialized
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.predict import predict_bp
    from .routes.history import history_bp
    from .routes.analytics import analytics_bp
    from .routes.report import report_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp,      url_prefix="/api/auth")
    app.register_blueprint(predict_bp,   url_prefix="/api")
    app.register_blueprint(history_bp,   url_prefix="/api")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
    app.register_blueprint(report_bp,    url_prefix="/api/report")
    app.register_blueprint(admin_bp,     url_prefix="/api/admin")

    # Health check
    @app.route("/api/health")
    def health():
        return {"status": "healthy", "version": "1.0.0"}

    return app