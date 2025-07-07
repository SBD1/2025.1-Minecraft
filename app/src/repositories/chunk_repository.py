"""
Implementação PostgreSQL do ChunkRepository
"""

from typing import List, Optional
from ..utils.db_helpers import connection_db
from ..models.chunk import Chunk
from abc import ABC, abstractmethod


class ChunkRepository(ABC):
    """Interface para repositório de Chunk"""
    
    @abstractmethod
    def find_all(self) -> List[Chunk]:
        """Retorna todos os chunks"""
        pass
    
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Chunk]:
        """Busca chunk por ID"""
        pass
    
    @abstractmethod
    def save(self, chunk: Chunk) -> Chunk:
        """Salva um chunk"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Deleta um chunk por ID"""
        pass
    
    @abstractmethod
    def find_by_mapa(self, mapa_nome: str, mapa_turno: str) -> List[Chunk]:
        """Busca chunks por mapa"""
        pass
    
    @abstractmethod
    def find_by_bioma(self, bioma_id: int) -> List[Chunk]:
        """Busca chunks por bioma"""
        pass


class ChunkRepositoryImpl(ChunkRepository):
    """Implementação PostgreSQL do ChunkRepository"""
    
    def find_all(self) -> List[Chunk]:
        """Retorna todos os chunks"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id_chunk, id_bioma, id_mapa, x, y
                        FROM chunk
                        ORDER BY id_chunk
                    """)
                    
                    results = cursor.fetchall()
                    chunks = []
                    
                    for row in results:
                        chunk = Chunk(
                            id_chunk=row[0],
                            id_bioma=row[1],
                            id_mapa=row[2],
                            x=row[3],
                            y=row[4]
                        )
                        chunks.append(chunk)
                    
                    return chunks
        except Exception as e:
            print(f"Erro ao buscar chunks: {str(e)}")
            return []
    
    def find_by_id(self, id: int) -> Optional[Chunk]:
        """Busca chunk por ID"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id_chunk, id_bioma, id_mapa, x, y
                        FROM chunk
                        WHERE id_chunk = %s
                    """, (id,))
                    result = cursor.fetchone()
                    if result:
                        return Chunk(
                            id_chunk=result[0],
                            id_bioma=result[1],
                            id_mapa=result[2],
                            x=result[3],
                            y=result[4]
                        )
                    return None
        except Exception as e:
            print(f"Erro ao buscar chunk {id}: {str(e)}")
            return None
    
    def save(self, chunk: Chunk) -> Chunk:
        """Salva um chunk"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO chunk (id_chunk, id_bioma, id_mapa, x, y)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (id_chunk)
                        DO UPDATE SET id_bioma = EXCLUDED.id_bioma,
                                       id_mapa  = EXCLUDED.id_mapa,
                                       x        = EXCLUDED.x,
                                       y        = EXCLUDED.y
                        RETURNING id_chunk, id_bioma, id_mapa, x, y
                    """, (chunk.id_chunk, chunk.id_bioma, chunk.id_mapa, chunk.x, chunk.y))
                    result = cursor.fetchone()
                    conn.commit()
                    return Chunk(
                        id_chunk=result[0],
                        id_bioma=result[1],
                        id_mapa=result[2],
                        x=result[3],
                        y=result[4]
                    )
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
            print(f"Erro ao salvar chunk: {str(e)}")
            return chunk
    
    def delete(self, id: int) -> bool:
        """Deleta um chunk por ID"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM chunk WHERE id_chunk = %s", (id,))
                    deleted = cursor.rowcount > 0
                    conn.commit()
                    return deleted
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
            print(f"Erro ao deletar chunk {id}: {str(e)}")
            return False
    
    def find_by_mapa(self, mapa_nome: str, mapa_turno: str) -> List[Chunk]:
        """Busca chunks por mapa"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT c.id_chunk, c.id_bioma, c.id_mapa, c.x, c.y
                        FROM chunk c
                        JOIN mapa m ON c.id_mapa = m.id_mapa
                        WHERE m.nome = %s AND m.turno = %s
                        ORDER BY c.id_chunk
                    """, (mapa_nome, mapa_turno))
                    
                    results = cursor.fetchall()
                    chunks = []
                    
                    for row in results:
                        chunk = Chunk(
                            id_chunk=row[0],
                            id_bioma=row[1],
                            id_mapa=row[2],
                            x=row[3],
                            y=row[4]
                        )
                        chunks.append(chunk)
                    
                    return chunks
        except Exception as e:
            print(f"Erro ao buscar chunks do mapa {mapa_nome} ({mapa_turno}): {str(e)}")
            return []
    
    def find_by_bioma(self, bioma_id: int) -> List[Chunk]:
        """Busca chunks por bioma"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id_chunk, id_bioma, id_mapa, x, y
                        FROM chunk
                        WHERE id_bioma = %s
                        ORDER BY id_chunk
                    """, (bioma_id,))
                    
                    results = cursor.fetchall()
                    chunks = []
                    
                    for row in results:
                        chunk = Chunk(
                            id_chunk=row[0],
                            id_bioma=row[1],
                            id_mapa=row[2],
                            x=row[3],
                            y=row[4]
                        )
                        chunks.append(chunk)
                    
                    return chunks
        except Exception as e:
            print(f"Erro ao buscar chunks do bioma {bioma_id}: {str(e)}")
            return [] 
