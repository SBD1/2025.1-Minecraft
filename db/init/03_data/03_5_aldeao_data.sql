-- Primeiro, garanta que a vila existe:
INSERT INTO Vila (nome_vila, descricao_vila, id_chunk)
VALUES ('Vila dos aldeões', 'A vila principal do mapa.', 1);

-- Agora, crie as casas dos aldeões:
INSERT INTO Casa_aldeao (descricao_casa, vila)
VALUES
  ('Casa do Bob, O Mago', 1),
  ('Casa do Bob, O Construtor', 1),
  ('Casa do Aldeão', 1),
  ('Casa do Aldeão', 1),
  ('Casa do Aldeão', 1),
  ('Casa do Aldeão', 1)
ON CONFLICT (id_casa) DO NOTHING;

-- Dados iniciais para tabela Aldeao
INSERT INTO Aldeao (nome, profissao, nivel_profissao, vida_maxima, vida_atual, id_casa, ativo)
VALUES
  ('João Ferreiro', 'Ferreiro', 3, 25, 25, 4, TRUE),
  ('Maria Fazendeira', 'Fazendeira', 2, 20, 20, 6, TRUE),
  ('Pedro Comerciante', 'Comerciante', 1, 20, 20, 3, TRUE),
  ('Ana Bibliotecária', 'Bibliotecária', 4, 20, 20, 6, TRUE),
  ('Carlos Pescador', 'Pescador', 2, 22, 22, 5, TRUE),
  ('Lucia Cartógrafa', 'Cartógrafa', 5, 20, 20, 5, TRUE),
  ('Roberto Padeiro', 'Padeiro', 1, 18, 18, 4, TRUE),
  ('Sofia Armeira', 'Armeira', 3, 24, 24, 3, TRUE),
  ('Bob, O Mago', 'Mago', 3, 25, 25, 1, TRUE),
  ('Bob, O Construtor', 'Construtor', 2, 22, 22, 2, TRUE)
ON CONFLICT (nome) DO NOTHING;

INSERT INTO Bob_construtor (id_aldeao_construtor, habilidades_construtor)
VALUES
  (10, 'Aumenta o level do totem de tropas');

INSERT INTO Bob_mago (id_aldeao_mago, habilidade_mago)
VALUES 
  (9, 'Aumenta o level das tropas');
