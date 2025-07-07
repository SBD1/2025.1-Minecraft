"""
Testes para ChunkRepositoryImpl
"""
import pytest
from unittest.mock import patch
from src.repositories.chunk_repository import ChunkRepositoryImpl
from src.models.chunk import Chunk


def test_find_all_chunks(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchall.return_value = [
        (1, 1, 1, 0, 0),
        (2, 2, 1, 1, 0)
    ]
    with patch('src.repositories.chunk_repository.connection_db', return_value=mock_conn):
        repo = ChunkRepositoryImpl()
        chunks = repo.find_all()
        mock_cursor.execute.assert_called_once()
        assert chunks == [
            Chunk(1, 1, 1, 0, 0),
            Chunk(2, 2, 1, 1, 0)
        ]


def test_find_chunk_by_id(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchone.return_value = (3, 2, 1, 2, 2)
    with patch('src.repositories.chunk_repository.connection_db', return_value=mock_conn):
        repo = ChunkRepositoryImpl()
        chunk = repo.find_by_id(3)
        mock_cursor.execute.assert_called_once()
        assert chunk == Chunk(3, 2, 1, 2, 2)


def test_save_chunk(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    input_chunk = Chunk(0, 1, 1, 5, 5)
    mock_cursor.fetchone.return_value = (4, 1, 1, 5, 5)
    with patch('src.repositories.chunk_repository.connection_db', return_value=mock_conn):
        repo = ChunkRepositoryImpl()
        saved = repo.save(input_chunk)
        mock_conn.commit.assert_called_once()
        assert saved == Chunk(4, 1, 1, 5, 5)


def test_delete_chunk(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.rowcount = 1
    with patch('src.repositories.chunk_repository.connection_db', return_value=mock_conn):
        repo = ChunkRepositoryImpl()
        deleted = repo.delete(7)
        mock_cursor.execute.assert_called_once_with("DELETE FROM chunk WHERE id_chunk = %s", (7,))
        mock_conn.commit.assert_called_once()
        assert deleted is True


def test_find_by_mapa(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchall.return_value = [
        (1, 1, 1, 0, 0),
        (2, 2, 1, 0, 1)
    ]
    with patch('src.repositories.chunk_repository.connection_db', return_value=mock_conn):
        repo = ChunkRepositoryImpl()
        chunks = repo.find_by_mapa('MapaX', 'Dia')
        mock_cursor.execute.assert_called_once()
        assert chunks == [
            Chunk(1, 1, 1, 0, 0),
            Chunk(2, 2, 1, 0, 1)
        ]


def test_find_by_bioma(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchall.return_value = [
        (5, 3, 2, 4, 4)
    ]
    with patch('src.repositories.chunk_repository.connection_db', return_value=mock_conn):
        repo = ChunkRepositoryImpl()
        chunks = repo.find_by_bioma(3)
        mock_cursor.execute.assert_called_once()
        assert chunks == [Chunk(5, 3, 2, 4, 4)]
