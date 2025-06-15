"""
Gerenciador de Sessão do Personagem Global
Mantém dados essenciais do personagem em memória para otimizar performance
"""

from typing import Optional, List, Tuple
from src.models.player import Player
from src.models.chunk import Chunk
from src.services.interface_service import InterfaceService
from colorama import Fore


# Variável global para armazenar o personagem ativo
current_player: Optional[Player] = None


def set_current_player(player_data: Player) -> None:
    """Define o personagem ativo da sessão"""
    global current_player
    current_player = player_data
    print(f"🎮 Personagem '{player_data.nome}' selecionado!")

def get_current_player() -> Optional[Player]:
    """Retorna o personagem ativo da sessão"""
    return current_player

def clear_current_player() -> None:
    """Limpa o personagem ativo (logout)"""
    global current_player
    current_player = None

def load_player_by_id(player_id: int) -> Optional[Player]:
    """
    Carrega um personagem completo do banco de dados usando repositório
    """
    try:
        interface_service = InterfaceService.get_instance()
        player = interface_service.get_player_by_id(player_id)
        
        if player:
            print(f"✅ Personagem '{player.nome}' carregado com sucesso!")
            return player
        else:
            print(f"❌ Personagem com ID {player_id} não encontrado!")
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
    Salva as alterações do personagem atual no banco de dados usando repositório
    """
    global current_player
    if not current_player:
        print("❌ Nenhum personagem ativo para salvar")
        return False
    
    try:
        interface_service = InterfaceService.get_instance()
        saved_player = interface_service.save_player(current_player)
        
        if saved_player:
            current_player = saved_player
            print("💾 Dados do personagem salvos no banco!")
            return True
        else:
            print("❌ Erro ao salvar personagem")
            return False
                
    except Exception as e:
        print(f"❌ Erro ao salvar personagem: {str(e)}")
        return False

def get_all_players() -> List[Player]:
    """Busca todos os personagens do banco usando repositório"""
    try:
        interface_service = InterfaceService.get_instance()
        players = interface_service.get_all_players()
        return players
    except Exception as e:
        print(f"❌ Erro ao buscar personagens: {str(e)}")
        return []

def create_new_player(nome: str, vida_max: int = 100, forca: int = 10) -> Optional[Player]:
    """
    Cria um novo personagem no banco de dados usando repositório
    """
    try:
        interface_service = InterfaceService.get_instance()
        new_player = interface_service.create_player(nome, vida_max, forca)
        
        if new_player:
            print(f"✅ Personagem '{nome}' criado com sucesso!")
            return new_player
        else:
            print(f"❌ Erro ao criar personagem '{nome}' ou nome já existe!")
            return None
                
    except Exception as e:
        print(f"❌ Erro ao criar personagem: {str(e)}")
        return None

def delete_player(player_id: int) -> bool:
    """
    Deleta um personagem do banco de dados usando repositório
    """
    try:
        interface_service = InterfaceService.get_instance()
        
        # Primeiro, verificar se o personagem existe
        player = interface_service.get_player_by_id(player_id)
        
        if not player:
            print(f"❌ Personagem com ID {player_id} não encontrado!")
            return False
        
        # Verificar se é o personagem ativo
        current_player = get_current_player()
        if current_player and current_player.id_jogador == player_id:
            print(f"❌ Não é possível deletar o personagem ativo '{player.nome}'!")
            print("💡 Dica: Troque de personagem primeiro ou saia da sessão.")
            return False
        
        # Deletar o personagem
        if interface_service.delete_player(player_id):
            print(f"🗑️  Personagem '{player.nome}' deletado com sucesso!")
            return True
        else:
            print(f"❌ Erro ao deletar personagem '{player.nome}'!")
            return False
                
    except Exception as e:
        print(f"❌ Erro ao deletar personagem: {str(e)}")
        return False

def confirm_player_deletion(player_name: str) -> bool:
    """Confirma a deleção de um personagem com o usuário"""
    print(f"\n⚠️  ATENÇÃO: Você está prestes a deletar o personagem '{player_name}'!")
    print("Esta ação é IRREVERSÍVEL e todos os dados do personagem serão perdidos.")
    print()
    
    while True:
        confirmacao = input("❓ Tem certeza que deseja continuar? (sim/não): ").strip().lower()
        
        if confirmacao in ['sim', 's', 'yes', 'y']:
            return True
        elif confirmacao in ['não', 'nao', 'n', 'no']:
            return False
        else:
            print("❌ Digite 'sim' ou 'não'.")

def display_player_status(player: Optional[Player] = None) -> None:
    """Exibe o status do personagem (atual ou especificado)"""
    if not player:
        player = get_current_player()
    
    if not player:
        print("❌ Nenhum personagem para exibir")
        return
    
    # Usar métodos da model para formatação
    localizacao = f"Chunk {player.localizacao}" if player.localizacao else "Desconhecida"
    vida_str = f"{player.vida_atual}/{player.vida_maxima}"
    
    table_width = 50
    print(f"""
╔═{'═' * table_width}═╗
║{' STATUS PERSONAGEM '.center(table_width)}  ║
╠═{'═' * table_width}═╣
║ Nome: {player.nome:<{table_width-6}} ║
║ Vida: {vida_str:<{table_width-6}} ║
║ XP: {player.experiencia:<{table_width-4}} ║
║ Força: {player.forca:<{table_width-7}} ║
║ Localização: {localizacao:<{table_width-13}} ║
╚═{'═' * table_width}═╝""")

def get_player_status_lines(player: Player, is_current: bool = False) -> list:
    """Retorna as linhas da tabela de status como lista de strings"""
    table_width = 50
    
    # Usar métodos da model para formatação
    localizacao = f"Chunk {player.localizacao}" if player.localizacao else "Desconhecida"
    vida_str = f"{player.vida_atual}/{player.vida_maxima}"
    
    # Título com indicador de personagem atual
    title = " PERSONAGEM ATIVO " if is_current else " STATUS PERSONAGEM "
    
    lines = [
        f"╔═{'═' * table_width}═╗",
        f"║{title.center(table_width)}  ║",
        f"╠═{'═' * table_width}═╣",
        f"║ Nome: {player.nome:<{table_width-6}} ║",
        f"║ Vida: {vida_str:<{table_width-6}} ║",
        f"║ XP: {player.experiencia:<{table_width-4}} ║",
        f"║ Força: {player.forca:<{table_width-7}} ║",
        f"║ Localização: {localizacao:<{table_width-13}} ║",
        f"╚═{'═' * table_width}═╝"
    ]
    
    return lines

def display_players_grid(players_data: List[Player]) -> None:
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
    
    # Obter personagem atual
    current_player_obj = get_current_player()
    current_id = current_player_obj.id_jogador if current_player_obj else None
    
    # Preparar dados dos jogadores
    player_sessions = []
    for player in players_data:
        is_current = current_id and player.id_jogador == current_id
        player_sessions.append((player, is_current))
    
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
    Retorna os chunks adjacentes ao chunk atual usando repositório
    Retorna lista de tuplas (chunk_id, bioma)
    """
    try:
        interface_service = InterfaceService.get_instance()
        return interface_service.get_adjacent_chunks(chunk_id, turno)
    except Exception as e:
        print(f"❌ Erro ao buscar chunks adjacentes: {str(e)}")
        return []

def move_player_to_chunk(chunk_id: int) -> bool:
    """
    Move o personagem atual para um novo chunk usando repositórios
    """
    global current_player
    if not current_player:
        print("❌ Nenhum personagem ativo")
        return False
    
    try:
        interface_service = InterfaceService.get_instance()
        updated_player = interface_service.move_player_to_chunk(current_player, chunk_id)
        
        if updated_player:
            current_player = updated_player
            print(f"✅ Movido para chunk {chunk_id}!")
            return True
        else:
            print(f"❌ Erro ao mover para chunk {chunk_id}!")
            return False
                
    except Exception as e:
        print(f"❌ Erro ao mover personagem: {str(e)}")
        return False

def get_desert_chunk(turno: str = 'Dia') -> Optional[int]:
    """
    Retorna o ID de um chunk de deserto no turno especificado usando repositório
    """
    try:
        interface_service = InterfaceService.get_instance()
        return interface_service.get_desert_chunk(turno)
    except Exception as e:
        print(f"❌ Erro ao buscar chunk de deserto: {str(e)}")
        return None

def ensure_player_location() -> bool:
    """
    Garante que o personagem atual tem uma localização válida usando repositórios
    """
    global current_player
    if not current_player:
        return False
    
    try:
        interface_service = InterfaceService.get_instance()
        return interface_service.ensure_player_location(current_player)
    except Exception as e:
        print(f"❌ Erro ao garantir localização: {str(e)}")
        return False
