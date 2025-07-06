-- Drop das tabelas existentes (para recriação limpa)
DROP TABLE IF EXISTS Inventario, Item, Player, Chunk, Mapa, Bioma CASCADE;

-- Bioma
CREATE TABLE Bioma (
    id_bioma   SERIAL PRIMARY KEY,
    nome       VARCHAR(100) NOT NULL,
    descricao  TEXT        NOT NULL
);

-- Mapa
CREATE TABLE Mapa (
    id_mapa  SERIAL PRIMARY KEY,
    nome     VARCHAR(100) NOT NULL,
    turno    VARCHAR(50)  NOT NULL,
    UNIQUE (nome, turno)
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
    nome             VARCHAR(100) NOT NULL,
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
    nome        VARCHAR(100) NOT NULL,
    tipo        VARCHAR(50)  NOT NULL,
    poder       INT,
    durabilidade INT
);

-- Inventario
CREATE TABLE Inventario (
    id           SERIAL PRIMARY KEY,
    player_id    INT    NOT NULL REFERENCES Player(id_player) ON DELETE CASCADE ON UPDATE CASCADE,
    item_id      INT    NOT NULL REFERENCES Item(id_item)   ON DELETE RESTRICT ON UPDATE CASCADE,
    quantidade   INT    NOT NULL
);

-- Índices de performance
CREATE INDEX idx_chunk_bioma    ON Chunk (id_bioma);
CREATE INDEX idx_chunk_mapa     ON Chunk (id_mapa);
CREATE INDEX idx_player_chunk   ON Player (current_chunk_id);
CREATE INDEX idx_inventario_plr ON Inventario (player_id);
CREATE INDEX idx_inventario_itm ON Inventario (item_id);