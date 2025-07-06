"""
Model que representa um Item do jogo
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Item:
    """
    Representa um item no inventário ou no jogo

    Attributes:
        id_item: Identificador único do item (chave primária)
        nome: Nome do item
        tipo: Tipo do item (e.g., 'Arma', 'Poção', 'Comida')
        poder: Opcional, poder de ataque ou efeito do item
        durabilidade: Opcional, durabilidade restante
    """
    id_item: int
    nome: str
    tipo: str
    poder: Optional[int] = None
    durabilidade: Optional[int] = None
