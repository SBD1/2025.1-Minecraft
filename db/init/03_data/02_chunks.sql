-- Gera chunks (1000 para Dia e 1000 para Noite)
DO $$
DECLARE
  chunk_id INTEGER := 1;
  x INTEGER;
  y INTEGER;
  biome_name TEXT;
  map_size INTEGER := 32;
  center_start INTEGER := 12;
  center_end   INTEGER := 20;
  current_turno TEXT;
BEGIN
  FOREACH current_turno IN ARRAY ARRAY['Dia','Noite'] LOOP
    chunk_id := 1 + (CASE WHEN current_turno='Noite' THEN 1000 ELSE 0 END);
    FOR y IN 1..map_size LOOP
      FOR x IN 1..map_size LOOP
        IF x=1 OR y=1 OR x=map_size OR y=map_size THEN
          biome_name := 'Oceano';
        ELSIF x BETWEEN center_start AND center_end AND y BETWEEN center_start AND center_end THEN
          biome_name := 'Deserto';
        ELSE
          biome_name := CASE WHEN (x+y)%2=0 THEN 'Selva' ELSE 'Floresta' END;
        END IF;
        
        INSERT INTO Chunk (id_bioma, id_mapa, x, y)
        VALUES (
          (SELECT id_bioma FROM Bioma WHERE nome=biome_name),
          (SELECT id_mapa  FROM Mapa  WHERE nome='Mapa_Principal' AND turno=current_turno),
          x-1, y-1
        );
        
        chunk_id := chunk_id + 1;
        EXIT WHEN chunk_id > (CASE WHEN current_turno='Noite' THEN 2000 ELSE 1000 END);
      END LOOP;
      EXIT WHEN chunk_id > (CASE WHEN current_turno='Noite' THEN 2000 ELSE 1000 END);
    END LOOP;
  END LOOP;
END
$$ LANGUAGE plpgsql;
