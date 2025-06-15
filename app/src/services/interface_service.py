"""
Interface Service
Coordena as ações do usuário e integra com os repositórios
Implementa o padrão Singleton para garantir uma única instância
"""

from typing import List, Optional, Dict, Any
from ..models.player import Player
from ..models.chunk import Chunk
from ..repositories import PlayerRepositoryImpl, ChunkRepositoryImpl, MapaRepositoryImpl
from ..models.mapa import TurnoType


class InterfaceService:
    """
    Serviço que coordena as ações da interface com os repositórios
    Implementa o padrão Singleton
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Implementa o padrão Singleton"""
        if cls._instance is None:
            cls._instance = super(InterfaceService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa o service apenas uma vez"""
        if not InterfaceService._initialized:
            self.player_repository = PlayerRepositoryImpl()
            self.chunk_repository = ChunkRepositoryImpl()
            self.mapa_repository = MapaRepositoryImpl()
            InterfaceService._initialized = True
    
    @classmethod
    def get_instance(cls) -> 'InterfaceService':
        """Método de classe para obter a instância singleton"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def reset_instance(cls) -> None:
        """Reseta a instância singleton (útil para testes)"""
        cls._instance = None
        cls._initialized = False
    
    def get_all_players(self) -> List[Player]:
        """Retorna todos os jogadores"""
        return self.player_repository.find_all()
    
    def get_player_by_id(self, player_id: int) -> Optional[Player]:
        """Busca jogador por ID"""
        return self.player_repository.find_by_id(player_id)
    
    def get_player_by_name(self, name: str) -> Optional[Player]:
        """Busca jogador por nome"""
        return self.player_repository.find_by_name(name)
    
    def create_player(self, nome: str, vida_maxima: int = 100, forca: int = 10) -> Optional[Player]:
        """Cria um novo jogador"""
        # Verificar se nome já existe
        existing_player = self.player_repository.find_by_name(nome)
        if existing_player:
            return None
        
        # Criar novo jogador
        new_player = Player(
            id_jogador=None,
            nome=nome,
            vida_maxima=vida_maxima,
            vida_atual=vida_maxima,
            forca=forca,
            localizacao="1",  # Chunk inicial
            nivel=1,
            experiencia=0
        )
        
        return self.player_repository.save(new_player)
    
    def save_player(self, player: Player) -> Optional[Player]:
        """Salva um jogador"""
        return self.player_repository.save(player)
    
    def delete_player(self, player_id: int) -> bool:
        """Deleta um jogador"""
        return self.player_repository.delete(player_id)
    
    def get_adjacent_chunks(self, chunk_id: int, turno: str = 'Dia') -> List[tuple]:
        """Retorna chunks adjacentes ao chunk atual"""
        try:
            # Buscar todos os chunks do turno
            all_chunks = self.chunk_repository.find_by_mapa('Mapa_Principal', turno)
            
            # Filtrar chunks adjacentes
            adjacent_chunks = []
            for chunk in all_chunks:
                # Verificar se é adjacente (lógica básica)
                if abs(chunk.numero_chunk - chunk_id) == 1 or abs(chunk.numero_chunk - chunk_id) == 32:
                    adjacent_chunks.append((chunk.numero_chunk, chunk.id_bioma))
            
            return adjacent_chunks
        except Exception as e:
            print(f"Erro ao buscar chunks adjacentes: {str(e)}")
            return []
    
    def move_player_to_chunk(self, player: Player, chunk_id: int) -> Optional[Player]:
        """Move um jogador para um novo chunk"""
        try:
            # Verificar se o chunk existe
            chunk = self.chunk_repository.find_by_id(chunk_id)
            if not chunk:
                return None
            
            # Atualizar localização do jogador
            player.localizacao = str(chunk_id)
            
            # Salvar no banco
            return self.player_repository.save(player)
        except Exception as e:
            print(f"Erro ao mover jogador: {str(e)}")
            return None
    
    def get_desert_chunk(self, turno: str = 'Dia') -> Optional[int]:
        """Retorna o ID de um chunk de deserto"""
        try:
            # Buscar chunks do deserto
            desert_chunks = self.chunk_repository.find_by_bioma('Deserto')
            
            # Filtrar por turno
            for chunk in desert_chunks:
                if chunk.id_mapa_turno == turno:
                    return chunk.numero_chunk
            
            return None
        except Exception as e:
            print(f"Erro ao buscar chunk de deserto: {str(e)}")
            return None
    
    def ensure_player_location(self, player: Player) -> bool:
        """Garante que o jogador tem uma localização válida"""
        if not player.localizacao or player.localizacao == "0":
            desert_chunk = self.get_desert_chunk('Dia')
            if desert_chunk:
                updated_player = self.move_player_to_chunk(player, desert_chunk)
                if updated_player:
                    # Atualizar o objeto original
                    player.localizacao = updated_player.localizacao
                    return True
            return False
        return True
    
    def get_active_players(self) -> List[Player]:
        """Retorna jogadores ativos (com vida > 0)"""
        return self.player_repository.find_active_players()
    
    def get_player_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas dos jogadores"""
        all_players = self.player_repository.find_all()
        active_players = self.player_repository.find_active_players()
        
        if not all_players:
            return {
                'total': 0,
                'active': 0,
                'average_level': 0,
                'average_health': 0
            }
        
        total_health = sum(p.vida_atual for p in all_players)
        total_level = sum(p.nivel for p in all_players)
        
        return {
            'total': len(all_players),
            'active': len(active_players),
            'average_level': total_level / len(all_players),
            'average_health': total_health / len(all_players)
        } 
