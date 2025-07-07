-- Drop das tabelas existentes (para recriação limpa)
DROP TABLE IF EXISTS Inventario, Item, Player, Chunk, Mapa, Bioma CASCADE;

-- Bioma
CREATE TABLE Bioma (
    id_bioma   SERIAL PRIMARY KEY,
    nome       VARCHAR(100) NOT NULL UNIQUE,
    descricao  TEXT        NOT NULL
);

-- Mapa
CREATE TABLE Mapa (
    id_mapa  SERIAL PRIMARY KEY,
    nome     VARCHAR(100) NOT NULL,
    turno    VARCHAR(50)  NOT NULL,
    CONSTRAINT uk_mapa_nome_turno UNIQUE (nome, turno)
);

-- Chunk
CREATE TABLE Chunk (
    id_chunk  SERIAL PRIMARY KEY,
    id_bioma  INT    NOT NULL REFERENCES Bioma(id_bioma) ON DELETE RESTRICT ON UPDATE CASCADE,
    id_mapa   INT    NOT NULL REFERENCES Mapa(id_mapa) ON DELETE RESTRICT ON UPDATE CASCADE,
    x         INT    NOT NULL,
    y         INT    NOT NULL
);

-- Player
CREATE TABLE Player (
    id_player        SERIAL PRIMARY KEY,
    nome             VARCHAR(100) NOT NULL UNIQUE,
    vida_maxima      INT    NOT NULL,
    vida_atual       INT    NOT NULL,
    forca            INT    NOT NULL,
    localizacao      VARCHAR(100),
    nivel            INT    NOT NULL,
    experiencia      INT    NOT NULL,
    current_chunk_id INT    REFERENCES Chunk(id_chunk) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Item
CREATE TABLE Item (
    id_item     SERIAL PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL UNIQUE,
    tipo        VARCHAR(50)  NOT NULL,
    poder       INT,
    durabilidade INT
);

-- Inventario
CREATE TABLE Inventario (
    id           SERIAL PRIMARY KEY,
    player_id    INT    NOT NULL REFERENCES Player(id_player) ON DELETE CASCADE ON UPDATE CASCADE,
    item_id      INT    NOT NULL REFERENCES Item(id_item)   ON DELETE RESTRICT ON UPDATE CASCADE,
    quantidade   INT    NOT NULL,
    CONSTRAINT uk_inventario_player_item UNIQUE(player_id, item_id)
);
-- DDL: criação da tabela fantasma
CREATE TABLE fantasma (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) NOT NULL,         -- 'minerador' ou 'construtor'
    chunk VARCHAR(50) NOT NULL,        -- nome ou id do chunk onde está o fantasma
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

-- Índices para melhorar busca
CREATE INDEX idx_fantasma_tipo ON fantasma(tipo);
CREATE INDEX idx_fantasma_chunk ON fantasma(chunk);

CREATE TABLE IF NOT EXISTS pontes (
    id SERIAL PRIMARY KEY,
    chunk_origem TEXT NOT NULL,
    chunk_destino TEXT NOT NULL,
    construida BOOLEAN DEFAULT FALSE
);

-- Garante que a coluna e a constraint só sejam adicionadas se não existirem.
DO $$
BEGIN
    -- Adicionar a coluna Id_Chunk_Atual à tabela Jogador se ela não existir
    -- Note que este bloco 'IF NOT EXISTS' não é padrão SQL, mas é uma extensão comum em PG.
    -- Ou você pode usar um bloco EXCEPTION WHEN duplicate_column THEN null; como antes
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='jogador' AND column_name='id_chunk_atual') THEN
        ALTER TABLE Jogador ADD COLUMN Id_Chunk_Atual INTEGER; -- <--- AGORA É INTEGER
    END IF;

-- Índices de performance
CREATE INDEX idx_chunk_bioma    ON Chunk (id_bioma);
CREATE INDEX idx_chunk_mapa     ON Chunk (id_mapa);
CREATE INDEX idx_player_chunk   ON Player (current_chunk_id);
CREATE INDEX idx_inventario_plr ON Inventario (player_id);
CREATE INDEX idx_inventario_itm ON Inventario (item_id);