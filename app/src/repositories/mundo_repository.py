"""
Implementação do repositório para a entidade Mundo.
Adaptado para o esquema da main.
"""

from typing import Optional
from ..utils.db_helpers import connection_db
from ..models.mundo import Mundo
from abc import ABC, abstractmethod

class MundoRepository(ABC):
    """Interface para repositório de Mundo"""

    @abstractmethod
    def get_estado(self) -> Optional[Mundo]:
        """Busca o estado atual do mundo."""
        pass

    @abstractmethod
    def update_estado(self, mundo: Mundo) -> bool:
        """Atualiza o estado do mundo."""
        pass

class MundoRepositoryImpl(MundoRepository):
    """Implementação PostgreSQL do MundoRepository - Adaptado para esquema da main"""

    def get_estado(self) -> Optional[Mundo]:
        """
        Busca o estado atual do mundo.
        Como só existe um mundo (ID=1), esta query é fixa.
        Adaptado para usar nomes de colunas em minúsculas do esquema da main.
        """
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT id_mundo, turno_atual, ticks_no_turno FROM Mundo WHERE id_mundo = 1"
                    )
                    row = cursor.fetchone()

                    if not row:
                        print("ERRO: Estado do mundo não encontrado no banco de dados.")
                        return None
                    
                    return Mundo(
                        id_mundo=row[0],
                        turno_atual=row[1],
                        ticks_no_turno=row[2]
                    )
        except Exception as e:
            print(f"Erro ao buscar o estado do mundo: {str(e)}")
            return None

    def update_estado(self, mundo: Mundo) -> bool:
        """
        Atualiza o estado do mundo no banco de dados.
        Adaptado para usar nomes de colunas em minúsculas do esquema da main.
        """
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE Mundo 
                        SET turno_atual = %s, ticks_no_turno = %s
                        WHERE id_mundo = %s
                        """,
                        (mundo.turno_atual, mundo.ticks_no_turno, mundo.id_mundo)
                    )
                    conn.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar o estado do mundo: {str(e)}")
            return False
