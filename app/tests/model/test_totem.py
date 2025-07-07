"""
Testes unitários para a model Totem
"""

import pytest
from src.models.totem import Totem  
from typing import Optional


class TestTotem:

    def test_criacao_completa(self):
        totem = Totem(id=1, nome="Totem do Sul", localizacao=101, tipo="ancestral", ativo=False)
        
        assert totem.id == 1
        assert totem.nome == "Totem do Sul"
        assert totem.localizacao == 101
        assert totem.tipo == "ancestral"
        assert totem.ativo is False

    def test_valores_padrao(self):
        totem = Totem(nome="Totem Norte", localizacao=55)
        
        assert totem.id is None
        assert totem.nome == "Totem Norte"
        assert totem.localizacao == 55
        assert totem.tipo == ""
        assert totem.ativo is True

    def test_repr(self):
        totem = Totem(id=9, nome="Guardião", localizacao=77, tipo="protetor", ativo=True)
        texto = repr(totem)

        assert "Totem" in texto
        assert "id=9" in texto
        assert "nome='Guardião'" in texto
        assert "ativo=True" in texto
