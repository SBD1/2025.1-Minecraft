"""
Configuração compartilhada para testes
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def mock_db_connection():
    """Mock para conexão com banco de dados"""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn
    return mock_conn, mock_cursor

@pytest.fixture
def sample_chunks():
    """Chunks de exemplo para testes"""
    from src.models.chunk import Chunk
    
    return [
        Chunk(1, "Deserto", "Mapa_Principal", "Dia"),
        Chunk(2, "Oceano", "Mapa_Principal", "Dia"),
        Chunk(3, "Selva", "Mapa_Principal", "Noite"),
        Chunk(4, "Floresta", "Mapa_Principal", "Noite"),
        Chunk(5, "Deserto", "Mapa_Principal", "Dia"),
    ]

@pytest.fixture
def sample_biomas():
    """Biomas de exemplo para testes"""
    from src.models.bioma import Bioma
    
    return [
        Bioma("Deserto"),
        Bioma("Oceano"),
        Bioma("Selva"),
        Bioma("Floresta"),
    ]

@pytest.fixture
def sample_mapas():
    """Mapas de exemplo para testes"""
    from src.models.mapa import Mapa, TurnoType
    
    return [
        Mapa("Mapa_Principal", TurnoType.DIA),
        Mapa("Mapa_Principal", TurnoType.NOITE),
        Mapa("Mapa_Secundario", TurnoType.DIA),
    ] 