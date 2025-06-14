
-- ====================================================================
-- Seção 1: Consultas de Jogador e Localização
-- ====================================================================

-- 1.1: Buscar o perfil completo de um jogador pelo seu ID.
-- PARÂMETRO DE ENTRADA: :id_jogador (INT)
SELECT * FROM Jogador WHERE Id_Jogador = :id_jogador;


-- 1.2: Obter o perfil do jogador e as informações completas de sua localização atual.
-- PARÂMETRO DE ENTRADA: :id_jogador (INT)
SELECT
    j.Nome AS Nome_Jogador,
    j.Vida_atual,
    j.xp,
    c.Numero_chunk,
    b.NomeBioma AS Bioma_Atual,
    c.Id_mapa_nome AS Nome_Mapa,
    c.Id_mapa_turno AS Turno_Mapa
FROM
    Jogador j
JOIN
    Chunk c ON j.Id_Chunk_Atual = c.Numero_chunk
JOIN
    Bioma b ON c.Id_bioma = b.NomeBioma
WHERE
    j.Id_Jogador = :id_jogador;


-- ====================================================================
-- Seção 2: Consultas de Inventário e Itens
-- ====================================================================

-- 2.1: Listar todos os itens no inventário de um jogador.
-- NOTA: A consulta assume uma tabela de junção chamada 'Inventario_Item'.
--       Se o nome da sua tabela for diferente, ajuste-o na linha 'FROM Item i JOIN Inventario_Item ii'.
-- PARÂMETRO DE ENTRADA: :id_jogador (INT)

SELECT
    i.nome_item,
    i.descricao,
    ii.quantidade
FROM
    Item i
JOIN
    Inventario_Item ii ON i.id_item = ii.id_item
JOIN
    Inventario inv ON ii.id_inventario = inv.id_inventario -- Ajustar conforme necessário
WHERE
    inv.id_jogador = :id_jogador;


-- 2.2: Buscar detalhes de um item específico pelo nome.
-- PARÂMETRO DE ENTRADA: :nome_item (VARCHAR)
SELECT * FROM Item WHERE nome_item = :nome_item;


-- ====================================================================
-- Seção 3: Consultas de Combate, Monstros e Loot
-- ====================================================================

-- 3.1: Listar todos os monstros em um chunk específico.
-- NOTA: A consulta assume uma tabela de junção chamada 'Monstro_Chunk'.
--       Se o nome da sua tabela for diferente, ajuste-o na linha 'JOIN Monstro_Chunk mc'.
-- PARÂMETRO DE ENTRADA: :numero_chunk (INT)

SELECT
    m.*
FROM
    Monstro m
JOIN
    Monstro_Chunk mc ON m.Id_Monstro = mc.id_monstro
WHERE
    mc.numero_chunk = :numero_chunk;


-- 3.2: Listar toda a tabela de loot possível de um monstro específico.
-- PARÂMETRO DE ENTRADA: :id_monstro (INT)
SELECT
    i.nome_item,
    i.descricao,
    l.chance_drop
FROM
    Loot l
JOIN
    Item i ON l.id_item = i.id_item
WHERE
    l.id_monstro = :id_monstro
ORDER BY
    l.chance_drop DESC;


-- ====================================================================
-- Seção 4: Consultas de Habilidades
-- ====================================================================

-- 4.1: Listar todas as habilidades que um jogador já aprendeu.
-- NOTA: A consulta assume uma tabela de junção chamada 'Jogador_Habilidade'.
--       Se o nome da sua tabela for diferente, ajuste-o na linha 'JOIN Jogador_Habilidade jh'.
-- PARÂMETRO DE ENTRADA: :id_jogador (INT)

SELECT
    h.nome,
    h.descricao,
    h.dano
FROM
    Habilidade h
JOIN
    Jogador_Habilidade jh ON h.id_habilidade = jh.id_habilidade
WHERE
    jh.id_jogador = :id_jogador;


-- 4.2: Encontrar todos os jogadores que conhecem uma habilidade específica.
-- NOTA: A consulta assume uma tabela de junção chamada 'Jogador_Habilidade'.
--       Se o nome da sua tabela for diferente, ajuste-o na linha 'JOIN Jogador_Habilidade jh'.
-- PARÂMETRO DE ENTRADA: :id_habilidade (INT)

SELECT
    j.Nome
FROM
    Jogador j
JOIN
    Jogador_Habilidade jh ON j.Id_Jogador = jh.id_jogador
WHERE
    jh.id_habilidade = :id_habilidade;


-- ====================================================================
-- Seção 5: Consultas de Missões / Quests
-- ====================================================================

-- 5.1: Listar todas as missões de um jogador e seus status (ativa, completa, etc.).
-- NOTA: A consulta assume uma tabela de junção chamada 'Jogador_Missao'.
--       Se o nome da sua tabela for diferente, ajuste-o na linha 'JOIN Jogador_Missao jm'.
-- PARÂMETRO DE ENTRADA: :id_jogador (INT)

SELECT
    m.titulo,
    m.descricao,
    m.xp_recompensa,
    jm.status -- Campo 'status' da tabela de junção
FROM
    Missao m
JOIN
    Jogador_Missao jm ON m.id_missao = jm.id_missao
WHERE
    jm.id_jogador = :id_jogador;


-- 5.2: Listar apenas as missões com um status específico para um jogador.
-- NOTA: A consulta assume uma tabela de junção chamada 'Jogador_Missao'.
--       Se o nome da sua tabela for diferente, ajuste-o na linha 'JOIN Jogador_Missao jm'.
-- PARÂMETROS DE ENTRADA:
-- :id_jogador (INT)
-- :status_missao (VARCHAR) -> ex: 'ativa'

SELECT
    m.titulo,
    m.descricao
FROM
    Missao m
JOIN
    Jogador_Missao jm ON m.id_missao = jm.id_missao
WHERE
    jm.id_jogador = :id_jogador AND jm.status = :status_missao;
