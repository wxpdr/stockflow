from flask import Blueprint, render_template, redirect, url_for, session

from models.movimentacao import listar_movimentacoes

movimentacoes = Blueprint("movimentacoes", __name__)


@movimentacoes.route("/movimentacoes")
def listar_movimentacoes_route():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    historico = listar_movimentacoes()

    return render_template("movimentacoes.html", historico=historico)