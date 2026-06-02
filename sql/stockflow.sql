DROP DATABASE IF EXISTS stockflow;
CREATE DATABASE stockflow;
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
    nome VARCHAR(100) NOT NULL
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

INSERT INTO usuarios (nome, email, senha, perfil, status) VALUES
('Administrador', 'admin@stockflow.com', 'pbkdf2_sha256$260000$7f1d9f5fdc9e4cebb0f67f5052df1a9d$8ef50186a3f3902fb0287c193464fb646caa956e311f2f898110fda75fa1b350', 'administrador', 'ativo'),
('Funcionário Estoque', 'funcionario@stockflow.com', 'pbkdf2_sha256$260000$9f08cf63b21f426d8e38f7b65b9379b2$cde7bf71413d3115600e38665e3e8edfc0e545a4be3987ebd0484563cf9af09a', 'funcionario', 'ativo'),
('Usuário Inativo', 'inativo@stockflow.com', 'pbkdf2_sha256$260000$9f08cf63b21f426d8e38f7b65b9379b2$cde7bf71413d3115600e38665e3e8edfc0e545a4be3987ebd0484563cf9af09a', 'funcionario', 'inativo');

INSERT INTO categorias (nome) VALUES
('Madeiras e Chapas'),
('Ferragens'),
('Colas e Adesivos'),
('Acabamentos'),
('Parafusos e Fixadores'),
('Ferramentas'),
('Embalagens'),
('EPI e Segurança');

INSERT INTO materiais (nome, id_categoria, quantidade_atual, quantidade_minima, status) VALUES
('Chapa MDF Branco 18mm', 1, 12, 5, 'ativo'),
('Chapa MDF Amadeirado 15mm', 1, 4, 5, 'ativo'),
('Compensado Naval 18mm', 1, 7, 3, 'ativo'),
('Sarrafo de Pinus', 1, 25, 10, 'ativo'),
('Dobradiça Caneco 35mm', 2, 80, 30, 'ativo'),
('Corrediça Telescópica 45cm', 2, 18, 20, 'ativo'),
('Puxador Alumínio 20cm', 2, 40, 15, 'ativo'),
('Cola de Madeira 1kg', 3, 6, 3, 'ativo'),
('Adesivo de Contato 750g', 3, 2, 3, 'ativo'),
('Fita de Borda Branca 22mm', 4, 9, 10, 'ativo'),
('Verniz Fosco 900ml', 4, 5, 2, 'ativo'),
('Tinta Primer 3,6L', 4, 3, 2, 'ativo'),
('Parafuso 4x40', 5, 350, 100, 'ativo'),
('Parafuso 3,5x16', 5, 90, 100, 'ativo'),
('Bucha Plástica 8mm', 5, 120, 50, 'ativo'),
('Lixa Grão 120', 6, 22, 10, 'ativo'),
('Luva de Proteção', 8, 8, 5, 'ativo'),
('Óculos de Proteção', 8, 0, 2, 'inativo');

INSERT INTO movimentacoes (id_material, id_usuario, tipo, quantidade, observacao) VALUES
(1, 1, 'entrada', 15, 'Compra inicial para reposição de estoque'),
(1, 2, 'saida', 3, 'Uso em produção de armário planejado'),
(2, 1, 'entrada', 8, 'Reposição de chapas amadeiradas'),
(2, 2, 'saida', 4, 'Uso em produção de painel'),
(5, 1, 'entrada', 100, 'Compra de ferragens'),
(5, 2, 'saida', 20, 'Uso em montagem de portas'),
(6, 1, 'entrada', 25, 'Reposição de corrediças'),
(6, 2, 'saida', 7, 'Uso em gaveteiro'),
(9, 2, 'descarte', 1, 'Produto danificado durante o uso'),
(10, 2, 'saida', 3, 'Acabamento de bordas'),
(13, 1, 'entrada', 500, 'Compra de parafusos'),
(13, 2, 'saida', 150, 'Uso em montagem geral'),
(14, 2, 'saida', 60, 'Uso em montagem de dobradiças'),
(16, 2, 'saida', 8, 'Uso em acabamento'),
(17, 1, 'entrada', 10, 'Reposição de equipamentos de segurança'),
(17, 2, 'saida', 2, 'Distribuição para funcionários');

INSERT INTO lista_compras (id_material, quantidade_sugerida, status) VALUES
(2, 10, 'pendente'),
(6, 15, 'pendente'),
(9, 5, 'pendente'),
(10, 12, 'pendente'),
(14, 200, 'pendente'),
(18, 5, 'pendente');