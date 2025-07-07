from typing import List, Optional, Tuple
from ..utils.db_helpers import connection_db
from ..models.aldeao import Aldeao, BobMago, BobConstrutor
from abc import ABC, abstractmethod

class AldeaoRepository(ABC):

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Tuple[Aldeao, Optional[BobMago], Optional[BobConstrutor]]]:
        """
        Busca um aldeão pelo seu ID e retorna uma tupla com o aldeão base
        e sua especialização (se houver).
        """
        pass

    @abstractmethod
    def save(self, aldeao: Aldeao, especializacao: Optional[BobMago | BobConstrutor] = None) -> Aldeao:
        """Salva um aldeão e sua especialização."""
        pass

class AldeaoRepositoryImpl(AldeaoRepository):
    """Implementação PostgreSQL do AldeaoRepository - Adaptado para o esquema da main"""

    def find_by_id(self, id: int) -> Optional[Tuple[Aldeao, Optional[BobMago], Optional[BobConstrutor]]]:
        """
        Busca um aldeão e sua especialização.
        Retorna uma tupla: (aldeao_base, mago_info, construtor_info)
        
        Adaptado para usar o esquema atual da main com nomes de colunas corretos.
        """
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    # 1. Busca o aldeão base (usando esquema da main se existir)
                    cursor.execute(
                        "SELECT id_aldeao, nome, tipo, descricao, id_casa FROM Aldeao WHERE id_aldeao = %s",
                        (id,)
                    )
                    aldeao_row = cursor.fetchone()

                    if not aldeao_row:
                        return None

                    aldeao = Aldeao(
                        id_aldeao=aldeao_row[0],
                        nome=aldeao_row[1],
                        tipo=aldeao_row[2],
                        descricao=aldeao_row[3],
                        id_casa=aldeao_row[4]
                    )

                    mago: Optional[BobMago] = None
                    construtor: Optional[BobConstrutor] = None

                    # 2. Se for Mago, busca os dados da especialização
                    if aldeao.tipo == 'Mago':
                        cursor.execute(
                            "SELECT id_aldeao_mago, habilidade_mago, nivel, descricao FROM Bob_mago WHERE id_aldeao_mago = %s",
                            (id,)
                        )
                        mago_row = cursor.fetchone()
                        if mago_row:
                            mago = BobMago(
                                id_aldeao_mago=mago_row[0],
                                habilidade_mago=mago_row[1],
                                nivel=mago_row[2],
                                descricao=mago_row[3]
                            )
                    
                    # 3. Se for Construtor, busca os dados da especialização
                    elif aldeao.tipo == 'Construtor':
                        cursor.execute(
                            "SELECT id_aldeao_construtor, habilidades_construtor, nivel, descricao FROM Bob_construtor WHERE id_aldeao_construtor = %s",
                            (id,)
                        )
                        construtor_row = cursor.fetchone()
                        if construtor_row:
                            construtor = BobConstrutor(
                                id_aldeao_construtor=construtor_row[0],
                                habilidades_construtor=construtor_row[1],
                                nivel=construtor_row[2],
                                descricao=construtor_row[3]
                            )
                    
                    return (aldeao, mago, construtor)

        except Exception as e:
            print(f"Erro ao buscar aldeão {id}: {str(e)}")
            return None

    def save(self, aldeao: Aldeao, especializacao: Optional[BobMago | BobConstrutor] = None) -> Aldeao:
        """
        Salva um aldeão e sua especialização.
        Adaptado para usar o esquema da main com constraint names corretos.
        """
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    # 1. Salva o Aldeão (pai)
                    if aldeao.id_aldeao:
                        # UPDATE
                        cursor.execute(
                            """
                            UPDATE Aldeao SET nome=%s, tipo=%s, descricao=%s, id_casa=%s
                            WHERE id_aldeao = %s
                            """,
                            (aldeao.nome, aldeao.tipo, aldeao.descricao, aldeao.id_casa, aldeao.id_aldeao)
                        )
                    else:
                        # INSERT
                        cursor.execute(
                            """
                            INSERT INTO Aldeao (nome, tipo, descricao, id_casa)
                            VALUES (%s, %s, %s, %s) RETURNING id_aldeao
                            """,
                            (aldeao.nome, aldeao.tipo, aldeao.descricao, aldeao.id_casa)
                        )
                        aldeao.id_aldeao = cursor.fetchone()[0]

                    # 2. Salva a especialização (se houver)
                    if especializacao:
                        if isinstance(especializacao, BobMago):
                            cursor.execute(
                                """
                                INSERT INTO Bob_mago (id_aldeao_mago, habilidade_mago, nivel, descricao)
                                VALUES (%s, %s, %s, %s)
                                ON CONFLICT (id_aldeao_mago) DO UPDATE SET
                                habilidade_mago = EXCLUDED.habilidade_mago,
                                nivel = EXCLUDED.nivel,
                                descricao = EXCLUDED.descricao
                                """,
                                (aldeao.id_aldeao, especializacao.habilidade_mago, especializacao.nivel, especializacao.descricao)
                            )
                        elif isinstance(especializacao, BobConstrutor):
                            cursor.execute(
                                """
                                INSERT INTO Bob_construtor (id_aldeao_construtor, habilidades_construtor, nivel, descricao)
                                VALUES (%s, %s, %s, %s)
                                ON CONFLICT (id_aldeao_construtor) DO UPDATE SET
                                habilidades_construtor = EXCLUDED.habilidades_construtor,
                                nivel = EXCLUDED.nivel,
                                descricao = EXCLUDED.descricao
                                """,
                                (aldeao.id_aldeao, especializacao.habilidades_construtor, especializacao.nivel, especializacao.descricao)
                            )
                    
                    conn.commit()
                    return aldeao

        except Exception as e:
            print(f"Erro ao salvar aldeão: {str(e)}")
            return None
