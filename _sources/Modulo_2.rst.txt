.. _Módulo 2:Documentação do Esquema e Dados do Projeto.. sectnum:::depth: 2.. contents:: Sumário:depth: 2:local:Esquema do Banco de Dados (DDL)Este é o DDL (Data Definition Language) para criar a estrutura do banco de dados do projeto. Ele define as tabelas, colunas, chaves primárias e estrangeiras necessárias... code-block:: sql-- Configurações para garantir que os comandos rodem sem parar em erros de "já existe"
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
Manipulação de Dados (DML)Este script DML (Data Manipulation Language) insere alguns dados iniciais nas tabelas do banco de dados para testes e demonstrações... code-block:: sqlINSERT INTO Mapa (Nome, Turno)
VALUES
    ('Mapa_Principal', 'Dia'),
    ('Mapa_Principal', 'Noite')
ON CONFLICT (Nome, Turno) DO NOTHING; 

INSERT INTO Bioma (NomeBioma)
VALUES
    ('Deserto'),
    ('Oceano'),
    ('Selva'),
    ('Floresta')
ON CONFLICT (NomeBioma) DO NOTHING; 

INSERT INTO Chunk (Numero_chunk, Id_bioma, Id_mapa_nome, Id_mapa_turno)
VALUES
    (1, 'Deserto', 'Mapa_Principal', 'Dia'),
    (2, 'Oceano', 'Mapa_Principal', 'Dia'),
    (3, 'Selva', 'Mapa_Principal', 'Noite'),
    (4, 'Floresta', 'Mapa_Principal', 'Noite')
ON CONFLICT (Numero_chunk) DO NOTHING;

INSERT INTO Jogador (Nome, Vida_max, Vida_atual, xp, forca, Id_Chunk_Atual)
VALUES
    ('Player1', 100, 100, 0, 10, 1), 
    ('Player2', 120, 120, 50, 12, 2); 

INSERT INTO Inventario (id_jogador, id_inventario, Instancia_Item, ArmaduraEquipada, ArmaEquipada)
VALUES
    (1, 1, '{"item_id": 101, "quantidade": 5}', 'Capacete de Ferro', 'Espada de Diamante'),
    (2, 1, '{"item_id": 201, "quantidade": 1}', 'Armadura de Couro', 'Arco Longo')
ON CONFLICT (id_jogador, id_inventario) DO NOTHING; 
Linguagem de Consulta de Dados (DQL)Aqui estão algumas consultas DQL (Data Query Language) para recuperar e analisar os dados armazenados no banco de dados... code-block:: sql-- =================================================================
--                  Consultas Básicas
-- Seleciona todos os dados de cada tabela individualmente.
-- =================================================================

-- Seleciona todos os mapas
SELECT * FROM Mapa;

-- Seleciona todos os biomas
SELECT * FROM Bioma;

-- Seleciona todos os chunks
SELECT * FROM Chunk;

-- Seleciona todos os jogadores
SELECT * FROM Jogador;

-- Seleciona todos os inventários
SELECT * FROM Inventario;

-- Consulta 1: Jogadores e sua Localização Atual
-- Mostra em qual chunk, bioma, mapa e turno cada jogador está.
SELECT
    j.Nome AS Nome_Jogador,
    j.Vida_atual,
    j.xp,
    c.Numero_chunk,
    c.Id_bioma AS Bioma,
    c.Id_mapa_nome AS Mapa,
    c.Id_mapa_turno AS Turno
FROM
    Jogador j
JOIN
    Chunk c ON j.Id_Chunk_Atual = c.Numero_chunk;


-- Consulta 2: Inventário de Cada Jogador
-- Lista os itens, armadura e arma equipada para cada jogador.
SELECT
    j.Nome AS Nome_Jogador,
    i.Instancia_Item,
    i.ArmaduraEquipada,
    i.ArmaEquipada
FROM
    Inventario i
JOIN
    Jogador j ON i.id_jogador = j.Id_jogador; -- Assumindo que 'Id_jogador' é a chave primária da tabela Jogador.


-- Consulta 3: Detalhes Completos dos Chunks
-- Visualiza os detalhes de cada chunk, incluindo o nome do bioma e as informações do mapa.
SELECT
    c.Numero_chunk,
    b.NomeBioma,
    m.Nome AS Nome_Mapa,
    m.Turno
FROM
    Chunk c
JOIN
    Bioma b ON c.Id_bioma = b.NomeBioma
JOIN
    Mapa m ON c.Id_mapa_nome = m.Nome AND c.Id_mapa_turno = m.Turno;
DML: Geração de 1000 ChunksEste script DML avançado preenche o banco de dados com 1000 "chunks" para simular um mapa maior. Ele inclui lógica para distribuir os biomas (Oceano, Deserto, Selva, Floresta) de forma programática... code-block:: sql-- Script DML para popular o banco de dados com 1000 chunks
-- Mapa: 32x32 chunks (1024 chunks total, mas vamos usar 1000)
-- Estrutura: Oceano ao redor, deserto no centro (20%), selva e floresta no resto

-- Inserir mapas (Dia e Noite)
INSERT INTO Mapa (Nome, Turno)
VALUES
    ('Mapa_Principal', 'Dia'),
    ('Mapa_Principal', 'Noite')
ON CONFLICT (Nome, Turno) DO NOTHING; 

-- Inserir biomas
INSERT INTO Bioma (NomeBioma)
VALUES
    ('Deserto'),
    ('Oceano'),
    ('Selva'),
    ('Floresta')
ON CONFLICT (NomeBioma) DO NOTHING; 

-- Função para gerar chunks com a distribuição especificada
-- Mapa 32x32 com oceano na borda, deserto no centro, selva e floresta no resto
DO $$
DECLARE
    chunk_id INTEGER := 1;
    x INTEGER;
    y INTEGER;
    biome_name VARCHAR(100);
    map_size INTEGER := 32;
    center_start INTEGER := 12; -- Início da área central (deserto)
    center_end INTEGER := 20;   -- Fim da área central (deserto)
    desert_chunks INTEGER := 0;
    ocean_chunks INTEGER := 0;
    jungle_chunks INTEGER := 0;
    forest_chunks INTEGER := 0;
BEGIN
    -- Gerar chunks para o mapa de dia
    FOR y IN 1..map_size LOOP
        FOR x IN 1..map_size LOOP
            -- Determinar bioma baseado na posição
            IF x = 1 OR x = map_size OR y = 1 OR y = map_size THEN
                -- Borda: Oceano
                biome_name := 'Oceano';
                ocean_chunks := ocean_chunks + 1;
            ELSIF x >= center_start AND x <= center_end AND y >= center_start AND y <= center_end THEN
                -- Centro: Deserto (área 9x9 = 81 chunks, aproximadamente 20% de 1000)
                biome_name := 'Deserto';
                desert_chunks := desert_chunks + 1;
            ELSE
                -- Resto: Alternar entre Selva e Floresta
                IF (x + y) % 2 = 0 THEN
                    biome_name := 'Selva';
                    jungle_chunks := jungle_chunks + 1;
                ELSE
                    biome_name := 'Floresta';
                    forest_chunks := forest_chunks + 1;
                END IF;
            END IF;
            
            -- Inserir chunk
            INSERT INTO Chunk (Numero_chunk, Id_bioma, Id_mapa_nome, Id_mapa_turno)
            VALUES (chunk_id, biome_name, 'Mapa_Principal', 'Dia')
            ON CONFLICT (Numero_chunk) DO NOTHING;
            
            chunk_id := chunk_id + 1;
            
            -- Parar após 1000 chunks
            IF chunk_id > 1000 THEN
                EXIT;
            END IF;
        END LOOP;
        
        -- Parar após 1000 chunks
        IF chunk_id > 1000 THEN
            EXIT;
        END IF;
    END LOOP;
    
    -- Gerar chunks para o mapa de noite (mesma distribuição)
    chunk_id := 1001;
    FOR y IN 1..map_size LOOP
        FOR x IN 1..map_size LOOP
            -- Determinar bioma baseado na posição
            IF x = 1 OR x = map_size OR y = 1 OR y = map_size THEN
                -- Borda: Oceano
                biome_name := 'Oceano';
            ELSIF x >= center_start AND x <= center_end AND y >= center_start AND y <= center_end THEN
                -- Centro: Deserto
                biome_name := 'Deserto';
            ELSE
                -- Resto: Alternar entre Selva e Floresta
                IF (x + y) % 2 = 0 THEN
                    biome_name := 'Selva';
                ELSE
                    biome_name := 'Floresta';
                END IF;
            END IF;
            
            -- Inserir chunk
            INSERT INTO Chunk (Numero_chunk, Id_bioma, Id_mapa_nome, Id_mapa_turno)
            VALUES (chunk_id, biome_name, 'Mapa_Principal', 'Noite')
            ON CONFLICT (Numero_chunk) DO NOTHING;
            
            chunk_id := chunk_id + 1;
            
            -- Parar após 2000 chunks total (1000 para cada turno)
            IF chunk_id > 2000 THEN
                EXIT;
            END IF;
        END LOOP;
        
        -- Parar após 2000 chunks total
        IF chunk_id > 2000 THEN
            EXIT;
        END IF;
    END LOOP;
    
    -- Mostrar estatísticas
    RAISE NOTICE 'Chunks gerados para o mapa de dia:';
    RAISE NOTICE 'Deserto: % chunks', desert_chunks;
    RAISE NOTICE 'Oceano: % chunks', ocean_chunks;
    RAISE NOTICE 'Selva: % chunks', jungle_chunks;
    RAISE NOTICE 'Floresta: % chunks', forest_chunks;
    RAISE NOTICE 'Total: % chunks', (desert_chunks + ocean_chunks + jungle_chunks + forest_chunks);
END
$$ LANGUAGE plpgsql;

-- Inserir alguns jogadores de exemplo (apenas se não existirem)
INSERT INTO Jogador (Nome, Vida_max, Vida_atual, xp, forca, Id_Chunk_Atual)
VALUES
    ('Player1', 100, 100, 0, 10, 1), 
    ('Player2', 120, 120, 50, 12, 2),
    ('Player3', 110, 110, 25, 11, 3)
ON CONFLICT (Id_Jogador) DO NOTHING;

Assista ao nosso vídeo de demonstração aqui: `Vídeo do módulo 2 no YouTube <https://youtu.be/Qz7BXkqUX40>`_


