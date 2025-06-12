-- Configurações para garantir que os comandos rodem sem parar em erros de "já existe"
-- Isso é útil se o script for executado em um ambiente onde partes já foram criadas.
SET client_min_messages TO WARNING; -- Suprime mensagens de NOTICE, mostrando WARNINGs e erros

CREATE TABLE IF NOT EXISTS Bioma (
    NomeBioma VARCHAR(100) PRIMARY KEY NOT NULL
);

CREATE TABLE IF NOT EXISTS Mapa (
    Nome VARCHAR(100) NOT NULL,
    Turno VARCHAR(50) NOT NULL,
    PRIMARY KEY (Nome, Turno)
);

CREATE TABLE IF NOT EXISTS Chunk (
    Numero_chunk INTEGER PRIMARY KEY NOT NULL,
    Id_bioma VARCHAR(100) NOT NULL,
    Id_mapa_nome VARCHAR(100) NOT NULL,
    Id_mapa_turno VARCHAR(50) NOT NULL,

    FOREIGN KEY (Id_bioma) REFERENCES Bioma(NomeBioma) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (Id_mapa_nome, Id_mapa_turno) REFERENCES Mapa(Nome, Turno) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Jogador (
    Id_Jogador SERIAL PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Vida_max INT NOT NULL,
    Vida_atual INT NOT NULL,
    xp INT NOT NULL,
    forca INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Inventario (
    id_jogador INT NOT NULL,          
    id_inventario INT NOT NULL,        
    Instancia_Item TEXT,
    ArmaduraEquipada VARCHAR(100),
    ArmaEquipada VARCHAR(100),

    PRIMARY KEY (id_jogador, id_inventario),
    FOREIGN KEY (id_jogador) REFERENCES Jogador(Id_Jogador) ON DELETE CASCADE ON UPDATE CASCADE
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

    -- Adicionar a constraint de chave estrangeira se ela não existir
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_jogador_chunk') THEN
        ALTER TABLE Jogador ADD CONSTRAINT fk_jogador_chunk
        FOREIGN KEY (Id_Chunk_Atual) REFERENCES Chunk(Numero_chunk) ON DELETE SET NULL ON UPDATE CASCADE;
    END IF;
END
$$ LANGUAGE plpgsql;


-- Índices para Chaves Estrangeiras (para otimização de performance em consultas)
CREATE INDEX IF NOT EXISTS idx_chunk_id_bioma ON Chunk (Id_bioma);
CREATE INDEX IF NOT EXISTS idx_chunk_id_mapa ON Chunk (Id_mapa_nome, Id_mapa_turno);
CREATE INDEX IF NOT EXISTS idx_inventario_id_jogador ON Inventario (id_jogador);
CREATE INDEX IF NOT EXISTS idx_jogador_id_chunk_atual ON Jogador (Id_Chunk_Atual);
