from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from models.usuario import (
    listar_usuarios,
    cadastrar_usuario,
    editar_usuario,
    inativar_usuario,
    reativar_usuario,
    buscar_usuario_por_id
)

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

@usuarios.route("/usuarios/editar", methods=["POST"])
def editar_usuario_route():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    id_usuario = request.form.get("id_usuario")
    nome = request.form.get("nome")
    email = request.form.get("email")
    perfil = request.form.get("perfil")

    usuario_atual = buscar_usuario_por_id(id_usuario)

    if not usuario_atual:
        flash("Usuário não encontrado.", "erro")
        return redirect(url_for("usuarios.listar_usuarios_route"))

    if not nome:
        nome = usuario_atual["nome"]

    if not email:
        email = usuario_atual["email"]

    if not perfil:
        perfil = usuario_atual["perfil"]

    editar_usuario(id_usuario, nome, email, perfil)

    flash("Usuário atualizado com sucesso.", "sucesso")

    return redirect(url_for("usuarios.listar_usuarios_route"))


@usuarios.route("/usuarios/inativar", methods=["POST"])
def inativar_usuario_route():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    id_usuario = request.form.get("id_usuario")

    inativar_usuario(id_usuario)

    flash("Usuário inativado com sucesso.", "sucesso")

    return redirect(url_for("usuarios.listar_usuarios_route"))

@usuarios.route("/usuarios/reativar", methods=["POST"])
def reativar_usuario_route():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    id_usuario = request.form.get("id_usuario")

    reativar_usuario(id_usuario)

    flash("Usuário reativado com sucesso.", "sucesso")

    return redirect(url_for("usuarios.listar_usuarios_route"))