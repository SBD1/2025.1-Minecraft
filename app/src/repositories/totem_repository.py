from typing import List, Optional
from ..utils.db_helpers import connection_db
from ..models.totem import Totem
from abc import ABC, abstractmethod

# Interface abstrata para o repositório de Totem
class TotemRepository(ABC):

    @abstractmethod
    def inserir(self, totem: Totem) -> Totem:
        """Insere um novo totem no banco e retorna o totem com o ID preenchido"""
        pass

    @abstractmethod
    def listar_ativos(self) -> List[Totem]:
        """Lista todos os totems ativos"""
        pass

    @abstractmethod
    def buscar_por_id(self, id_totem: int) -> Optional[Totem]:
        """Retorna um totem com base no ID"""
        pass

    @abstractmethod
    def desativar(self, id_totem: int) -> None:
        """Desativa um totem (marca como ativo = False)"""
        pass

class TotemRepositoryImpl(TotemRepository):

    def inserir(self, totem: Totem) -> Totem:
        query = """
        INSERT INTO totems (chunk, altura, material_principal, possui_luz, ativo)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        with connection_db() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    totem.chunk,
                    totem.altura,
                    totem.material_principal,
                    totem.possui_luz,
                    totem.ativo
                ))
                totem.id = cur.fetchone()[0]
        return totem

    def listar_ativos(self) -> List[Totem]:
        query = """
        SELECT id, chunk, altura, material_principal, possui_luz, ativo
        FROM totems
        WHERE ativo = TRUE
        """
        with connection_db() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [Totem(*row) for row in rows]

    def buscar_por_id(self, id_totem: int) -> Optional[Totem]:
        query = """
        SELECT id, chunk, altura, material_principal, possui_luz, ativo
        FROM totems
        WHERE id = %s
        """
        with connection_db() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (id_totem,))
                row = cur.fetchone()
                return Totem(*row) if row else None

    def desativar(self, id_totem: int) -> None:
        query = "UPDATE totems SET ativo = FALSE WHERE id = %s"
        with connection_db() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (id_totem,))
