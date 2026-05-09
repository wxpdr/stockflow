from database.db import conectar


def listar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            id_usuario,
            nome,
            email,
            perfil,
            status,
            data_criacao
        FROM usuarios
        ORDER BY nome
    """)

    usuarios = cursor.fetchall()

    cursor.close()
    conexao.close()

    return usuarios


def cadastrar_usuario(nome, email, senha, perfil):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO usuarios
        (nome, email, senha, perfil, status)
        VALUES (%s, %s, %s, %s, 'ativo')
    """, (nome, email, senha, perfil))

    conexao.commit()

    cursor.close()
    conexao.close()