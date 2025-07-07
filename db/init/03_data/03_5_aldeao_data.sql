-- Dados iniciais para tabela Aldeao
INSERT INTO Aldeao (nome, profissao, nivel_profissao, vida_maxima, vida_atual, id_chunk, ativo)
VALUES
  ('João Ferreiro', 'Ferreiro', 3, 25, 25, 1, TRUE),
  ('Maria Fazendeira', 'Fazendeira', 2, 20, 20, 2, TRUE),
  ('Pedro Comerciante', 'Comerciante', 1, 20, 20, 3, TRUE),
  ('Ana Bibliotecária', 'Bibliotecária', 4, 20, 20, 4, TRUE),
  ('Carlos Pescador', 'Pescador', 2, 22, 22, 5, TRUE)
ON CONFLICT (nome) DO NOTHING;

-- Adicionar mais aldeões com diferentes profissões
INSERT INTO Aldeao (nome, profissao, nivel_profissao, vida_maxima, vida_atual, id_chunk, ativo)
VALUES
  ('Lucia Cartógrafa', 'Cartógrafa', 5, 20, 20, 10, TRUE),
  ('Roberto Padeiro', 'Padeiro', 1, 18, 18, 15, TRUE),
  ('Sofia Armeira', 'Armeira', 3, 24, 24, 20, TRUE)
ON CONFLICT (nome) DO NOTHING;
