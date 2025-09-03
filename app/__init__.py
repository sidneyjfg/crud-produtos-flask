from pathlib import Path
from flask import Flask
from config import Config
from .helpers import csrf, login_manager
from .db import init_engine_and_session
from .models import Base, User
from . import db


def create_app() -> Flask:
    # raiz do projeto = .../crud-produtos
    project_root = Path(__file__).resolve().parent.parent
    templates_dir = project_root / "templates"  # fora de app/
    static_dir = project_root / "static"        # fora de app/

    app = Flask(
        __name__,
        template_folder=str(templates_dir),
        static_folder=str(static_dir),
    )
    app.config.from_object(Config)

    # Extensões
    csrf.init_app(app)
    login_manager.init_app(app)

    # DB
    init_engine_and_session(app.config["SQLALCHEMY_DATABASE_URI"])
    Base.metadata.create_all(db.engine)

    # Blueprints (sem template_folder — usam o diretório central acima)
    from .blueprints.auth import bp as auth_bp
    from .blueprints.products import bp as products_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)

    @login_manager.user_loader
    def load_user(user_id: str):
        with db.Session() as s:
            return s.get(User, int(user_id))

    @app.teardown_appcontext
    def remove_session(exc=None):
        db.Session.remove()

    return app
