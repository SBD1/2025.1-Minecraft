"""
Testes para o padrão Singleton
Verifica se o InterfaceService implementa corretamente o Singleton
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.interface_service import InterfaceService


class TestInterfaceServiceSingleton:
    """Testes para verificar o padrão Singleton"""
    
    def test_singleton_instance(self):
        """Testa se sempre retorna a mesma instância"""
        # Reset da instância para teste limpo
        InterfaceService.reset_instance()
        
        # Criar duas instâncias
        instance1 = InterfaceService()
        instance2 = InterfaceService()
        
        # Verificar se são a mesma instância
        assert instance1 is instance2
        assert id(instance1) == id(instance2)
    
    def test_get_instance_method(self):
        """Testa o método de classe get_instance()"""
        # Reset da instância para teste limpo
        InterfaceService.reset_instance()
        
        # Obter instâncias usando get_instance()
        instance1 = InterfaceService.get_instance()
        instance2 = InterfaceService.get_instance()
        
        # Verificar se são a mesma instância
        assert instance1 is instance2
        assert id(instance1) == id(instance2)
    
    def test_mixed_instantiation(self):
        """Testa se get_instance() e construtor retornam a mesma instância"""
        # Reset da instância para teste limpo
        InterfaceService.reset_instance()
        
        # Criar instância usando construtor
        instance1 = InterfaceService()
        
        # Obter instância usando get_instance()
        instance2 = InterfaceService.get_instance()
        
        # Verificar se são a mesma instância
        assert instance1 is instance2
        assert id(instance1) == id(instance2)
    
    def test_single_initialization(self):
        """Testa se a inicialização acontece apenas uma vez"""
        # Reset da instância para teste limpo
        InterfaceService.reset_instance()
        
        # Mock do GameServiceImpl
        with patch('src.services.interface_service.GameServiceImpl') as mock_game_service:
            mock_instance = Mock()
            mock_game_service.return_value = mock_instance
            
            # Criar primeira instância
            instance1 = InterfaceService()
            
            # Criar segunda instância
            instance2 = InterfaceService()
            
            # Verificar se GameServiceImpl foi chamado apenas uma vez
            assert mock_game_service.call_count == 1
            
            # Verificar se são a mesma instância
            assert instance1 is instance2
            
            # Verificar se o game_service foi criado
            assert hasattr(instance1, 'game_service')
            
            # Criar segunda instância
            instance2 = InterfaceService()
            
            # Verificar se são a mesma instância
            assert instance1 is instance2
            
            # Verificar se o game_service é o mesmo
            assert instance1.game_service is instance2.game_service
    
    def test_reset_instance(self):
        """Testa se reset_instance() funciona corretamente"""
        # Criar primeira instância
        instance1 = InterfaceService()
        
        # Reset da instância
        InterfaceService.reset_instance()
        
        # Criar segunda instância
        instance2 = InterfaceService()
        
        # Verificar se são instâncias diferentes
        assert instance1 is not instance2
        assert id(instance1) != id(instance2)
    
    def test_singleton_with_mocks(self):
        """Testa o Singleton com mocks do GameService"""
        # Reset da instância para teste limpo
        InterfaceService.reset_instance()
        
        # Mock do GameServiceImpl ANTES de instanciar o InterfaceService
        with patch('src.services.interface_service.GameServiceImpl') as mock_game_service:
            mock_instance = Mock()
            mock_game_service.return_value = mock_instance
            
            # Obter instância
            service = InterfaceService.get_instance()
            
            # Verificar se o game_service foi criado
            assert hasattr(service, 'game_service')
            assert service.game_service is mock_instance
            
            # Verificar se o mock foi chamado
            assert mock_game_service.call_count == 1
            
            # Obter instância novamente
            service2 = InterfaceService.get_instance()
            
            # Verificar se é a mesma instância e o mock não foi chamado novamente
            assert service is service2
            assert mock_game_service.call_count == 1
    
    def test_multiple_calls_same_instance(self):
        """Testa se múltiplas chamadas retornam a mesma instância"""
        # Reset da instância para teste limpo
        InterfaceService.reset_instance()
        
        instances = []
        
        # Criar várias instâncias
        for i in range(5):
            instance = InterfaceService.get_instance()
            instances.append(instance)
        
        # Verificar se todas são a mesma instância
        first_instance = instances[0]
        for instance in instances[1:]:
            assert instance is first_instance
            assert id(instance) == id(first_instance)


class TestInterfaceServiceIntegration:
    """Testes de integração com o Singleton"""
    
    def setup_method(self):
        """Setup para cada teste"""
        # Reset da instância para teste limpo
        InterfaceService.reset_instance()
        
        # Mock do GameService
        self.mock_game_service = Mock()
        self.mock_player_repo = Mock()
        self.mock_chunk_repo = Mock()
        self.mock_mapa_repo = Mock()
        
        # Configurar mocks dos repositórios no game_service
        self.mock_game_service.player_repository = self.mock_player_repo
        self.mock_game_service.chunk_repository = self.mock_chunk_repo
        self.mock_game_service.mapa_repository = self.mock_mapa_repo
    
    def test_singleton_persistence_across_calls(self):
        """Testa se o Singleton mantém estado entre chamadas"""
        # Reset da instância para teste limpo
        InterfaceService.reset_instance()
        
        # Mock do GameServiceImpl
        with patch('src.services.interface_service.GameServiceImpl', return_value=self.mock_game_service):
            # Obter primeira instância
            service1 = InterfaceService.get_instance()
            
            # Configurar mock para retornar dados
            from src.models.player import Player
            test_player = Player(
                id_player=1,
                nome="TestPlayer",
                vida_maxima=100,
                vida_atual=100,
                forca=10,
                localizacao="1",
                nivel=1,
                experiencia=0
            )
            self.mock_player_repo.find_by_id.return_value = test_player
            
            # Obter segunda instância
            service2 = InterfaceService.get_instance()
            
            # Verificar se são a mesma instância
            assert service1 is service2
            
            # Usar a segunda instância para buscar jogador
            result = service2.get_player_by_id(1)
            
            # Verificar se os repositórios são os mesmos
            assert result == test_player
            self.mock_player_repo.find_by_id.assert_called_once_with(1)


if __name__ == "__main__":
    pytest.main([__file__]) 
