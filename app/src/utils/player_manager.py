"""
Gerenciador de Sessão do Personagem Global
Mantém dados essenciais do personagem em memória para otimizar performance
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List, Tuple
from src.utils.db_helpers import connection_db
from colorama import Fore

@dataclass
class PlayerSession:
    """Classe para armazenar dados essenciais do personagem ativo na sessão"""
    id_jogador: int
    nome: str
    vida_max: int
    vida_atual: int
    xp: int
    forca: int
    id_chunk_atual: Optional[int] = None
    
    # Dados do chunk atual (evita JOIN desnecessário)
    chunk_bioma: Optional[str] = None
    chunk_mapa_nome: Optional[str] = None
    chunk_mapa_turno: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário para facilitar manipulação"""
        return {
            'id_jogador': self.id_jogador,
            'nome': self.nome,
            'vida_max': self.vida_max,
            'vida_atual': self.vida_atual,
            'xp': self.xp,
            'forca': self.forca,
            'id_chunk_atual': self.id_chunk_atual,
            'chunk_bioma': self.chunk_bioma,
            'chunk_mapa_nome': self.chunk_mapa_nome,
            'chunk_mapa_turno': self.chunk_mapa_turno
        }
    
    def is_alive(self) -> bool:
        """Verifica se o personagem está vivo"""
        return self.vida_atual > 0
    
    def take_damage(self, damage: int) -> bool:
        """Aplica dano ao personagem. Retorna True se ainda está vivo"""
        self.vida_atual = max(0, self.vida_atual - damage)
        return self.is_alive()
    
    def heal(self, amount: int) -> None:
        """Cura o personagem até o máximo de vida"""
        self.vida_atual = min(self.vida_max, self.vida_atual + amount)
    
    def gain_xp(self, amount: int) -> None:
        """Adiciona experiência ao personagem"""
        self.xp += amount


# Variável global para armazenar o personagem ativo
current_player: Optional[PlayerSession] = None


def set_current_player(player_data: PlayerSession) -> None:
    """Define o personagem ativo da sessão"""
    global current_player
    current_player = player_data
    print(f"🎮 Personagem '{player_data.nome}' selecionado!")


def get_current_player() -> Optional[PlayerSession]:
    """Retorna o personagem ativo da sessão"""
    return current_player


def clear_current_player() -> None:
    """Limpa o personagem ativo (logout)"""
    global current_player
    current_player = None


def load_player_by_id(player_id: int) -> Optional[PlayerSession]:
    """
    Carrega um personagem completo do banco de dados com dados do chunk atual
    Otimizado com JOIN para evitar múltiplas queries
    """
    try:
        with connection_db() as conn:
            with conn.cursor() as cursor:
                # Query otimizada com LEFT JOIN para pegar dados do chunk
                cursor.execute("""
                    SELECT 
                        j.id_jogador, j.nome, j.vida_max, j.vida_atual, 
                        j.xp, j.forca, j.id_chunk_atual,
                        c.id_bioma, c.id_mapa_nome, c.id_mapa_turno
                    FROM jogador j
                    LEFT JOIN chunk c ON j.id_chunk_atual = c.numero_chunk
                    WHERE j.id_jogador = %s
                """, (player_id,))
                
                result = cursor.fetchone()
                
                if result:
                    return PlayerSession(
                        id_jogador=result[0],
                        nome=result[1],
                        vida_max=result[2],
                        vida_atual=result[3],
                        xp=result[4],
                        forca=result[5],
                        id_chunk_atual=result[6],
                        chunk_bioma=result[7],
                        chunk_mapa_nome=result[8],
                        chunk_mapa_turno=result[9]
                    )
                return None
                
    except Exception as e:
        print(f"❌ Erro ao carregar personagem {player_id}: {str(e)}")
        return None


def refresh_current_player() -> bool:
    """
    Atualiza os dados do personagem atual do banco de dados
    Útil após operações que modificam o banco
    """
    global current_player
    if not current_player:
        return False
    
    updated_player = load_player_by_id(current_player.id_jogador)
    if updated_player:
        current_player = updated_player
        print("🔄 Dados do personagem atualizados!")
        return True
    else:
        print("❌ Erro ao atualizar dados do personagem")
        return False


def save_player_changes() -> bool:
    """
    Salva as alterações do personagem atual no banco de dados
    Útil após modificações na sessão (vida, XP, etc.)
    """
    global current_player
    if not current_player:
        print("❌ Nenhum personagem ativo para salvar")
        return False
    
    try:
        with connection_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE jogador 
                    SET vida_atual = %s, xp = %s, forca = %s, id_chunk_atual = %s
                    WHERE id_jogador = %s
                """, (
                    current_player.vida_atual,
                    current_player.xp,
                    current_player.forca,
                    current_player.id_chunk_atual,
                    current_player.id_jogador
                ))
                conn.commit()
                print("💾 Dados do personagem salvos no banco!")
                return True
                
    except Exception as e:
        print(f"❌ Erro ao salvar personagem: {str(e)}")
        return False


def get_all_players() -> list:
    """Busca todos os personagens do banco para seleção"""
    try:
        with connection_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id_jogador, nome, vida_max, vida_atual, xp, forca, id_chunk_atual
                    FROM jogador 
                    ORDER BY nome
                """)
                return cursor.fetchall()
    except Exception as e:
        print(f"❌ Erro ao buscar personagens: {str(e)}")
        return []


def create_new_player(nome: str, vida_max: int = 100, forca: int = 10) -> Optional[PlayerSession]:
    """
    Cria um novo personagem no banco de dados
    Retorna o PlayerSession do personagem criado
    """
    try:
        with connection_db() as conn:
            with conn.cursor() as cursor:
                # Para novos personagens, começar no deserto (chunk 1)
                cursor.execute("""
                    INSERT INTO jogador (nome, vida_max, vida_atual, xp, forca, id_chunk_atual)
                    VALUES (%s, %s, %s, 0, %s, 1)
                    RETURNING id_jogador
                """, (nome, vida_max, vida_max, forca))
                
                player_id = cursor.fetchone()[0]
                conn.commit()
                
                # Carrega o personagem recém-criado
                new_player = load_player_by_id(player_id)
                if new_player:
                    print(f"✅ Personagem '{nome}' criado com sucesso!")
                    return new_player
                
    except Exception as e:
        print(f"❌ Erro ao criar personagem: {str(e)}")
        return None


def delete_player(player_id: int) -> bool:
    """
    Deleta um personagem do banco de dados
    Retorna True se deletado com sucesso
    """
    try:
        with connection_db() as conn:
            with conn.cursor() as cursor:
                # Primeiro, verificar se o personagem existe e pegar o nome
                cursor.execute("SELECT nome FROM jogador WHERE id_jogador = %s", (player_id,))
                result = cursor.fetchone()
                
                if not result:
                    print(f"❌ Personagem com ID {player_id} não encontrado!")
                    return False
                
                player_name = result[0]
                
                # Verificar se é o personagem ativo
                current_player = get_current_player()
                if current_player and current_player.id_jogador == player_id:
                    print(f"❌ Não é possível deletar o personagem ativo '{player_name}'!")
                    print("💡 Dica: Troque de personagem primeiro ou saia da sessão.")
                    return False
                
                # Deletar o personagem (CASCADE irá deletar inventário automaticamente)
                cursor.execute("DELETE FROM jogador WHERE id_jogador = %s", (player_id,))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    print(f"🗑️  Personagem '{player_name}' deletado com sucesso!")
                    return True
                else:
                    print(f"❌ Erro ao deletar personagem '{player_name}'!")
                    return False
                
    except Exception as e:
        print(f"❌ Erro ao deletar personagem: {str(e)}")
        return False


def confirm_player_deletion(player_name: str) -> bool:
    """
    Solicita confirmação para deletar um personagem
    Retorna True se confirmado
    """
    print(f"\n⚠️  ATENÇÃO: Você está prestes a deletar o personagem '{player_name}'!")
    print("🗑️  Esta ação é IRREVERSÍVEL e deletará:")
    print("   • Todos os dados do personagem")
    print("   • Todo o inventário do personagem")
    print("   • Todo o progresso salvo")
    print()
    
    while True:
        confirm = input(f"❓ Tem certeza que deseja deletar '{player_name}'? (sim/não): ").strip().lower()
        
        if confirm in ['sim', 's', 'yes', 'y']:
            # Confirmação final
            final_confirm = input(f"🔴 Digite {Fore.RED}'DELETAR'{Fore.RESET} para confirmar definitivamente: ").strip()
            return final_confirm == 'DELETAR'
        elif confirm in ['não', 'nao', 'n', 'no']:
            print("✅ Operação cancelada.")
            return False
        else:
            print("❌ Digite 'sim' ou 'não'.")


def display_player_status(player: Optional[PlayerSession] = None) -> None:
    """Exibe o status do personagem (atual ou especificado)"""
    if not player:
        player = current_player
    
    if not player:
        print("❌ Nenhum personagem ativo")
        return
    
    # Largura da tabela: 50 caracteres internos (suficiente para maior localização possível)
    table_width = 50
    
    # Formatação da localização
    if player.chunk_bioma:
        localizacao = f"{player.chunk_bioma} ({player.chunk_mapa_nome} - {player.chunk_mapa_turno})".replace("_", " ")
    else:
        localizacao = "Desconhecida"
    
    # Formatação da vida
    vida_str = f"{player.vida_atual}/{player.vida_max}"
    
    print(f"""
╔═{'═' * table_width}═╗
║{' STATUS DO PERSONAGEM '.center(table_width)}  ║
╠═{'═' * table_width}═╣
║ Nome: {player.nome:<{table_width-6}} ║
║ Vida: {vida_str:<{table_width-6}} ║
║ XP: {player.xp:<{table_width-4}} ║
║ Força: {player.forca:<{table_width-7}} ║
║ Localização: {localizacao:<{table_width-13}} ║
╚═{'═' * table_width}═╝""")


def get_player_status_lines(player: PlayerSession, is_current: bool = False) -> list:
    """Retorna as linhas da tabela de status como lista de strings"""
    table_width = 50
    
    # Formatação da localização
    if player.chunk_bioma:
        localizacao = f"{player.chunk_bioma} ({player.chunk_mapa_nome} - {player.chunk_mapa_turno})".replace("_", " ")
    else:
        localizacao = "Desconhecida"
    
    # Formatação da vida
    vida_str = f"{player.vida_atual}/{player.vida_max}"
    
    # Título com indicador de personagem atual
    title = " PERSONAGEM ATIVO " if is_current else " STATUS PERSONAGEM "
    
    lines = [
        f"╔═{'═' * table_width}═╗",
        f"║{title.center(table_width)}  ║",
        f"╠═{'═' * table_width}═╣",
        f"║ Nome: {player.nome:<{table_width-6}} ║",
        f"║ Vida: {vida_str:<{table_width-6}} ║",
        f"║ XP: {player.xp:<{table_width-4}} ║",
        f"║ Força: {player.forca:<{table_width-7}} ║",
        f"║ Localização: {localizacao:<{table_width-13}} ║",
        f"╚═{'═' * table_width}═╝"
    ]
    
    return lines


def display_players_grid(players_data: list) -> None:
    """Exibe múltiplos personagens em formato de grid lado a lado"""
    if not players_data:
        print("❌ Nenhum personagem para exibir")
        return
    
    # Detectar largura do terminal (padrão 80 se não conseguir detectar)
    try:
        import os
        terminal_width = os.get_terminal_size().columns
    except:
        terminal_width = 120  # Fallback para terminal padrão mais largo
    
    # Largura de cada tabela + espaçamento
    table_total_width = 52  # 50 internos + 2 bordas
    spacing = 3  # Espaçamento entre tabelas
    
    # Calcular quantas tabelas cabem por linha
    tables_per_line = max(1, (terminal_width + spacing) // (table_total_width + spacing))
    
    # Converter dados brutos em PlayerSession objects
    current_player_obj = get_current_player()
    current_id = current_player_obj.id_jogador if current_player_obj else None
    
    player_sessions = []
    for player_data in players_data:
        # Carregar dados completos do personagem
        player_session = load_player_by_id(player_data[0])
        if player_session:
            player_sessions.append((player_session, player_data[0] == current_id))
    
    # Organizar em linhas
    for i in range(0, len(player_sessions), tables_per_line):
        line_players = player_sessions[i:i + tables_per_line]
        
        # Obter todas as linhas de cada tabela
        all_tables_lines = []
        for player_session, is_current in line_players:
            table_lines = get_player_status_lines(player_session, is_current)
            all_tables_lines.append(table_lines)
        
        # Imprimir linha por linha, combinando as tabelas horizontalmente
        max_lines = max(len(table_lines) for table_lines in all_tables_lines)
        
        for line_idx in range(max_lines):
            line_parts = []
            for table_lines in all_tables_lines:
                if line_idx < len(table_lines):
                    line_parts.append(table_lines[line_idx])
                else:
                    line_parts.append(" " * table_total_width)  # Espaço vazio se tabela acabou
            
            # Juntar as partes com espaçamento
            print((" " * spacing).join(line_parts))
        
        # Espaçamento entre linhas de tabelas
        if i + tables_per_line < len(player_sessions):
            print()  # Linha vazia entre grupos


def get_adjacent_chunks(chunk_id: int, turno: str = 'Dia') -> List[Tuple[int, str]]:
    """
    Retorna os chunks adjacentes ao chunk atual
    Retorna lista de tuplas (chunk_id, bioma)
    """
    try:
        with connection_db() as conn:
            with conn.cursor() as cursor:
                # Busca chunks adjacentes no mesmo turno
                cursor.execute("""
                    SELECT numero_chunk, id_bioma
                    FROM chunk 
                    WHERE id_mapa_turno = %s 
                    AND numero_chunk IN (
                        %s - 1, %s + 1,  -- Horizontal
                        %s - 32, %s + 32  -- Vertical (assumindo mapa 32x32)
                    )
                    ORDER BY numero_chunk
                """, (turno, chunk_id, chunk_id, chunk_id, chunk_id))
                
                return cursor.fetchall()
    except Exception as e:
        print(f"❌ Erro ao buscar chunks adjacentes: {str(e)}")
        return []


def move_player_to_chunk(chunk_id: int) -> bool:
    """
    Move o personagem atual para um novo chunk
    Atualiza tanto a sessão quanto o banco de dados
    """
    global current_player
    if not current_player:
        print("❌ Nenhum personagem ativo")
        return False
    
    try:
        with connection_db() as conn:
            with conn.cursor() as cursor:
                # Verifica se o chunk existe e obtém seus dados
                cursor.execute("""
                    SELECT id_bioma, id_mapa_nome, id_mapa_turno
                    FROM chunk 
                    WHERE numero_chunk = %s
                """, (chunk_id,))
                
                chunk_data = cursor.fetchone()
                if not chunk_data:
                    print(f"❌ Chunk {chunk_id} não encontrado!")
                    return False
                
                # Atualiza o banco de dados
                cursor.execute("""
                    UPDATE jogador 
                    SET id_chunk_atual = %s
                    WHERE id_jogador = %s
                """, (chunk_id, current_player.id_jogador))
                
                # Atualiza a sessão
                current_player.id_chunk_atual = chunk_id
                current_player.chunk_bioma = chunk_data[0]
                current_player.chunk_mapa_nome = chunk_data[1]
                current_player.chunk_mapa_turno = chunk_data[2]
                
                conn.commit()
                print(f"✅ Movido para {chunk_data[0]}!")
                return True
                
    except Exception as e:
        print(f"❌ Erro ao mover personagem: {str(e)}")
        return False


def get_desert_chunk(turno: str = 'Dia') -> Optional[int]:
    """
    Retorna o ID de um chunk de deserto no turno especificado
    """
    try:
        with connection_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT numero_chunk
                    FROM chunk 
                    WHERE id_bioma = 'Deserto' AND id_mapa_turno = %s
                    LIMIT 1
                """, (turno,))
                
                result = cursor.fetchone()
                return result[0] if result else None
                
    except Exception as e:
        print(f"❌ Erro ao buscar chunk de deserto: {str(e)}")
        return None


def ensure_player_location() -> bool:
    """
    Garante que o personagem atual tem uma localização válida
    Se não tiver, coloca no deserto
    """
    global current_player
    if not current_player:
        return False
    
    # Se o personagem não tem localização, coloca no deserto
    if not current_player.id_chunk_atual:
        desert_chunk = get_desert_chunk('Dia')
        if desert_chunk:
            return move_player_to_chunk(desert_chunk)
        else:
            print("❌ Não foi possível encontrar um chunk de deserto!")
            return False
    
    return True 