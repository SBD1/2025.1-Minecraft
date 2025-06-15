"""
Service layer que usa repositories para lógica de negócio
Demonstra o uso do Repository Pattern
"""

from typing import List, Optional, Dict, Any
from ..repositories import (
    BiomaRepository,
    ChunkRepository,
    MapaRepository,
    PlayerRepository
)
from ..models.mapa import Mapa, TurnoType
from ..models.player import Player
from ..models.chunk import Chunk


class GameService:
    """
    Service que encapsula a lógica de negócio do jogo
    Usa repositories para acesso a dados
    """
    
    def __init__(self):
        """Inicializa o service com repositories"""
        self.chunk_repository = ChunkRepository()
        self.mapa_repository = MapaRepository()
        self.player_repository = PlayerRepository()
    
    def get_map_info(self, mapa_nome: str, turno: TurnoType) -> Dict[str, Any]:
        """
        Obtém informações completas de um mapa
        
        Args:
            mapa_nome: Nome do mapa
            turno: Turno do mapa
            
        Returns:
            Dicionário com informações do mapa
        """
        # Busca o mapa
        mapa = self.mapa_repository.find_by_id(mapa_nome, turno)
        if not mapa:
            return {"error": "Mapa não encontrado"}
        
        # Busca chunks do mapa
        chunks = self.chunk_repository.find_by_mapa(mapa_nome, turno.value)
        
        # Calcula distribuição de biomas
        bioma_distribution = {}
        for chunk in chunks:
            bioma = chunk.id_bioma
            bioma_distribution[bioma] = bioma_distribution.get(bioma, 0) + 1
        
        return {
            "nome": mapa.nome,
            "turno": mapa.turno.value,
            "total_chunks": len(chunks),
            "distribuicao_biomas": bioma_distribution,
            "chunks": [chunk.numero_chunk for chunk in chunks[:10]]  # Primeiros 10 chunks
        }
    
    def get_player_status(self, player_id: int) -> Dict[str, Any]:
        """
        Obtém status completo de um jogador
        
        Args:
            player_id: ID do jogador
            
        Returns:
            Dicionário com status do jogador
        """
        player = self.player_repository.find_by_id(player_id)
        if not player:
            return {"error": "Jogador não encontrado"}
        
        # Calcula porcentagem de vida
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
        """
        Move um jogador para um chunk específico
        
        Args:
            player_id: ID do jogador
            chunk_id: ID do chunk
            
        Returns:
            Dicionário com resultado da operação
        """
        # Busca jogador
        player = self.player_repository.find_by_id(player_id)
        if not player:
            return {"error": "Jogador não encontrado"}
        
        # Busca chunk
        chunk = self.chunk_repository.find_by_id(chunk_id)
        if not chunk:
            return {"error": "Chunk não encontrado"}
        
        # Atualiza localização do jogador
        player.localizacao = f"{chunk.id_mapa_nome} - Chunk {chunk.numero_chunk}"
        
        # Salva jogador
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
        """
        Busca jogadores que estão em um bioma específico
        
        Args:
            bioma_id: ID do bioma
            
        Returns:
            Lista de jogadores no bioma
        """
        # Busca chunks do bioma
        chunks = self.chunk_repository.find_by_bioma(bioma_id)
        
        # Busca todos os jogadores
        players = self.player_repository.find_all()
        
        # Filtra jogadores que estão em chunks do bioma
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
                    break  # Jogador encontrado, não precisa verificar outros chunks
        
        return players_in_bioma
    
    def get_map_statistics(self) -> Dict[str, Any]:
        """
        Obtém estatísticas gerais dos mapas
        
        Returns:
            Dicionário com estatísticas
        """
        # Busca todos os mapas
        mapas = self.mapa_repository.find_all()
        
        # Busca todos os chunks
        chunks = self.chunk_repository.find_all()
        
        # Busca todos os jogadores
        players = self.player_repository.find_all()
        
        # Calcula estatísticas
        total_chunks = len(chunks)
        total_players = len(players)
        active_players = len([p for p in players if p.vida_atual > 0])
        
        # Distribuição por turno
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
            "chunks_por_turno": chunks_por_turno,
            "mapas": [{"nome": m.nome, "turno": m.turno.value} for m in mapas]
        }
    
    def create_new_player(self, nome: str, localizacao: str = "Spawn") -> Dict[str, Any]:
        """
        Cria um novo jogador
        
        Args:
            nome: Nome do jogador
            localizacao: Localização inicial
            
        Returns:
            Dicionário com resultado da operação
        """
        # Verifica se já existe jogador com esse nome
        existing_player = self.player_repository.find_by_name(nome)
        if existing_player:
            return {"error": f"Já existe um jogador com o nome '{nome}'"}
        
        # Cria novo jogador
        new_player = Player(
            id_jogador=None,  # Será gerado pelo banco
            nome=nome,
            vida_maxima=100,
            vida_atual=100,
            forca=10,
            localizacao=localizacao,
            nivel=1,
            experiencia=0
        )
        
        # Salva jogador
        saved_player = self.player_repository.save(new_player)
        
        return {
            "success": True,
            "message": f"Jogador '{nome}' criado com sucesso",
            "player": {
                "id": saved_player.id_jogador,
                "nome": saved_player.nome,
                "vida_atual": saved_player.vida_atual,
                "vida_maxima": saved_player.vida_maxima,
                "forca": saved_player.forca,
                "localizacao": saved_player.localizacao,
                "nivel": saved_player.nivel,
                "experiencia": saved_player.experiencia
            }
        }


# Exemplo de uso do service
def exemplo_uso_service():
    """Exemplo de como usar o GameService"""
    
    service = GameService()
    
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
    
    return service 