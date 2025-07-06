"""
Testes para ItemRepositoryImpl
"""
import pytest
from unittest.mock import patch
from src.repositories.item_repository import ItemRepositoryImpl
from src.models.item import Item

def test_find_all_items(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    # Simula retorno do cursor.fetchall
    mock_cursor.fetchall.return_value = [
        (1, 'Espada', 'Arma', 10, 100),
        (2, 'Poção', 'Consumo', None, None)
    ]
    with patch('src.repositories.item_repository.connection_db', return_value=mock_conn):
        repo = ItemRepositoryImpl()
        items = repo.find_all()
        # Verifica execução da query
        mock_cursor.execute.assert_called_once()
        assert items == [
            Item(1, 'Espada', 'Arma', 10, 100),
            Item(2, 'Poção', 'Consumo', None, None)
        ]

def test_find_item_by_id(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchone.return_value = (1, 'Espada', 'Arma', 10, 100)
    with patch('src.repositories.item_repository.connection_db', return_value=mock_conn):
        repo = ItemRepositoryImpl()
        item = repo.find_by_id(1)
        mock_cursor.execute.assert_called_once()
        assert item == Item(1, 'Espada', 'Arma', 10, 100)

def test_save_item(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    # Simula INSERT com conflito (update)
    input_item = Item(0, 'Arco', 'Arma', 8, 50)
    mock_cursor.fetchone.return_value = (3, 'Arco', 'Arma', 8, 50)
    with patch('src.repositories.item_repository.connection_db', return_value=mock_conn):
        repo = ItemRepositoryImpl()
        saved = repo.save(input_item)
        # Verifica commit e retorno correto
        mock_conn.commit.assert_called_once()
        assert saved == Item(3, 'Arco', 'Arma', 8, 50)

def test_delete_item(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.rowcount = 1
    with patch('src.repositories.item_repository.connection_db', return_value=mock_conn):
        repo = ItemRepositoryImpl()
        deleted = repo.delete(5)
        mock_cursor.execute.assert_called_once_with('DELETE FROM item WHERE id_item = %s', (5,))
        mock_conn.commit.assert_called_once()
        assert deleted is True
