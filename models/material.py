from database.db import conectar


def listar_materiais(status=None):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT 
            m.id_material,
            m.nome,
            c.nome AS categoria,
            m.quantidade_atual,
            m.quantidade_minima,
            m.status
        FROM materiais m
        INNER JOIN categorias c ON m.id_categoria = c.id_categoria
    """

    parametros = ()

    if status:
        sql += " WHERE m.status = %s"
        parametros = (status,)

    sql += " ORDER BY m.nome"

    cursor.execute(sql, parametros)

    materiais = cursor.fetchall()

    cursor.close()
    conexao.close()

    return materiais


def listar_categorias():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_categoria, nome
        FROM categorias
        ORDER BY nome
    """)

    categorias = cursor.fetchall()

    cursor.close()
    conexao.close()

    return categorias


def cadastrar_material(nome, id_categoria, quantidade_atual, quantidade_minima):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO materiais 
        (nome, id_categoria, quantidade_atual, quantidade_minima, status)
        VALUES (%s, %s, %s, %s, 'ativo')
    """, (nome, id_categoria, quantidade_atual, quantidade_minima))

    conexao.commit()

    cursor.close()
    conexao.close()


def listar_alertas_baixo_estoque():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            m.id_material,
            m.nome,
            c.nome AS categoria,
            m.quantidade_atual,
            m.quantidade_minima,
            m.status
        FROM materiais m
        INNER JOIN categorias c ON m.id_categoria = c.id_categoria
        WHERE m.quantidade_atual <= m.quantidade_minima
        AND m.status = 'ativo'
        ORDER BY m.nome
    """)

    alertas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return alertas


def buscar_material_por_id(id_material):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_material, quantidade_atual
        FROM materiais
        WHERE id_material = %s
    """, (id_material,))

    material = cursor.fetchone()

    cursor.close()
    conexao.close()

    return material


def atualizar_estoque_entrada(id_material, quantidade):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE materiais
        SET quantidade_atual = quantidade_atual + %s
        WHERE id_material = %s
    """, (quantidade, id_material))

    conexao.commit()

    cursor.close()
    conexao.close()


def atualizar_estoque_saida(id_material, quantidade):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE materiais
        SET quantidade_atual = quantidade_atual - %s
        WHERE id_material = %s
    """, (quantidade, id_material))

    conexao.commit()

    cursor.close()
    conexao.close()

def atualizar_estoque_saida(id_material, quantidade):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE materiais
        SET quantidade_atual = quantidade_atual - %s
        WHERE id_material = %s
    """, (quantidade, id_material))

    conexao.commit()

    cursor.close()
    conexao.close()


def registrar_entrada_material(id_material, id_usuario, quantidade, observacao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE materiais
        SET quantidade_atual = quantidade_atual + %s
        WHERE id_material = %s
    """, (quantidade, id_material))

    cursor.execute("""
        INSERT INTO movimentacoes
        (id_material, id_usuario, tipo, quantidade, observacao)
        VALUES (%s, %s, 'entrada', %s, %s)
    """, (id_material, id_usuario, quantidade, observacao))

    conexao.commit()

    cursor.close()
    conexao.close()


def registrar_saida_material(id_material, id_usuario, quantidade, observacao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE materiais
        SET quantidade_atual = quantidade_atual - %s
        WHERE id_material = %s
    """, (quantidade, id_material))

    cursor.execute("""
        INSERT INTO movimentacoes
        (id_material, id_usuario, tipo, quantidade, observacao)
        VALUES (%s, %s, 'saida', %s, %s)
    """, (id_material, id_usuario, quantidade, observacao))

    conexao.commit()

    cursor.close()
    conexao.close()

def registrar_descarte_material(id_material, id_usuario, quantidade, observacao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE materiais
        SET quantidade_atual = quantidade_atual - %s
        WHERE id_material = %s
    """, (quantidade, id_material))

    cursor.execute("""
        INSERT INTO movimentacoes
        (id_material, id_usuario, tipo, quantidade, observacao)
        VALUES (%s, %s, 'descarte', %s, %s)
    """, (id_material, id_usuario, quantidade, observacao))

    conexao.commit()

    cursor.close()
    conexao.close()

def editar_material(id_material, nome, id_categoria, quantidade_minima):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE materiais
        SET
            nome = %s,
            id_categoria = %s,
            quantidade_minima = %s
        WHERE id_material = %s
    """, (nome, id_categoria, quantidade_minima, id_material))

    conexao.commit()

    cursor.close()
    conexao.close()

def inativar_material(id_material):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE materiais
        SET status = 'inativo'
        WHERE id_material = %s
    """, (id_material,))

    conexao.commit()

    cursor.close()
    conexao.close()

def reativar_material(id_material):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE materiais
        SET status = 'ativo'
        WHERE id_material = %s
    """, (id_material,))

    conexao.commit()

    cursor.close()
    conexao.close()