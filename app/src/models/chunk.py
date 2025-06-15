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
        numero_chunk: ID único do chunk (chave primária)
        id_bioma: Nome do bioma do chunk (FK para Bioma.NomeBioma)
        id_mapa_nome: Nome do mapa (parte da FK para Mapa)
        id_mapa_turno: Turno do mapa (parte da FK para Mapa)
    """
    numero_chunk: int
    id_bioma: str
    id_mapa_nome: str
    id_mapa_turno: str
    
    def get_display_name(self) -> str:
        """
        Retorna o nome formatado do chunk para exibição
        
        Returns:
            String formatada do chunk
        """
        return f"{self.id_bioma} ({self.id_mapa_nome} - {self.id_mapa_turno})"
    
    def is_desert(self) -> bool:
        """Verifica se o chunk é um deserto"""
        return self.id_bioma.lower() == 'deserto'
    
    def is_jungle(self) -> bool:
        """Verifica se o chunk é uma selva"""
        return self.id_bioma.lower() == 'selva'
    
    def is_forest(self) -> bool:
        """Verifica se o chunk é uma floresta"""
        return self.id_bioma.lower() == 'floresta'
    
    def is_ocean(self) -> bool:
        """Verifica se o chunk é um oceano"""
        return self.id_bioma.lower() == 'oceano'
    
    def is_day(self) -> bool:
        """Verifica se é dia no chunk"""
        return self.id_mapa_turno.lower() == 'dia'
    
    def is_night(self) -> bool:
        """Verifica se é noite no chunk"""
        return self.id_mapa_turno.lower() == 'noite'
    
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
        if self.numero_chunk > 1:
            adjacent.append(self.numero_chunk - 1)
        if self.numero_chunk < 1000:  # Assumindo 1000 chunks
            adjacent.append(self.numero_chunk + 1)
        
        # Vertical
        if self.numero_chunk > map_size:
            adjacent.append(self.numero_chunk - map_size)
        if self.numero_chunk <= 1000 - map_size:
            adjacent.append(self.numero_chunk + map_size)
        
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
        return self.id_mapa_nome == mapa_nome and self.id_mapa_turno == mapa_turno
    
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
        return (self.id_mapa_nome, self.id_mapa_turno)
    
    def __str__(self) -> str:
        """Representação string do chunk"""
        return f"Chunk({self.numero_chunk}: {self.get_display_name()})"
    
    def __repr__(self) -> str:
        """Representação detalhada do chunk"""
        return (f"Chunk(numero_chunk={self.numero_chunk}, "
                f"id_bioma='{self.id_bioma}', "
                f"id_mapa_nome='{self.id_mapa_nome}', "
                f"id_mapa_turno='{self.id_mapa_turno}')")
    
    def __eq__(self, other) -> bool:
        """Comparação de igualdade baseada na chave primária"""
        if not isinstance(other, Chunk):
            return False
        return self.numero_chunk == other.numero_chunk
    
    def __hash__(self) -> int:
        """Hash baseado na chave primária"""
        return hash(self.numero_chunk) 
