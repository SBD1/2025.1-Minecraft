-- Tabelas de relacionamento (dependem de Player e Item)

-- Inventario (depende de Player e Item)
CREATE TABLE Inventario (
    id           SERIAL PRIMARY KEY,
    player_id    INT    NOT NULL REFERENCES Player(id_player) ON DELETE CASCADE ON UPDATE CASCADE,
    item_id      INT    NOT NULL REFERENCES Item(id_item)   ON DELETE RESTRICT ON UPDATE CASCADE,
    quantidade   INT    NOT NULL,
    CONSTRAINT uk_inventario_player_item UNIQUE(player_id, item_id)
);
