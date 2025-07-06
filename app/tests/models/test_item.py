"""
Testes unitários para a model Item
"""
import pytest
from src.models.item import Item


class TestItem:
    """Testes para a classe Item"""

    def test_item_creation_with_optional(self):
        """Testa criação de item com atributos opcionais"""
        item = Item(1, "Espada", "Arma", poder=10, durabilidade=100)
        assert item.id_item == 1
        assert item.nome == "Espada"
        assert item.tipo == "Arma"
        assert item.poder == 10
        assert item.durabilidade == 100

    def test_item_creation_without_optional(self):
        """Testa criação de item sem atributos opcionais"""
        item = Item(2, "Poção", "Consumo")
        assert item.id_item == 2
        assert item.poder is None
        assert item.durabilidade is None

    def test_item_equality_and_hash(self):
        """Testa igualdade e hash entre itens"""
        item1 = Item(1, "Espada", "Arma", 10, 100)
        item2 = Item(1, "Espada", "Arma", 10, 100)
        item3 = Item(2, "Arco", "Arma", 8, 50)
        assert item1 == item2
        assert not (item1 != item2)
        assert item1 != item3
        assert hash(item1) == hash(item2)
        assert hash(item1) != hash(item3)

    def test_item_repr(self):
        """Testa representação de string via repr"""
        item = Item(3, "Comida", "Consumo", 0, 5)
        expected = "Item(id_item=3, nome='Comida', tipo='Consumo', poder=0, durabilidade=5)"
        assert repr(item) == expected
