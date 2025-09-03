from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from app.db import Session
from app.models import User
from . import bp
from .forms import LoginForm

@bp.route("/", methods=["GET", "POST"])
@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("products.lista_produtos"))
    form = LoginForm()
    if form.validate_on_submit():
        with Session() as db:
            user = db.query(User).filter(User.username == form.username.data.strip()).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login realizado com sucesso!", "success")
                next_url = request.args.get("next") or url_for("products.lista_produtos")
                return redirect(next_url)
        flash("Usuário ou senha inválidos.", "danger")
    return render_template("auth/login.html", form=form)

@bp.route("/logout")
def logout():
    logout_user()
    flash("Você saiu da sessão.", "info")
    return redirect(url_for("auth.login"))
