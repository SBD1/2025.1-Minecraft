"""
Models para Aldeão e suas especializações (Bob Mago, Bob Construtor)
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Aldeao:
    """
    Model que representa a entidade Aldeao (tabela pai).
    
    Attributes:
        id_aldeao: ID único do aldeão.
        nome: Nome do aldeão.
        tipo: Tipo do aldeão ('Normal', 'Mago', 'Construtor').
        descricao: Descrição geral do aldeão.
        id_casa: ID da casa onde o aldeão mora (pode ser nulo).
    """
    id_aldeao: Optional[int]
    nome: str
    tipo: str
    descricao: Optional[str]
    id_casa: Optional[int]

@dataclass
class BobMago:
    """
    Model que representa a especialização Bob_mago.
    
    Attributes:
        id_aldeao_mago: ID do aldeão (chave primária e estrangeira).
        habilidade_mago: Habilidade principal do mago.
        nivel: Nível da especialização.
        descricao: Descrição específica da sua função como mago.
    """
    id_aldeao_mago: int
    habilidade_mago: Optional[str]
    nivel: int
    descricao: Optional[str]

@dataclass
class BobConstrutor:
    """
    Model que representa a especialização Bob_construtor.
    
    Attributes:
        id_aldeao_construtor: ID do aldeão (chave primária e estrangeira).
        habilidades_construtor: Habilidades de construção.
        nivel: Nível da especialização.
        descricao: Descrição específica da sua função como construtor.
    """
    id_aldeao_construtor: int
    habilidades_construtor: Optional[str]
    nivel: int
    descricao: Optional[str]
