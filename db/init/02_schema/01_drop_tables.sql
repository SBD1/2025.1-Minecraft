-- Drop das tabelas existentes (para recriação limpa)
DROP TABLE IF EXISTS Inventario, Item, Player, Chunk, Mapa, Bioma, fantasma, pontes, totem, Aldeao, Casa_aldeao, vila, Bob_construtor, Bob_mago CASCADE;

-- Extensões necessárias
CREATE EXTENSION IF NOT EXISTS pg_cron;
