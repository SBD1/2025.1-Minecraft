"""
Testes para MapaRepositoryImpl
"""
from unittest.mock import patch
from src.repositories.mapa_repository import MapaRepositoryImpl
from src.models.mapa import Mapa, TurnoType


def test_find_all_mapas(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchall.return_value = [
        (1, 'Mapa1', 'Dia'),
        (2, 'Mapa2', 'Noite')
    ]
    with patch('src.repositories.mapa_repository.connection_db', return_value=mock_conn):
        repo = MapaRepositoryImpl()
        mapas = repo.find_all()
        mock_cursor.execute.assert_called_once()
        assert mapas == [
            Mapa(1, 'Mapa1', TurnoType.DIA),
            Mapa(2, 'Mapa2', TurnoType.NOITE)
        ]


def test_find_by_id_mapa(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchone.return_value = (3, 'MapaX', 'Noite')
    with patch('src.repositories.mapa_repository.connection_db', return_value=mock_conn):
        repo = MapaRepositoryImpl()
        mapa = repo.find_by_id('MapaX', TurnoType.NOITE)
        mock_cursor.execute.assert_called_once()
        assert mapa == Mapa(3, 'MapaX', TurnoType.NOITE)


def test_save_mapa(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchone.return_value = (4, 'MapaNovo', 'Dia')
    with patch('src.repositories.mapa_repository.connection_db', return_value=mock_conn):
        repo = MapaRepositoryImpl()
        mapa = Mapa(0, 'MapaNovo', TurnoType.DIA)
        saved = repo.save(mapa)
        mock_conn.commit.assert_called_once()
        assert saved == Mapa(4, 'MapaNovo', TurnoType.DIA)


def test_delete_mapa(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.rowcount = 1
    with patch('src.repositories.mapa_repository.connection_db', return_value=mock_conn):
        repo = MapaRepositoryImpl()
        deleted = repo.delete('Mapa1', TurnoType.DIA)
        mock_cursor.execute.assert_called_once_with(
            'DELETE FROM mapa WHERE nome = %s AND turno = %s',
            ('Mapa1', TurnoType.DIA.value)
        )
        mock_conn.commit.assert_called_once()
        assert deleted is True


def test_find_by_turno(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    mock_cursor.fetchall.return_value = [
        (5, 'MapaA', 'Dia')
    ]
    with patch('src.repositories.mapa_repository.connection_db', return_value=mock_conn):
        repo = MapaRepositoryImpl()
        mapas = repo.find_by_turno(TurnoType.DIA)
        mock_cursor.execute.assert_called_once()
        assert mapas == [Mapa(5, 'MapaA', TurnoType.DIA)]
