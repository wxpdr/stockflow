from flask import Blueprint, render_template, request, redirect, url_for

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        # MVP: validação simples (sem banco ainda)
        if email == "admin" and senha == "123":
            return redirect(url_for("dashboard"))

        return "Login inválido"

    return render_template("login.html")