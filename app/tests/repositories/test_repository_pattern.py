"""
Testes para o Repository Pattern
Verifica se os repositories estão funcionando corretamente
"""

import pytest
from unittest.mock import Mock, patch
from src.repositories import (
    BiomaRepositoryImpl,
    ChunkRepositoryImpl,
    MapaRepositoryImpl,
    PlayerRepositoryImpl
)
from src.models.mapa import Mapa, TurnoType
from src.models.player import Player
from src.models.chunk import Chunk
from src.services.game_service import GameServiceImpl


class TestRepositoryPattern:
    """Testes para o Repository Pattern"""
    
    def test_chunk_repository_find_by_mapa(self):
        """Testa busca de chunks por mapa usando repository"""
        # Arrange
        mock_chunks = [
            Chunk(1, "Deserto", "Mapa_Principal", "Dia"),
            Chunk(2, "Oceano", "Mapa_Principal", "Dia"),
            Chunk(3, "Deserto", "Mapa_Principal", "Dia"),
        ]
        
        # Mock do repository
        with patch.object(ChunkRepositoryImpl, 'find_by_mapa', return_value=mock_chunks):
            repo = ChunkRepositoryImpl()
            
            # Act
            chunks = repo.find_by_mapa("Mapa_Principal", "Dia")
            
            # Assert
            assert len(chunks) == 3
            assert chunks[0].id_bioma == "Deserto"
            assert chunks[1].id_bioma == "Oceano"
            assert chunks[2].id_bioma == "Deserto"
    
    def test_mapa_repository_find_by_turno(self):
        """Testa busca de mapas por turno usando repository"""
        # Arrange
        mock_mapas = [
            Mapa("Mapa_Principal", TurnoType.DIA),
            Mapa("Mapa_Secundario", TurnoType.DIA),
        ]
        
        # Mock do repository
        with patch.object(MapaRepositoryImpl, 'find_by_turno', return_value=mock_mapas):
            repo = MapaRepositoryImpl()
            
            # Act
            mapas = repo.find_by_turno(TurnoType.DIA)
            
            # Assert
            assert len(mapas) == 2
            assert all(mapa.turno == TurnoType.DIA for mapa in mapas)
            assert mapas[0].nome == "Mapa_Principal"
            assert mapas[1].nome == "Mapa_Secundario"
    
    def test_player_repository_find_active_players(self):
        """Testa busca de jogadores ativos usando repository"""
        # Arrange
        mock_players = [
            Player(1, "Jogador1", 100, 50, 10, "Spawn", 1, 0),  # Vivo
            Player(2, "Jogador2", 100, 0, 10, "Spawn", 1, 0),   # Morto
            Player(3, "Jogador3", 100, 75, 10, "Spawn", 1, 0),  # Vivo
        ]
        
        # Mock do repository
        with patch.object(PlayerRepositoryImpl, 'find_active_players', return_value=[mock_players[0], mock_players[2]]):
            repo = PlayerRepositoryImpl()
            
            # Act
            active_players = repo.find_active_players()
            
            # Assert
            assert len(active_players) == 2
            assert all(player.vida_atual > 0 for player in active_players)
            assert active_players[0].nome == "Jogador1"
            assert active_players[1].nome == "Jogador3"
    
    def test_game_service_get_map_info(self):
        """Testa service usando repositories"""
        # Arrange
        mock_mapa = Mapa("Mapa_Principal", TurnoType.DIA)
        mock_chunks = [
            Chunk(1, "Deserto", "Mapa_Principal", "Dia"),
            Chunk(2, "Oceano", "Mapa_Principal", "Dia"),
            Chunk(3, "Deserto", "Mapa_Principal", "Dia"),
        ]
        
        # Mock dos repositories
        with patch.object(MapaRepositoryImpl, 'find_by_id', return_value=mock_mapa), \
             patch.object(ChunkRepositoryImpl, 'find_by_mapa', return_value=mock_chunks):
            
            service = GameServiceImpl()
            
            # Act
            info = service.get_map_info("Mapa_Principal", TurnoType.DIA)
            
            # Assert
            assert info["nome"] == "Mapa_Principal"
            assert info["turno"] == "Dia"
            assert info["total_chunks"] == 3
            assert info["distribuicao_biomas"]["Deserto"] == 2
            assert info["distribuicao_biomas"]["Oceano"] == 1
    
    def test_game_service_create_new_player(self):
        """Testa criação de novo jogador via service"""
        # Arrange
        mock_saved_player = Player(1, "NovoJogador", 100, 100, 10, "Spawn", 1, 0)
        
        # Mock dos repositories
        with patch.object(PlayerRepositoryImpl, 'find_all', return_value=[]), \
             patch.object(PlayerRepositoryImpl, 'save', return_value=mock_saved_player):
            
            service = GameServiceImpl()
            
            # Act
            result = service.create_new_player("NovoJogador")
            
            # Assert
            assert result["success"] is True
            assert result["player"]["nome"] == "NovoJogador"
            assert result["player"]["vida_atual"] == 100
            assert result["player"]["nivel"] == 1
    
    def test_game_service_create_player_duplicate_name(self):
        """Testa criação de jogador com nome duplicado"""
        # Arrange
        existing_player = Player(1, "JogadorExistente", 100, 100, 10, "Spawn", 1, 0)
        
        # Mock do repository
        with patch.object(PlayerRepositoryImpl, 'find_all', return_value=[existing_player]):
            service = GameServiceImpl()
            
            # Act
            result = service.create_new_player("JogadorExistente")
            
            # Assert
            assert "error" in result
            assert "Nome de jogador já existe" in result["error"]
    
    def test_game_service_move_player_to_chunk(self):
        """Testa movimento de jogador para chunk"""
        # Arrange
        mock_player = Player(1, "Jogador", 100, 100, 10, "Spawn", 1, 0)
        mock_chunk = Chunk(5, "Deserto", "Mapa_Principal", "Dia")
        mock_updated_player = Player(1, "Jogador", 100, 100, 10, "Mapa_Principal - Chunk 5", 1, 0)
        
        # Mock dos repositories
        with patch.object(PlayerRepositoryImpl, 'find_by_id', return_value=mock_player), \
             patch.object(ChunkRepositoryImpl, 'find_by_id', return_value=mock_chunk), \
             patch.object(PlayerRepositoryImpl, 'save', return_value=mock_updated_player):
            
            service = GameServiceImpl()
            
            # Act
            result = service.move_player_to_chunk(1, 5)
            
            # Assert
            assert result["success"] is True
            assert "movido para" in result["message"]
            assert result["player"]["localizacao"] == "Mapa_Principal - Chunk 5"
            assert result["chunk"]["id"] == 5
            assert result["chunk"]["bioma"] == "Deserto"
    
    def test_game_service_get_map_statistics(self):
        """Testa obtenção de estatísticas dos mapas"""
        # Arrange
        mock_mapas = [
            Mapa("Mapa_Principal", TurnoType.DIA),
            Mapa("Mapa_Principal", TurnoType.NOITE),
        ]
        mock_chunks = [
            Chunk(1, "Deserto", "Mapa_Principal", "Dia"),
            Chunk(2, "Oceano", "Mapa_Principal", "Dia"),
            Chunk(3, "Deserto", "Mapa_Principal", "Noite"),
        ]
        mock_players = [
            Player(1, "Jogador1", 100, 50, 10, "Spawn", 1, 0),  # Vivo
            Player(2, "Jogador2", 100, 0, 10, "Spawn", 1, 0),   # Morto
        ]
        
        # Mock dos repositories
        with patch.object(MapaRepositoryImpl, 'find_all', return_value=mock_mapas), \
             patch.object(ChunkRepositoryImpl, 'find_all', return_value=mock_chunks), \
             patch.object(PlayerRepositoryImpl, 'find_all', return_value=mock_players):
            
            service = GameServiceImpl()
            
            # Act
            stats = service.get_map_statistics()
            
            # Assert
            assert stats["total_mapas"] == 2
            assert stats["total_chunks"] == 3
            assert stats["total_jogadores"] == 2
            assert stats["jogadores_ativos"] == 1
            assert stats["jogadores_mortos"] == 1
            assert stats["chunks_por_turno"]["Dia"] == 2
            assert stats["chunks_por_turno"]["Noite"] == 1
    
    def test_repository_interface_compliance(self):
        """Testa se as implementações seguem a interface"""
        # Arrange & Act
        chunk_repo = ChunkRepositoryImpl()
        mapa_repo = MapaRepositoryImpl()
        player_repo = PlayerRepositoryImpl()
        
        # Assert - Verifica se os métodos existem
        assert hasattr(chunk_repo, 'find_all')
        assert hasattr(chunk_repo, 'find_by_id')
        assert hasattr(chunk_repo, 'save')
        assert hasattr(chunk_repo, 'delete')
        assert hasattr(chunk_repo, 'find_by_mapa')
        assert hasattr(chunk_repo, 'find_by_bioma')
        
        assert hasattr(mapa_repo, 'find_all')
        assert hasattr(mapa_repo, 'find_by_id')
        assert hasattr(mapa_repo, 'save')
        assert hasattr(mapa_repo, 'delete')
        assert hasattr(mapa_repo, 'find_by_turno')
        
        assert hasattr(player_repo, 'find_all')
        assert hasattr(player_repo, 'find_by_id')
        assert hasattr(player_repo, 'save')
        assert hasattr(player_repo, 'delete')
        assert hasattr(player_repo, 'find_by_name')
        assert hasattr(player_repo, 'find_active_players') 
