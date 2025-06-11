CREATE EXTENSION pg_cron;

-- Tabela Jogador
CREATE TABLE Jogador (
    id_jogador SERIAL PRIMARY KEY, -- SERIAL cria uma sequência auto-incrementável para a PK
    Nome VARCHAR(255) NOT NULL,
    Vida_max INTEGER NOT NULL CHECK (Vida_max > 0), -- Vida máxima deve ser positiva
    Vida_atual INTEGER NOT NULL CHECK (Vida_atual >= 0), -- Vida atual não pode ser negativa
    xp INTEGER NOT NULL DEFAULT 0 CHECK (xp >= 0), -- XP não pode ser negativo, valor padrão 0
    forca INTEGER NOT NULL DEFAULT 1 CHECK (forca > 0) -- Força deve ser positiva, valor padrão 1
);

-- Tabela Inventario
CREATE TABLE Inventario (
    id_inventario INTEGER UNIQUE NOT NULL, -- UNIQUE para garantir 1 inventário por jogador
    armaEquipada VARCHAR(255) DEFAULT 'Mãos Vazias', -- Valor padrão, O que o jogador tem na mão (ex: 'Machado', 'Espada')
    ArmaduraEquipada VARCHAR(255) DEFAULT 'Nenhuma', -- Valor padrão

    CONSTRAINT fk_jogador_inventario FOREIGN KEY (id_inventario)
        REFERENCES Jogador (id_jogador)
);

CREATE TABLE InventarioItem (
    id_inventario INTEGER PRIMARY KEY,
    nome_item VARCHAR(30) NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 1 CHECK (quantidade > 0),

    CONSTRAINT fk_inventario FOREIGN KEY (id_inventario)
        REFERENCES Inventario(id_inventario),

    CONSTRAINT fk_item FOREIGN KEY (nome_item)
        REFERENCES Item(nome)
);

CREATE TYPE tipo_item AS ENUM ('material', 'minerio');

-- Tabela Item
CREATE TABLE Item (
    nome VARCHAR(30) PRIMARY KEY,
    tipo_item tipo_item NOT NULL,
    descricao TEXT,
    raridade VARCHAR(30)
);


CREATE TABLE Bioma (
    Nome_bioma VARCHAR(30) UNIQUE NOT NULL PRIMARY KEY -- Nome do bioma deve ser único
);

CREATE TYPE ciclo_dia AS ENUM ('dia', 'tarde', 'noite');
-- Tabela Mapa
CREATE TABLE Mapa (
    nome_mapa VARCHAR(30) NOT NULL PRIMARY KEY,
    Turno ciclo_dia NOT NULL
);

-- Tabela Chunk
CREATE TABLE Chunk (
    id_chunk INTEGER PRIMARY KEY, -- Assumindo que o número do chunk é único e serve como PK
    id_bioma VARCHAR(30) NOT NULL,
    id_mapa VARCHAR(30) NOT NULL,
    -- Chave estrangeira para ligar ao Bioma
    CONSTRAINT fk_bioma_chunk FOREIGN KEY (id_bioma)
        REFERENCES Bioma (Nome_bioma),
    -- Chave estrangeira para ligar ao Mapa
    CONSTRAINT fk_mapa_chunk FOREIGN KEY (id_mapa)
        REFERENCES Mapa (nome_mapa)
);
