from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import db, Usuario, LogAcesso
from datetime import datetime

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        senha = request.form.get("password", "")
        user = Usuario.query.filter_by(username=username, ativo=True).first()

        sucesso = False
        motivo = ""
        if user and user.check_password(senha):
            login_user(user)
            user.ultimo_login = datetime.utcnow()
            sucesso = True
            db.session.commit()
            return redirect(url_for("main.index"))
        else:
            motivo = "Credenciais inválidas"
            flash("Usuário ou senha inválidos", "danger")

        # registra log sempre
        db.session.add(LogAcesso(usuario=user, sucesso=sucesso, motivo=motivo, ip=request.remote_addr if user else None))
        db.session.commit()

    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
