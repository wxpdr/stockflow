from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from models.usuario import listar_usuarios, cadastrar_usuario

usuarios = Blueprint("usuarios", __name__)


@usuarios.route("/usuarios")
def listar_usuarios_route():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    usuarios_lista = listar_usuarios()

    return render_template("usuarios.html", usuarios=usuarios_lista)


@usuarios.route("/usuarios/cadastrar", methods=["POST"])
def cadastrar_usuario_route():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    perfil = request.form.get("perfil")

    if not nome or not email or not senha or not perfil:
        flash("Preencha todos os campos do usuário.", "erro")
        return redirect(url_for("usuarios.listar_usuarios_route"))

    if len(senha) < 8:
        flash("A senha deve possuir no mínimo 8 caracteres.", "erro")
        return redirect(url_for("usuarios.listar_usuarios_route"))

    cadastrar_usuario(nome, email, senha, perfil)

    flash("Usuário cadastrado com sucesso.", "sucesso")

    return redirect(url_for("usuarios.listar_usuarios_route"))