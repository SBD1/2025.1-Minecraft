"""
Service layer que usa repositories para lógica de negócio
Demonstra o uso do Repository Pattern e Singleton
"""

from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod
from ..repositories import (
    BiomaRepositoryImpl,
    ChunkRepositoryImpl,
    MapaRepositoryImpl,
    PlayerRepositoryImpl
)
from ..models.mapa import Mapa, TurnoType
from ..models.player import Player
from ..models.chunk import Chunk


class GameService(ABC):
    """
    Interface abstrata para a lógica de negócio do jogo
    """
    @abstractmethod
    def get_map_info(self, mapa_nome: str, turno: TurnoType) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_player_status(self, player_id: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def move_player_to_chunk(self, player_id: int, chunk_id: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_players_in_bioma(self, bioma_id: int) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_map_statistics(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create_new_player(self, nome: str, localizacao: str = "Spawn") -> Dict[str, Any]:
        pass


class GameServiceImpl(GameService):
    """
    Implementação Singleton do GameService
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameServiceImpl, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not GameServiceImpl._initialized:
            self.chunk_repository = ChunkRepositoryImpl()
            self.mapa_repository = MapaRepositoryImpl()
            self.player_repository = PlayerRepositoryImpl()
            GameServiceImpl._initialized = True

    @classmethod
    def get_instance(cls) -> 'GameServiceImpl':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        cls._instance = None
        cls._initialized = False

    def get_map_info(self, mapa_nome: str, turno: TurnoType) -> Dict[str, Any]:
        mapa = self.mapa_repository.find_by_id(mapa_nome, turno)
        if not mapa:
            return {"error": "Mapa não encontrado"}
        
        chunks = self.chunk_repository.find_by_mapa(mapa_nome, turno.value)
        bioma_distribution = {}
        
        for chunk in chunks:
            bioma = chunk.id_bioma
            bioma_distribution[bioma] = bioma_distribution.get(bioma, 0) + 1
        return {
            "nome": mapa.nome,
            "turno": mapa.turno.value,
            "total_chunks": len(chunks),
            "distribuicao_biomas": bioma_distribution,
            "chunks": [chunk.id_chunk for chunk in chunks[:10]]
        }

    def get_player_status(self, player_id: int) -> Dict[str, Any]:
        player = self.player_repository.find_by_id(player_id)
        if not player:
            return {"error": "Jogador não encontrado"}

        vida_percentual = (player.vida_atual / player.vida_maxima) * 100 if player.vida_maxima > 0 else 0
        return {
            "id": player.id_player,
            "nome": player.nome,
            "vida_atual": player.vida_atual,
            "vida_maxima": player.vida_maxima,
            "vida_percentual": round(vida_percentual, 1),
            "forca": player.forca,
            "localizacao": player.localizacao,
            "nivel": player.nivel,
            "experiencia": player.experiencia,
            "status": "Vivo" if player.vida_atual > 0 else "Morto"
        }

    def move_player_to_chunk(self, player_id: int, chunk_id: int) -> Dict[str, Any]:
        player = self.player_repository.find_by_id(player_id)
        chunk = self.chunk_repository.find_by_id(chunk_id)

        if not player:
            return {"error": "Jogador não encontrado"}
        
        if not chunk:
            return {"error": "Chunk não encontrado"}

        player.localizacao = f"Mapa {chunk.id_mapa} - Chunk {chunk.id_chunk}"
        updated_player = self.player_repository.save(player)
        return {
            "success": True,
            "message": f"Jogador {player.nome} movido para {player.localizacao}",
            "player": {
                "id": updated_player.id_player,
                "nome": updated_player.nome,
                "localizacao": updated_player.localizacao
            },
            "chunk": {
                "id": chunk.id_chunk,
                "bioma": chunk.id_bioma,
                "mapa": chunk.id_mapa,
                "turno": "N/A"  # Turno agora vem do mapa, não do chunk
            }
        }

    def get_players_in_bioma(self, bioma_id: int) -> List[Dict[str, Any]]:
        players_in_bioma = []
        chunks = self.chunk_repository.find_by_bioma(bioma_id)
        players = self.player_repository.find_all()

        for player in players:
            for chunk in chunks:
                if f"Chunk {chunk.id_chunk}" in player.localizacao:
                    players_in_bioma.append({
                        "id": player.id_player,
                        "nome": player.nome,
                        "localizacao": player.localizacao,
                        "vida_atual": player.vida_atual,
                        "nivel": player.nivel
                    })
                    break
        return players_in_bioma

    def get_map_statistics(self) -> Dict[str, Any]:
        mapas = self.mapa_repository.find_all()
        chunks = self.chunk_repository.find_all()
        players = self.player_repository.find_all()

        total_chunks = len(chunks)
        total_players = len(players)
        active_players = len([p for p in players if p.vida_atual > 0])

        chunks_por_turno = {}
        for chunk in chunks:
            # Como não temos mais id_mapa_turno, vamos buscar o turno do mapa
            mapa = next((m for m in mapas if m.id_mapa == chunk.id_mapa), None)
            if mapa:
                turno = mapa.turno.value
                chunks_por_turno[turno] = chunks_por_turno.get(turno, 0) + 1
        return {
            "total_mapas": len(mapas),
            "total_chunks": total_chunks,
            "total_jogadores": total_players,
            "jogadores_ativos": active_players,
            "jogadores_mortos": total_players - active_players,
            "chunks_por_turno": chunks_por_turno
        }

    def create_new_player(self, nome: str, localizacao: str = "Spawn") -> Dict[str, Any]:
        existing = [p for p in self.player_repository.find_all() if p.nome == nome]
        if existing:
            return {"error": "Nome de jogador já existe"}
        
        player = Player(
            id_player=0,  # Será definido pelo repository
            nome=nome,
            vida_maxima=100,
            vida_atual=100,
            forca=10,
            localizacao=localizacao,
            nivel=1,
            experiencia=0
        )
        saved = self.player_repository.save(player)
        return {
            "success": True,
            "player": {
                "id": saved.id_player,
                "nome": saved.nome,
                "vida_atual": saved.vida_atual,
                "vida_maxima": saved.vida_maxima,
                "forca": saved.forca,
                "nivel": saved.nivel,
                "experiencia": saved.experiencia,
                "localizacao": saved.localizacao
            }
        }
