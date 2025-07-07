INSERT INTO Mapa (Nome, Turno)
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

-- Fantasmas construtores
Fantasmas construtores (máx 5)
INSERT INTO fantasma (nome, tipo, chunk, ativo) VALUES
('Construtor 1', 'construtor', 'Chunk-001', TRUE),
('Construtor 2', 'construtor', 'Chunk-002', TRUE),
('Construtor 3', 'construtor', 'Chunk-003', TRUE),
('Construtor 4', 'construtor', 'Chunk-004', TRUE),
('Construtor 5', 'construtor', 'Chunk-005', TRUE);

-- Fantasmas mineradores (máx 5)
INSERT INTO fantasma (nome, tipo, chunk, ativo) VALUES
('Minerador 1', 'minerador', 'Chunk-001', TRUE),
('Minerador 2', 'minerador', 'Chunk-002', TRUE),
('Minerador 3', 'minerador', 'Chunk-003', TRUE),
('Minerador 4', 'minerador', 'Chunk-004', TRUE),
('Minerador 5', 'minerador', 'Chunk-005', TRUE);

-- Inserindo pontes
INSERT INTO ponte (chunk_origem, chunk_destino, durabilidade) VALUES
('Chunk-001', 'Chunk-002', 100),
('Chunk-002', 'Chunk-003', 80),
('Chunk-004', 'Chunk-005', 90);

-- Inserindo totens
INSERT INTO totem (nome, localizacao, tipo, ativo) VALUES
('Totem do Norte', 'Chunk-001', 'ancestral', TRUE),
('Totem do Sul', 'Chunk-004', 'protetor', TRUE),
('Totem Central', 'Chunk-003', 'ancestral', TRUE);
