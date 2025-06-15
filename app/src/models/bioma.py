"""
Model do Bioma
Representa um bioma do jogo com suas características
"""

from dataclasses import dataclass
from enum import Enum


class BiomaType(Enum):
    """Tipos de bioma disponíveis no jogo"""
    DESERTO = "Deserto"
    SELVA = "Selva"
    FLORESTA = "Floresta"
    OCEANO = "Oceano"


@dataclass
class Bioma:
    """
    Model que representa um bioma do jogo
    
    Attributes:
        nome: Nome do bioma (chave primária - NomeBioma)
    """
    nome: str
    
    def __str__(self) -> str:
        """Representação string do bioma"""
        return f"Bioma({self.nome})"
    
    def __repr__(self) -> str:
        """Representação detalhada do bioma"""
        return f"Bioma(nome='{self.nome}')"
    
    def __eq__(self, other) -> bool:
        """Comparação de igualdade baseada na chave primária"""
        if not isinstance(other, Bioma):
            return False
        return self.nome == other.nome
    
    def __hash__(self) -> int:
        """Hash baseado na chave primária"""
        return hash(self.nome)


# Biomas predefinidos do jogo (baseados nos dados do banco)
BIOMAS_PREDEFINIDOS = {
    BiomaType.DESERTO: Bioma("Deserto"),
    BiomaType.SELVA: Bioma("Selva"),
    BiomaType.FLORESTA: Bioma("Floresta"),
    BiomaType.OCEANO: Bioma("Oceano")
}
