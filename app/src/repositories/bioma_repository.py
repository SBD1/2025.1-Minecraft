"""
Implementação PostgreSQL do BiomaRepository
"""

from typing import List, Optional
from ..utils.db_helpers import connection_db
from ..models.bioma import Bioma
from abc import ABC, abstractmethod


class BiomaRepository(ABC):
    """Interface para repositório de Bioma"""
    
    @abstractmethod
    def find_all(self) -> List[Bioma]:
        """Retorna todos os biomas"""
        pass
    
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Bioma]:
        """Busca bioma por ID"""
        pass
    
    @abstractmethod
    def save(self, bioma: Bioma) -> Bioma:
        """Salva um bioma"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Deleta um bioma por ID"""
        pass


class BiomaRepositoryImpl(BiomaRepository):
    """Implementação PostgreSQL do BiomaRepository"""
    
    def find_all(self) -> List[Bioma]:
        """Retorna todos os biomas"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id_bioma, nome, descricao
                        FROM bioma
                        ORDER BY nome
                    """)
                    
                    results = cursor.fetchall()
                    biomas = []
                    
                    for row in results:
                        bioma = Bioma(
                            id_bioma=row[0],
                            nome=row[1],
                            descricao=row[2]
                        )
                        biomas.append(bioma)
                    
                    return biomas
        except Exception as e:
            print(f"Erro ao buscar biomas: {str(e)}")
            return []
    
    def find_by_id(self, id: int) -> Optional[Bioma]:
        """Busca bioma por ID"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id_bioma, nome, descricao
                        FROM bioma
                        WHERE id_bioma = %s
                    """, (id,))
                    
                    result = cursor.fetchone()
                    if result:
                        return Bioma(
                            id_bioma=result[0],
                            nome=result[1],
                            descricao=result[2]
                        )
                    return None
        except Exception as e:
            print(f"Erro ao buscar bioma {id}: {str(e)}")
            return None
    
    def save(self, bioma: Bioma) -> Bioma:
        """Salva um bioma"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO bioma (id_bioma, nome, descricao)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (id_bioma)
                        DO UPDATE SET nome = EXCLUDED.nome, descricao = EXCLUDED.descricao
                        RETURNING id_bioma, nome, descricao
                    """, (bioma.id_bioma, bioma.nome, bioma.descricao))
                    result = cursor.fetchone()
                    conn.commit()
                    return Bioma(
                        id_bioma=result[0],
                        nome=result[1],
                        descricao=result[2]
                    )
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
            print(f"Erro ao salvar bioma: {str(e)}")
            return bioma
    
    def delete(self, id: int) -> bool:
        """Deleta um bioma por ID"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM bioma WHERE id_bioma = %s", (id,))
                    deleted = cursor.rowcount > 0
                    conn.commit()
                    return deleted
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
            print(f"Erro ao deletar bioma {id}: {str(e)}")
            return False 
