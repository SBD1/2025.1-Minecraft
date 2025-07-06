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
        # Criar mocks para os repositórios
        self.mock_player_repo = Mock()
        self.mock_chunk_repo = Mock()
        self.mock_mapa_repo = Mock()
        
        # Mock do InterfaceService com repositórios mockados
        with patch.object(InterfaceService, '__init__', return_value=None):
            self.interface_service = InterfaceService()
            self.interface_service.player_repository = self.mock_player_repo
            self.interface_service.chunk_repository = self.mock_chunk_repo
            self.interface_service.mapa_repository = self.mock_mapa_repo
    
    def test_create_player_integration(self):
        """Testa a criação de jogador através do InterfaceService"""
        # Arrange
        # Mock do find_by_name retornando None (nome não existe)
        self.mock_player_repo.find_by_name.return_value = None
        
        # Mock do save retornando um jogador criado
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
        self.mock_player_repo.save.return_value = expected_player
        
        # Act
        result = self.interface_service.create_player("TestPlayer", 100, 10)
        
        # Assert
        assert result is not None
        assert result.nome == "TestPlayer"
        assert result.vida_maxima == 100
        assert result.forca == 10
        self.mock_player_repo.find_by_name.assert_called_once_with("TestPlayer")
        self.mock_player_repo.save.assert_called_once()
    
    def test_create_player_duplicate_name(self):
        """Testa criação de jogador com nome duplicado"""
        # Arrange
        # Mock do find_by_name retornando um jogador existente
        existing_player = Player(
            id_player=1,
            nome="TestPlayer",
            vida_maxima=100,
            vida_atual=100,
            forca=10,
            localizacao="1",
            nivel=1,
            experiencia=0
        )
        self.mock_player_repo.find_by_name.return_value = existing_player
        
        # Act
        result = self.interface_service.create_player("TestPlayer", 100, 10)
        
        # Assert
        assert result is None
        self.mock_player_repo.find_by_name.assert_called_once_with("TestPlayer")
        self.mock_player_repo.save.assert_not_called()
    
    def test_move_player_integration(self):
        """Testa o movimento de jogador através do InterfaceService"""
        # Arrange
        # Mock do chunk existente
        chunk = Chunk(
            id_chunk=2,
            id_bioma=1,
            id_mapa=1,
            x=1,
            y=0
        )
        self.mock_chunk_repo.find_by_id.return_value = chunk
        
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
        
        # Mock do save retornando jogador atualizado
        updated_player = Player(
            id_player=1,
            nome="TestPlayer",
            vida_maxima=100,
            vida_atual=100,
            forca=10,
            localizacao="2",  # Localização atualizada
            nivel=1,
            experiencia=0
        )
        self.mock_player_repo.save.return_value = updated_player
        
        # Act
        result = self.interface_service.move_player_to_chunk(player, 2)
        
        # Assert
        assert result is not None
        assert result.localizacao == "2"
        self.mock_chunk_repo.find_by_id.assert_called_once_with(2)
        self.mock_player_repo.save.assert_called_once()
    
    def test_get_player_statistics_integration(self):
        """Testa a obtenção de estatísticas dos jogadores"""
        # Arrange
        # Mock de jogadores
        players = [
            Player(id_player=1, nome="Player1", vida_maxima=100, vida_atual=80, 
                   forca=10, localizacao="1", nivel=2, experiencia=150),
            Player(id_player=2, nome="Player2", vida_maxima=100, vida_atual=100, 
                   forca=12, localizacao="2", nivel=3, experiencia=250),
            Player(id_player=3, nome="Player3", vida_maxima=100, vida_atual=0, 
                   forca=8, localizacao="3", nivel=1, experiencia=50)
        ]
        
        active_players = [players[0], players[1]]  # Apenas os vivos
        
        self.mock_player_repo.find_all.return_value = players
        self.mock_player_repo.find_active_players.return_value = active_players
        
        # Act
        stats = self.interface_service.get_player_statistics()
        
        # Assert
        assert stats['total'] == 3
        assert stats['active'] == 2
        assert stats['average_level'] == 2.0  # (2+3+1)/3
        assert stats['average_health'] == 60.0  # (80+100+0)/3
        self.mock_player_repo.find_all.assert_called_once()
        self.mock_player_repo.find_active_players.assert_called_once()


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
