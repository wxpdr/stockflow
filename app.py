from flask import Flask, render_template
from routes.auth_routes import auth
from database.db import conectar

app = Flask(__name__)

app.register_blueprint(auth)

@app.route("/")
def dashboard():
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