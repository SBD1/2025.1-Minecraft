-- Tabelas com dependências das tabelas básicas

-- Chunk (depende de Bioma e Mapa)
CREATE TABLE Chunk (
    id_chunk  SERIAL PRIMARY KEY,
    id_bioma  INT    NOT NULL REFERENCES Bioma(id_bioma) ON DELETE RESTRICT ON UPDATE CASCADE,
    id_mapa   INT    NOT NULL REFERENCES Mapa(id_mapa) ON DELETE RESTRICT ON UPDATE CASCADE,
    x         INT    NOT NULL,
    y         INT    NOT NULL
);

-- Player (depende de Chunk, mas com referência nullable)
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
