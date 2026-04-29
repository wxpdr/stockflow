import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="130500",
            database="stockflow"
        )

        if conexao.is_connected():
            return conexao

    except Error as erro:
        print("Erro ao conectar:", erro)
        return None