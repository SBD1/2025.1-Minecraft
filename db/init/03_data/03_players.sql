-- Jogadores (agora que chunks já existem)
INSERT INTO Player (
  nome, vida_maxima, vida_atual, forca,
  localizacao, nivel, experiencia, current_chunk_id
)
VALUES
  ('Player1', 100, 100, 10, NULL, 1, 0, 1),
  ('Player2', 120, 120, 12, NULL, 1, 50, 2)
ON CONFLICT (nome) DO NOTHING;
