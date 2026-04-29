from flask import Blueprint, render_template, redirect, url_for, session

from database.db import conectar

movimentacoes = Blueprint("movimentacoes", __name__)


@movimentacoes.route("/movimentacoes")
def listar_movimentacoes():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            mov.id_movimentacao,
            mat.nome AS material,
            usu.nome AS usuario,
            mov.tipo,
            mov.quantidade,
            mov.observacao,
            mov.data_movimentacao
        FROM movimentacoes mov
        INNER JOIN materiais mat ON mov.id_material = mat.id_material
        INNER JOIN usuarios usu ON mov.id_usuario = usu.id_usuario
        ORDER BY mov.data_movimentacao DESC
    """)

    historico = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("movimentacoes.html", historico=historico)