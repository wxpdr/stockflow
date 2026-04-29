from flask import Blueprint, render_template, request, redirect, url_for, session

from database.db import conectar

materiais = Blueprint("materiais", __name__)


@materiais.route("/materiais")
def listar_materiais():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            m.id_material,
            m.nome,
            c.nome AS categoria,
            m.quantidade_atual,
            m.quantidade_minima,
            m.status
        FROM materiais m
        INNER JOIN categorias c ON m.id_categoria = c.id_categoria
        ORDER BY m.nome
    """)

    materiais_lista = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("materiais.html", materiais=materiais_lista)


@materiais.route("/materiais/cadastrar", methods=["POST"])
def cadastrar_material():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    nome = request.form.get("nome")
    id_categoria = request.form.get("id_categoria")
    quantidade_atual = request.form.get("quantidade_atual")
    quantidade_minima = request.form.get("quantidade_minima")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO materiais 
        (nome, id_categoria, quantidade_atual, quantidade_minima, status)
        VALUES (%s, %s, %s, %s, 'ativo')
    """, (nome, id_categoria, quantidade_atual, quantidade_minima))

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect(url_for("materiais.listar_materiais"))

@materiais.route("/materiais/entrada", methods=["POST"])
def registrar_entrada():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    id_material = request.form.get("id_material")
    quantidade = int(request.form.get("quantidade"))
    observacao = request.form.get("observacao")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE materiais
        SET quantidade_atual = quantidade_atual + %s
        WHERE id_material = %s
    """, (quantidade, id_material))

    cursor.execute("""
        INSERT INTO movimentacoes
        (id_material, id_usuario, tipo, quantidade, observacao)
        VALUES (%s, %s, 'entrada', %s, %s)
    """, (id_material, session["id_usuario"], quantidade, observacao))

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect(url_for("materiais.listar_materiais"))

@materiais.route("/materiais/saida", methods=["POST"])
def registrar_saida():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    id_material = request.form.get("id_material")
    quantidade = int(request.form.get("quantidade"))
    observacao = request.form.get("observacao")

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT quantidade_atual
        FROM materiais
        WHERE id_material = %s
    """, (id_material,))

    material = cursor.fetchone()

    if not material or quantidade > material["quantidade_atual"]:
        cursor.close()
        conexao.close()
        return "Quantidade indisponível em estoque."

    cursor.execute("""
        UPDATE materiais
        SET quantidade_atual = quantidade_atual - %s
        WHERE id_material = %s
    """, (quantidade, id_material))

    cursor.execute("""
        INSERT INTO movimentacoes
        (id_material, id_usuario, tipo, quantidade, observacao)
        VALUES (%s, %s, 'saida', %s, %s)
    """, (id_material, session["id_usuario"], quantidade, observacao))

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect(url_for("materiais.listar_materiais"))