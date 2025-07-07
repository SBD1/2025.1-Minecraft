from dataclasses import dataclass
from typing import Optional

# Model que representa uma ponte entre dois chunks
# Pode ser usada para permitir passagem, travessia ou ligação de áreas
@dataclass
class Ponte:
    id: Optional[int] = None           # ID único da ponte no banco
    chunk_origem: int = 0             # ID do chunk de origem
    chunk_destino: int = 0            # ID do chunk de destino
    tipo: str = ""                    # Tipo da ponte (ex: 'madeira', 'pedra', etc.)
    ativa: bool = True                # Indica se a ponte está ativa
