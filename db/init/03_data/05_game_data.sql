-- Dados específicos do jogo

-- Fantasmas construtores (máx 5)
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

-- Pontes
INSERT INTO pontes (chunk_origem, chunk_destino, durabilidade, construida) VALUES
('Chunk-001', 'Chunk-002', 100, TRUE),
('Chunk-002', 'Chunk-003', 80, TRUE),
('Chunk-004', 'Chunk-005', 90, TRUE),
('Chunk-003', 'Chunk-004', 70, FALSE);

-- Totens
INSERT INTO totem (nome, localizacao, tipo, ativo) VALUES
('Totem do Norte', 'Chunk-001', 'ancestral', TRUE),
('Totem do Sul', 'Chunk-004', 'protetor', TRUE),
('Totem Central', 'Chunk-003', 'ancestral', TRUE),
('Totem do Leste', 'Chunk-005', 'protetor', FALSE);
