"""Health checks: servidor vivo + conexión a DB."""
from flask import Blueprint, jsonify
from sqlalchemy import text

from app.infrastructure.database.connection import get_session

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    return jsonify({"status": "ok", "service": "Sabor Caleño SGO"})


@health_bp.get("/health/db")
def health_db():
    try:
        with get_session() as db:
            db.execute(text("SELECT 1"))
        return jsonify({"status": "ok", "database": "connected"})
    except Exception as exc:
        return jsonify({"status": "error", "database": str(exc)}), 500