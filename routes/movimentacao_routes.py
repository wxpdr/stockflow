from flask import Blueprint, render_template

from decorators import admin_required
from models.movimentacao import listar_movimentacoes

movimentacoes = Blueprint("movimentacoes", __name__)


@movimentacoes.route("/movimentacoes")
@admin_required
def listar_movimentacoes_route():
    historico = listar_movimentacoes()

    return render_template("movimentacoes.html", historico=historico)