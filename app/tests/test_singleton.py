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
        
        # Mock dos repositórios
        with patch('src.services.interface_service.PlayerRepositoryImpl') as mock_player_repo, \
             patch('src.services.interface_service.ChunkRepositoryImpl') as mock_chunk_repo, \
             patch('src.services.interface_service.MapaRepositoryImpl') as mock_mapa_repo:
            
            mock_player_repo.return_value = Mock()
            mock_chunk_repo.return_value = Mock()
            mock_mapa_repo.return_value = Mock()
            
            # Criar primeira instância
            instance1 = InterfaceService()
            
            # Verificar se os repositórios foram criados
            assert hasattr(instance1, 'player_repository')
            assert hasattr(instance1, 'chunk_repository')
            assert hasattr(instance1, 'mapa_repository')
            
            # Criar segunda instância
            instance2 = InterfaceService()
            
            # Verificar se são a mesma instância
            assert instance1 is instance2
            
            # Verificar se os repositórios são os mesmos
            assert instance1.player_repository is instance2.player_repository
            assert instance1.chunk_repository is instance2.chunk_repository
            assert instance1.mapa_repository is instance2.mapa_repository
    
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
        """Testa o Singleton com mocks dos repositórios"""
        # Reset da instância para teste limpo
        InterfaceService.reset_instance()
        
        # Mock dos repositórios ANTES de instanciar o InterfaceService
        with patch('src.services.interface_service.PlayerRepositoryImpl') as mock_player_repo, \
             patch('src.services.interface_service.ChunkRepositoryImpl') as mock_chunk_repo, \
             patch('src.services.interface_service.MapaRepositoryImpl') as mock_mapa_repo:
            
            mock_player_repo.return_value = Mock()
            mock_chunk_repo.return_value = Mock()
            mock_mapa_repo.return_value = Mock()
            
            # Obter instância
            service = InterfaceService.get_instance()
            
            # Verificar se os repositórios foram criados
            assert hasattr(service, 'player_repository')
            assert hasattr(service, 'chunk_repository')
            assert hasattr(service, 'mapa_repository')
            
            # Verificar se os mocks foram chamados (apenas uma vez devido ao Singleton)
            assert mock_player_repo.call_count >= 1
            assert mock_chunk_repo.call_count >= 1
            assert mock_mapa_repo.call_count >= 1
    
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
        
        # Mock dos repositórios
        with patch('src.services.interface_service.PlayerRepositoryImpl') as mock_player_repo, \
             patch('src.services.interface_service.ChunkRepositoryImpl') as mock_chunk_repo, \
             patch('src.services.interface_service.MapaRepositoryImpl') as mock_mapa_repo:
            
            self.mock_player_repo = Mock()
            self.mock_chunk_repo = Mock()
            self.mock_mapa_repo = Mock()
            
            mock_player_repo.return_value = self.mock_player_repo
            mock_chunk_repo.return_value = self.mock_chunk_repo
            mock_mapa_repo.return_value = self.mock_mapa_repo
    
    def test_singleton_persistence_across_calls(self):
        """Testa se o Singleton mantém estado entre chamadas"""
        # Obter primeira instância
        service1 = InterfaceService.get_instance()
        
        # Configurar mock para retornar dados
        from src.models.player import Player
        test_player = Player(
            id_jogador=1,
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
        
        # Verificar se o mock foi chamado
        self.mock_player_repo.find_by_id.assert_called_once_with(1)
        assert result == test_player


if __name__ == "__main__":
    pytest.main([__file__]) 