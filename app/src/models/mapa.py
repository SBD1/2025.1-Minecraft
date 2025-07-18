"""
Model do Mapa
Representa um mapa do jogo com seus chunks e características
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from .chunk import Chunk


class TurnoType(Enum):
    """Tipos de turno disponíveis"""
    DIA = "Dia"
    NOITE = "Noite"


@dataclass
class Mapa:
    """
    Model que representa um mapa do jogo
    
    Attributes:
        id_mapa: Identificador único do mapa (chave primária)
        nome: Nome do mapa
        turno: Turno do mapa
        chunks: Lista de chunks relacionados a este mapa
        _chunk_repository: Repository para acesso aos chunks (injeção de dependência)
    """
    id_mapa: int
    nome: str
    turno: TurnoType
    chunks: List[Chunk] = field(default_factory=list)
    _chunk_repository = None  # Será injetado via setter
    
    def __post_init__(self):
        """Converte string para enum se necessário"""
        if isinstance(self.turno, str):
            self.turno = TurnoType(self.turno)
    
    def set_chunk_repository(self, repository):
        """Define o repository de chunks (injeção de dependência)"""
        self._chunk_repository = repository
    
    def get_chunks_by_bioma(self, bioma: str) -> List[Chunk]:
        """
        Retorna todos os chunks de um bioma específico neste mapa
        
        Args:
            bioma: Nome do bioma
            
        Returns:
            Lista de chunks do bioma
        """
        if not self._chunk_repository:
            raise ValueError("Chunk repository não foi configurado")
        
        chunks = self.get_chunks()
        return [chunk for chunk in chunks if chunk.id_bioma == bioma]
    
    def get_bioma_distribution(self) -> Dict[str, int]:
        """
        Retorna a distribuição de biomas no mapa
        
        Returns:
            Dicionário com bioma e quantidade de chunks
        """
        if not self._chunk_repository:
            raise ValueError("Chunk repository não foi configurado")
        
        chunks = self.get_chunks()
        if not chunks:
            return {}
        
        distribution = {}
        for chunk in chunks:
            bioma = chunk.id_bioma
            distribution[bioma] = distribution.get(bioma, 0) + 1
        return distribution
    
    def is_day_map(self) -> bool:
        """Verifica se é um mapa de dia"""
        return self.turno == TurnoType.DIA
    
    def is_night_map(self) -> bool:
        """Verifica se é um mapa de noite"""
        return self.turno == TurnoType.NOITE
    
    def get_display_info(self) -> Dict[str, Any]:
        """
        Retorna informações formatadas do mapa para exibição
        
        Returns:
            Dicionário com informações do mapa
        """
        if not self._chunk_repository:
            raise ValueError("Chunk repository não foi configurado")
        
        info = {
            'nome': self.nome,
            'turno': self.turno.value,
            'tipo': 'Dia' if self.is_day_map() else 'Noite'
        }
        
        chunks = self.get_chunks()
        if chunks:
            info['total_chunks'] = len(chunks)
            info['distribuicao'] = self.get_bioma_distribution()
        
        return info
    
    def get_chunks(self) -> List[Chunk]:
        """
        Retorna os chunks deste mapa usando o repository
        """
        if not self._chunk_repository:
            raise ValueError("Chunk repository não foi configurado")
        
        return self._chunk_repository.find_by_mapa(self.nome, self.turno.value)
    
    def get_chunk_by_id(self, chunk_id: int) -> Optional[Chunk]:
        """
        Busca um chunk pelo ID neste mapa
        
        Args:
            chunk_id: ID do chunk
            
        Returns:
            Chunk encontrado ou None
        """
        if not self._chunk_repository:
            raise ValueError("Chunk repository não foi configurado")
        
        chunks = self.get_chunks()
        
        for chunk in chunks:
            if chunk.id_chunk == chunk_id:
                return chunk
        return None
    
    def __str__(self) -> str:
        """Representação string do mapa"""
        try:
            chunks = self.get_chunks()
            chunk_count = len(chunks) if chunks else 0
            return f"Mapa({self.nome} - {self.turno.value}, {chunk_count} chunks)"
        except ValueError:
            return f"Mapa({self.nome} - {self.turno.value}, repository não configurado)"
    
    def __repr__(self) -> str:
        """Representação detalhada do mapa"""
        return f"Mapa(nome='{self.nome}', turno={self.turno})"
    
    def __eq__(self, other) -> bool:
        """Comparação de igualdade baseada na chave primária composta"""
        if not isinstance(other, Mapa):
            return False
        return self.id_mapa == other.id_mapa
    
    def __hash__(self) -> int:
        """Hash baseado na chave primária composta"""
        return hash(self.id_mapa)

