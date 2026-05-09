from database.db import conectar


def listar_movimentacoes():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            mov.id_movimentacao,
            mat.nome AS material,
            usu.nome AS usuario,
            mov.tipo,
            mov.quantidade,
            mov.observacao,
            mov.data_movimentacao
        FROM movimentacoes mov
        INNER JOIN materiais mat ON mov.id_material = mat.id_material
        INNER JOIN usuarios usu ON mov.id_usuario = usu.id_usuario
        ORDER BY mov.data_movimentacao DESC
    """)

    movimentacoes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return movimentacoes