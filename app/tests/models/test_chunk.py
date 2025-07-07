"""
Testes unitários para a model Chunk
"""
import pytest
from src.models.chunk import Chunk


class TestChunk:
    """Testes para a classe Chunk"""
    
    def test_chunk_creation(self):
        """Testa criação de chunk"""
        chunk = Chunk(1, 1, 1, 0, 0)  # id_chunk, id_bioma, id_mapa, x, y
        assert chunk.id_chunk == 1
        assert chunk.id_bioma == 1
        assert chunk.id_mapa == 1
        assert chunk.x == 0
        assert chunk.y == 0
    
    def test_chunk_string_representation(self):
        """Testa representação string do chunk"""
        chunk = Chunk(1, 1, 1, 0, 0)
        expected_str = "Chunk(1: 1 (1 - 0, 0))"
        assert str(chunk) == expected_str
        
        expected_repr = "Chunk(id_chunk=1, id_bioma=1, id_mapa=1, x=0, y=0)"
        assert repr(chunk) == expected_repr
    
    def test_chunk_equality(self):
        """Testa igualdade entre chunks"""
        chunk1 = Chunk(1, 1, 1, 0, 0)
        chunk2 = Chunk(1, 2, 2, 1, 1)  # Mesmo ID
        chunk3 = Chunk(2, 1, 1, 0, 0)  # ID diferente
        
        assert chunk1 == chunk2  # Baseado apenas no id_chunk
        assert chunk1 != chunk3
        assert chunk1 != "Chunk"  # Tipo diferente
    
    def test_chunk_hash(self):
        """Testa hash do chunk"""
        chunk1 = Chunk(1, 1, 1, 0, 0)
        chunk2 = Chunk(1, 2, 2, 1, 1)
        chunk3 = Chunk(2, 1, 1, 0, 0)
        
        assert hash(chunk1) == hash(chunk2)
        assert hash(chunk1) != hash(chunk3)
    
    def test_get_display_name(self):
        """Testa nome para exibição"""
        chunk = Chunk(1, 1, 1, 0, 0)
        assert chunk.get_display_name() == "1 (1 - 0, 0)"
    
    def test_bioma_type_checks(self):
        """Testa verificações de tipo de bioma"""
        chunk_deserto = Chunk(1, 1, 1, 0, 0)  # id_bioma=1
        chunk_selva = Chunk(2, 2, 1, 1, 0)    # id_bioma=2
        chunk_floresta = Chunk(3, 3, 1, 2, 0) # id_bioma=3
        chunk_oceano = Chunk(4, 4, 1, 3, 0)   # id_bioma=4
        
        # Como agora id_bioma é inteiro, os métodos is_desert() etc. 
        # precisam ser adaptados ou removidos do teste
        # Por enquanto, testamos apenas o get_bioma_type
        assert chunk_deserto.get_bioma_type() == 1
        assert chunk_selva.get_bioma_type() == 2
        assert chunk_floresta.get_bioma_type() == 3
        assert chunk_oceano.get_bioma_type() == 4
    
    def test_turno_checks(self):
        """Testa verificações de turno"""
        chunk_dia = Chunk(1, 1, 1, 0, 0)    # x=0 (par)
        chunk_noite = Chunk(2, 2, 1, 1, 0)  # x=1 (ímpar)
        
        assert chunk_dia.is_day() is True
        assert chunk_noite.is_night() is True
        
        # Testes negativos
        assert chunk_dia.is_night() is False
        assert chunk_noite.is_day() is False
    
    def test_get_adjacent_chunk_ids(self):
        """Testa cálculo de chunks adjacentes"""
        chunk = Chunk(1, 1, 1, 0, 0)
        adjacentes = chunk.get_adjacent_chunk_ids()
        
        # Chunk 1 deve ter adjacentes baseados na nova lógica
        assert 2 in adjacentes
        assert 33 in adjacentes
        assert 1 not in adjacentes  # Não deve incluir a si mesmo
    
    def test_get_adjacent_chunk_ids_edge_cases(self):
        """Testa casos extremos para chunks adjacentes"""
        # Chunk no canto superior esquerdo
        chunk_1 = Chunk(1, 1, 1, 0, 0)
        adjacentes_1 = chunk_1.get_adjacent_chunk_ids()
        assert 1 not in adjacentes_1  # Não deve incluir a si mesmo
        assert 2 in adjacentes_1  # Direita
        assert 33 in adjacentes_1  # Abaixo
        
        # Chunk no meio do mapa
        chunk_500 = Chunk(500, 1, 1, 15, 15)
        adjacentes_500 = chunk_500.get_adjacent_chunk_ids()
        assert 499 in adjacentes_500  # Esquerda
        assert 501 in adjacentes_500  # Direita
        assert 468 in adjacentes_500  # Abaixo
        assert 532 in adjacentes_500  # Acima
    
    def test_belongs_to_map(self):
        """Testa verificação de pertencimento ao mapa"""
        chunk = Chunk(1, 1, 1, 0, 0)  # id_mapa=1, x=0
        
        # Como a função foi alterada para usar id_mapa inteiro e x como segundo parâmetro
        assert chunk.belongs_to_map(1, 0) is True
        assert chunk.belongs_to_map(1, 1) is False
        assert chunk.belongs_to_map(2, 0) is False
    
    def test_get_bioma_type(self):
        """Testa obtenção do tipo de bioma"""
        chunk = Chunk(1, 1, 1, 0, 0)
        assert chunk.get_bioma_type() == 1
    
    def test_get_map_key(self):
        """Testa obtenção da chave do mapa"""
        chunk = Chunk(1, 1, 1, 0, 0)
        assert chunk.get_map_key() == (1, 0)  # (id_mapa, x)
    
    def test_multiple_chunks(self, sample_chunks):
        """Testa criação de múltiplos chunks"""
        assert len(sample_chunks) == 5
        assert all(isinstance(chunk, Chunk) for chunk in sample_chunks)
        
        # Verifica que todos têm IDs únicos
        ids = [chunk.id_chunk for chunk in sample_chunks]
        assert len(set(ids)) == len(ids)  # Todos únicos 
