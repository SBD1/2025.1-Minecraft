"""
Testes para BiomaRepositoryImpl
"""
from unittest.mock import patch
from src.repositories.bioma_repository import BiomaRepositoryImpl
from src.models.bioma import Bioma

def test_find_all_biomas(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchall.return_value = [
        (1, 'Deserto', 'desc1'),
        (2, 'Selva', 'desc2')
    ]
    with patch('src.repositories.bioma_repository.connection_db', return_value=mock_conn):
        repo = BiomaRepositoryImpl()
        biomas = repo.find_all()
        mock_cursor.execute.assert_called_once()
        assert biomas == [Bioma(1, 'Deserto', 'desc1'), Bioma(2, 'Selva', 'desc2')]

def test_find_by_id_bioma(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchone.return_value = (1, 'Deserto', 'descricao')
    with patch('src.repositories.bioma_repository.connection_db', return_value=mock_conn):
        repo = BiomaRepositoryImpl()
        bioma = repo.find_by_id(1)
        mock_cursor.execute.assert_called_once()
        assert bioma == Bioma(1, 'Deserto', 'descricao')

def test_save_bioma(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    input_bioma = Bioma(0, 'Novo', 'nova')
    mock_cursor.fetchone.return_value = (3, 'Novo', 'nova')
    with patch('src.repositories.bioma_repository.connection_db', return_value=mock_conn):
        repo = BiomaRepositoryImpl()
        saved = repo.save(input_bioma)
        mock_conn.commit.assert_called_once()
        assert saved == Bioma(3, 'Novo', 'nova')

def test_delete_bioma(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.rowcount = 1
    with patch('src.repositories.bioma_repository.connection_db', return_value=mock_conn):
        repo = BiomaRepositoryImpl()
        deleted = repo.delete(5)
        mock_cursor.execute.assert_called_once_with('DELETE FROM bioma WHERE id_bioma = %s', (5,))
        mock_conn.commit.assert_called_once()
        assert deleted is True
