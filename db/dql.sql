-- =================================================================
--                  Consultas Básicas
-- Seleciona todos os dados de cada tabela individualmente.
-- =================================================================

-- Seleciona todos os mapas
SELECT * FROM Mapa;

-- Seleciona todos os biomas
SELECT * FROM Bioma;

-- Seleciona todos os chunks
SELECT * FROM Chunk;

-- Seleciona todos os jogadores
SELECT * FROM Player;

-- Seleciona todos os inventários
SELECT * FROM Inventario;

-- Seleciona todos os aldeões
SELECT * FROM Aldeao;

-- Seleciona todos os itens
SELECT * FROM Item;

-- Consulta 1: Jogadores e sua Localização Atual
-- Mostra em qual chunk, bioma, mapa e turno cada jogador está.
SELECT
    p.nome AS Nome_Jogador,
    p.vida_atual,
    p.experiencia,
    c.id_chunk,
    b.nome AS Bioma,
    m.nome AS Mapa,
    m.turno AS Turno
FROM
    Player p
LEFT JOIN
    Chunk c ON p.current_chunk_id = c.id_chunk
LEFT JOIN
    Bioma b ON c.id_bioma = b.id_bioma
LEFT JOIN
    Mapa m ON c.id_mapa = m.id_mapa;


-- Consulta 2: Inventário de Cada Jogador
-- Lista os itens e quantidades para cada jogador.
SELECT
    p.nome AS Nome_Jogador,
    i.nome AS Item,
    inv.quantidade
FROM
    Inventario inv
JOIN
    Player p ON inv.player_id = p.id_player
JOIN
    Item i ON inv.item_id = i.id_item;


-- Consulta 3: Aldeões por Chunk (via Casa_aldeao e Vila)
-- Lista aldeões, suas casas, vilas e localização do chunk
SELECT
    a.nome AS Nome_Aldeao,
    a.profissao AS Profissao,
    a.nivel_profissao AS Nivel,
    a.vida_atual AS Vida,
    ca.descricao_casa AS Casa,
    v.nome_vila AS Vila,
    c.id_chunk AS Chunk,
    c.x AS Chunk_X,
    c.y AS Chunk_Y,
    b.nome AS Bioma
FROM
    Aldeao a
JOIN
    Casa_aldeao ca ON a.id_casa = ca.id_casa
JOIN
    Vila v ON ca.vila = v.id_vila
JOIN
    Chunk c ON v.id_chunk = c.id_chunk
JOIN
    Bioma b ON c.id_bioma = b.id_bioma
WHERE
    a.ativo = TRUE;


-- Consulta 4: Detalhes Completos dos Chunks
-- Visualiza os detalhes de cada chunk, incluindo o nome do bioma e as informações do mapa.
SELECT
    c.id_chunk,
    c.x,
    c.y,
    b.nome AS NomeBioma,
    m.nome AS Nome_Mapa,
    m.turno AS Turno
FROM
    Chunk c
JOIN
    Bioma b ON c.id_bioma = b.id_bioma
JOIN
    Mapa m ON c.id_mapa = m.id_mapa;
