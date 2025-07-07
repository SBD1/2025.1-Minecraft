from dataclasses import dataclass
from enum import Enum
from typing import Optional 


# Model que representa a entidade Totem no banco de dados

@dataclass
class Totem:
    id: Optional[int] = None  # ID único no banco (gerado automaticamente)
    nome: str = ""            # Nome do totem
    localizacao: int = 0      # ID do chunk onde o totem está localizado
    tipo: str = ""            # Tipo do totem (ex: 'ancestral', 'protetor', etc.)
    ativo: bool = True        # Indica se o totem está ativo no jogo
