"""
Interface Service
Coordena as ações do usuário e delega para o GameService
Implementa o padrão Singleton para garantir uma única instância
"""

from typing import List, Optional, Dict, Any
from ..models.player import Player
from ..models.chunk import Chunk
from ..models.mapa import TurnoType
from .game_service import GameServiceImpl


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
            self.game_service = GameServiceImpl()
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
        return self.game_service.player_repository.find_all()

    def get_player_by_id(self, player_id: int) -> Optional[Player]:
        """Busca jogador por ID"""
        return self.game_service.player_repository.find_by_id(player_id)

    def get_player_by_name(self, name: str) -> Optional[Player]:
        """Busca jogador por nome"""
        return self.game_service.player_repository.find_by_name(name)

    def create_player(self, nome: str, vida_maxima: int = 100, forca: int = 10) -> Optional[Player]:
        """Cria um novo jogador"""
        result = self.game_service.create_new_player(nome)
        if result.get("success"):
            # O game_service já retorna o player salvo no dicionário
            player_data = result["player"]
            
            # Se player_data é uma instância de Player (para compatibilidade com testes)
            if isinstance(player_data, Player):
                return player_data
            
            # Se player_data é um dicionário (comportamento normal)
            if isinstance(player_data, dict):
                return self.game_service.player_repository.find_by_id(player_data["id"])
        return None

    def save_player(self, player: Player) -> Optional[Player]:
        """Salva um jogador"""
        return self.game_service.player_repository.save(player)

    def delete_player(self, player_id: int) -> bool:
        """Deleta um jogador"""
        return self.game_service.player_repository.delete(player_id)

    def get_adjacent_chunks(self, chunk_id: int, turno: str = 'Dia') -> List[tuple]:
        """Retorna chunks adjacentes ao chunk atual"""
        try:
            # Buscar todos os chunks do turno
            all_chunks = self.game_service.chunk_repository.find_by_mapa('Mapa_Principal', turno)
            
            # Filtrar chunks adjacentes
            adjacent_chunks = []
            for chunk in all_chunks:
                # Verificar se é adjacente (lógica básica)
                cid = chunk.id_chunk
                if abs(cid - chunk_id) == 1 or abs(cid - chunk_id) == 32:
                    adjacent_chunks.append((cid, chunk.id_bioma))
            
            return adjacent_chunks
        except Exception as e:
            print(f"Erro ao buscar chunks adjacentes: {str(e)}")
            return []

    def move_player_to_chunk(self, player: Player, chunk_id: int) -> Optional[Player]:
        """Move um jogador para um novo chunk"""
        result = self.game_service.move_player_to_chunk(player.id_player, chunk_id)
        if result.get("success"):
            # Atualizar o objeto player local
            player.localizacao = f"Mapa {result['chunk']['mapa']} - Chunk {result['chunk']['id']}"
            return player
        return None

    def get_desert_chunk(self, turno: str = 'Dia') -> Optional[int]:
        """Retorna o ID de um chunk de deserto"""
        try:
            # ID do bioma deserto (1 conforme BIOMAS_PREDEFINIDOS)
            desert_id = 1  # Deserto
            # Buscar chunks do deserto pelo ID
            desert_chunks = self.game_service.chunk_repository.find_by_bioma(desert_id)
            # Buscar mapas do turno
            maps = self.game_service.mapa_repository.find_by_turno(TurnoType(turno))
            # Filtrar por mapa e retornar primeiro
            for chunk in desert_chunks:
                if any(m.id_mapa == chunk.id_mapa for m in maps):
                    return chunk.id_chunk
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
        return self.game_service.player_repository.find_active_players()

    def get_player_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas dos jogadores"""
        stats = self.game_service.get_map_statistics()
        return {
            'total': stats.get('total_jogadores', 0),
            'active': stats.get('jogadores_ativos', 0),
            'average_level': 1,  # Valor padrão já que não temos essa estatística no game_service
            'average_health': 50  # Valor padrão já que não temos essa estatística no game_service
        }

    def get_chunk_by_id(self, chunk_id: int) -> Optional[Chunk]:
        """Busca chunk por ID"""
        return self.game_service.chunk_repository.find_by_id(chunk_id)

    def get_map_by_id(self, map_id: int) -> Optional['Mapa']:
        """Busca mapa por ID"""
        from ..models.mapa import Mapa, TurnoType
        
        try:
            # Try to find the map by ID from the mapa repository
            mapas = self.game_service.mapa_repository.find_all()
            for mapa in mapas:
                if mapa.id_mapa == map_id:
                    return mapa
            return None
        except Exception as e:
            print(f"Erro ao buscar mapa {map_id}: {str(e)}")
            return None

    def get_bioma_by_id(self, bioma_id: int) -> Optional['Bioma']:
        """Busca bioma por ID"""
        from ..models.bioma import Bioma
        
        try:
            # Use the bioma repository from game_service
            bioma = self.game_service.bioma_repository.find_by_id(bioma_id)
            return bioma
        except Exception as e:
            print(f"Erro ao buscar bioma {bioma_id}: {str(e)}")
            return None
