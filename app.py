import os

from dotenv import load_dotenv
from flask import Flask, render_template, session, redirect, url_for

load_dotenv()

from routes.auth_routes import auth
from routes.material_routes import materiais
from routes.movimentacao_routes import movimentacoes
from routes.usuario_routes import usuarios

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError(
        "SECRET_KEY não configurada. Defina essa variável no arquivo .env "
        "ou nas variáveis de ambiente da hospedagem."
    )

app.register_blueprint(auth)
app.register_blueprint(materiais)
app.register_blueprint(movimentacoes)
app.register_blueprint(usuarios)


@app.route("/")
def dashboard():
    if "id_usuario" not in session:
        return redirect(url_for("auth.login"))

    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
