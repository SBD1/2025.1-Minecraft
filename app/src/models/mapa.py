"""
Model do Mapa
Representa um mapa do jogo com seus chunks e características
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
from .chunk import Chunk
import psycopg2
from functools import wraps


def memoize(func):
    """Decorator para cachear resultados de funções"""
    cache = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Usa os argumentos como chave do cache
        key = str(args) + str(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    return wrapper


class TurnoType(Enum):
    """Tipos de turno disponíveis"""
    DIA = "Dia"
    NOITE = "Noite"


@dataclass
class Mapa:
    """
    Model que representa um mapa do jogo
    
    Attributes:
        nome: Nome do mapa (parte da chave primária composta)
        turno: Turno do mapa (parte da chave primária composta)
        chunks: Lista de chunks do mapa (opcional, para cache)
    """
    nome: str
    turno: TurnoType
    
    def __post_init__(self):
        """Converte string para enum se necessário"""
        if isinstance(self.turno, str):
            self.turno = TurnoType(self.turno)
    
    def get_chunks_by_bioma(self, bioma: str) -> List[Chunk]:
        """
        Retorna todos os chunks de um bioma específico neste mapa
        
        Args:
            bioma: Nome do bioma
            
        Returns:
            Lista de chunks do bioma
        """
        chunks = self.get_chunks()
        return [chunk for chunk in chunks if chunk.id_bioma.lower() == bioma.lower()]
    
    def get_bioma_distribution(self) -> Dict[str, int]:
        """
        Retorna a distribuição de biomas no mapa
        
        Returns:
            Dicionário com bioma e quantidade de chunks
        """
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
    
    @memoize
    def get_chunks(self) -> List[Chunk]:
        """
        Retorna os chunks deste mapa consultando o banco de dados
        Resultado é cacheado automaticamente via memoize
        """
        try:
            from ..utils.db_helpers import connection_db
            
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT numero_chunk, id_bioma, id_mapa_nome, id_mapa_turno
                        FROM chunk
                        WHERE id_mapa_nome = %s AND id_mapa_turno = %s
                        ORDER BY numero_chunk
                    """, (self.nome, self.turno.value))
                    
                    results = cursor.fetchall()
                    chunks = []
                    
                    for row in results:
                        chunk = Chunk(
                            numero_chunk=row[0],
                            id_bioma=row[1],
                            id_mapa_nome=row[2],
                            id_mapa_turno=row[3]
                        )
                        chunks.append(chunk)
                    
                    print(f"✅ Carregados {len(chunks)} chunks do mapa {self.nome} ({self.turno.value})")
                    return chunks
                    
        except Exception as e:
            print(f"❌ Erro ao carregar chunks do banco: {str(e)}")
            return []
    
    def set_chunks(self, chunks: List[Chunk]) -> None:
        """
        Define chunks manualmente (para cache customizado)
        Sobrescreve o cache do memoize
        
        Args:
            chunks: Lista de chunks do mapa
        """
        # Filtra apenas chunks deste mapa
        filtered_chunks = [chunk for chunk in chunks if chunk.id_mapa_nome == self.nome and chunk.id_mapa_turno == self.turno.value]
        
        # Sobrescreve o cache do memoize
        cache_key = str((self,)) + str(sorted({}.items()))
        memoize.cache[cache_key] = filtered_chunks
        
        print(f"✅ Definidos {len(filtered_chunks)} chunks manualmente para {self.nome} ({self.turno.value})")
    
    def get_chunk_by_id(self, chunk_id: int) -> Optional[Chunk]:
        """
        Busca um chunk pelo ID neste mapa
        
        Args:
            chunk_id: ID do chunk
            
        Returns:
            Chunk encontrado ou None
        """
        chunks = self.get_chunks()
        
        for chunk in chunks:
            if chunk.numero_chunk == chunk_id:
                return chunk
        return None
    
    def __str__(self) -> str:
        """Representação string do mapa"""
        chunks = self.get_chunks()
        chunk_count = len(chunks) if chunks else 0
        return f"Mapa({self.nome} - {self.turno.value}, {chunk_count} chunks)"
    
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