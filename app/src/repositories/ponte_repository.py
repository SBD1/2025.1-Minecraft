from typing import List, Optional
from ..utils.db_helpers import connection_db
from ..models.ponte import Ponte
from abc import ABC, abstractmethod

# Interface abstrata para o repositório de Pontes
class PonteRepository(ABC):

    @abstractmethod
    def inserir(self, ponte: Ponte) -> Ponte:
        """Insere uma nova ponte entre dois chunks"""
        pass

    @abstractmethod
    def listar_ativas(self) -> List[Ponte]:
        """Lista todas as pontes ativas"""
        pass

    @abstractmethod
    def existe_ponte_entre(self, origem: int, destino: int) -> bool:
        """Verifica se há uma ponte entre dois chunks"""
        pass

    @abstractmethod
    def desativar(self, id_ponte: int) -> None:
        """Desativa uma ponte (ativa = False)"""
        pass

class PonteRepositoryImpl(PonteRepository):

    def inserir(self, ponte: Ponte) -> Ponte:
        query = """
        INSERT INTO pontes (origem, destino, comprimento, largura, material, ativa)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        with connection_db() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    ponte.origem,
                    ponte.destino,
                    ponte.comprimento,
                    ponte.largura,
                    ponte.material,
                    ponte.ativa
                ))
                ponte.id = cur.fetchone()[0]
        return ponte

    def listar_ativas(self) -> List[Ponte]:
        query = """
        SELECT id, origem, destino, comprimento, largura, material, ativa
        FROM pontes
        WHERE ativa = TRUE
        """
        with connection_db() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [Ponte(*row) for row in rows]

    def existe_ponte_entre(self, origem: int, destino: int) -> bool:
        query = """
        SELECT 1 FROM pontes
        WHERE origem = %s AND destino = %s AND ativa = TRUE
        LIMIT 1
        """
        with connection_db() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (origem, destino))
                return cur.fetchone() is not None

    def desativar(self, id_ponte: int) -> None:
        query = "UPDATE pontes SET ativa = FALSE WHERE id = %s"
        with connection_db() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (id_ponte,))