"""
Implementação PostgreSQL do PlayerRepository
"""

from typing import List, Optional
from ..utils.db_helpers import connection_db
from ..models.player import Player
from abc import ABC, abstractmethod


class PlayerRepository(ABC):
    """Interface para repositório de Player"""
    
    @abstractmethod
    def find_all(self) -> List[Player]:
        """Retorna todos os jogadores"""
        pass
    
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[Player]:
        """Busca jogador por ID"""
        pass
    
    @abstractmethod
    def save(self, player: Player) -> Player:
        """Salva um jogador"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Deleta um jogador por ID"""
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Player]:
        """Busca jogador por nome"""
        pass
    
    @abstractmethod
    def find_active_players(self) -> List[Player]:
        """Busca jogadores ativos"""
        pass


class PlayerRepositoryImpl(PlayerRepository):
    """Implementação PostgreSQL do PlayerRepository"""
    
    def find_all(self) -> List[Player]:
        """Retorna todos os jogadores"""
        try:
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT Id_Jogador, Nome, Vida_max, Vida_atual, forca, 
                               COALESCE(Id_Chunk_Atual, 1) as localizacao,
                               COALESCE(xp, 0) as experiencia,
                               1 as nivel
                        FROM Jogador
                        ORDER BY Nome
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
                            localizacao=str(row[5]),
                            nivel=row[7],
                            experiencia=row[6]
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
                        SELECT Id_Jogador, Nome, Vida_max, Vida_atual, forca, 
                               COALESCE(Id_Chunk_Atual, 1) as localizacao,
                               COALESCE(xp, 0) as experiencia,
                               1 as nivel
                        FROM Jogador
                        WHERE Id_Jogador = %s
                    """, (id,))
                    
                    result = cursor.fetchone()
                    if result:
                        return Player(
                            id_jogador=result[0],
                            nome=result[1],
                            vida_maxima=result[2],
                            vida_atual=result[3],
                            forca=result[4],
                            localizacao=str(result[5]),
                            nivel=result[7],
                            experiencia=result[6]
                        )
                    return None
        except Exception as e:
            print(f"❌ Erro ao buscar jogador {id}: {str(e)}")
            return None
    
    def save(self, player: Player) -> Player:
        """Salva um jogador com validações"""
        try:
            # Validações
            if not player.nome or not player.nome.strip():
                print("❌ Nome do jogador não pode estar vazio")
                return player
            
            if player.vida_atual < 0:
                print("❌ Vida atual não pode ser negativa")
                return player
            
            if player.vida_maxima <= 0:
                print("❌ Vida máxima deve ser maior que zero")
                return player
            
            if player.vida_atual > player.vida_maxima:
                print("❌ Vida atual não pode ser maior que vida máxima")
                return player
            
            if player.forca < 0:
                print("❌ Força não pode ser negativa")
                return player
            
            if player.nivel < 1:
                print("❌ Nível deve ser pelo menos 1")
                return player
            
            if player.experiencia < 0:
                print("❌ Experiência não pode ser negativa")
                return player
            
            with connection_db() as conn:
                with conn.cursor() as cursor:
                    if player.id_jogador:
                        # Update existing player - only update columns that exist in DB
                        cursor.execute("""
                            UPDATE Jogador 
                            SET Nome = %s, Vida_max = %s, Vida_atual = %s, 
                                forca = %s, Id_Chunk_Atual = %s, xp = %s
                            WHERE Id_Jogador = %s
                            RETURNING Id_Jogador, Nome, Vida_max, Vida_atual, 
                                     forca, Id_Chunk_Atual, xp
                        """, (player.nome, player.vida_maxima, player.vida_atual,
                              player.forca, int(player.localizacao) if player.localizacao.isdigit() else 1, 
                              player.experiencia, player.id_jogador))
                    else:
                        # Insert new player - only insert columns that exist in DB
                        cursor.execute("""
                            INSERT INTO Jogador (Nome, Vida_max, Vida_atual, forca, 
                                               Id_Chunk_Atual, xp)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            RETURNING Id_Jogador, Nome, Vida_max, Vida_atual, 
                                     forca, Id_Chunk_Atual, xp
                        """, (player.nome, player.vida_maxima, player.vida_atual,
                              player.forca, int(player.localizacao) if player.localizacao.isdigit() else 1, 
                              player.experiencia))
                    result = cursor.fetchone()
                    conn.commit()
                    return Player(
                        id_jogador=result[0],
                        nome=result[1],
                        vida_maxima=result[2],  # Map Vida_max to vida_maxima
                        vida_atual=result[3],
                        forca=result[4],
                        localizacao=str(result[5]) if result[5] else "1",  # Map Id_Chunk_Atual to localizacao
                        nivel=player.nivel,  # Keep the model's nivel since it's not in DB
                        experiencia=result[6]  # Map xp to experiencia
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
                    cursor.execute("DELETE FROM Jogador WHERE Id_Jogador = %s", (id,))
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
                        SELECT Id_Jogador, Nome, Vida_max, Vida_atual, forca, 
                               COALESCE(Id_Chunk_Atual, 1) as localizacao,
                               COALESCE(xp, 0) as experiencia,
                               1 as nivel
                        FROM Jogador
                        WHERE Nome = %s
                    """, (name,))
                    
                    result = cursor.fetchone()
                    if result:
                        return Player(
                            id_jogador=result[0],
                            nome=result[1],
                            vida_maxima=result[2],  # Map Vida_max to vida_maxima
                            vida_atual=result[3],
                            forca=result[4],
                            localizacao=str(result[5]),  # Convert chunk ID to string
                            nivel=result[7],  # Default to 1
                            experiencia=result[6]  # Map xp to experiencia
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
                        SELECT Id_Jogador, Nome, Vida_max, Vida_atual, forca, 
                               COALESCE(Id_Chunk_Atual, 1) as localizacao,
                               COALESCE(xp, 0) as experiencia,
                               1 as nivel
                        FROM Jogador
                        WHERE Vida_atual > 0
                        ORDER BY Nome
                    """)
                    
                    results = cursor.fetchall()
                    players = []
                    
                    for row in results:
                        player = Player(
                            id_jogador=row[0],
                            nome=row[1],
                            vida_maxima=row[2],  # Map Vida_max to vida_maxima
                            vida_atual=row[3],
                            forca=row[4],
                            localizacao=str(row[5]),  # Convert chunk ID to string
                            nivel=row[7],  # Default to 1
                            experiencia=row[6]  # Map xp to experiencia
                        )
                        players.append(player)
                    
                    return players
        except Exception as e:
            print(f"❌ Erro ao buscar jogadores ativos: {str(e)}")
            return [] 