from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(funcao):
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        if "id_usuario" not in session:
            return redirect(url_for("auth.login"))

        return funcao(*args, **kwargs)

    return wrapper


def admin_required(funcao):
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        if "id_usuario" not in session:
            return redirect(url_for("auth.login"))

        if session.get("perfil") != "administrador":
            flash("Acesso restrito ao administrador.", "erro")
            return redirect(url_for("dashboard"))

        return funcao(*args, **kwargs)

    return wrapper