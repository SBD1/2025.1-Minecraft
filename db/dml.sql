-- Jogadores (sem current_chunk_id para evitar conflito de FK com chunks)
INSERT INTO Player (
  id_player, nome, vida_maxima, vida_atual, forca,
  localizacao, nivel, experiencia, current_chunk_id
)
VALUES
  (1,'Player1', 100, 100, 10, NULL, 1, 0, NULL),
  (2, 'Player2', 120, 120, 12, NULL, 1, 50, NULL)
ON CONFLICT (nome) DO NOTHING;

-- Mapas
INSERT INTO Mapa (id_mapa, nome, turno)
VALUES
  (1, 'Mapa_Principal', 'Dia'),
  (2, 'Mapa_Principal', 'Noite')
ON CONFLICT ON CONSTRAINT uk_mapa_nome_turno DO NOTHING;

-- Biomas
INSERT INTO Bioma (id_bioma, nome, descricao)
VALUES
  (1, 'Deserto',   'Bioma árido com pouca vegetação.'),
  (2, 'Oceano',    'Bioma de água salgada.'),
  (3, 'Selva',     'Bioma tropical úmido.'),
  (4, 'Floresta',  'Bioma temperado com muita vegetação.')
ON CONFLICT (nome) DO NOTHING;

-- Itens de exemplo
INSERT INTO Item (id_item, nome, tipo, poder, durabilidade)
VALUES
  (1, 'Espada de Ferro', 'Arma', 8, 200),
  (2, 'Poção de Vida',   'Poção', 50, NULL),
  (3, 'Maçã', 'Comida', NULL, NULL),
  (4, 'Pedra', 'Construção', NULL, NULL),
  (5, 'Madeira', 'Construção', NULL, NULL),
  (6, 'Redstone', 'Minério', NULL, NULL),
  (7, 'Pedra', 'Construção', NULL, NULL),
  (8, 'Ferro', 'Minério', NULL, NULL),
  (9, 'Carvão', 'Minério', NULL, NULL),
  (10, 'Diamante', 'Minério', NULL, NULL)
ON CONFLICT (nome) DO NOTHING;

-- Inventário de exemplo
INSERT INTO Inventario (player_id, item_id, quantidade)
VALUES
  (1, (SELECT id_item FROM Item WHERE nome='Espada de Ferro'), 1),
  (1, (SELECT id_item FROM Item WHERE nome='Maçã'), 5),
  (1, (SELECT id_item FROM Item WHERE nome='Poção de Vida'), 2),
  (1, (SELECT id_item FROM Item WHERE nome='Pedra'), 10),
  (1, (SELECT id_item FROM Item WHERE nome='Madeira'), 15),
  (1, (SELECT id_item FROM Item WHERE nome='Redstone'), 3),
  (1, (SELECT id_item FROM Item WHERE nome='Ferro'), 4),
  (1, (SELECT id_item FROM Item WHERE nome='Carvão'), 6),
  (1, (SELECT id_item FROM Item WHERE nome='Diamante'), 1),

  (2, (SELECT id_item FROM Item WHERE nome='Espada de Ferro'), 1),
  (2, (SELECT id_item FROM Item WHERE nome='Maçã'), 3),
  (2, (SELECT id_item FROM Item WHERE nome='Poção de Vida'), 1),
  (2, (SELECT id_item FROM Item WHERE nome='Pedra'), 8),
  (2, (SELECT id_item FROM Item WHERE nome='Madeira'), 12),
  (2, (SELECT id_item FROM Item WHERE nome='Redstone'), 2),
  (2, (SELECT id_item FROM Item WHERE nome='Ferro'), 2),
  (2, (SELECT id_item FROM Item WHERE nome='Carvão'), 5),
  (2, (SELECT id_item FROM Item WHERE nome='Diamante'), 1)
ON CONFLICT ON CONSTRAINT uk_inventario_player_item DO NOTHING;

-- Aldeao
INSERT INTO Aldeao (id_aldeao, nome, tipo, descricao, id_casa)
VALUES
  (1, 'Bob, O Mago', 'Mago', 'Homem elegante para um construtor e utiliza uma lupa com 3 lentes em seu olho esquerdo, para ter mais precisão no manuseio de suas ferramentas', 1),
  (2, 'Bob, O Construtor', 'Construtor', 'Um Homem ríspido, mas com um coração gentil disposto a ajudar pessoas que compartilham do mesmo sentimento', 2),
  (3, 'Aldeão', 'Aldeão', 'Aldeão normal', 3),
  (4, 'Aldeão', 'Aldeão', 'Aldeão normal', 4),
  (5, 'Aldeão', 'Aldeão', 'Aldeão normal', 5),
  (6, 'Aldeão', 'Aldeão', 'Aldeão normal', 6)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO Bob_construtor (id_aldeao_construtor, habilidades_construtor, nivel)
VALUES
  (2, 'Aumenta o level do totem de tropas', 1)

INSERT INTO Bob_mago (id_aldeao_mago, habilidade_mago, nivel)
VALUES (1, 'Aumenta o level das tropas', 1);

-- Primeiro, garanta que a vila existe:
INSERT INTO Vila (id_vila, nome_vila, descricao_vila, id_chunk)
VALUES (1, 'Vila dos aldeões', 'A vila principal do mapa.', 1)
ON CONFLICT (nome_vila) DO NOTHING;

-- Agora, crie as casas dos aldeões:
INSERT INTO Casa_aldeao (id_casa, descricao_casa, nome_vila)
VALUES
  (1, 'Casa do Bob, O Mago', 1),
  (2, 'Casa do Bob, O Construtor', 1),
  (3, 'Casa do Aldeão', 1),
  (4, 'Casa do Aldeão', 1),
  (5, 'Casa do Aldeão', 1),
  (6, 'Casa do Aldeão', 1)
ON CONFLICT (id_casa) DO NOTHING;