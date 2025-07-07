-- Mapas
INSERT INTO Mapa (nome, turno)
VALUES
  ('Mapa_Principal', 'Dia'),
  ('Mapa_Principal', 'Noite')
ON CONFLICT ON CONSTRAINT uk_mapa_nome_turno DO NOTHING;

-- Biomas
INSERT INTO Bioma (nome, descricao)
VALUES
  ('Deserto',   'Bioma árido com pouca vegetação.'),
  ('Oceano',    'Bioma de água salgada.'),
  ('Selva',     'Bioma tropical úmido.'),
  ('Floresta',  'Bioma temperado com muita vegetação.')
ON CONFLICT (nome) DO NOTHING;

-- Itens de exemplo
INSERT INTO Item (nome, tipo, poder, durabilidade)
VALUES
  ('Espada de Ferro', 'Arma', 8, 200),
  ('Poção de Vida',   'Poção', 50, NULL),
  ('Maçã',            'Comida', NULL, NULL)
ON CONFLICT (nome) DO NOTHING;

-- Jogadores (sem current_chunk_id para evitar conflito de FK com chunks)
INSERT INTO Player (
  nome, vida_maxima, vida_atual, forca,
  localizacao, nivel, experiencia, current_chunk_id
)
VALUES
  ('Player1', 100, 100, 10, NULL, 1, 0, NULL),
  ('Player2', 120, 120, 12, NULL, 1, 50, NULL)
ON CONFLICT (nome) DO NOTHING;

-- Inventário de exemplo (corrigido)
INSERT INTO Inventario (player_id, item_id, quantidade)
VALUES
  (1, (SELECT id_item FROM Item WHERE nome='Espada de Ferro'), 1),
  (1, (SELECT id_item FROM Item WHERE nome='Maçã'), 5)
ON CONFLICT ON CONSTRAINT uk_inventario_player_item DO NOTHING; 

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

-- Inserindo pontes
INSERT INTO pontes (chunk_origem, chunk_destino, durabilidade) VALUES
('Chunk-001', 'Chunk-002', 100),
('Chunk-002', 'Chunk-003', 80),
('Chunk-004', 'Chunk-005', 90);

-- Inserindo totens
INSERT INTO totem (nome, localizacao, tipo, ativo) VALUES
('Totem do Norte', 'Chunk-001', 'ancestral', TRUE),
('Totem do Sul', 'Chunk-004', 'protetor', TRUE),
('Totem Central', 'Chunk-003', 'ancestral', TRUE);
