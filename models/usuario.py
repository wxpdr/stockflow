from database.db import conectar
import hashlib
import hmac
import secrets


def gerar_hash_senha(senha):
    salt = secrets.token_hex(16)
    iteracoes = 260000
    hash_senha = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        salt.encode("utf-8"),
        iteracoes
    ).hex()

    return f"pbkdf2_sha256${iteracoes}${salt}${hash_senha}"


def senha_esta_criptografada(senha_armazenada):
    return isinstance(senha_armazenada, str) and senha_armazenada.startswith("pbkdf2_sha256$")


def verificar_senha(senha_informada, senha_armazenada):
    if not senha_informada or not senha_armazenada:
        return False

    if not senha_esta_criptografada(senha_armazenada):
        # Compatibilidade temporária para usuários antigos ainda salvos em texto puro.
        # Após o login, a senha deve ser atualizada para hash.
        return hmac.compare_digest(senha_informada, senha_armazenada)

    try:
        algoritmo, iteracoes, salt, hash_salvo = senha_armazenada.split("$")
        novo_hash = hashlib.pbkdf2_hmac(
            "sha256",
            senha_informada.encode("utf-8"),
            salt.encode("utf-8"),
            int(iteracoes)
        ).hex()

        return algoritmo == "pbkdf2_sha256" and hmac.compare_digest(novo_hash, hash_salvo)
    except ValueError:
        return False


def atualizar_senha_usuario(id_usuario, nova_senha):
    senha_hash = gerar_hash_senha(nova_senha)

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET senha = %s
        WHERE id_usuario = %s
    """, (senha_hash, id_usuario))

    conexao.commit()

    cursor.close()
    conexao.close()



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
    senha_hash = gerar_hash_senha(senha)

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO usuarios
        (nome, email, senha, perfil, status)
        VALUES (%s, %s, %s, %s, 'ativo')
    """, (nome, email, senha_hash, perfil))

    conexao.commit()

    cursor.close()
    conexao.close()

    
def editar_usuario(id_usuario, nome, email, perfil):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET nome = %s,
            email = %s,
            perfil = %s
        WHERE id_usuario = %s
    """, (nome, email, perfil, id_usuario))

    conexao.commit()

    cursor.close()
    conexao.close()


def inativar_usuario(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET status = 'inativo'
        WHERE id_usuario = %s
    """, (id_usuario,))

    conexao.commit()

    cursor.close()
    conexao.close()



def buscar_usuario_por_id(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_usuario, nome, email, perfil, status
        FROM usuarios
        WHERE id_usuario = %s
    """, (id_usuario,))

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return usuario


def reativar_usuario(id_usuario):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET status = 'ativo'
        WHERE id_usuario = %s
    """, (id_usuario,))

    conexao.commit()

    cursor.close()
    conexao.close()