"""
Script de inicialização do banco de dados do sistema StockFlow.

Objetivo:
Permitir a criação automática da estrutura do banco de dados a partir do arquivo
sql/stockflow.sql.

Observação:
As credenciais do banco são lidas por variáveis de ambiente, evitando que senhas
fiquem expostas diretamente no código-fonte.
"""

import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def inicializar_banco():
    conexao = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    cursor = conexao.cursor()

    with open("sql/stockflow.sql", "r", encoding="utf-8") as arquivo:
        comandos = arquivo.read()

    for comando in comandos.split(";"):
        if comando.strip():
            cursor.execute(comando)

    conexao.commit()
    cursor.close()
    conexao.close()

    print("Banco inicializado com sucesso.")
