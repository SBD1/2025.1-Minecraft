"""
Testes unitários para a model Ponte
"""

import pytest
from src.models.ponte import Ponte 
from typing import Optional


class TestPonte:

    def test_criacao_completa(self):
        ponte = Ponte(id=1, chunk_origem=100, chunk_destino=200, tipo="pedra", ativa=False)
        
        assert ponte.id == 1
        assert ponte.chunk_origem == 100
        assert ponte.chunk_destino == 200
        assert ponte.tipo == "pedra"
        assert ponte.ativa is False

    def test_valores_padrao(self):
        ponte = Ponte(chunk_origem=5, chunk_destino=10)
        
        assert ponte.id is None
        assert ponte.chunk_origem == 5
        assert ponte.chunk_destino == 10
        assert ponte.tipo == ""
        assert ponte.ativa is True

    def test_repr(self):
        ponte = Ponte(id=3, chunk_origem=1, chunk_destino=2, tipo="madeira", ativa=True)
        texto = repr(ponte)

        assert "Ponte" in texto
        assert "id=3" in texto
        assert "chunk_origem=1" in texto
        assert "tipo='madeira'" in texto
