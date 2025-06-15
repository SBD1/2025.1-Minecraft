"""
Implementação PostgreSQL do MapaRepository
"""

from typing import List, Optional
from ..utils.db_helpers import connection_db
from ..models.mapa import Mapa, TurnoType
from abc import ABC, abstractmethod


class MapaRepository(ABC):
    """Interface para repositório de Mapa"""
    
    @abstractmethod
    def find_all(self) -> List[Mapa]:
        """Retorna todos os mapas"""
        pass
    
    @abstractmethod
    def find_by_id(self, nome: str, turno: TurnoType) -> Optional[Mapa]:
        """Busca mapa por nome e turno"""
        pass
    
    @abstractmethod
    def save(self, mapa: Mapa) -> Mapa:
        """Salva um mapa"""
        pass
    
    @abstractmethod
    def delete(self, nome: str, turno: TurnoType) -> bool:
        """Deleta um mapa por nome e turno"""
        pass
    
    @abstractmethod
    def find_by_turno(self, turno: TurnoType) -> List[Mapa]:
        """Busca mapas por turno"""
        pass


class MapaRepositoryImpl(MapaRepository):
    """Implementação PostgreSQL do MapaRepository"""
    
    def find_all(self) -> List[Mapa]:
        """Retorna todos os mapas"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT nome, turno
                        FROM mapa
                        ORDER BY nome, turno
                    """)
                    
                    results = cursor.fetchall()
                    mapas = []
                    
                    for row in results:
                        mapa = Mapa(nome=row[0], turno=row[1])
                        mapas.append(mapa)
                    
                    return mapas
        except Exception as e:
            print(f"❌ Erro ao buscar mapas: {str(e)}")
            return []
    
    def find_by_id(self, nome: str, turno: TurnoType) -> Optional[Mapa]:
        """Busca mapa por nome e turno"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT nome, turno
                        FROM mapa
                        WHERE nome = %s AND turno = %s
                    """, (nome, turno.value))
                    
                    result = cursor.fetchone()
                    if result:
                        return Mapa(nome=result[0], turno=result[1])
                    return None
        except Exception as e:
            print(f"❌ Erro ao buscar mapa {nome} ({turno.value}): {str(e)}")
            return None
    
    def save(self, mapa: Mapa) -> Mapa:
        """Salva um mapa"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO mapa (nome, turno)
                        VALUES (%s, %s)
                        ON CONFLICT (nome, turno)
                        DO UPDATE SET nome = EXCLUDED.nome, turno = EXCLUDED.turno
                        RETURNING nome, turno
                    """, (mapa.nome, mapa.turno.value))
                    result = cursor.fetchone()
                    conn.commit()
                    return Mapa(nome=result[0], turno=result[1])
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
            print(f"❌ Erro ao salvar mapa: {str(e)}")
            return mapa
    
    def delete(self, nome: str, turno: TurnoType) -> bool:
        """Deleta um mapa por nome e turno"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM mapa WHERE nome = %s AND turno = %s", (nome, turno.value))
                    deleted = cursor.rowcount > 0
                    conn.commit()
                    return deleted
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
            print(f"❌ Erro ao deletar mapa {nome} ({turno.value}): {str(e)}")
            return False
    
    def find_by_turno(self, turno: TurnoType) -> List[Mapa]:
        """Busca mapas por turno"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT nome, turno
                        FROM mapa
                        WHERE turno = %s
                        ORDER BY nome
                    """, (turno.value,))
                    
                    results = cursor.fetchall()
                    mapas = []
                    
                    for row in results:
                        mapa = Mapa(nome=row[0], turno=row[1])
                        mapas.append(mapa)
                    
                    return mapas
        except Exception as e:
            print(f"❌ Erro ao buscar mapas do turno {turno.value}: {str(e)}")
            return [] 