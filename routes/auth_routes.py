from flask import Blueprint, render_template, request, redirect, url_for, session

from database.db import conectar

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_usuario, nome, email, senha, perfil, status
            FROM usuarios
            WHERE email = %s
        """, (email,))

        usuario = cursor.fetchone()

        cursor.close()
        conexao.close()

        if usuario and usuario["senha"] == senha and usuario["status"] == "ativo":
            session["id_usuario"] = usuario["id_usuario"]
            session["nome"] = usuario["nome"]
            session["perfil"] = usuario["perfil"]

            return redirect(url_for("dashboard"))

        return render_template("login.html", erro="E-mail ou senha inválidos.")

    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login")) 