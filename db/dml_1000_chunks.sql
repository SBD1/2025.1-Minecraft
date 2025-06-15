-- Script DML para popular o banco de dados com 1000 chunks
-- Mapa: 32x32 chunks (1024 chunks total, mas vamos usar 1000)
-- Estrutura: Oceano ao redor, deserto no centro (20%), selva e floresta no resto

-- Inserir mapas (Dia e Noite)
INSERT INTO Mapa (Nome, Turno)
VALUES
    ('Mapa_Principal', 'Dia'),
    ('Mapa_Principal', 'Noite')
ON CONFLICT (Nome, Turno) DO NOTHING; 

-- Inserir biomas
INSERT INTO Bioma (NomeBioma)
VALUES
    ('Deserto'),
    ('Oceano'),
    ('Selva'),
    ('Floresta')
ON CONFLICT (NomeBioma) DO NOTHING; 

-- Função para gerar chunks com a distribuição especificada
-- Mapa 32x32 com oceano na borda, deserto no centro, selva e floresta no resto
DO $$
DECLARE
    chunk_id INTEGER := 1;
    x INTEGER;
    y INTEGER;
    biome_name VARCHAR(100);
    map_size INTEGER := 32;
    center_start INTEGER := 12; -- Início da área central (deserto)
    center_end INTEGER := 20;   -- Fim da área central (deserto)
    desert_chunks INTEGER := 0;
    ocean_chunks INTEGER := 0;
    jungle_chunks INTEGER := 0;
    forest_chunks INTEGER := 0;
BEGIN
    -- Gerar chunks para o mapa de dia
    FOR y IN 1..map_size LOOP
        FOR x IN 1..map_size LOOP
            -- Determinar bioma baseado na posição
            IF x = 1 OR x = map_size OR y = 1 OR y = map_size THEN
                -- Borda: Oceano
                biome_name := 'Oceano';
                ocean_chunks := ocean_chunks + 1;
            ELSIF x >= center_start AND x <= center_end AND y >= center_start AND y <= center_end THEN
                -- Centro: Deserto (área 9x9 = 81 chunks, aproximadamente 20% de 1000)
                biome_name := 'Deserto';
                desert_chunks := desert_chunks + 1;
            ELSE
                -- Resto: Alternar entre Selva e Floresta
                IF (x + y) % 2 = 0 THEN
                    biome_name := 'Selva';
                    jungle_chunks := jungle_chunks + 1;
                ELSE
                    biome_name := 'Floresta';
                    forest_chunks := forest_chunks + 1;
                END IF;
            END IF;
            
            -- Inserir chunk
            INSERT INTO Chunk (Numero_chunk, Id_bioma, Id_mapa_nome, Id_mapa_turno)
            VALUES (chunk_id, biome_name, 'Mapa_Principal', 'Dia')
            ON CONFLICT (Numero_chunk) DO NOTHING;
            
            chunk_id := chunk_id + 1;
            
            -- Parar após 1000 chunks
            IF chunk_id > 1000 THEN
                EXIT;
            END IF;
        END LOOP;
        
        -- Parar após 1000 chunks
        IF chunk_id > 1000 THEN
            EXIT;
        END IF;
    END LOOP;
    
    -- Gerar chunks para o mapa de noite (mesma distribuição)
    chunk_id := 1001;
    FOR y IN 1..map_size LOOP
        FOR x IN 1..map_size LOOP
            -- Determinar bioma baseado na posição
            IF x = 1 OR x = map_size OR y = 1 OR y = map_size THEN
                -- Borda: Oceano
                biome_name := 'Oceano';
            ELSIF x >= center_start AND x <= center_end AND y >= center_start AND y <= center_end THEN
                -- Centro: Deserto
                biome_name := 'Deserto';
            ELSE
                -- Resto: Alternar entre Selva e Floresta
                IF (x + y) % 2 = 0 THEN
                    biome_name := 'Selva';
                ELSE
                    biome_name := 'Floresta';
                END IF;
            END IF;
            
            -- Inserir chunk
            INSERT INTO Chunk (Numero_chunk, Id_bioma, Id_mapa_nome, Id_mapa_turno)
            VALUES (chunk_id, biome_name, 'Mapa_Principal', 'Noite')
            ON CONFLICT (Numero_chunk) DO NOTHING;
            
            chunk_id := chunk_id + 1;
            
            -- Parar após 2000 chunks total (1000 para cada turno)
            IF chunk_id > 2000 THEN
                EXIT;
            END IF;
        END LOOP;
        
        -- Parar após 2000 chunks total
        IF chunk_id > 2000 THEN
            EXIT;
        END IF;
    END LOOP;
    
    -- Mostrar estatísticas
    RAISE NOTICE 'Chunks gerados para o mapa de dia:';
    RAISE NOTICE 'Deserto: % chunks', desert_chunks;
    RAISE NOTICE 'Oceano: % chunks', ocean_chunks;
    RAISE NOTICE 'Selva: % chunks', jungle_chunks;
    RAISE NOTICE 'Floresta: % chunks', forest_chunks;
    RAISE NOTICE 'Total: % chunks', (desert_chunks + ocean_chunks + jungle_chunks + forest_chunks);
END
$$ LANGUAGE plpgsql;

-- Inserir alguns jogadores de exemplo (apenas se não existirem)
INSERT INTO Jogador (Nome, Vida_max, Vida_atual, xp, forca, Id_Chunk_Atual)
VALUES
    ('Player1', 100, 100, 0, 10, 1), 
    ('Player2', 120, 120, 50, 12, 2),
    ('Player3', 110, 110, 25, 11, 3)
ON CONFLICT (Id_Jogador) DO NOTHING; 