# app/__init__.py
from __future__ import annotations
from flask import Flask
from config import Config
from .helpers import csrf, login_manager
from .db import init_engine_and_session
from .models import Base, User

def create_app() -> Flask:
    # aponta para app/templates e app/static
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    # extensões
    csrf.init_app(app)
    login_manager.init_app(app)

    # banco (engine + Session)
    database_url = app.config.get("SQLALCHEMY_DATABASE_URI")
    if not database_url:
        raise RuntimeError("SQLALCHEMY_DATABASE_URI/DATABASE_URL não configurado no .env")

    init_engine_and_session(database_url)

    # criar tabelas se não existirem
    from . import db  # importa o módulo (evita problema de rebind do engine)
    Base.metadata.create_all(db.engine)

    # registrar blueprints
    from .blueprints.auth import bp as auth_bp
    from .blueprints.products import bp as products_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)

    # login loader
    @login_manager.user_loader
    def load_user(user_id: str):
        with db.Session() as s:
            return s.get(User, int(user_id))

    # encerrar sessão por request
    @app.teardown_appcontext
    def remove_session(exc=None):
        db.Session.remove()

    return app
