-- Inventário (agora que players e itens existem)
INSERT INTO Inventario (player_id, item_id, quantidade)
VALUES
  (1, (SELECT id_item FROM Item WHERE nome='Espada de Ferro'), 1),
  (1, (SELECT id_item FROM Item WHERE nome='Maçã'), 5),
  (1, (SELECT id_item FROM Item WHERE nome='Poção de Vida'), 2),
  (1, (SELECT id_item FROM Item WHERE nome='Espada de Ferro'), 1),
  (1, (SELECT id_item FROM Item WHERE nome='Maçã'), 5),
  (1, (SELECT id_item FROM Item WHERE nome='Poção de Vida'), 2),
  (1, (SELECT id_item FROM Item WHERE nome='Pedra'), 10),
  (1, (SELECT id_item FROM Item WHERE nome='Madeira'), 15),
  (1, (SELECT id_item FROM Item WHERE nome='Redstone'), 3),
  (1, (SELECT id_item FROM Item WHERE nome='Ferro'), 4),
  (1, (SELECT id_item FROM Item WHERE nome='Carvão'), 6),
  (1, (SELECT id_item FROM Item WHERE nome='Diamante'), 1),

  (2, (SELECT id_item FROM Item WHERE nome='Espada de Diamante'), 1),
  (2, (SELECT id_item FROM Item WHERE nome='Armadura de Couro'), 1),
  (2, (SELECT id_item FROM Item WHERE nome='Arco Longo'), 1),
  (2, (SELECT id_item FROM Item WHERE nome='Espada de Ferro'), 1),
  (2, (SELECT id_item FROM Item WHERE nome='Maçã'), 3),
  (2, (SELECT id_item FROM Item WHERE nome='Poção de Vida'), 1),
  (2, (SELECT id_item FROM Item WHERE nome='Pedra'), 8),
  (2, (SELECT id_item FROM Item WHERE nome='Madeira'), 12),
  (2, (SELECT id_item FROM Item WHERE nome='Redstone'), 2),
  (2, (SELECT id_item FROM Item WHERE nome='Ferro'), 2),
  (2, (SELECT id_item FROM Item WHERE nome='Carvão'), 5),
  (2, (SELECT id_item FROM Item WHERE nome='Diamante'), 1)
ON CONFLICT ON CONSTRAINT uk_inventario_player_item DO NOTHING;
