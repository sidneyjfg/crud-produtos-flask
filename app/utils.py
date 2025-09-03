from __future__ import annotations
from flask import current_app


def get_database_url(app=None):
    if app is None:
        app = current_app
    url = app.config.get("SQLALCHEMY_DATABASE_URI")
    if not url:
        raise RuntimeError("DATABASE_URL não configurado. Defina no .env")
    return url
