-- Índices para melhorar performance

-- Índices para tabela Chunk
CREATE INDEX idx_chunk_bioma ON Chunk (id_bioma);
CREATE INDEX idx_chunk_mapa ON Chunk (id_mapa);

-- Índices para tabela Player
CREATE INDEX idx_player_chunk ON Player (current_chunk_id);

-- Índices para tabela Inventario
CREATE INDEX idx_inventario_plr ON Inventario (player_id);
CREATE INDEX idx_inventario_itm ON Inventario (item_id);

-- Índices para tabela fantasma
CREATE INDEX idx_fantasma_tipo ON fantasma(tipo);
CREATE INDEX idx_fantasma_chunk ON fantasma(chunk);

-- Índices para tabela pontes
CREATE INDEX idx_pontes_origem ON pontes(chunk_origem);
CREATE INDEX idx_pontes_destino ON pontes(chunk_destino);

-- Índices para tabela totem
CREATE INDEX idx_totem_localizacao ON totem(localizacao);
CREATE INDEX idx_totem_tipo ON totem(tipo);

-- Índices para tabela Vila
CREATE INDEX idx_vila_nome ON Vila(nome_vila);
CREATE INDEX idx_vila_chunk ON Vila(id_chunk);

-- Índices para tabela Casa_aldeao
CREATE INDEX idx_casa_vila ON Casa_aldeao(vila);

-- Índices para tabela Aldeao
CREATE INDEX idx_aldeao_nome ON Aldeao(nome);
CREATE INDEX idx_aldeao_profissao ON Aldeao(profissao);
CREATE INDEX idx_aldeao_id_casa ON Aldeao(id_casa);
CREATE INDEX idx_aldeao_ativo ON Aldeao(ativo);

-- Índices para tabela Bob_mago
CREATE INDEX idx_bobmago_habilidade ON Bob_mago(habilidade_mago);

-- Índices para tabela Bob_construtor
CREATE INDEX idx_bobconstrutor_habilidades ON Bob_construtor(habilidades_construtor);
