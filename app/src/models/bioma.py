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
        id_bioma: Identificador único do bioma (chave primária)
        nome: Nome do bioma
        descricao: Descrição do bioma
    """
    id_bioma: int
    nome: str
    descricao: str
    
    def __str__(self) -> str:
        """Representação string do bioma"""
        return f"Bioma({self.nome})"
    
    def __repr__(self) -> str:
        """Representação detalhada do bioma"""
        return f"Bioma(id_bioma={self.id_bioma}, nome='{self.nome}', descricao='{self.descricao}')"
    
    def __eq__(self, other) -> bool:
        """Comparação de igualdade baseada na chave primária"""
        if not isinstance(other, Bioma):
            return False
        return self.id_bioma == other.id_bioma
    
    def __hash__(self) -> int:
        """Hash baseado na chave primária"""
        return hash(self.id_bioma)


# Biomas predefinidos do jogo (baseados nos dados do banco)
BIOMAS_PREDEFINIDOS = {
    BiomaType.DESERTO: Bioma(1, "Deserto", "Um bioma árido com pouca vegetação."),
    BiomaType.SELVA: Bioma(2, "Selva", "Um bioma tropical denso e úmido."),
    BiomaType.FLORESTA: Bioma(3, "Floresta", "Um bioma com muitas árvores e vida selvagem."),
    BiomaType.OCEANO: Bioma(4, "Oceano", "Um vasto bioma de água salgada.")
}
