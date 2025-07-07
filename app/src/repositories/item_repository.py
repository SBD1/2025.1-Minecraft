"""
Implementação PostgreSQL do ItemRepository
"""

from typing import List, Optional
from ..utils.db_helpers import connection_db
from ..models.item import Item
from abc import ABC, abstractmethod


class ItemRepository(ABC):
    """Interface para repositório de Item"""
    
    @abstractmethod
    def find_all(self) -> List[Item]:
        """Retorna todos os items"""
        pass
    
    @abstractmethod
    def find_by_id(self, id_item: int) -> Optional[Item]:
        """Busca item por ID"""
        pass
    
    @abstractmethod
    def save(self, item: Item) -> Item:
        """Salva um item"""
        pass
    
    @abstractmethod
    def delete(self, id_item: int) -> bool:
        """Deleta um item por ID"""
        pass


class ItemRepositoryImpl(ItemRepository):
    """Implementação PostgreSQL do ItemRepository"""
    
    def find_all(self) -> List[Item]:
        """Retorna todos os items"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id_item, nome, tipo, poder, durabilidade
                        FROM item
                        ORDER BY nome
                    """)
                    rows = cursor.fetchall()
                    items: List[Item] = []
                    for r in rows:
                        items.append(Item(
                            id_item=r[0], nome=r[1], tipo=r[2],
                            poder=r[3], durabilidade=r[4]
                        ))
                    return items
        except Exception as e:
            print(f"Erro ao buscar items: {e}")
            return []

    def find_by_id(self, id_item: int) -> Optional[Item]:
        """Busca item por ID"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id_item, nome, tipo, poder, durabilidade
                        FROM item
                        WHERE id_item = %s
                    """, (id_item,))
                    r = cursor.fetchone()
                    if r:
                        return Item(
                            id_item=r[0], nome=r[1], tipo=r[2],
                            poder=r[3], durabilidade=r[4]
                        )
                    return None
        except Exception as e:
            print(f"Erro ao buscar item {id_item}: {e}")
            return None

    def save(self, item: Item) -> Item:
        """Salva ou atualiza um item"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO item (id_item, nome, tipo, poder, durabilidade)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (id_item)
                        DO UPDATE SET nome = EXCLUDED.nome,
                                       tipo = EXCLUDED.tipo,
                                       poder = EXCLUDED.poder,
                                       durabilidade = EXCLUDED.durabilidade
                        RETURNING id_item, nome, tipo, poder, durabilidade
                    """, (
                        item.id_item, item.nome, item.tipo,
                        item.poder, item.durabilidade
                    ))
                    result = cursor.fetchone()
                    conn.commit()
                    return Item(
                        id_item=result[0], nome=result[1], tipo=result[2],
                        poder=result[3], durabilidade=result[4]
                    )
        except Exception as e:
            print(f"Erro ao salvar item: {e}")
            return item

    def delete(self, id_item: int) -> bool:
        """Deleta um item por ID"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM item WHERE id_item = %s", (id_item,))
                    deleted = cursor.rowcount > 0
                    conn.commit()
                    return deleted
        except Exception as e:
            print(f"Erro ao deletar item {id_item}: {e}")
            return False
