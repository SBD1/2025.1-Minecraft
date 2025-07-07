"""
Model do Chunk
Representa um chunk do mapa do jogo
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Chunk:
    """
    Model que representa um chunk do mapa
    
    Attributes:
        id_chunk: Identificador único do chunk (chave primária)
        id_bioma: FK para Bioma.id_bioma
        id_mapa: FK para Mapa.id_mapa
        x: Coordenada X do chunk no grid
        y: Coordenada Y do chunk no grid
    """
    id_chunk: int
    id_bioma: int
    id_mapa: int
    x: int
    y: int
    
    def get_display_name(self) -> str:
        """
        Retorna o nome formatado do chunk para exibição
        
        Returns:
            String formatada do chunk
        """
        return f"{self.id_bioma} ({self.id_mapa} - {self.x}, {self.y})"
    
    def is_desert(self) -> bool:
        """Verifica se o chunk é um deserto"""
        return self.id_bioma == 'deserto'
    
    def is_jungle(self) -> bool:
        """Verifica se o chunk é uma selva"""
        return self.id_bioma == 'selva'
    
    def is_forest(self) -> bool:
        """Verifica se o chunk é uma floresta"""
        return self.id_bioma == 'floresta'
    
    def is_ocean(self) -> bool:
        """Verifica se o chunk é um oceano"""
        return self.id_bioma == 'oceano'
    
    def is_day(self) -> bool:
        """Verifica se é dia no chunk"""
        return self.x % 2 == 0
    
    def is_night(self) -> bool:
        """Verifica se é noite no chunk"""
        return self.x % 2 != 0
    
    def get_adjacent_chunk_ids(self, map_size: int = 32) -> List[int]:
        """
        Retorna os IDs dos chunks adjacentes
        Baseado na lógica de grid do mapa
        
        Args:
            map_size: Tamanho do mapa (assumindo mapa quadrado)
            
        Returns:
            Lista de IDs dos chunks adjacentes
        """
        adjacent = []
        
        # Horizontal
        if self.id_chunk > 1:
            adjacent.append(self.id_chunk - 1)
        if self.id_chunk < 1000:  # Assumindo 1000 chunks
            adjacent.append(self.id_chunk + 1)
        
        # Vertical
        if self.id_chunk > map_size:
            adjacent.append(self.id_chunk - map_size)
        if self.id_chunk <= 1000 - map_size:
            adjacent.append(self.id_chunk + map_size)
        
        return adjacent
    
    def belongs_to_map(self, mapa_nome: str, mapa_turno: str) -> bool:
        """
        Verifica se o chunk pertence a um mapa específico
        
        Args:
            mapa_nome: Nome do mapa
            mapa_turno: Turno do mapa
            
        Returns:
            True se o chunk pertence ao mapa
        """
        return self.id_mapa == mapa_nome and self.x == mapa_turno
    
    def get_bioma_type(self) -> str:
        """
        Retorna o tipo de bioma como string
        
        Returns:
            Nome do bioma
        """
        return self.id_bioma
    
    def get_map_key(self) -> tuple:
        """
        Retorna a chave do mapa como tupla
        
        Returns:
            Tupla (nome_mapa, turno_mapa)
        """
        return (self.id_mapa, self.x)
    
    def __str__(self) -> str:
        """Representação string do chunk"""
        return f"Chunk({self.id_chunk}: {self.get_display_name()})"
    
    def __repr__(self) -> str:
        """Representação detalhada do chunk"""
        return (f"Chunk(id_chunk={self.id_chunk}, "
                f"id_bioma={self.id_bioma}, "
                f"id_mapa={self.id_mapa}, "
                f"x={self.x}, "
                f"y={self.y})")
    
    def __eq__(self, other) -> bool:
        """Comparação de igualdade baseada na chave primária"""
        if not isinstance(other, Chunk):
            return False
        return self.id_chunk == other.id_chunk
    
    def __hash__(self) -> int:
        """Hash baseado na chave primária"""
        return hash(self.id_chunk)
