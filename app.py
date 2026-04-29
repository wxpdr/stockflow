from flask import Flask, render_template, session, redirect, url_for
from database.db import conectar
from routes.auth_routes import auth
from routes.material_routes import materiais
from routes.movimentacao_routes import movimentacoes

app = Flask(__name__)
app.secret_key = "stockflow_chave_temporaria_dev"

app.register_blueprint(auth)
app.register_blueprint(materiais)
app.register_blueprint(movimentacoes)

@app.route("/")
def dashboard():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    return render_template("dashboard.html")


@app.route("/teste-banco")
def teste_banco():
    conexao = conectar()

    if not conexao:
        return "Erro ao conectar ao banco ❌"

    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuarios")

    resultados = cursor.fetchall()

    conexao.close()

    return str(resultados)


if __name__ == "__main__":
    app.run(debug=True)