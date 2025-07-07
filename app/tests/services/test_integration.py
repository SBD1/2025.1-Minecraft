"""
Testes de Integração
Testa a integração entre InterfaceService, repositórios e interface
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.interface_service import InterfaceService
from src.models.player import Player
from src.models.chunk import Chunk


class TestInterfaceServiceIntegration:
    """Testes de integração do InterfaceService"""
    
    def setup_method(self):
        """Setup para cada teste"""
        # Reset do singleton para cada teste
        InterfaceService.reset_instance()
        
        # Criar mocks para os repositórios
        self.mock_player_repo = Mock()
        self.mock_chunk_repo = Mock()
        self.mock_mapa_repo = Mock()
        
        # Mock do GameService com repositórios mockados
        self.mock_game_service = Mock()
        self.mock_game_service.player_repository = self.mock_player_repo
        self.mock_game_service.chunk_repository = self.mock_chunk_repo
        self.mock_game_service.mapa_repository = self.mock_mapa_repo
        
        # Patch GameServiceImpl para retornar nosso mock
        with patch('src.services.interface_service.GameServiceImpl', return_value=self.mock_game_service):
            self.interface_service = InterfaceService.get_instance()
    
    def test_create_player_integration(self):
        """Testa a criação de jogador através do InterfaceService"""
        # Arrange
        expected_player = Player(
            id_player=1,
            nome="TestPlayer",
            vida_maxima=100,
            vida_atual=100,
            forca=10,
            localizacao="1",
            nivel=1,
            experiencia=0
        )
        
        # Mock do game_service.create_new_player
        self.mock_game_service.create_new_player.return_value = {
            "success": True,
            "player": expected_player
        }
        
        # Act
        result = self.interface_service.create_player("TestPlayer", 100, 10)
        
        # Assert
        assert result is not None
        assert result.nome == "TestPlayer"
        assert result.vida_maxima == 100
        assert result.forca == 10
        self.mock_game_service.create_new_player.assert_called_once_with("TestPlayer")
    
    def test_create_player_duplicate_name(self):
        """Testa criação de jogador com nome duplicado"""
        # Arrange
        # Mock do game_service.create_new_player retornando erro de nome duplicado
        self.mock_game_service.create_new_player.return_value = {
            "success": False,
            "error": "Nome já existe"
        }
        
        # Act
        result = self.interface_service.create_player("TestPlayer", 100, 10)
        
        # Assert
        assert result is None
        self.mock_game_service.create_new_player.assert_called_once_with("TestPlayer")
    
    def test_move_player_integration(self):
        """Testa o movimento de jogador através do InterfaceService"""
        # Arrange
        # Mock do jogador
        player = Player(
            id_player=1,
            nome="TestPlayer",
            vida_maxima=100,
            vida_atual=100,
            forca=10,
            localizacao="1",
            nivel=1,
            experiencia=0
        )
        
        # Mock do game_service.move_player_to_chunk
        self.mock_game_service.move_player_to_chunk.return_value = {
            "success": True,
            "chunk": {
                "id": 2,
                "mapa": "Mapa_Principal"
            }
        }
        
        # Act
        result = self.interface_service.move_player_to_chunk(player, 2)
        
        # Assert
        assert result is not None
        assert "Mapa Mapa_Principal - Chunk 2" in result.localizacao
        self.mock_game_service.move_player_to_chunk.assert_called_once_with(1, 2)
    
    def test_get_player_statistics_integration(self):
        """Testa a obtenção de estatísticas dos jogadores"""
        # Arrange
        # Mock do game_service.get_map_statistics
        self.mock_game_service.get_map_statistics.return_value = {
            "total_jogadores": 3,
            "jogadores_ativos": 2
        }
        
        # Act
        stats = self.interface_service.get_player_statistics()
        
        # Assert
        assert stats['total'] == 3
        assert stats['active'] == 2
        assert stats['average_level'] == 1  # Valor padrão
        assert stats['average_health'] == 50  # Valor padrão
        self.mock_game_service.get_map_statistics.assert_called_once()


class TestPlayerManagerIntegration:
    """Testes de integração do PlayerManager com InterfaceService"""
    
    def test_player_manager_uses_repository(self):
        """Testa se o PlayerManager usa o repositório corretamente"""
        from src.utils.player_manager import get_all_players
        
        # Arrange - Mock do InterfaceService
        with patch('src.utils.player_manager.InterfaceService') as mock_interface_service:
            mock_instance = Mock()
            mock_interface_service.get_instance.return_value = mock_instance
            
            # Mock para get_all_players
            players = [
                Player(id_player=1, nome="Player1", vida_maxima=100, vida_atual=80, 
                       forca=10, localizacao="1", nivel=2, experiencia=150)
            ]
            mock_instance.get_all_players.return_value = players
            
            # Act
            result = get_all_players()
            
            # Assert
            assert result == players
            mock_instance.get_all_players.assert_called_once()
    
    def test_create_player_validation(self):
        """Testa validação na criação de jogador"""
        from src.utils.player_manager import create_new_player
        
        # Arrange - Mock do InterfaceService
        with patch('src.utils.player_manager.InterfaceService') as mock_interface_service:
            mock_instance = Mock()
            mock_interface_service.get_instance.return_value = mock_instance
            
            # Mock para nome duplicado (retorna None)
            mock_instance.create_player.return_value = None
            
            # Act
            result = create_new_player("TestPlayer", 100, 10)
            
            # Assert
            assert result is None
            mock_instance.create_player.assert_called_once_with("TestPlayer", 100, 10)


class TestRepositoryValidation:
    """Testes de validação dos repositórios"""
    
    def test_player_repository_validation(self):
        """Testa se o repositório de jogadores funciona corretamente"""
        from src.repositories.player_repository import PlayerRepositoryImpl
        
        # Arrange
        repo = PlayerRepositoryImpl()
        
        # Act & Assert - Verifica se os métodos existem
        assert hasattr(repo, 'find_all')
        assert hasattr(repo, 'find_by_id')
        assert hasattr(repo, 'save')
        assert hasattr(repo, 'delete')
        assert hasattr(repo, 'find_by_name')
        assert hasattr(repo, 'find_active_players')


if __name__ == "__main__":
    pytest.main([__file__]) 
