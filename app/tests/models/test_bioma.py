"""
Testes unitários para a model Bioma
"""
import pytest
from src.models.bioma import Bioma


class TestBioma:
    """Testes para a classe Bioma"""
    
    def test_bioma_creation(self):
        """Testa criação de bioma"""
        bioma = Bioma(1, "Deserto", "Bioma árido")
        assert bioma.id_bioma == 1
        assert bioma.nome == "Deserto"
        assert bioma.descricao == "Bioma árido"
    
    def test_bioma_string_representation(self):
        """Testa representação string do bioma"""
        bioma = Bioma(2, "Selva", "Bioma tropical")
        assert str(bioma) == "Bioma(Selva)"
        assert repr(bioma) == "Bioma(id_bioma=2, nome='Selva', descricao='Bioma tropical')"
    
    def test_bioma_equality(self):
        """Testa igualdade entre biomas"""
        bioma1 = Bioma(1, "Deserto", "Bioma árido")
        bioma2 = Bioma(1, "Deserto", "Bioma árido")
        bioma3 = Bioma(2, "Selva", "Bioma tropical")
        
        assert bioma1 == bioma2
        assert bioma1 != bioma3
        assert bioma1 != "Deserto"  # Tipo diferente
    
    def test_bioma_hash(self):
        """Testa hash do bioma"""
        bioma1 = Bioma(1, "Deserto", "Bioma árido")
        bioma2 = Bioma(1, "Deserto", "Bioma árido")
        bioma3 = Bioma(2, "Selva", "Bioma tropical")
        
        assert hash(bioma1) == hash(bioma2)
        assert hash(bioma1) != hash(bioma3)
    
    def test_bioma_in_set(self):
        """Testa uso do bioma em conjuntos"""
        bioma1 = Bioma(1, "Deserto", "Bioma árido")
        bioma2 = Bioma(1, "Deserto", "Bioma árido")
        bioma3 = Bioma(2, "Selva", "Bioma tropical")
        
        biomas_set = {bioma1, bioma2, bioma3}
        assert len(biomas_set) == 2  # bioma1 e bioma2 são iguais
    
    def test_bioma_in_dict(self):
        """Testa uso do bioma como chave de dicionário"""
        bioma1 = Bioma(1, "Deserto", "Bioma árido")
        bioma2 = Bioma(1, "Deserto", "Bioma árido")
        
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
