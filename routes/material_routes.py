from flask import Blueprint, render_template, request, redirect, url_for, session

from models.material import (
    listar_materiais,
    listar_categorias,
    cadastrar_material,
    listar_alertas_baixo_estoque,
    buscar_material_por_id,
    registrar_entrada_material,
    registrar_saida_material,
    registrar_descarte_material
)

materiais = Blueprint("materiais", __name__)


@materiais.route("/materiais")
def listar_materiais_route():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    materiais_lista = listar_materiais()
    categorias = listar_categorias()

    return render_template(
        "materiais.html",
        materiais=materiais_lista,
        categorias=categorias
    )


@materiais.route("/materiais/cadastrar", methods=["POST"])
def cadastrar_material_route():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    nome = request.form.get("nome")
    id_categoria = request.form.get("id_categoria")
    quantidade_atual = request.form.get("quantidade_atual")
    quantidade_minima = request.form.get("quantidade_minima")

    if not nome or not id_categoria or quantidade_atual == "" or quantidade_minima == "":
        return "Preencha todos os campos obrigatórios."

    quantidade_atual = int(quantidade_atual)
    quantidade_minima = int(quantidade_minima)

    if quantidade_atual < 0 or quantidade_minima < 0:
        return "As quantidades não podem ser negativas."

    cadastrar_material(nome, id_categoria, quantidade_atual, quantidade_minima)

    return redirect(url_for("materiais.listar_materiais_route"))


@materiais.route("/materiais/entrada", methods=["POST"])
def registrar_entrada():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    id_material = request.form.get("id_material")
    quantidade = int(request.form.get("quantidade"))
    observacao = request.form.get("observacao")
    id_usuario = session["id_usuario"]

    if quantidade <= 0:
        return "A quantidade de entrada deve ser maior que zero."

    registrar_entrada_material(id_material, id_usuario, quantidade, observacao)

    return redirect(url_for("materiais.listar_materiais_route"))


@materiais.route("/materiais/saida", methods=["POST"])
def registrar_saida():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    id_material = request.form.get("id_material")
    quantidade = int(request.form.get("quantidade"))
    observacao = request.form.get("observacao")
    id_usuario = session["id_usuario"]

    if quantidade <= 0:
        return "A quantidade de saída deve ser maior que zero."

    material = buscar_material_por_id(id_material)

    if not material or quantidade > material["quantidade_atual"]:
        return "Quantidade indisponível em estoque."

    registrar_saida_material(id_material, id_usuario, quantidade, observacao)

    return redirect(url_for("materiais.listar_materiais_route"))


@materiais.route("/materiais/descarte", methods=["POST"])
def registrar_descarte():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    id_material = request.form.get("id_material")
    quantidade = int(request.form.get("quantidade"))
    observacao = request.form.get("observacao")
    id_usuario = session["id_usuario"]

    if quantidade <= 0:
        return "A quantidade de descarte deve ser maior que zero."

    material = buscar_material_por_id(id_material)

    if not material or quantidade > material["quantidade_atual"]:
        return "Quantidade indisponível em estoque."

    registrar_descarte_material(id_material, id_usuario, quantidade, observacao)

    return redirect(url_for("materiais.listar_materiais_route"))


@materiais.route("/alertas")
def listar_alertas():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    alertas = listar_alertas_baixo_estoque()

    return render_template("alertas.html", alertas=alertas)