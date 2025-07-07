"""
Testes unitários para a model Fantasma
"""

import pytest
from src.models.fantasma import Fantasma

def test_minerador_minera_com_sucesso():
    fantasma = Fantasma(id=1, chunk="C1", tipo="minerador")
    resultado = fantasma.minerar("madeira")
    assert resultado is not None
    assert "madeira" in resultado
    assert 20 <= resultado["madeira"] <= 30
    assert fantasma.acao_realizada is True

def test_construtor_construcao_totem_sucesso():
    recursos = {"pedra": 15, "carvão": 5, "redstone": 2}
    fantasma = Fantasma(id=2, chunk="C2", tipo="construtor")
    resposta = fantasma.construir("totem", recursos)
    assert "Totem construído" in resposta
    assert recursos["pedra"] == 5
    assert recursos["carvão"] == 2
    assert recursos["redstone"] == 1
    assert fantasma.acao_realizada is True
    assert fantasma.tipo_construcao == "totem"

def test_fantasma_nao_pode_fazer_acao_duas_vezes():
    recursos = {"pedra": 20, "carvão": 5, "redstone": 5}
    fantasma = Fantasma(id=3, chunk="C3", tipo="construtor")
    fantasma.construir("totem", recursos)
    resposta = fantasma.construir("ponte", recursos, destino_chunk="C4")
    assert resposta == "Não pode construir."

def test_minerador_nao_minerador_nao_mina():
    fantasma = Fantasma(id=4, chunk="C4", tipo="construtor")
    resultado = fantasma.minerar("pedra")
    assert resultado is None

def test_repr_to_dict():
    f = Fantasma(id=10, chunk="Z1", tipo="minerador")
    d = f.to_dict()
    assert d["id"] == 10
    assert d["tipo"] == "minerador"
    assert "Fantasma" in repr(f)
