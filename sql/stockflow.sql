CREATE DATABASE IF NOT EXISTS stockflow;
USE stockflow;

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    perfil ENUM('administrador', 'funcionario') NOT NULL,
    status ENUM('ativo', 'inativo') NOT NULL DEFAULT 'ativo',
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE materiais (
    id_material INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_categoria INT NOT NULL,
    quantidade_atual INT NOT NULL DEFAULT 0,
    quantidade_minima INT NOT NULL DEFAULT 0,
    status ENUM('ativo', 'inativo') NOT NULL DEFAULT 'ativo',
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

CREATE TABLE movimentacoes (
    id_movimentacao INT AUTO_INCREMENT PRIMARY KEY,
    id_material INT NOT NULL,
    id_usuario INT NOT NULL,
    tipo ENUM('entrada', 'saida', 'descarte') NOT NULL,
    quantidade INT NOT NULL,
    observacao TEXT,
    data_movimentacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_material) REFERENCES materiais(id_material),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE lista_compras (
    id_item_compra INT AUTO_INCREMENT PRIMARY KEY,
    id_material INT NOT NULL,
    quantidade_sugerida INT NOT NULL,
    status ENUM('pendente', 'comprado') NOT NULL DEFAULT 'pendente',
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_material) REFERENCES materiais(id_material)
);


-- Inserção de usuário administrador padrão (seed)
-- Este usuário é criado apenas se não existir
-- Senha em texto simples temporária (será substituída por hash futuramente)


INSERT INTO usuarios (nome, email, senha, perfil, status)
SELECT 'Administrador', 'admin@stockflow.com', '12345678', 'administrador', 'ativo'
WHERE NOT EXISTS (
    SELECT 1 FROM usuarios WHERE email = 'admin@stockflow.com'
);