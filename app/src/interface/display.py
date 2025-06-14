import os
import time
from colorama import Fore, init
from src.utils.screen_helpers import clear_terminal, players_status
from src.utils.db_helpers import connection_db
from src.utils.player_manager import (
    get_current_player, set_current_player, clear_current_player,
    load_player_by_id, get_all_players, create_new_player,
    display_player_status, save_player_changes, display_players_grid,
    delete_player, confirm_player_deletion
)

init(autoreset=True)

MINECRAFT_ART = [
    "⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️",
    "⬛️⬛️⬛️⬛️⬛️🟫⬛️ M I N E C R A F T ⬛️⬛️🟫⬛️⬛️⬛⬛️⬛️",
    "⬛️⬛️⬛️⬛️⬛️🟫  F G A ⬛️ 2 0 2 5 / 1 ⬛️🟫⬛️⬛️⬛️⬛️⬛️",
    "⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️ "
]


def mostrar_creeper():
    """Exibe o Creeper na posição especificada."""

    largura_terminal = os.get_terminal_size().columns
    largura_creeper = 10 
    posicao = largura_terminal // 2 - largura_creeper // 2

    for linha in MINECRAFT_ART:
        print(" " * posicao + linha + " " * (largura_terminal - posicao - largura_creeper))

def tela_inicial():
    clear_terminal()
    mostrar_creeper()
    time.sleep(5)
    menu_inicial()

def exibir_titulo():
    """Exibe o título do jogo"""
    print("╔══════════════════════════════════════════════════╗")
    print("║         🟩 MINECRAFT - FGA - 2025/1              ║")
    print("║              Python Edition                      ║") 
    print("╚══════════════════════════════════════════════════╝")
    print()

def exibir_jogador_atual():
    """Exibe informações do personagem ativo no topo do menu"""
    current_player = get_current_player()
    if current_player:
        print(f"🎮 Personagem ativo: {Fore.GREEN}{current_player.nome}{Fore.RESET}")
        print(f"❤️  Vida: {current_player.vida_atual}/{current_player.vida_max} | "
              f"⭐ XP: {current_player.xp} | 💪 Força: {current_player.forca}")
        if current_player.chunk_bioma:
            print(f"📍 Localização: {current_player.chunk_bioma} ({current_player.chunk_mapa_nome} - {current_player.chunk_mapa_turno})")
        print("-" * 50)
    else:
        print(f"{Fore.YELLOW}⚠️  Nenhum personagem selecionado{Fore.RESET}")
        print("-" * 50)

def menu_inicial():
    """Menu principal do jogo em loop até o usuário escolher sair"""
    while True:
        clear_terminal()
        exibir_titulo()
        exibir_jogador_atual()
        
        current_player = get_current_player()
        
        # Opções do menu
        print("📋 MENU PRINCIPAL:")
        print()
        
        if current_player:
            print("1. 🎮 Iniciar jogo")
            print("2. 📊 Ver status detalhado")
            print("3. 💾 Salvar progresso")
            print("4. 👥 Trocar personagem")
            print("5. 📋 Lista de personagens")
            print("6. ➕ Criar novo personagem")
            print("7. 🚪 Sair")
        else:
            print("1. 👥 Selecionar personagem")
            print("2. ➕ Criar novo personagem") 
            print("3. 📋 Lista de personagens")
            print("4. 🚪 Sair")
        
        print()
        opcao = input("🎯 Escolha uma opção: ").strip()
        
        if current_player:
            # Menu com personagem ativo
            if opcao == "1":
                iniciar_jogo()
            elif opcao == "2":
                ver_status_detalhado()
            elif opcao == "3":
                salvar_progresso()
            elif opcao == "4":
                trocar_jogador()
            elif opcao == "5":
                listar_jogadores()
            elif opcao == "6":
                criar_jogador()
            elif opcao == "7":
                sair_jogo()
                break
            else:
                print(f"{Fore.RED}❌ Opção inválida!{Fore.RESET}")
                input("⏳ Pressione Enter para continuar...")
        else:
            # Menu sem personagem ativo
            if opcao == "1":
                selecionar_jogador()
            elif opcao == "2":
                criar_jogador()
            elif opcao == "3":
                listar_jogadores()
            elif opcao == "4":
                sair_jogo()
                break
            else:
                print(f"{Fore.RED}❌ Opção inválida!{Fore.RESET}")
                input("⏳ Pressione Enter para continuar...")

def iniciar_jogo():
    """Inicia o jogo com o personagem atual"""
    current_player = get_current_player()
    if not current_player:
        print(f"{Fore.RED}❌ Nenhum personagem selecionado!{Fore.RESET}")
        input("⏳ Pressione Enter para continuar...")
        return
    
    print(f"🎮 Iniciando jogo com {current_player.nome}...")
    print("🚧 Em desenvolvimento...")
    input("⏳ Pressione Enter para voltar ao menu...")

def ver_status_detalhado():
    """Exibe status detalhado do personagem atual"""
    clear_terminal()
    display_player_status()
    input("\n⏳ Pressione Enter para voltar ao menu...")

def salvar_progresso():
    """Salva o progresso do personagem atual"""
    if save_player_changes():
        print(f"{Fore.GREEN}✅ Progresso salvo com sucesso!{Fore.RESET}")
    else:
        print(f"{Fore.RED}❌ Erro ao salvar progresso!{Fore.RESET}")
    input("⏳ Pressione Enter para continuar...")

def trocar_jogador():
    """Permite trocar para outro personagem"""
    clear_current_player()
    selecionar_jogador()

def selecionar_jogador():
    """Interface para seleção de personagem"""
    clear_terminal()
    print("👥 SELEÇÃO DE PERSONAGEM")
    print("=" * 40)
    
    players = get_all_players()
    
    if not players:
        print(f"{Fore.YELLOW}⚠️  Nenhum personagem encontrado!{Fore.RESET}")
        print("Crie um novo personagem primeiro.")
        input("⏳ Pressione Enter para continuar...")
        return
    
    print("Personagens disponíveis:")
    print()
    
    for i, player in enumerate(players, 1):
        print(f"{i}. {player[1]} (Vida: {player[3]}/{player[2]} | XP: {player[4]} | Força: {player[5]})")
    
    print()
    try:
        escolha = input("🎯 Digite o número do personagem (ou 'c' para cancelar): ").strip()
        
        if escolha.lower() == 'c':
            return
        
        indice = int(escolha) - 1
        
        if 0 <= indice < len(players):
            player_id = players[indice][0]
            player_name = players[indice][1]
            
            # Verificar se é o personagem atual
            current_player = get_current_player()
            current_id = current_player.id_jogador if current_player else None
            
            if current_id and player_id == current_id:
                print(f"{Fore.YELLOW}⚠️  '{player_name}' já é o personagem ativo!{Fore.RESET}")
                input("⏳ Pressione Enter para continuar...")
                return
            
            # Carregar e definir personagem
            player_session = load_player_by_id(player_id)
            
            if player_session:
                set_current_player(player_session)
                print(f"{Fore.GREEN}✅ Personagem '{player_name}' selecionado com sucesso!{Fore.RESET}")
                input("⏳ Pressione Enter para continuar...")
                return  # Sair da função e voltar ao menu principal
            else:
                print(f"{Fore.RED}❌ Erro ao carregar personagem!{Fore.RESET}")
                input("⏳ Pressione Enter para continuar...")
                return
        else:
            print(f"{Fore.RED}❌ Número inválido! Digite um número entre 1 e {len(players)}.{Fore.RESET}")
            input("⏳ Pressione Enter para continuar...")
            
    except ValueError:
        print(f"{Fore.RED}❌ Digite apenas números!{Fore.RESET}")
        input("⏳ Pressione Enter para continuar...")

def criar_jogador():
    """Interface para criação de novo personagem"""
    clear_terminal()
    print("➕ CRIAR NOVO PERSONAGEM")
    print("=" * 40)
    
    nome = input("📝 Digite o nome do personagem: ").strip()
    
    if not nome:
        print(f"{Fore.RED}❌ Nome não pode estar vazio!{Fore.RESET}")
        input("⏳ Pressione Enter para continuar...")
        return
    
    # Verificar se nome já existe
    players = get_all_players()
    if any(player[1].lower() == nome.lower() for player in players):
        print(f"{Fore.RED}❌ Já existe um personagem com esse nome!{Fore.RESET}")
        input("⏳ Pressione Enter para continuar...")
        return
    
    print(f"\n⚙️ Status iniciais:")
    print(f"❤️  Vida máxima: 100")
    print(f"💪 Força inicial: 10")
    print(f"⭐ XP inicial: 0")
    
    # Criar personagem com valores padrão fixos
    new_player = create_new_player(nome, vida_max=100, forca=10)
    
    if new_player:
        print(f"\n{Fore.GREEN}✅ Personagem '{nome}' criado com sucesso!{Fore.RESET}")
        escolha = input("🎮 Deseja selecionar este personagem agora? (s/n): ").strip().lower()
        
        if escolha == 's':
            set_current_player(new_player)
        
    input("⏳ Pressione Enter para continuar...")

def listar_jogadores():
    """Lista todos os personagens"""
    clear_terminal()
    print("📋 LISTA DE PERSONAGENS")
    print("=" * 70)
    print()
    
    players = get_all_players()
    
    if not players:
        print(f"{Fore.YELLOW}⚠️  Nenhum personagem cadastrado.{Fore.RESET}")
        print("Use a opção 'Criar novo personagem' para adicionar personagens.")
        print()
        input("⏳ Pressione Enter para voltar ao menu...")
        return
    
    print(f"📊 Total de personagens: {len(players)}")
    print()
    
    # Exibir personagens em formato de grid com tabelas
    display_players_grid(players)
    
    print()
    print("=" * 70)
    print("⚙️  OPÇÕES:")
    print("1. 🎮 Selecionar personagem")
    print("2. 🗑️  Deletar personagem")
    print("3. 🔙 Voltar ao menu")
    print()
    
    while True:
        try:
            opcao = input("🎯 Escolha uma opção: ").strip()
            
            if opcao == "1":
                # Mostrar lista numerada para seleção
                clear_terminal()
                print("👥 SELEÇÃO DE PERSONAGEM")
                print("=" * 40)
                print()
                
                current_player = get_current_player()
                current_id = current_player.id_jogador if current_player else None
                
                print("Personagens disponíveis:")
                for i, player in enumerate(players, 1):
                    status_icon = "🎮" if player[0] == current_id else "👤"
                    print(f"{i}. {status_icon} {player[1]} (Vida: {player[3]}/{player[2]} | XP: {player[4]} | Força: {player[5]})")
                
                print()
                
                while True:
                    try:
                        escolha = input("🎯 Digite o número do personagem (ou 'c' para cancelar): ").strip()
                        
                        if escolha.lower() == 'c':
                            break
                        
                        indice = int(escolha) - 1
                        
                        if 0 <= indice < len(players):
                            player_id = players[indice][0]
                            player_name = players[indice][1]
                            
                            # Verificar se é o personagem atual
                            if current_id and player_id == current_id:
                                print(f"{Fore.YELLOW}⚠️  '{player_name}' já é o personagem ativo!{Fore.RESET}")
                                input("⏳ Pressione Enter para continuar...")
                                return
                            
                            # Carregar e definir personagem
                            player_session = load_player_by_id(player_id)
                            
                            if player_session:
                                set_current_player(player_session)
                                print(f"{Fore.GREEN}✅ Personagem '{player_name}' selecionado com sucesso!{Fore.RESET}")
                                input("⏳ Pressione Enter para continuar...")
                                return  # Sair da função e voltar ao menu principal
                            else:
                                print(f"{Fore.RED}❌ Erro ao carregar personagem!{Fore.RESET}")
                                input("⏳ Pressione Enter para continuar...")
                                return
                        else:
                            print(f"{Fore.RED}❌ Número inválido! Digite um número entre 1 e {len(players)}.{Fore.RESET}")
                            
                    except ValueError:
                        print(f"{Fore.RED}❌ Digite apenas números válidos!{Fore.RESET}")
                
                # Voltar para a lista principal
                break
                
            elif opcao == "2":
                # Mostrar lista numerada para deletar
                clear_terminal()
                print("🗑️  DELETAR PERSONAGEM")
                print("=" * 40)
                print()
                
                current_player = get_current_player()
                current_id = current_player.id_jogador if current_player else None
                
                print("Personagens disponíveis para deletar:")
                for i, player in enumerate(players, 1):
                    status_icon = "🎮" if player[0] == current_id else "👤"
                    print(f"{i}. {status_icon} {player[1]} (Vida: {player[3]}/{player[2]} | XP: {player[4]} | Força: {player[5]})")
                
                print()
                
                while True:
                    try:
                        escolha = input("🗑️  Digite o número do personagem para deletar (ou 'c' para cancelar): ").strip()
                        
                        if escolha.lower() == 'c':
                            break
                        
                        indice = int(escolha) - 1
                        
                        if 0 <= indice < len(players):
                            player_id = players[indice][0]
                            player_name = players[indice][1]
                            
                            # Verificar se é o personagem atual
                            if current_id and player_id == current_id:
                                print(f"{Fore.RED}❌ Não é possível deletar o personagem ativo '{player_name}'!{Fore.RESET}")
                                print("💡 Dica: Troque de personagem primeiro ou saia da sessão.")
                                input("⏳ Pressione Enter para continuar...")
                                return
                            
                            # Confirmar deleção
                            if confirm_player_deletion(player_name):
                                # Deletar personagem
                                if delete_player(player_id):
                                    print(f"{Fore.GREEN}✅ Personagem '{player_name}' deletado com sucesso!{Fore.RESET}")
                                    input("⏳ Pressione Enter para continuar...")
                                    return  # Sair da função e voltar ao menu principal
                                else:
                                    print(f"{Fore.RED}❌ Erro ao deletar personagem!{Fore.RESET}")
                                    input("⏳ Pressione Enter para continuar...")
                                    return
                            else:
                                print("✅ Operação cancelada pelo usuário.")
                                input("⏳ Pressione Enter para continuar...")
                                return
                        else:
                            print(f"{Fore.RED}❌ Número inválido! Digite um número entre 1 e {len(players)}.{Fore.RESET}")
                            
                    except ValueError:
                        print(f"{Fore.RED}❌ Digite apenas números válidos!{Fore.RESET}")
                
                # Voltar para a lista principal
                break
                
            elif opcao == "3":
                return  # Voltar ao menu principal
            else:
                print(f"{Fore.RED}❌ Opção inválida! Digite 1, 2 ou 3.{Fore.RESET}")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⚠️  Operação cancelada.{Fore.RESET}")
            return

def sair_jogo():
    """Encerra o jogo"""
    current_player = get_current_player()
    
    if current_player:
        print(f"👋 Encerrando sessão de {current_player.nome}...")
        save_player_changes()  # Salva automaticamente ao sair
        clear_current_player()
    
    print("🚪 Saindo do Minecraft")
    print("Até a próxima! 🎮")