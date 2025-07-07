"""
Model para o estado global do Mundo
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Mundo:
    """
    Model que representa o estado global do jogo, refletindo a tabela 'Mundo'.
    
    Attributes:
        id_mundo: ID fixo (sempre 1).
        turno_atual: O turno corrente ('Dia' ou 'Noite').
        ticks_no_turno: Contador de tempo/ações dentro do turno atual.
    """
    id_mundo: int
    turno_atual: str
    ticks_no_turno: int
