"""
Model para representar um registro de inventário de um jogador
"""

from dataclasses import dataclass


@dataclass
class InventoryEntry:
    """
    Representa uma entrada de inventário (itens de um jogador)

    Attributes:
        id: Identificador único da entrada (chave primária)
        player_id: FK para Player.id_player
        item_id: FK para Item.id_item
        quantidade: Quantidade do item possuído
    """
    id: int
    player_id: int
    item_id: int
    quantidade: int
