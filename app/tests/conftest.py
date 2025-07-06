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
    # Setup cursor as context manager
    mock_cursor_cm = Mock()
    mock_cursor_cm.__enter__.return_value = mock_cursor
    mock_cursor_cm.__exit__.return_value = None
    mock_conn.cursor.return_value = mock_cursor_cm
    # Setup connection as context manager
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.__exit__.return_value = None
    return mock_conn, mock_cursor

@pytest.fixture
def sample_chunks():
    """Chunks de exemplo para testes"""
    from src.models.chunk import Chunk
    
    return [
        Chunk(1, 1, 1, 0, 0),  # id_chunk, id_bioma, id_mapa, x, y
        Chunk(2, 2, 1, 1, 0),
        Chunk(3, 3, 2, 0, 1),
        Chunk(4, 4, 2, 1, 1),
        Chunk(5, 1, 1, 2, 0),
    ]

@pytest.fixture
def sample_biomas():
    """Biomas de exemplo para testes"""
    from src.models.bioma import Bioma
    
    return [
        Bioma(1, "Deserto", "Bioma árido com pouca vegetação"),
        Bioma(2, "Oceano", "Bioma de água salgada"),
        Bioma(3, "Selva", "Bioma tropical úmido"),
        Bioma(4, "Floresta", "Bioma temperado com muita vegetação"),
    ]

@pytest.fixture
def sample_mapas():
    """Mapas de exemplo para testes"""
    from src.models.mapa import Mapa, TurnoType
    
    return [
        Mapa(1, "Mapa_Principal", TurnoType.DIA),
        Mapa(2, "Mapa_Principal", TurnoType.NOITE),
        Mapa(3, "Mapa_Secundario", TurnoType.DIA),
    ] 
