-- Dados básicos (sem dependências)

-- Biomas
INSERT INTO Bioma (nome, descricao)
VALUES
  ('Deserto',   'Bioma árido com pouca vegetação.'),
  ('Oceano',    'Bioma de água salgada.'),
  ('Selva',     'Bioma tropical úmido.'),
  ('Floresta',  'Bioma temperado com muita vegetação.')
ON CONFLICT (nome) DO NOTHING;

-- Mapas
INSERT INTO Mapa (nome, turno)
VALUES
  ('Mapa_Principal', 'Dia'),
  ('Mapa_Principal', 'Noite')
ON CONFLICT ON CONSTRAINT uk_mapa_nome_turno DO NOTHING;

-- Itens de exemplo
INSERT INTO Item (nome, tipo, poder, durabilidade)
VALUES
  ('Espada de Ferro', 'Arma', 8, 200),
  ('Poção de Vida',   'Poção', 50, NULL),
  ('Maçã',            'Comida', NULL, NULL),
  ('Capacete de Ferro', 'Armadura', 5, 150),
  ('Espada de Diamante', 'Arma', 15, 500),
  ('Armadura de Couro', 'Armadura', 3, 100),
  ('Arco Longo', 'Arma', 10, 300),
  ('Pedra', 'Construção', NULL, NULL),
  ('Madeira', 'Construção', NULL, NULL),
  ('Redstone', 'Minério', NULL, NULL),
  ('Pedra', 'Construção', NULL, NULL),
  ('Ferro', 'Minério', NULL, NULL),
  ('Carvão', 'Minério', NULL, NULL),
  ('Diamante', 'Minério', NULL, NULL)
ON CONFLICT (nome) DO NOTHING;
