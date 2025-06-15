"""
Testes unitários para a model Chunk
"""
import pytest
from src.models.chunk import Chunk


class TestChunk:
    """Testes para a classe Chunk"""
    
    def test_chunk_creation(self):
        """Testa criação de chunk"""
        chunk = Chunk(1, "Deserto", "Mapa_Principal", "Dia")
        assert chunk.numero_chunk == 1
        assert chunk.id_bioma == "Deserto"
        assert chunk.id_mapa_nome == "Mapa_Principal"
        assert chunk.id_mapa_turno == "Dia"
    
    def test_chunk_string_representation(self):
        """Testa representação string do chunk"""
        chunk = Chunk(1, "Deserto", "Mapa_Principal", "Dia")
        expected_str = "Chunk(1: Deserto (Mapa_Principal - Dia))"
        assert str(chunk) == expected_str
        
        expected_repr = "Chunk(numero_chunk=1, id_bioma='Deserto', id_mapa_nome='Mapa_Principal', id_mapa_turno='Dia')"
        assert repr(chunk) == expected_repr
    
    def test_chunk_equality(self):
        """Testa igualdade entre chunks"""
        chunk1 = Chunk(1, "Deserto", "Mapa_Principal", "Dia")
        chunk2 = Chunk(1, "Selva", "Mapa_Principal", "Noite")  # Mesmo ID
        chunk3 = Chunk(2, "Deserto", "Mapa_Principal", "Dia")  # ID diferente
        
        assert chunk1 == chunk2  # Baseado apenas no numero_chunk
        assert chunk1 != chunk3
        assert chunk1 != "Chunk"  # Tipo diferente
    
    def test_chunk_hash(self):
        """Testa hash do chunk"""
        chunk1 = Chunk(1, "Deserto", "Mapa_Principal", "Dia")
        chunk2 = Chunk(1, "Selva", "Mapa_Principal", "Noite")
        chunk3 = Chunk(2, "Deserto", "Mapa_Principal", "Dia")
        
        assert hash(chunk1) == hash(chunk2)
        assert hash(chunk1) != hash(chunk3)
    
    def test_get_display_name(self):
        """Testa nome para exibição"""
        chunk = Chunk(1, "Deserto", "Mapa_Principal", "Dia")
        assert chunk.get_display_name() == "Deserto (Mapa_Principal - Dia)"
    
    def test_bioma_type_checks(self):
        """Testa verificações de tipo de bioma"""
        chunk_deserto = Chunk(1, "Deserto", "Mapa_Principal", "Dia")
        chunk_selva = Chunk(2, "Selva", "Mapa_Principal", "Dia")
        chunk_floresta = Chunk(3, "Floresta", "Mapa_Principal", "Dia")
        chunk_oceano = Chunk(4, "Oceano", "Mapa_Principal", "Dia")
        
        assert chunk_deserto.is_desert() is True
        assert chunk_selva.is_jungle() is True
        assert chunk_floresta.is_forest() is True
        assert chunk_oceano.is_ocean() is True
        
        # Testes negativos
        assert chunk_deserto.is_jungle() is False
        assert chunk_selva.is_desert() is False
    
    def test_turno_checks(self):
        """Testa verificações de turno"""
        chunk_dia = Chunk(1, "Deserto", "Mapa_Principal", "Dia")
        chunk_noite = Chunk(2, "Selva", "Mapa_Principal", "Noite")
        
        assert chunk_dia.is_day() is True
        assert chunk_noite.is_night() is True
        
        # Testes negativos
        assert chunk_dia.is_night() is False
        assert chunk_noite.is_day() is False
    
    def test_get_adjacent_chunk_ids(self):
        """Testa cálculo de chunks adjacentes"""
        chunk = Chunk(1, "Deserto", "Mapa_Principal", "Dia")
        adjacentes = chunk.get_adjacent_chunk_ids()
        
        # Chunk 1 deve ter adjacentes 2 (direita) e 33 (abaixo)
        assert 2 in adjacentes
        assert 33 in adjacentes
        assert 1 not in adjacentes  # Não deve incluir a si mesmo
    
    def test_get_adjacent_chunk_ids_edge_cases(self):
        """Testa casos extremos para chunks adjacentes"""
        # Chunk no canto superior esquerdo
        chunk_1 = Chunk(1, "Deserto", "Mapa_Principal", "Dia")
        adjacentes_1 = chunk_1.get_adjacent_chunk_ids()
        assert 1 not in adjacentes_1  # Não deve incluir a si mesmo
        assert 2 in adjacentes_1  # Direita
        assert 33 in adjacentes_1  # Abaixo
        
        # Chunk no meio do mapa
        chunk_500 = Chunk(500, "Selva", "Mapa_Principal", "Dia")
        adjacentes_500 = chunk_500.get_adjacent_chunk_ids()
        assert 499 in adjacentes_500  # Esquerda
        assert 501 in adjacentes_500  # Direita
        assert 468 in adjacentes_500  # Abaixo
        assert 532 in adjacentes_500  # Acima
    
    def test_belongs_to_map(self):
        """Testa verificação de pertencimento ao mapa"""
        chunk = Chunk(1, "Deserto", "Mapa_Principal", "Dia")
        
        assert chunk.belongs_to_map("Mapa_Principal", "Dia") is True
        assert chunk.belongs_to_map("Mapa_Principal", "Noite") is False
        assert chunk.belongs_to_map("Mapa_Secundario", "Dia") is False
    
    def test_get_bioma_type(self):
        """Testa obtenção do tipo de bioma"""
        chunk = Chunk(1, "Deserto", "Mapa_Principal", "Dia")
        assert chunk.get_bioma_type() == "Deserto"
    
    def test_get_map_key(self):
        """Testa obtenção da chave do mapa"""
        chunk = Chunk(1, "Deserto", "Mapa_Principal", "Dia")
        assert chunk.get_map_key() == ("Mapa_Principal", "Dia")
    
    def test_multiple_chunks(self, sample_chunks):
        """Testa criação de múltiplos chunks"""
        assert len(sample_chunks) == 5
        assert all(isinstance(chunk, Chunk) for chunk in sample_chunks)
        
        # Verifica que todos têm IDs únicos
        ids = [chunk.numero_chunk for chunk in sample_chunks]
        assert len(set(ids)) == len(ids)  # Todos únicos 
