"""Factory de la aplicación Flask."""
from flask import Flask, jsonify
from flask_cors import CORS

from app.core.config import get_settings
from app.core.exceptions import AppException


def create_app() -> Flask:
    settings = get_settings()

    app = Flask(__name__)
    app.config["DEBUG"] = settings.debug
    app.config["JSON_SORT_KEYS"] = False

    CORS(
        app,
        resources={r"/*": {"origins": settings.cors_origins_list}},
        supports_credentials=True,
    )

    # Blueprints
    from app.api.health import health_bp

    app.register_blueprint(health_bp)

    # Manejo de errores de negocio
    @app.errorhandler(AppException)
    def handle_app_exception(exc: AppException):
        return jsonify({"detail": exc.detail}), exc.status_code

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"detail": "Ruta no encontrada"}), 404

    @app.errorhandler(500)
    def server_error(_):
        return jsonify({"detail": "Error interno del servidor"}), 500

    return app