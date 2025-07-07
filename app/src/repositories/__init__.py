"""
Repositories package
Implementa o padrão Repository para acesso a dados
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..models.bioma import Bioma
from ..models.chunk import Chunk
from ..models.mapa import Mapa, TurnoType
from ..models.player import Player
from ..models.fantasma import Fantasma
from ..models.totem import Totem
from ..models.ponte import Ponte
from .bioma_repository import BiomaRepository, BiomaRepositoryImpl
from .chunk_repository import ChunkRepository, ChunkRepositoryImpl
from .mapa_repository import MapaRepository, MapaRepositoryImpl
from .player_repository import PlayerRepository, PlayerRepositoryImpl
from .totem_repository import TotemRepository, TotemRepositoryImpl
from .ponte_repository import PonteRepository, PonteRepositoryImpl
from .fatasma_repository import FantasmaRepository, FantasmaRepositoryImpl
class BaseRepository(ABC):
    """Interface base para todos os repositories"""
    
    @abstractmethod
    def find_all(self) -> List[Any]:
        """Retorna todos os registros"""
        pass
    
    @abstractmethod
    def find_by_id(self, id: Any) -> Optional[Any]:
        """Busca por ID"""
        pass
    
    @abstractmethod
    def save(self, entity: Any) -> Any:
        """Salva uma entidade"""
        pass
    
    @abstractmethod
    def delete(self, id: Any) -> bool:
        """Deleta uma entidade por ID"""
        pass


class BiomaRepository(BaseRepository):
    """Repository para entidade Bioma"""
    
    def find_all(self) -> List[Bioma]:
        """Retorna todos os biomas"""
        pass
    
    def find_by_id(self, id: str) -> Optional[Bioma]:
        """Busca bioma por ID"""
        pass
    
    def save(self, bioma: Bioma) -> Bioma:
        """Salva um bioma"""
        pass
    
    def delete(self, id: str) -> bool:
        """Deleta um bioma por ID"""
        pass


class ChunkRepository(BaseRepository):
    """Repository para entidade Chunk"""
    
    def find_all(self) -> List[Chunk]:
        """Retorna todos os chunks"""
        pass
    
    def find_by_id(self, id: int) -> Optional[Chunk]:
        """Busca chunk por ID"""
        pass
    
    def save(self, chunk: Chunk) -> Chunk:
        """Salva um chunk"""
        pass
    
    def delete(self, id: int) -> bool:
        """Deleta um chunk por ID"""
        pass
    
    def find_by_mapa(self, mapa_nome: str, mapa_turno: str) -> List[Chunk]:
        """Busca chunks por mapa"""
        pass
    
    def find_by_bioma(self, bioma_id: str) -> List[Chunk]:
        """Busca chunks por bioma"""
        pass


class MapaRepository(BaseRepository):
    """Repository para entidade Mapa"""
    
    def find_all(self) -> List[Mapa]:
        """Retorna todos os mapas"""
        pass
    
    def find_by_id(self, nome: str, turno: TurnoType) -> Optional[Mapa]:
        """Busca mapa por nome e turno"""
        pass
    
    def save(self, mapa: Mapa) -> Mapa:
        """Salva um mapa"""
        pass
    
    def delete(self, nome: str, turno: TurnoType) -> bool:
        """Deleta um mapa por nome e turno"""
        pass
    
    def find_by_turno(self, turno: TurnoType) -> List[Mapa]:
        """Busca mapas por turno"""
        pass


class PlayerRepository(BaseRepository):
    """Repository para entidade Player"""
    
    def find_all(self) -> List[Player]:
        """Retorna todos os jogadores"""
        pass
    
    def find_by_id(self, id: int) -> Optional[Player]:
        """Busca jogador por ID"""
        pass
    
    def save(self, player: Player) -> Player:
        """Salva um jogador"""
        pass
    
    def delete(self, id: int) -> bool:
        """Deleta um jogador por ID"""
        pass
    
    def find_by_name(self, name: str) -> Optional[Player]:
        """Busca jogador por nome"""
        pass
    
    def find_active_players(self) -> List[Player]:
        """Busca jogadores ativos"""
        pass 

class FantasmaRepository(BaseRepository):
    """Repository para entidade Fantasma"""
    
    def find_all(self) -> List[Fantasma]:
        """Retorna todos os fantasmas"""
        pass
    
    def find_by_id(self, id: int) -> Optional[Fantasma]:
        """Busca fantasma por ID"""
        pass
    
    def save(self, fantasma: Fantasma) -> Fantasma:
        """Salva um fantasma"""
        pass
    
    def delete(self, id: int) -> bool:
        """Deleta um fantasma por ID"""
        pass
    
    def find_by_tipo(self, tipo: str) -> List[Fantasma]:
        """Busca fantasmas por tipo (minerador/construtor)"""
        pass
    
    def find_by_chunk(self, chunk_nome: str) -> List[Fantasma]:
        """Busca fantasmas de um chunk específico"""
        pass


class TotemRepository(BaseRepository):
    """Repository para entidade Totem"""
    
    def find_all(self) -> List[Totem]:
        """Retorna todos os totems ativos"""
        pass
    
    def find_by_id(self, id: int) -> Optional[Totem]:
        """Busca totem por ID"""
        pass
    
    def save(self, totem: Totem) -> Totem:
        """Salva um totem"""
        pass
    
    def delete(self, id: int) -> bool:
        """Deleta um totem por ID"""
        pass

class PonteRepository(BaseRepository):
    """Repository para entidade Ponte"""
    
    def find_all(self) -> List[Ponte]:
        """Retorna todas as pontes ativas"""
        pass
    
    def find_by_id(self, id: int) -> Optional[Ponte]:
        """Busca ponte por ID"""
        pass
    
    def save(self, ponte: Ponte) -> Ponte:
        """Salva uma ponte"""
        pass
    
    def delete(self, id: int) -> bool:
        """Deleta uma ponte por ID"""
        pass
