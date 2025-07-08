-- Drop das tabelas existentes (para recriação limpa)
DROP TABLE IF EXISTS Inventario, Item, Player, Chunk, Mapa, Bioma, aldeao, bob_mago, bob_construtor, vila, casa_aldeao CASCADE;

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

-- Vila
CREATE TABLE IF NOT EXISTS Vila (
    id_vila INTEGER PRIMARY KEY NOT NULL,
    nome_vila VARCHAR(100),
    descricao_vila TEXT,
    id_chunk INTEGER NOT NULL UNIQUE,
    CONSTRAINT fk_vila_chunk FOREIGN KEY (id_chunk) REFERENCES chunk(id_chunk) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS Casa_aldeao (
    id_casa SERIAL PRIMARY KEY,
    descricao_casa TEXT,
    vila INTEGER NOT NULL,
    CONSTRAINT fk_casa_vila FOREIGN KEY (vila) REFERENCES vila(id_vila) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
);

-- Aldeao
CREATE TABLE IF NOT EXISTS Aldeao (
    id_aldeao SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    descricao VARCHAR(500),
    id_casa INTEGER,
    CONSTRAINT chk_tipo_aldeao CHECK (tipo IN ('Normal', 'Mago', 'Construtor')),
    CONSTRAINT fk_aldeao_casa FOREIGN KEY (id_casa) REFERENCES casa_aldeao(id_casa) ON DELETE SET NULL ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS Bob_mago (
    id_aldeao_mago INTEGER PRIMARY KEY,
    habilidade_mago VARCHAR(100),
    nivel INTEGER NOT NULL,
    CONSTRAINT fk_mago_aldeao FOREIGN KEY (id_aldeao_mago) REFERENCES aldeao(id_aldeao) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS Bob_construtor (
    id_aldeao_construtor INTEGER PRIMARY KEY,
    habilidades_construtor TEXT,
    nivel INTEGER NOT NULL,
    CONSTRAINT fk_construtor_aldeao FOREIGN KEY (id_aldeao_construtor) REFERENCES aldeao(id_aldeao) ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE INITIALLY DEFERRED
);


-- Índices de performance
CREATE INDEX IF NOT EXISTS idx_chunk_id_bioma ON chunk (id_bioma);
CREATE INDEX IF NOT EXISTS idx_chunk_id_mapa ON chunk (id_mapa);

CREATE INDEX IF NOT EXISTS idx_inventario_player_id ON inventario (player_id);
CREATE INDEX IF NOT EXISTS idx_inventario_item_id ON inventario (item_id);

CREATE INDEX IF NOT EXISTS idx_player_current_chunk_id ON player (current_chunk_id);

CREATE INDEX IF NOT EXISTS idx_vila_id_chunk ON vila (id_chunk);

CREATE INDEX IF NOT EXISTS idx_casa_aldeao_vila ON casa_aldeao (vila);

CREATE INDEX IF NOT EXISTS idx_aldeao_id_casa ON aldeao (id_casa);