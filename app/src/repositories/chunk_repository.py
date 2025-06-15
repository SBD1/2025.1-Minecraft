"""
Implementação PostgreSQL do ChunkRepository
"""

from typing import List, Optional
from ..utils.db_helpers import connection_db
from ..models.chunk import Chunk
from . import ChunkRepository


class ChunkRepository(ChunkRepository):
    """Implementação PostgreSQL do ChunkRepository"""
    
    def find_all(self) -> List[Chunk]:
        """Retorna todos os chunks"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT numero_chunk, id_bioma, id_mapa_nome, id_mapa_turno
                        FROM chunk
                        ORDER BY numero_chunk
                    """)
                    
                    results = cursor.fetchall()
                    chunks = []
                    
                    for row in results:
                        chunk = Chunk(
                            numero_chunk=row[0],
                            id_bioma=row[1],
                            id_mapa_nome=row[2],
                            id_mapa_turno=row[3]
                        )
                        chunks.append(chunk)
                    
                    return chunks
        except Exception as e:
            print(f"❌ Erro ao buscar chunks: {str(e)}")
            return []
    
    def find_by_id(self, id: int) -> Optional[Chunk]:
        """Busca chunk por ID"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT numero_chunk, id_bioma, id_mapa_nome, id_mapa_turno
                        FROM chunk
                        WHERE numero_chunk = %s
                    """, (id,))
                    
                    result = cursor.fetchone()
                    if result:
                        return Chunk(
                            numero_chunk=result[0],
                            id_bioma=result[1],
                            id_mapa_nome=result[2],
                            id_mapa_turno=result[3]
                        )
                    return None
        except Exception as e:
            print(f"❌ Erro ao buscar chunk {id}: {str(e)}")
            return None
    
    def save(self, chunk: Chunk) -> Chunk:
        """Salva um chunk"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO chunk (numero_chunk, id_bioma, id_mapa_nome, id_mapa_turno)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (numero_chunk, id_mapa_nome, id_mapa_turno)
                        DO UPDATE SET id_bioma = EXCLUDED.id_bioma
                        RETURNING numero_chunk, id_bioma, id_mapa_nome, id_mapa_turno
                    """, (chunk.numero_chunk, chunk.id_bioma, chunk.id_mapa_nome, chunk.id_mapa_turno))
                    result = cursor.fetchone()
                    conn.commit()
                    return Chunk(
                        numero_chunk=result[0],
                        id_bioma=result[1],
                        id_mapa_nome=result[2],
                        id_mapa_turno=result[3]
                    )
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
            print(f"❌ Erro ao salvar chunk: {str(e)}")
            return chunk
    
    def delete(self, id: int) -> bool:
        """Deleta um chunk por ID"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM chunk WHERE numero_chunk = %s", (id,))
                    deleted = cursor.rowcount > 0
                    conn.commit()
                    return deleted
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
            print(f"❌ Erro ao deletar chunk {id}: {str(e)}")
            return False
    
    def find_by_mapa(self, mapa_nome: str, mapa_turno: str) -> List[Chunk]:
        """Busca chunks por mapa"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT numero_chunk, id_bioma, id_mapa_nome, id_mapa_turno
                        FROM chunk
                        WHERE id_mapa_nome = %s AND id_mapa_turno = %s
                        ORDER BY numero_chunk
                    """, (mapa_nome, mapa_turno))
                    
                    results = cursor.fetchall()
                    chunks = []
                    
                    for row in results:
                        chunk = Chunk(
                            numero_chunk=row[0],
                            id_bioma=row[1],
                            id_mapa_nome=row[2],
                            id_mapa_turno=row[3]
                        )
                        chunks.append(chunk)
                    
                    return chunks
        except Exception as e:
            print(f"❌ Erro ao buscar chunks do mapa {mapa_nome} ({mapa_turno}): {str(e)}")
            return []
    
    def find_by_bioma(self, bioma_id: str) -> List[Chunk]:
        """Busca chunks por bioma"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT numero_chunk, id_bioma, id_mapa_nome, id_mapa_turno
                        FROM chunk
                        WHERE id_bioma = %s
                        ORDER BY numero_chunk
                    """, (bioma_id,))
                    
                    results = cursor.fetchall()
                    chunks = []
                    
                    for row in results:
                        chunk = Chunk(
                            numero_chunk=row[0],
                            id_bioma=row[1],
                            id_mapa_nome=row[2],
                            id_mapa_turno=row[3]
                        )
                        chunks.append(chunk)
                    
                    return chunks
        except Exception as e:
            print(f"❌ Erro ao buscar chunks do bioma {bioma_id}: {str(e)}")
            return [] 