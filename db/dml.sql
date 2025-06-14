INSERT INTO Mapa (Nome, Turno)
VALUES
    ('Mapa_Principal', 'Dia'),
    ('Mapa_Principal', 'Noite')
ON CONFLICT (Nome, Turno) DO NOTHING; 

INSERT INTO Bioma (NomeBioma)
VALUES
    ('Deserto'),
    ('Oceano'),
    ('Selva'),
    ('Floresta')
ON CONFLICT (NomeBioma) DO NOTHING; 

INSERT INTO Chunk (Numero_chunk, Id_bioma, Id_mapa_nome, Id_mapa_turno)
VALUES
    (1, 'Deserto', 'Mapa_Principal', 'Dia'),
    (2, 'Oceano', 'Mapa_Principal', 'Dia'),
    (3, 'Selva', 'Mapa_Principal', 'Noite'),
    (4, 'Floresta', 'Mapa_Principal', 'Noite')
ON CONFLICT (Numero_chunk) DO NOTHING;

INSERT INTO Jogador (Nome, Vida_max, Vida_atual, xp, forca, Id_Chunk_Atual)
VALUES
    ('Player1', 100, 100, 0, 10, 1), 
    ('Player2', 120, 120, 50, 12, 2); 

INSERT INTO Inventario (id_jogador, id_inventario, Instancia_Item, ArmaduraEquipada, ArmaEquipada)
VALUES
    (1, 1, '{"item_id": 101, "quantidade": 5}', 'Capacete de Ferro', 'Espada de Diamante'),
    (2, 1, '{"item_id": 201, "quantidade": 1}', 'Armadura de Couro', 'Arco Longo')
ON CONFLICT (id_jogador, id_inventario) DO NOTHING; 