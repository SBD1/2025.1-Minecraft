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
<<<<<<< HEAD

# Imports adicionais para funcionalidade do mundo
try:
    from ..repositories.mundo_repository import MundoRepositoryImpl
    from ..models.mundo import Mundo
    MUNDO_AVAILABLE = True
except ImportError:
    MUNDO_AVAILABLE = False

=======
from ..models.fantasma import Fantasma
from ..models.totem import Totem 
from ..models.ponte import Ponte
>>>>>>> feature/fantasma

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

<<<<<<< HEAD
    # Métodos adicionais para funcionalidade do mundo
    @abstractmethod
    def get_mundo_estado(self) -> Optional[Dict[str, Any]]:
        """Retorna o estado atual do mundo (turno, ticks)"""
        pass

    @abstractmethod
    def avancar_tempo(self) -> Dict[str, Any]:
        """Avança o tempo do mundo e retorna o novo estado"""
        pass

=======
    @abstractmethod
    def get_all_totens(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_all_pontes(self) -> List[Dict[str, Any]]:
        pass
>>>>>>> feature/fantasma

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
            self.bioma_repository = BiomaRepositoryImpl()
            self.chunk_repository = ChunkRepositoryImpl()
            self.mapa_repository = MapaRepositoryImpl()
            self.player_repository = PlayerRepositoryImpl()
<<<<<<< HEAD
            
            # Inicializa repositório do mundo se disponível
            if MUNDO_AVAILABLE:
                self.mundo_repository = MundoRepositoryImpl()
                self.TEMPO_MAX_TURNO = 20  # Turno dura 20 ações
            else:
                self.mundo_repository = None
                
=======
            self.fantasma_repository = FantasmaRepositoryImpl()
            self.totem_repository = TotemRepositoryImpl()  
            self.ponte_repository = PonteRepositoryImpl()
>>>>>>> feature/fantasma
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

    def create_new_player(self, nome: str, localizacao: str = "1") -> Dict[str, Any]:
        # O chunk 1 é o inicial do deserto (ver docs/database.rst)
        existing = [p for p in self.player_repository.find_all() if p.nome == nome]
        if existing:
            return {"error": "Nome de jogador já existe"}
        
        # Get the chunk to format the location properly
        chunk = self.chunk_repository.find_by_id(1)  # Chunk 1 (Deserto)
        initial_location = f"Mapa {chunk.id_mapa} - Chunk {chunk.id_chunk}" if chunk else "1"
        
        player = Player(
            id_player=0,  # Será definido pelo repository
            nome=nome,
            vida_maxima=100,
            vida_atual=100,
            forca=10,
            localizacao=initial_location,  # Use proper format
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


    

    def get_mundo_estado(self) -> Optional[Dict[str, Any]]:
        """Retorna o estado atual do mundo (turno, ticks)"""
        if not MUNDO_AVAILABLE or not self.mundo_repository:
            return {"error": "Funcionalidade do mundo não disponível"}
        
        mundo = self.mundo_repository.get_estado()
        if not mundo:
            return {"error": "Estado do mundo não encontrado"}
        
        return {
            "turno_atual": mundo.turno_atual,
            "ticks_no_turno": mundo.ticks_no_turno,
            "tempo_max_turno": self.TEMPO_MAX_TURNO,
            "progresso": f"{mundo.ticks_no_turno}/{self.TEMPO_MAX_TURNO}"
        }

    def avancar_tempo(self) -> Dict[str, Any]:
        """Avança o tempo do mundo e retorna o novo estado"""
        if not MUNDO_AVAILABLE or not self.mundo_repository:
            return {"error": "Funcionalidade do mundo não disponível"}
        
        mundo = self.mundo_repository.get_estado()
        if not mundo:
            return {"error": "Estado do mundo não encontrado"}
        
        # Incrementa o contador de tempo
        mundo.ticks_no_turno += 1
        turno_mudou = False

        # Verifica se o tempo do turno acabou
        if mundo.ticks_no_turno >= self.TEMPO_MAX_TURNO:
            turno_mudou = True
            # Muda o turno
            if mundo.turno_atual == 'Dia':
                mundo.turno_atual = 'Noite'
                mensagem = "O sol se pôs. A noite chegou trazendo perigos..."
            else:
                mundo.turno_atual = 'Dia'
                mensagem = "O sol nasce em um novo dia."
            
            # Reseta o contador
            mundo.ticks_no_turno = 0
        else:
            mensagem = f"Tempo avança... ({mundo.ticks_no_turno}/{self.TEMPO_MAX_TURNO})"

        # Salva o novo estado do mundo no banco
        if self.mundo_repository.update_estado(mundo):
            return {
                "success": True,
                "turno_atual": mundo.turno_atual,
                "ticks_no_turno": mundo.ticks_no_turno,
                "turno_mudou": turno_mudou,
                "mensagem": mensagem,
                "progresso": f"{mundo.ticks_no_turno}/{self.TEMPO_MAX_TURNO}"
            }
        else:
            return {"error": "Falha ao atualizar estado do mundo"}

    def _avancar_relogio_mundo(self) -> Optional['Mundo']:
        """
        Método privado para incrementar o tempo automaticamente em ações que consomem tempo.
        É chamado por ações como mover-se.
        """
        if not MUNDO_AVAILABLE or not self.mundo_repository:
            return None
        
        resultado = self.avancar_tempo()
        if resultado.get("success"):
            return self.mundo_repository.get_estado()
        return None
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
