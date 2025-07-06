"""
Implementação PostgreSQL do InventoryRepository
"""

from typing import List, Optional
from ..utils.db_helpers import connection_db
from ..models.inventory import InventoryEntry
from abc import ABC, abstractmethod


class InventoryRepository(ABC):
    """Interface para repositório de InventoryEntry"""

    @abstractmethod
    def find_all(self) -> List[InventoryEntry]:
        """Retorna todas as entradas de inventário"""
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[InventoryEntry]:
        """Busca entrada de inventário por ID"""
        pass

    @abstractmethod
    def save(self, entry: InventoryEntry) -> InventoryEntry:
        """Salva ou atualiza uma entrada de inventário"""
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Deleta uma entrada de inventário por ID"""
        pass


class InventoryRepositoryImpl(InventoryRepository):
    """Implementação PostgreSQL do InventoryRepository"""

    def find_all(self) -> List[InventoryEntry]:
        """Retorna todas as entradas de inventário"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id, player_id, item_id, quantidade
                        FROM inventario
                        ORDER BY id
                    """ )
                    rows = cursor.fetchall()
                    result: List[InventoryEntry] = []
                    for r in rows:
                        result.append(InventoryEntry(
                            id=r[0], player_id=r[1], item_id=r[2], quantidade=r[3]
                        ))
                    return result
        except Exception as e:
            print(f"Erro ao buscar inventário: {e}")
            return []

    def find_by_id(self, id: int) -> Optional[InventoryEntry]:
        """Busca entrada de inventário por ID"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id, player_id, item_id, quantidade
                        FROM inventario
                        WHERE id = %s
                    """, (id,))
                    r = cursor.fetchone()
                    if r:
                        return InventoryEntry(
                            id=r[0], player_id=r[1], item_id=r[2], quantidade=r[3]
                        )
                    return None
        except Exception as e:
            print(f"Erro ao buscar inventário {id}: {e}")
            return None

    def save(self, entry: InventoryEntry) -> InventoryEntry:
        """Salva ou atualiza uma entrada de inventário"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO inventario (id, player_id, item_id, quantidade)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (id)
                        DO UPDATE SET player_id = EXCLUDED.player_id,
                                       item_id   = EXCLUDED.item_id,
                                       quantidade= EXCLUDED.quantidade
                        RETURNING id, player_id, item_id, quantidade
                    """, (
                        entry.id, entry.player_id, entry.item_id, entry.quantidade
                    ))
                    result = cursor.fetchone()
                    conn.commit()
                    return InventoryEntry(
                        id=result[0], player_id=result[1], item_id=result[2], quantidade=result[3]
                    )
        except Exception as e:
            print(f"Erro ao salvar inventário: {e}")
            return entry

    def delete(self, id: int) -> bool:
        """Deleta uma entrada de inventário por ID"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM inventario WHERE id = %s", (id,))
                    deleted = cursor.rowcount > 0
                    conn.commit()
                    return deleted
        except Exception as e:
            print(f"Erro ao deletar inventário {id}: {e}")
            return False
