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
    PlayerRepositoryImpl,
    FantasmaRepositoryImpl,
    TotemRepositoryImpl,
    PonteRepositoryImpl
)
from ..models.mapa import Mapa, TurnoType
from ..models.player import Player
from ..models.chunk import Chunk
from ..models.fantasma import Fantasma
from ..models.totem import Totem 
from ..models.ponte import Ponte

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
    def get_players_in_bioma(self, bioma_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_map_statistics(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create_new_player(self, nome: str, localizacao: str = "Spawn") -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_all_totens(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_all_pontes(self) -> List[Dict[str, Any]]:
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
            self.fantasma_repository = FantasmaRepositoryImpl()
            self.totem_repository = TotemRepositoryImpl()  
            self.ponte_repository = PonteRepositoryImpl()
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
            "chunks": [chunk.numero_chunk for chunk in chunks[:10]]
        }

    def get_player_status(self, player_id: int) -> Dict[str, Any]:
        player = self.player_repository.find_by_id(player_id)
        if not player:
            return {"error": "Jogador não encontrado"}
        vida_percentual = (player.vida_atual / player.vida_maxima) * 100 if player.vida_maxima > 0 else 0
        return {
            "id": player.id_jogador,
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
        if not player:
            return {"error": "Jogador não encontrado"}
        chunk = self.chunk_repository.find_by_id(chunk_id)
        if not chunk:
            return {"error": "Chunk não encontrado"}
        player.localizacao = f"{chunk.id_mapa_nome} - Chunk {chunk.numero_chunk}"
        updated_player = self.player_repository.save(player)
        return {
            "success": True,
            "message": f"Jogador {player.nome} movido para {player.localizacao}",
            "player": {
                "id": updated_player.id_jogador,
                "nome": updated_player.nome,
                "localizacao": updated_player.localizacao
            },
            "chunk": {
                "id": chunk.numero_chunk,
                "bioma": chunk.id_bioma,
                "mapa": chunk.id_mapa_nome,
                "turno": chunk.id_mapa_turno
            }
        }

    def get_players_in_bioma(self, bioma_id: str) -> List[Dict[str, Any]]:
        chunks = self.chunk_repository.find_by_bioma(bioma_id)
        players = self.player_repository.find_all()
        players_in_bioma = []
        for player in players:
            for chunk in chunks:
                if f"Chunk {chunk.numero_chunk}" in player.localizacao:
                    players_in_bioma.append({
                        "id": player.id_jogador,
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
            turno = chunk.id_mapa_turno
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
            id_jogador=None,
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
                "id": saved.id_jogador,
                "nome": saved.nome,
                "vida_atual": saved.vida_atual,
                "vida_maxima": saved.vida_maxima,
                "forca": saved.forca,
                "nivel": saved.nivel,
                "experiencia": saved.experiencia,
                "localizacao": saved.localizacao
            }
        }
    
    def get_all_totens(self) -> List[Dict[str, Any]]:
        totens = self.totem_repository.find_all()
        return [
            {
                "id": totem.id_totem,
                "id_jogador": totem.id_jogador,
                "id_chunk": totem.id_chunk,
                "ativo": totem.ativo
            }
            for totem in totens
        ]

    def get_all_pontes(self) -> List[Dict[str, Any]]:
        pontes = self.ponte_repository.find_all()
        return [
            {
                "id": ponte.id_ponte,
                "chunk_origem": ponte.chunk_origem,
                "chunk_destino": ponte.chunk_destino,
                "durabilidade": ponte.durabilidade
            }
            for ponte in pontes
        ]
    
    def get_all_fantasmas(self) -> List[Dict[str, Any]]:
        fantasmas = self.fantasma_repository.find_all()
        return [f.to_dict() for f in fantasmas]

    def realizar_acao_fantasma(self, fantasma_id: int, acao: str, **kwargs) -> Dict[str, Any]:
        fantasma = self.fantasma_repository.find_by_id(fantasma_id)
        if not fantasma:
            return {"error": "Fantasma não encontrado"}

        if fantasma.acao_realizada:
            return {"error": "Fantasma já realizou sua ação"}

        # Minerador
        if fantasma.tipo == "minerador" and acao == "minerar":
            material = kwargs.get("material")
            if not material:
                return {"error": "Material não especificado"}
            resultado = fantasma.minerar(material)
            self.fantasma_repository.save(fantasma)
            return {
                "success": True,
                "acao": "minerar",
                "fantasma_id": fantasma.id,
                "resultado": resultado
            }

        # Construtor
        elif fantasma.tipo == "construtor" and acao == "construir":
            tipo_construcao = kwargs.get("tipo")
            recursos = kwargs.get("recursos")
            destino_chunk = kwargs.get("destino_chunk", None)
            if not tipo_construcao or not recursos:
                return {"error": "Tipo de construção ou recursos ausentes"}
            resposta = fantasma.construir(tipo_construcao, recursos, destino_chunk)
            self.fantasma_repository.save(fantasma)
            return {
                "success": True,
                "acao": "construir",
                "fantasma_id": fantasma.id,
                "resultado": resposta,
                "recursos_atuais": recursos
            }

        return {"error": "Ação ou tipo de fantasma inválido"}


    


# Exemplo de uso do service
def exemplo_uso_service():
    """Exemplo de como usar o GameService"""
    
    service = GameServiceImpl.get_instance()
    
    # 1. Obter informações de um mapa
    mapa_info = service.get_map_info("Mapa_Principal", TurnoType.DIA)
    print(f"Informações do mapa: {mapa_info}")
    
    # 2. Obter estatísticas gerais
    stats = service.get_map_statistics()
    print(f"Estatísticas: {stats}")
    
    # 3. Criar novo jogador
    novo_jogador = service.create_new_player("NovoJogador")
    print(f"Novo jogador: {novo_jogador}")
    
    # 4. Buscar jogadores em um bioma
    if novo_jogador.get("success"):
        player_id = novo_jogador["player"]["id"]
        # Move jogador para um chunk
        move_result = service.move_player_to_chunk(player_id, 1)
        print(f"Movimento: {move_result}")
        
        # Busca jogadores no bioma
        players_in_bioma = service.get_players_in_bioma("Deserto")
        print(f"Jogadores no deserto: {players_in_bioma}")

    # 5. Listar todos os totens
    totens = service.get_all_totens()
    print(f"Totens: {totens}")

    # 6. Listar todas as pontes
    pontes = service.get_all_pontes()
    print(f"Pontes: {pontes}")

     # 7. Listar fantasmas
    fantasmas = service.get_all_fantasmas()
    print(f"Fantasmas: {fantasmas}")

    # 8. Fazer fantasma minerar madeira
    if fantasmas:
        f1 = fantasmas[0]
        if f1["tipo"] == "minerador":
            resultado_mineracao = service.realizar_acao_fantasma(f1["id"], acao="minerar", material="madeira")
            print(f"Ação de mineração: {resultado_mineracao}")

    
    return service 
