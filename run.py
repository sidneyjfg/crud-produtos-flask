# run.py
from __future__ import annotations
import click
from werkzeug.security import generate_password_hash
from app import create_app
from app import db
from app.models import Base, User

app = create_app()

@app.cli.command("init-db")
def init_db():
    """Cria as tabelas no banco (se não existirem)."""
    Base.metadata.create_all(bind=db.engine)
    click.echo("Tabelas criadas/atualizadas.")

@app.cli.command("create-user")
@click.option("--username", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
def create_user(username: str, password: str):
    """Cria um usuário de login no banco."""
    with db.Session() as session:
        exists = session.query(User).filter(User.username == username).first()
        if exists:
            click.echo("Usuário já existe.")
            return
        user = User(username=username.strip(),
                    password_hash=generate_password_hash(password))
        session.add(user)
        session.commit()
        click.echo(f"Usuário '{username}' criado com sucesso!")

if __name__ == "__main__":
    # subir o servidor (desenvolvimento)
    debug = app.config.get("FLASK_DEBUG", False)
    app.run(debug=debug)
