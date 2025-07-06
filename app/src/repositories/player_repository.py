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
                        SELECT id_player, nome, vida_maxima, vida_atual, forca,
                               localizacao, nivel, experiencia, current_chunk_id
                        FROM Player
                        ORDER BY nome
                    """)
                    
                    results = cursor.fetchall()
                    players = []
                    
                    for row in results:
                        player = Player(
                            id_player=row[0],
                            nome=row[1],
                            vida_maxima=row[2],
                            vida_atual=row[3],
                            forca=row[4],
                            localizacao=row[5] or "",
                            nivel=row[6],
                            experiencia=row[7],
                            current_chunk_id=row[8]
                        )
                        players.append(player)
                    
                    return players
        except Exception as e:
            print(f"Erro ao buscar jogadores: {str(e)}")
            return []
    
    def find_by_id(self, id: int) -> Optional[Player]:
        """Busca um jogador por ID"""
        try:
            conn = connection_db()
            cursor = conn.cursor()
            
            query = """
                SELECT id_player, nome, vida_maxima, vida_atual, forca, localizacao,
                       nivel, experiencia, current_chunk_id
                FROM Player
                WHERE id_player = %s
            """
            
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result:
                return Player(
                    id_player=result[0],
                    nome=result[1],
                    vida_maxima=result[2],
                    vida_atual=result[3],
                    forca=result[4],
                    localizacao=result[5] or "",
                    nivel=result[6],
                    experiencia=result[7],
                    current_chunk_id=result[8]
                )
            return None
            
        except Exception as e:
            print(f"Erro ao buscar jogador {id}: {str(e)}")
            return None
    
    def save(self, player: Player) -> Player:
        """Salva um jogador no banco de dados"""
        # Validações
        if not player.nome or not player.nome.strip():
            print("Nome do jogador não pode estar vazio")
            return player
        
        if player.vida_atual < 0:
            print("Vida atual não pode ser negativa")
            return player
        
        if player.vida_maxima <= 0:
            print("Vida máxima deve ser maior que zero")
            return player
        
        if player.vida_atual > player.vida_maxima:
            print("Vida atual não pode ser maior que vida máxima")
            return player
        
        if player.forca < 0:
            print("Força não pode ser negativa")
            return player
        
        if player.nivel < 1:
            print("Nível deve ser pelo menos 1")
            return player
        
        if player.experiencia < 0:
            print("Experiência não pode ser negativa")
            return player
        
        try:
            conn = connection_db()
            cursor = conn.cursor()
            
            if player.id_player:
                # Update
                query = """
                    UPDATE Player
                    SET nome = %s, vida_maxima = %s, vida_atual = %s,
                        experiencia = %s, forca = %s, current_chunk_id = %s
                    WHERE id_player = %s
                    RETURNING id_player, nome, vida_maxima, vida_atual,
                              forca, localizacao, nivel, experiencia, current_chunk_id
                """
                cursor.execute(query, (
                    player.nome, player.vida_maxima, player.vida_atual, 
                    player.experiencia, player.forca, int(player.localizacao) if player.localizacao else 1,
                    player.id_player
                ))
            else:
                # Insert
                query = """
                    INSERT INTO Player (nome, vida_maxima, vida_atual, experiencia, forca, current_chunk_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id_player, nome, vida_maxima, vida_atual,
                              forca, localizacao, nivel, experiencia, current_chunk_id
                """
                cursor.execute(query, (
                    player.nome, player.vida_maxima, player.vida_atual, 
                    player.experiencia, player.forca, int(player.localizacao) if player.localizacao else 1
                ))
            
            result = cursor.fetchone()
            
            conn.commit()
            cursor.close()
            conn.close()
            
            if result:
                return Player(
                    id_player=result[0],
                    nome=result[1],
                    vida_maxima=result[2],
                    vida_atual=result[3],
                    forca=result[4],
                    localizacao=result[5] or "",
                    nivel=result[6],
                    experiencia=result[7],
                    current_chunk_id=result[8]
                )
            return None
            
        except Exception as e:
            print(f"Erro ao salvar jogador: {str(e)}")
            return player
    
    def delete(self, id: int) -> bool:
        """Deleta um jogador do banco de dados"""
        try:
            conn = connection_db()
            cursor = conn.cursor()
            
            query = "DELETE FROM Player WHERE id_player = %s"
            cursor.execute(query, (id,))
            
            deleted = cursor.rowcount > 0
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return deleted
            
        except Exception as e:
            print(f"Erro ao deletar jogador {id}: {str(e)}")
            return False
    
    def find_by_name(self, name: str) -> Optional[Player]:
        """Busca um jogador por nome"""
        try:
            conn = connection_db()
            cursor = conn.cursor()
            
            query = """
                SELECT id_player, nome, vida_maxima, vida_atual, forca,
                       localizacao, nivel, experiencia, current_chunk_id
                FROM Player
                WHERE nome = %s
            """
            
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if result:
                return Player(
                    id_player=result[0],
                    nome=result[1],
                    vida_maxima=result[2],
                    vida_atual=result[3],
                    forca=result[4],
                    localizacao=result[5] or "",
                    nivel=result[6],
                    experiencia=result[7],
                    current_chunk_id=result[8]
                )
            return None
            
        except Exception as e:
            print(f"Erro ao buscar jogador por nome {name}: {str(e)}")
            return None
    
    def find_active_players(self) -> List[Player]:
        """Busca jogadores ativos (com vida > 0)"""
        try:
            conn = connection_db()
            cursor = conn.cursor()
            
            query = """
                SELECT id_player, nome, vida_maxima, vida_atual, forca,
                       localizacao, nivel, experiencia, current_chunk_id
                FROM Player
                WHERE vida_atual > 0
                ORDER BY nome
            """
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            players = []
            for row in results:
                players.append(Player(
                    id_player=row[0],
                    nome=row[1],
                    vida_maxima=row[2],
                    vida_atual=row[3],
                    forca=row[4],
                    localizacao=row[5] or "",
                    nivel=row[6],
                    experiencia=row[7],
                    current_chunk_id=row[8]
                ))
            
            return players
            
        except Exception as e:
            print(f"Erro ao buscar jogadores ativos: {str(e)}")
            return [] 
