"""
Model do Mapa refatorado usando Repository Pattern
Representa um mapa do jogo com seus chunks e características
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
from .chunk import Chunk
from ..repositories import ChunkRepository


class TurnoType(Enum):
    """Tipos de turno disponíveis"""
    DIA = "Dia"
    NOITE = "Noite"


@dataclass
class Mapa:
    """
    Model que representa um mapa do jogo (versão refatorada)
    
    Attributes:
        nome: Nome do mapa (parte da chave primária composta)
        turno: Turno do mapa (parte da chave primária composta)
        _chunk_repository: Repository para acesso aos chunks (injetado)
    """
    nome: str
    turno: TurnoType
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
        return [chunk for chunk in chunks if chunk.id_bioma.lower() == bioma.lower()]
    
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
            if chunk.numero_chunk == chunk_id:
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
        return self.nome == other.nome and self.turno == other.turno
    
    def __hash__(self) -> int:
        """Hash baseado na chave primária composta"""
        return hash((self.nome, self.turno))


# Exemplo de uso com Repository Pattern
def exemplo_uso_repository():
    """Exemplo de como usar o Mapa com Repository Pattern"""
    
    # 1. Configurar repositories
    chunk_repo = ChunkRepository()
    
    # 2. Criar mapa e injetar repository
    mapa = Mapa("Mapa_Principal", TurnoType.DIA)
    mapa.set_chunk_repository(chunk_repo)
    
    # 3. Usar o mapa (agora sem acesso direto ao banco)
    chunks = mapa.get_chunks()
    print(f"Mapa tem {len(chunks)} chunks")
    
    # 4. Buscar por bioma
    chunks_deserto = mapa.get_chunks_by_bioma("Deserto")
    print(f"Chunks de deserto: {len(chunks_deserto)}")
    
    # 5. Informações de exibição
    info = mapa.get_display_info()
    print(f"Informações: {info}")
    
    return mapa 