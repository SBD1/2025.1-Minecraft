-- Tabelas básicas (sem dependências)

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

-- Item
CREATE TABLE Item (
    id_item     SERIAL PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL UNIQUE,
    tipo        VARCHAR(50)  NOT NULL,
    poder       INT,
    durabilidade INT
);
