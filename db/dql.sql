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
SELECT * FROM Jogador;

-- Seleciona todos os inventários
SELECT * FROM Inventario;

-- Consulta 1: Jogadores e sua Localização Atual
-- Mostra em qual chunk, bioma, mapa e turno cada jogador está.
SELECT
    j.Nome AS Nome_Jogador,
    j.Vida_atual,
    j.xp,
    c.Numero_chunk,
    c.Id_bioma AS Bioma,
    c.Id_mapa_nome AS Mapa,
    c.Id_mapa_turno AS Turno
FROM
    Jogador j
JOIN
    Chunk c ON j.Id_Chunk_Atual = c.Numero_chunk;


-- Consulta 2: Inventário de Cada Jogador
-- Lista os itens, armadura e arma equipada para cada jogador.
SELECT
    j.Nome AS Nome_Jogador,
    i.Instancia_Item,
    i.ArmaduraEquipada,
    i.ArmaEquipada
FROM
    Inventario i
JOIN
    Jogador j ON i.id_jogador = j.Id_jogador; -- Assumindo que 'Id_jogador' é a chave primária da tabela Jogador.


-- Consulta 3: Detalhes Completos dos Chunks
-- Visualiza os detalhes de cada chunk, incluindo o nome do bioma e as informações do mapa.
SELECT
    c.Numero_chunk,
    b.NomeBioma,
    m.Nome AS Nome_Mapa,
    m.Turno
FROM
    Chunk c
JOIN
    Bioma b ON c.Id_bioma = b.NomeBioma
JOIN
    Mapa m ON c.Id_mapa_nome = m.Nome AND c.Id_mapa_turno = m.Turno;
