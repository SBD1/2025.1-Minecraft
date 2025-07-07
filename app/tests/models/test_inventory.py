"""
Testes unitários para a model InventoryEntry
"""
import pytest
from src.models.inventory import InventoryEntry


def test_inventory_entry_creation():
    """Testa criação de entrada de inventário"""
    entry = InventoryEntry(id=1, player_id=10, item_id=20, quantidade=5)
    assert entry.id == 1
    assert entry.player_id == 10
    assert entry.item_id == 20
    assert entry.quantidade == 5


def test_inventory_entry_equality():
    """Testa igualdade entre entradas"""
    entry1 = InventoryEntry(1,1,2,5)
    entry2 = InventoryEntry(1,1,2,5)
    entry3 = InventoryEntry(2,1,2,5)
    assert entry1 == entry2
    assert entry1 != entry3


def test_inventory_entry_repr():
    """Testa representação de string via repr"""
    entry = InventoryEntry(3,2,4,10)
    expected = "InventoryEntry(id=3, player_id=2, item_id=4, quantidade=10)"
    assert repr(entry) == expected
