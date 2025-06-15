"""
Testes unitários para a model Mapa
"""
import pytest
from unittest.mock import patch, Mock
from src.models.mapa import Mapa, TurnoType
from src.models.chunk import Chunk


class TestMapa:
    """Testes para a classe Mapa"""
    
    def test_mapa_creation(self):
        """Testa criação de mapa"""
        mapa = Mapa("Mapa_Principal", TurnoType.DIA)
        assert mapa.nome == "Mapa_Principal"
        assert mapa.turno == TurnoType.DIA
    
    def test_mapa_creation_with_string(self):
        """Testa criação de mapa com string para turno"""
        mapa = Mapa("Mapa_Principal", "Dia")
        assert mapa.nome == "Mapa_Principal"
        assert mapa.turno == TurnoType.DIA
    
    def test_mapa_string_representation(self):
        """Testa representação string do mapa"""
        mapa = Mapa("Mapa_Principal", TurnoType.DIA)
        
        # Mock do repository
        mock_repo = Mock()
        mock_chunks = [Chunk(i, "Deserto", "Mapa_Principal", "Dia") for i in range(1, 1001)]
        mock_repo.find_by_mapa.return_value = mock_chunks
        mapa.set_chunk_repository(mock_repo)
        
        assert str(mapa) == "Mapa(Mapa_Principal - Dia, 1000 chunks)"
        assert repr(mapa) == "Mapa(nome='Mapa_Principal', turno=TurnoType.DIA)"
    
    def test_mapa_equality(self):
        """Testa igualdade entre mapas"""
        mapa1 = Mapa("Mapa_Principal", TurnoType.DIA)
        mapa2 = Mapa("Mapa_Principal", TurnoType.DIA)
        mapa3 = Mapa("Mapa_Principal", TurnoType.NOITE)
        
        assert mapa1 == mapa2
        assert mapa1 != mapa3
        assert mapa1 != "Mapa"  # Tipo diferente
    
    def test_mapa_hash(self):
        """Testa hash do mapa"""
        mapa1 = Mapa("Mapa_Principal", TurnoType.DIA)
        mapa2 = Mapa("Mapa_Principal", TurnoType.DIA)
        mapa3 = Mapa("Mapa_Principal", TurnoType.NOITE)
        
        assert hash(mapa1) == hash(mapa2)
        assert hash(mapa1) != hash(mapa3)
    
    def test_turno_checks(self):
        """Testa verificações de turno"""
        mapa_dia = Mapa("Mapa_Principal", TurnoType.DIA)
        mapa_noite = Mapa("Mapa_Principal", TurnoType.NOITE)
        
        assert mapa_dia.is_day_map() is True
        assert mapa_noite.is_night_map() is True
        
        # Testes negativos
        assert mapa_dia.is_night_map() is False
        assert mapa_noite.is_day_map() is False
    
    def test_get_display_info_empty(self):
        """Testa informações de exibição sem chunks"""
        mapa = Mapa("Mapa_Principal", TurnoType.DIA)
        
        # Mock do repository
        mock_repo = Mock()
        mock_chunks = [Chunk(i, "Deserto", "Mapa_Principal", "Dia") for i in range(1, 1001)]
        mock_repo.find_by_mapa.return_value = mock_chunks
        mapa.set_chunk_repository(mock_repo)
        
        info = mapa.get_display_info()
        assert info['nome'] == "Mapa_Principal"
        assert info['turno'] == "Dia"
        assert info['tipo'] == "Dia"
        assert info['total_chunks'] == 1000
        assert 'distribuicao' in info
    
    def test_get_display_info_with_chunks(self):
        """Testa informações de exibição com chunks"""
        mapa = Mapa("Mapa_Principal", TurnoType.DIA)
        
        # Mock do repository
        mock_repo = Mock()
        chunks = [
            Chunk(1, "Deserto", "Mapa_Principal", "Dia"),
            Chunk(2, "Oceano", "Mapa_Principal", "Dia"),
            Chunk(3, "Deserto", "Mapa_Principal", "Dia"),
        ]
        mock_repo.find_by_mapa.return_value = chunks
        mapa.set_chunk_repository(mock_repo)
        
        info = mapa.get_display_info()
        
        assert info['nome'] == "Mapa_Principal"
        assert info['turno'] == "Dia"
        assert info['tipo'] == "Dia"
        assert info['total_chunks'] == 3
        assert info['distribuicao'] == {'Deserto': 2, 'Oceano': 1}
    
    def test_get_chunks_by_bioma(self):
        """Testa busca de chunks por bioma"""
        mapa = Mapa("Mapa_Principal", TurnoType.DIA)
        
        # Mock do repository
        mock_repo = Mock()
        chunks = [
            Chunk(1, "Deserto", "Mapa_Principal", "Dia"),
            Chunk(2, "Oceano", "Mapa_Principal", "Dia"),
            Chunk(3, "Deserto", "Mapa_Principal", "Dia"),
        ]
        mock_repo.find_by_mapa.return_value = chunks
        mapa.set_chunk_repository(mock_repo)
        
        chunks_deserto = mapa.get_chunks_by_bioma("Deserto")
        chunks_oceano = mapa.get_chunks_by_bioma("Oceano")
        chunks_selva = mapa.get_chunks_by_bioma("Selva")
        
        assert len(chunks_deserto) == 2
        assert len(chunks_oceano) == 1
        assert len(chunks_selva) == 0
        
        # Verifica case insensitive
        chunks_deserto_upper = mapa.get_chunks_by_bioma("DESERTO")
        assert len(chunks_deserto_upper) == 2
    
    def test_get_bioma_distribution(self):
        """Testa distribuição de biomas"""
        mapa = Mapa("Mapa_Principal", TurnoType.DIA)
        
        # Mock do repository
        mock_repo = Mock()
        chunks = [
            Chunk(1, "Deserto", "Mapa_Principal", "Dia"),
            Chunk(2, "Oceano", "Mapa_Principal", "Dia"),
            Chunk(3, "Deserto", "Mapa_Principal", "Dia"),
            Chunk(4, "Selva", "Mapa_Principal", "Dia"),
        ]
        mock_repo.find_by_mapa.return_value = chunks
        mapa.set_chunk_repository(mock_repo)
        
        distribuicao = mapa.get_bioma_distribution()
        
        assert distribuicao['Deserto'] == 2
        assert distribuicao['Oceano'] == 1
        assert distribuicao['Selva'] == 1
    
    def test_get_bioma_distribution_empty(self):
        """Testa distribuição de biomas sem chunks"""
        mapa = Mapa("Mapa_Principal", TurnoType.DIA)
        
        # Mock do repository
        mock_repo = Mock()
        mock_repo.find_by_mapa.return_value = []
        mapa.set_chunk_repository(mock_repo)
        
        distribuicao = mapa.get_bioma_distribution()
        assert distribuicao == {}
    
    def test_get_chunk_by_id(self):
        """Testa busca de chunk por ID"""
        mapa = Mapa("Mapa_Principal", TurnoType.DIA)
        
        # Mock do repository
        mock_repo = Mock()
        chunks = [
            Chunk(1, "Deserto", "Mapa_Principal", "Dia"),
            Chunk(2, "Oceano", "Mapa_Principal", "Dia"),
        ]
        mock_repo.find_by_mapa.return_value = chunks
        mapa.set_chunk_repository(mock_repo)
        
        chunk_encontrado = mapa.get_chunk_by_id(1)
        chunk_nao_encontrado = mapa.get_chunk_by_id(999)
        
        assert chunk_encontrado is not None
        assert chunk_encontrado.numero_chunk == 1
        assert chunk_nao_encontrado is None
    
    def test_get_chunk_by_id_empty(self):
        """Testa busca de chunk por ID sem chunks"""
        mapa = Mapa("Mapa_Principal", TurnoType.DIA)
        
        # Mock do repository
        mock_repo = Mock()
        mock_repo.find_by_mapa.return_value = []
        mapa.set_chunk_repository(mock_repo)
        
        chunk = mapa.get_chunk_by_id(1)
        assert chunk is None
    
    def test_multiple_mapas(self, sample_mapas):
        """Testa criação de múltiplos mapas"""
        assert len(sample_mapas) == 3
        assert all(isinstance(mapa, Mapa) for mapa in sample_mapas)
        
        # Verifica que os mapas são diferentes
        assert sample_mapas[0] != sample_mapas[1]  # Diferentes turnos
        assert sample_mapas[0] != sample_mapas[2]  # Diferentes nomes
    
    def test_repository_not_configured_error(self):
        """Testa erro quando repository não está configurado"""
        mapa = Mapa("Mapa_Principal", TurnoType.DIA)
        
        # Testa métodos que requerem repository
        with pytest.raises(ValueError, match="Chunk repository não foi configurado"):
            mapa.get_chunks()
        
        with pytest.raises(ValueError, match="Chunk repository não foi configurado"):
            mapa.get_display_info()
        
        with pytest.raises(ValueError, match="Chunk repository não foi configurado"):
            mapa.get_chunks_by_bioma("Deserto")
        
        with pytest.raises(ValueError, match="Chunk repository não foi configurado"):
            mapa.get_bioma_distribution()
        
        with pytest.raises(ValueError, match="Chunk repository não foi configurado"):
            mapa.get_chunk_by_id(1) 
