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

-- Inventário de exemplo
INSERT INTO Inventario (player_id, item_id, quantidade)
VALUES
  (1, (SELECT id_item FROM Item WHERE nome='Espada de Ferro'), 1),
  (1, (SELECT id_item FROM Item WHERE nome='Maçã'), 5)
ON CONFLICT ON CONSTRAINT uk_inventario_player_item DO NOTHING;