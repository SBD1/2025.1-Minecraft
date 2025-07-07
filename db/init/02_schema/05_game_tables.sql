-- Tabelas específicas do jogo

-- Fantasma
CREATE TABLE fantasma (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) NOT NULL,         -- 'minerador' ou 'construtor'
    chunk VARCHAR(50) NOT NULL,        -- nome ou id do chunk onde está o fantasma
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

-- Pontes (corrigindo erro de sintaxe)
CREATE TABLE pontes (
    id SERIAL PRIMARY KEY,
    chunk_origem TEXT NOT NULL,
    chunk_destino TEXT NOT NULL,
    construida BOOLEAN DEFAULT FALSE,
    durabilidade INT DEFAULT 100
);

-- Totem
CREATE TABLE totem (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    localizacao VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);
