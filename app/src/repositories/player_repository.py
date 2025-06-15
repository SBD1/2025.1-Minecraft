"""
Implementação PostgreSQL do PlayerRepository
"""

from typing import List, Optional
from ..utils.db_helpers import connection_db
from ..models.player import Player
from . import PlayerRepository


class PlayerRepository(PlayerRepository):
    """Implementação PostgreSQL do PlayerRepository"""
    
    def find_all(self) -> List[Player]:
        """Retorna todos os jogadores"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id_jogador, nome, vida_maxima, vida_atual, forca, 
                               localizacao, nivel, experiencia
                        FROM jogador
                        ORDER BY nome
                    """)
                    
                    results = cursor.fetchall()
                    players = []
                    
                    for row in results:
                        player = Player(
                            id_jogador=row[0],
                            nome=row[1],
                            vida_maxima=row[2],
                            vida_atual=row[3],
                            forca=row[4],
                            localizacao=row[5],
                            nivel=row[6],
                            experiencia=row[7]
                        )
                        players.append(player)
                    
                    return players
        except Exception as e:
            print(f"❌ Erro ao buscar jogadores: {str(e)}")
            return []
    
    def find_by_id(self, id: int) -> Optional[Player]:
        """Busca jogador por ID"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id_jogador, nome, vida_maxima, vida_atual, forca, 
                               localizacao, nivel, experiencia
                        FROM jogador
                        WHERE id_jogador = %s
                    """, (id,))
                    
                    result = cursor.fetchone()
                    if result:
                        return Player(
                            id_jogador=result[0],
                            nome=result[1],
                            vida_maxima=result[2],
                            vida_atual=result[3],
                            forca=result[4],
                            localizacao=result[5],
                            nivel=result[6],
                            experiencia=result[7]
                        )
                    return None
        except Exception as e:
            print(f"❌ Erro ao buscar jogador {id}: {str(e)}")
            return None
    
    def save(self, player: Player) -> Player:
        """Salva um jogador"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    if player.id_jogador:
                        cursor.execute("""
                            UPDATE jogador 
                            SET nome = %s, vida_maxima = %s, vida_atual = %s, 
                                forca = %s, localizacao = %s, nivel = %s, experiencia = %s
                            WHERE id_jogador = %s
                            RETURNING id_jogador, nome, vida_maxima, vida_atual, 
                                     forca, localizacao, nivel, experiencia
                        """, (player.nome, player.vida_maxima, player.vida_atual,
                              player.forca, player.localizacao, player.nivel, 
                              player.experiencia, player.id_jogador))
                    else:
                        cursor.execute("""
                            INSERT INTO jogador (nome, vida_maxima, vida_atual, forca, 
                                               localizacao, nivel, experiencia)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            RETURNING id_jogador, nome, vida_maxima, vida_atual, 
                                     forca, localizacao, nivel, experiencia
                        """, (player.nome, player.vida_maxima, player.vida_atual,
                              player.forca, player.localizacao, player.nivel, 
                              player.experiencia))
                    result = cursor.fetchone()
                    conn.commit()
                    return Player(
                        id_jogador=result[0],
                        nome=result[1],
                        vida_maxima=result[2],
                        vida_atual=result[3],
                        forca=result[4],
                        localizacao=result[5],
                        nivel=result[6],
                        experiencia=result[7]
                    )
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
            print(f"❌ Erro ao salvar jogador: {str(e)}")
            return player
    
    def delete(self, id: int) -> bool:
        """Deleta um jogador por ID"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM jogador WHERE id_jogador = %s", (id,))
                    deleted = cursor.rowcount > 0
                    conn.commit()
                    return deleted
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
            print(f"❌ Erro ao deletar jogador {id}: {str(e)}")
            return False
    
    def find_by_name(self, name: str) -> Optional[Player]:
        """Busca jogador por nome"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id_jogador, nome, vida_maxima, vida_atual, forca, 
                               localizacao, nivel, experiencia
                        FROM jogador
                        WHERE nome = %s
                    """, (name,))
                    
                    result = cursor.fetchone()
                    if result:
                        return Player(
                            id_jogador=result[0],
                            nome=result[1],
                            vida_maxima=result[2],
                            vida_atual=result[3],
                            forca=result[4],
                            localizacao=result[5],
                            nivel=result[6],
                            experiencia=result[7]
                        )
                    return None
        except Exception as e:
            print(f"❌ Erro ao buscar jogador por nome {name}: {str(e)}")
            return None
    
    def find_active_players(self) -> List[Player]:
        """Busca jogadores ativos (com vida > 0)"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id_jogador, nome, vida_maxima, vida_atual, forca, 
                               localizacao, nivel, experiencia
                        FROM jogador
                        WHERE vida_atual > 0
                        ORDER BY nome
                    """)
                    
                    results = cursor.fetchall()
                    players = []
                    
                    for row in results:
                        player = Player(
                            id_jogador=row[0],
                            nome=row[1],
                            vida_maxima=row[2],
                            vida_atual=row[3],
                            forca=row[4],
                            localizacao=row[5],
                            nivel=row[6],
                            experiencia=row[7]
                        )
                        players.append(player)
                    
                    return players
        except Exception as e:
            print(f"❌ Erro ao buscar jogadores ativos: {str(e)}")
            return [] 