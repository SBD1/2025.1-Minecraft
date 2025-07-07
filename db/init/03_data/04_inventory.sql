-- Inventário (agora que players e itens existem)
INSERT INTO Inventario (player_id, item_id, quantidade)
VALUES
  (1, (SELECT id_item FROM Item WHERE nome='Espada de Ferro'), 1),
  (1, (SELECT id_item FROM Item WHERE nome='Maçã'), 5),
  (1, (SELECT id_item FROM Item WHERE nome='Poção de Vida'), 2),
  (2, (SELECT id_item FROM Item WHERE nome='Espada de Diamante'), 1),
  (2, (SELECT id_item FROM Item WHERE nome='Armadura de Couro'), 1),
  (2, (SELECT id_item FROM Item WHERE nome='Arco Longo'), 1)
ON CONFLICT ON CONSTRAINT uk_inventario_player_item DO NOTHING;
