"""
Testes unitários para a model Bioma
"""
import pytest
from src.models.bioma import Bioma


class TestBioma:
    """Testes para a classe Bioma"""
    
    def test_bioma_creation(self):
        """Testa criação de bioma"""
        bioma = Bioma("Deserto")
        assert bioma.nome == "Deserto"
    
    def test_bioma_string_representation(self):
        """Testa representação string do bioma"""
        bioma = Bioma("Selva")
        assert str(bioma) == "Bioma(Selva)"
        assert repr(bioma) == "Bioma(nome='Selva')"
    
    def test_bioma_equality(self):
        """Testa igualdade entre biomas"""
        bioma1 = Bioma("Deserto")
        bioma2 = Bioma("Deserto")
        bioma3 = Bioma("Selva")
        
        assert bioma1 == bioma2
        assert bioma1 != bioma3
        assert bioma1 != "Deserto"  # Tipo diferente
    
    def test_bioma_hash(self):
        """Testa hash do bioma"""
        bioma1 = Bioma("Deserto")
        bioma2 = Bioma("Deserto")
        bioma3 = Bioma("Selva")
        
        assert hash(bioma1) == hash(bioma2)
        assert hash(bioma1) != hash(bioma3)
    
    def test_bioma_in_set(self):
        """Testa uso do bioma em conjuntos"""
        bioma1 = Bioma("Deserto")
        bioma2 = Bioma("Deserto")
        bioma3 = Bioma("Selva")
        
        biomas_set = {bioma1, bioma2, bioma3}
        assert len(biomas_set) == 2  # bioma1 e bioma2 são iguais
    
    def test_bioma_in_dict(self):
        """Testa uso do bioma como chave de dicionário"""
        bioma1 = Bioma("Deserto")
        bioma2 = Bioma("Deserto")
        
        biomas_dict = {bioma1: "valor1"}
        assert bioma2 in biomas_dict
        assert biomas_dict[bioma2] == "valor1"
    
    def test_multiple_biomas(self, sample_biomas):
        """Testa criação de múltiplos biomas"""
        assert len(sample_biomas) == 4
        assert all(isinstance(bioma, Bioma) for bioma in sample_biomas)
        
        nomes = [bioma.nome for bioma in sample_biomas]
        assert "Deserto" in nomes
        assert "Oceano" in nomes
        assert "Selva" in nomes
        assert "Floresta" in nomes 