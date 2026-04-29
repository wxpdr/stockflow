"""
Script de inicialização do banco de dados do sistema StockFlow.

Objetivo:
Permitir a criação automática da estrutura do banco de dados (database, tabelas e dados iniciais)
sem a necessidade de intervenção manual via ferramentas como MySQL Workbench.

Funcionamento:
- Executa o script SQL localizado em sql/stockflow.sql
- Cria o banco de dados caso não exista
- Cria todas as tabelas necessárias para o funcionamento do sistema
- Insere um usuário administrador padrão (seed)

Observação:
Atualmente, a senha do usuário administrador é armazenada em formato simples (texto puro),
sendo esta uma abordagem temporária para fins de desenvolvimento inicial (MVP).

Em versões futuras, será implementado:
- Criptografia de senha (bcrypt)
- Melhorias de segurança no processo de autenticação
"""

import mysql.connector

def inicializar_banco():
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="130500"
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