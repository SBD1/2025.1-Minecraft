"""
Funções auxiliares para exibição na tela
"""

from colorama import Fore, Back, Style
from src.services.interface_service import InterfaceService
from src.utils.player_manager import get_current_player


def clear_terminal():
    """Limpa o terminal"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def players_status():
    """Exibe o status dos jogadores usando InterfaceService Singleton"""
    interface_service = InterfaceService.get_instance()
    
    # Obter estatísticas
    stats = interface_service.get_player_statistics()
    
    print(f"📊 ESTATÍSTICAS DOS JOGADORES")
    print("=" * 40)
    print(f"👥 Total de jogadores: {stats['total']}")
    print(f"🟢 Jogadores ativos: {stats['active']}")
    print(f"📈 Nível médio: {stats['average_level']:.1f}")
    print(f"❤️  Vida média: {stats['average_health']:.1f}")
    print("=" * 40)
    
    # Exibir jogadores ativos
    active_players = interface_service.get_active_players()
    if active_players:
        print("\n🟢 JOGADORES ATIVOS:")
        for player in active_players:
            status_icon = "🎮" if player == get_current_player() else "👤"
            print(f"{status_icon} {player.nome} - Nível {player.nivel} (Vida: {player.vida_atual}/{player.vida_maxima})")
    else:
        print("\n⚠️  Nenhum jogador ativo encontrado")
    
    print()


def format_health_bar(current: int, maximum: int, width: int = 20) -> str:
    """Formata uma barra de vida visual"""
    if maximum <= 0:
        return "░" * width
    
    percentage = current / maximum
    filled = int(width * percentage)
    empty = width - filled
    
    if percentage > 0.6:
        color = Fore.GREEN
    elif percentage > 0.3:
        color = Fore.YELLOW
    else:
        color = Fore.RED
        
    bar = "█" * filled + "░" * empty
    return f"{color}{bar}{Fore.RESET}"


def format_player_card(player) -> str:
    """Formata um card de jogador para exibição"""
    health_bar = format_health_bar(player.vida_atual, player.vida_maxima)
    
    card = f"""
╔══════════════════════════════════════════════════════════════╗
║ {player.nome:<50} ║
╠══════════════════════════════════════════════════════════════╣
║ ❤️  Vida: {player.vida_atual}/{player.vida_maxima} {health_bar} ║
║ ⭐ XP: {player.experiencia:<8} 💪 Força: {player.forca:<8} 📍 Nível: {player.nivel} ║
║ 📍 Localização: Chunk {player.localizacao or 'Desconhecida':<35} ║
╚══════════════════════════════════════════════════════════════╝
"""
    return card


def display_player_list(players, title: str = "LISTA DE JOGADORES"):
    """Exibe uma lista formatada de jogadores"""
    print(f"📋 {title}")
    print("=" * 60)
    
    if not players:
        print("⚠️  Nenhum jogador encontrado")
        return
    
    for i, player in enumerate(players, 1):
        print(f"{i}. {player.nome} - Nível {player.nivel}")
        print(f"   ❤️  {player.vida_atual}/{player.vida_maxima} | ⭐ {player.experiencia} XP | 💪 {player.forca}")
        if player.localizacao:
            print(f"   📍 Chunk {player.localizacao}")
        print()
    
    print("=" * 60)