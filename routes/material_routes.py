from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from decorators import login_required, admin_required

from models.material import (
    listar_materiais,
    listar_categorias,
    cadastrar_material,
    listar_alertas_baixo_estoque,
    buscar_material_por_id,
    registrar_entrada_material,
    registrar_saida_material,
    registrar_descarte_material,
    editar_material,
    inativar_material,
    reativar_material,
    cadastrar_categoria,
    editar_categoria
)

materiais = Blueprint("materiais", __name__)


def converter_inteiro(valor, nome_campo):
    try:
        if valor is None or valor == "":
            return None, f"O campo {nome_campo} é obrigatório."

        numero = int(valor)

        return numero, None
    except ValueError:
        return None, f"O campo {nome_campo} deve conter um número válido."


def validar_material_ativo(id_material):
    material = buscar_material_por_id(id_material)

    if not material:
        return None, "Material não encontrado."

    if material["status"] != "ativo":
        return None, "Materiais inativos não podem receber movimentações."

    return material, None


@materiais.route("/materiais")
@login_required
def listar_materiais_route():
    materiais_ativos = listar_materiais("ativo")
    materiais_inativos = listar_materiais("inativo")
    categorias = listar_categorias()

    return render_template(
        "materiais.html",
        materiais=materiais_ativos,
        materiais_ativos=materiais_ativos,
        materiais_inativos=materiais_inativos,
        categorias=categorias
    )


@materiais.route("/materiais/cadastrar", methods=["POST"])
@admin_required
def cadastrar_material_route():
    nome = request.form.get("nome")
    id_categoria = request.form.get("id_categoria")
    quantidade_atual_raw = request.form.get("quantidade_atual")
    quantidade_minima_raw = request.form.get("quantidade_minima")

    if not nome or not id_categoria:
        flash("Preencha todos os campos obrigatórios.", "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    quantidade_atual, erro = converter_inteiro(quantidade_atual_raw, "quantidade atual")
    if erro:
        flash(erro, "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    quantidade_minima, erro = converter_inteiro(quantidade_minima_raw, "quantidade mínima")
    if erro:
        flash(erro, "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    if quantidade_atual < 0 or quantidade_minima < 0:
        flash("As quantidades não podem ser negativas.", "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    cadastrar_material(nome, id_categoria, quantidade_atual, quantidade_minima)

    flash("Material cadastrado com sucesso.", "sucesso")
    return redirect(url_for("materiais.listar_materiais_route"))


@materiais.route("/materiais/entrada", methods=["POST"])
@login_required
def registrar_entrada():
    id_material = request.form.get("id_material")
    quantidade_raw = request.form.get("quantidade")
    observacao = request.form.get("observacao")
    id_usuario = session["id_usuario"]

    quantidade, erro = converter_inteiro(quantidade_raw, "quantidade")
    if erro:
        flash(erro, "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    if quantidade <= 0:
        flash("A quantidade de entrada deve ser maior que zero.", "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    material, erro = validar_material_ativo(id_material)
    if erro:
        flash(erro, "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    registrar_entrada_material(id_material, id_usuario, quantidade, observacao)

    flash("Entrada registrada com sucesso.", "sucesso")
    return redirect(url_for("materiais.listar_materiais_route"))


@materiais.route("/materiais/saida", methods=["POST"])
@login_required
def registrar_saida():
    id_material = request.form.get("id_material")
    quantidade_raw = request.form.get("quantidade")
    observacao = request.form.get("observacao")
    id_usuario = session["id_usuario"]

    quantidade, erro = converter_inteiro(quantidade_raw, "quantidade")
    if erro:
        flash(erro, "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    if quantidade <= 0:
        flash("A quantidade de saída deve ser maior que zero.", "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    material, erro = validar_material_ativo(id_material)
    if erro:
        flash(erro, "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    if quantidade > material["quantidade_atual"]:
        flash("Quantidade indisponível em estoque.", "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    registrar_saida_material(id_material, id_usuario, quantidade, observacao)

    flash("Saída registrada com sucesso.", "sucesso")
    return redirect(url_for("materiais.listar_materiais_route"))


@materiais.route("/materiais/descarte", methods=["POST"])
@login_required
def registrar_descarte():
    id_material = request.form.get("id_material")
    quantidade_raw = request.form.get("quantidade")
    observacao = request.form.get("observacao")
    id_usuario = session["id_usuario"]

    quantidade, erro = converter_inteiro(quantidade_raw, "quantidade")
    if erro:
        flash(erro, "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    if quantidade <= 0:
        flash("A quantidade de descarte deve ser maior que zero.", "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    material, erro = validar_material_ativo(id_material)
    if erro:
        flash(erro, "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    if quantidade > material["quantidade_atual"]:
        flash("Quantidade indisponível em estoque.", "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    registrar_descarte_material(id_material, id_usuario, quantidade, observacao)

    flash("Descarte registrado com sucesso.", "sucesso")
    return redirect(url_for("materiais.listar_materiais_route"))


@materiais.route("/alertas")
@login_required
def listar_alertas():
    alertas = listar_alertas_baixo_estoque()

    return render_template("alertas.html", alertas=alertas)


@materiais.route("/materiais/editar", methods=["POST"])
@login_required
def editar_material_route():
    id_material = request.form.get("id_material")
    nome = request.form.get("nome")
    id_categoria = request.form.get("id_categoria")
    quantidade_minima_raw = request.form.get("quantidade_minima")

    if not nome or not id_categoria:
        flash("Preencha todos os campos da edição.", "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    quantidade_minima, erro = converter_inteiro(quantidade_minima_raw, "quantidade mínima")
    if erro:
        flash(erro, "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    if quantidade_minima < 0:
        flash("A quantidade mínima não pode ser negativa.", "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    material = buscar_material_por_id(id_material)

    if not material:
        flash("Material não encontrado.", "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    editar_material(id_material, nome, id_categoria, quantidade_minima)

    flash("Material atualizado com sucesso.", "sucesso")

    return redirect(url_for("materiais.listar_materiais_route"))


@materiais.route("/materiais/inativar", methods=["POST"])
@admin_required
def inativar_material_route():
    id_material = request.form.get("id_material")

    material = buscar_material_por_id(id_material)

    if not material:
        flash("Material não encontrado.", "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    inativar_material(id_material)

    flash("Material inativado com sucesso.", "sucesso")

    return redirect(url_for("materiais.listar_materiais_route"))


@materiais.route("/materiais/reativar", methods=["POST"])
@admin_required
def reativar_material_route():
    id_material = request.form.get("id_material")

    material = buscar_material_por_id(id_material)

    if not material:
        flash("Material não encontrado.", "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    reativar_material(id_material)

    flash("Material reativado com sucesso.", "sucesso")

    return redirect(url_for("materiais.listar_materiais_route"))


@materiais.route("/categorias/cadastrar", methods=["POST"])
@admin_required
def cadastrar_categoria_route():
    nome = request.form.get("nome")

    if not nome:
        flash("Informe o nome da categoria.", "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    cadastrar_categoria(nome)

    flash("Categoria cadastrada com sucesso.", "sucesso")

    return redirect(url_for("materiais.listar_materiais_route"))


@materiais.route("/categorias/editar", methods=["POST"])
@admin_required
def editar_categoria_route():
    id_categoria = request.form.get("id_categoria")
    nome = request.form.get("nome")

    if not id_categoria or not nome:
        flash("Preencha todos os campos da categoria.", "erro")
        return redirect(url_for("materiais.listar_materiais_route"))

    editar_categoria(id_categoria, nome)

    flash("Categoria atualizada com sucesso.", "sucesso")

    return redirect(url_for("materiais.listar_materiais_route"))