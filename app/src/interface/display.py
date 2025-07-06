import os
import time
from colorama import Fore, init
from src.utils.screen_helpers import clear_terminal, players_status
from src.services.interface_service import InterfaceService
from src.utils.player_manager import (
    get_current_player, set_current_player, clear_current_player,
    load_player_by_id, get_all_players, create_new_player,
    display_player_status, save_player_changes, display_players_grid,
    delete_player, confirm_player_deletion, get_adjacent_chunks,
    move_player_to_chunk, ensure_player_location
)
import re

init(autoreset=True)

MINECRAFT_ART = [
    "⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️",
    "⬛️⬛️⬛️⬛️⬛️🟫⬛️ M I N E C R A F T ⬛️⬛️🟫⬛️⬛️⬛⬛️⬛️",
    "⬛️⬛️⬛️⬛️⬛️🟫  F G A ⬛️ 2 0 2 5 / 1 ⬛️🟫⬛️⬛️⬛️⬛️⬛️",
    "⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️ "
]


def mostrar_logo():
    """Exibe o logo na posição especificada."""

    largura_terminal = os.get_terminal_size().columns
    largura_logo = 10 
    posicao = largura_terminal // 2 - largura_logo // 2

    for linha in MINECRAFT_ART:
        print(" " * posicao + linha + " " * (largura_terminal - posicao - largura_logo))

def tela_inicial():
    clear_terminal()
    mostrar_logo()
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
        print(f"❤️  Vida: {current_player.vida_atual}/{current_player.vida_maxima} | "
              f"⭐ XP: {current_player.experiencia} | 💪 Força: {current_player.forca}")
        if current_player.localizacao:
            print(f"📍 Localização: Chunk {current_player.localizacao}")
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

def exibir_localizacao_atual():
    """Exibe a localização atual do personagem de forma detalhada"""
    current_player = get_current_player()
    if not current_player:
        return
    
    print("=" * 60)
    print(f"🎮 JOGANDO COM: {Fore.GREEN}{current_player.nome}{Fore.RESET}")
    print("=" * 60)
    
    # Exibir informações de localização
    if current_player.localizacao:
        print(f"📍 CHUNK: {current_player.localizacao}")
        
        # Buscar informações do chunk usando InterfaceService Singleton
        interface_service = InterfaceService.get_instance()
        chunk = interface_service.get_chunk_by_id(extract_chunk_id_from_location(current_player.localizacao))
        
        if chunk:
            bioma_emoji = {
                'Deserto': '🏜️',
                'Oceano': '🌊',
                'Selva': '🌴',
                'Floresta': '🌲'
            }
            
            # Get bioma name by ID
            bioma_name = str(chunk.id_bioma)  # Default to ID if name not found
            try:
                bioma = interface_service.get_bioma_by_id(chunk.id_bioma)
                if bioma:
                    bioma_name = bioma.nome
            except Exception:
                # If we can't get bioma info, use the ID
                pass
            
            emoji = bioma_emoji.get(bioma_name, '📍')
            
            # Get turno information from the map
            turno_display = 'Dia'  # Default
            turno_emoji = '☀️'  # Default
            
            try:
                # Get map information using the chunk's id_mapa
                mapa = interface_service.get_map_by_id(chunk.id_mapa)
                if mapa:
                    turno_display = mapa.turno.value
                    turno_emoji = '☀️' if mapa.turno.value == 'Dia' else '🌙'
            except Exception:
                # If we can't get map info, use defaults
                pass
            
            print(f"{emoji} BIOMA: {Fore.YELLOW}{bioma_name}{Fore.RESET}")
            print(f"{turno_emoji} TURNO: {turno_display}")
        else:
            print(f"{Fore.YELLOW}⚠️  Informações do chunk não disponíveis{Fore.RESET}")
    else:
        print(f"{Fore.RED}❌ Localização desconhecida{Fore.RESET}")
    
    print("=" * 60)

def determinar_direcao(current_chunk: int, target_chunk: int) -> str:
    """Determina a direção de movimento baseada na diferença entre chunks"""
    diff = target_chunk - current_chunk
    
    # Assumindo que os chunks são organizados em uma grade 32x32
    # Chunks adjacentes horizontalmente têm diferença de ±1
    # Chunks adjacentes verticalmente têm diferença de ±32
    
    if diff == 1:
        return "➡️ Direita"
    elif diff == -1:
        return "⬅️ Esquerda"
    elif diff == 32:
        return "⬇️ Baixo"
    elif diff == -32:
        return "⬆️ Cima"
    elif diff > 1 and diff < 32:
        return "➡️ Direita (distante)"
    elif diff < -1 and diff > -32:
        return "⬅️ Esquerda (distante)"
    elif diff > 32:
        return "⬇️ Baixo (distante)"
    elif diff < -32:
        return "⬆️ Cima (distante)"
    else:
        return "📍 Direção"

def exibir_opcoes_movimento():
    """Exibe as opções de movimento disponíveis com direções"""
    current_player = get_current_player()
    if not current_player or not current_player.localizacao:
        print(f"{Fore.RED}❌ Não é possível mover - localização inválida{Fore.RESET}")
        return []
    
    # Usar InterfaceService Singleton
    interface_service = InterfaceService.get_instance()
    adjacent_chunks = interface_service.get_adjacent_chunks(extract_chunk_id_from_location(current_player.localizacao), 'Dia')
    
    if not adjacent_chunks:
        print(f"{Fore.YELLOW}⚠️  Nenhuma direção disponível para movimento{Fore.RESET}")
        return []
    
    print("🚶 OPÇÕES DE MOVIMENTO:")
    print("-" * 40)
    
    # Determinar direções baseado na diferença de chunk_id
    current_chunk = extract_chunk_id_from_location(current_player.localizacao)
    directions = []
    
    for chunk_id, bioma in adjacent_chunks:
        direction = determinar_direcao(current_chunk, chunk_id)
        directions.append((chunk_id, bioma, direction))
    
    # Ordenar por direção (cima, baixo, esquerda, direita)
    direction_order = {"⬆️ Cima": 0, "⬇️ Baixo": 1, "⬅️ Esquerda": 2, "➡️ Direita": 3, "📍 Direção": 4}
    directions.sort(key=lambda x: direction_order.get(x[2].split()[0], 5))
    
    bioma_emoji = {
        'Deserto': '🏜️',
        'Oceano': '🌊',
        'Selva': '🌴',
        'Floresta': '🌲'
    }
    
    for i, (chunk_id, bioma, direction) in enumerate(directions, 1):
        # Get bioma name by ID if bioma is a number
        bioma_name = bioma
        if isinstance(bioma, int):
            try:
                bioma_obj = interface_service.get_bioma_by_id(bioma)
                if bioma_obj:
                    bioma_name = bioma_obj.nome
            except Exception:
                bioma_name = str(bioma)
        
        emoji = bioma_emoji.get(bioma_name, '📍')
        print(f"{i}. {direction} - {emoji} {bioma_name} (Chunk {chunk_id})")
    
    return [(chunk_id, bioma) for chunk_id, bioma, _ in directions]

def iniciar_jogo():
    """Inicia o jogo com o personagem atual"""
    current_player = get_current_player()
    if not current_player:
        print(f"{Fore.RED}❌ Nenhum personagem selecionado!{Fore.RESET}")
        input("⏳ Pressione Enter para continuar...")
        return
    
    # Usar InterfaceService Singleton para garantir localização
    interface_service = InterfaceService.get_instance()
    if not interface_service.ensure_player_location(current_player):
        print(f"{Fore.RED}❌ Erro ao definir localização do personagem!{Fore.RESET}")
        input("⏳ Pressione Enter para continuar...")
        return
    
    # Loop principal do jogo
    while True:
        clear_terminal()
        exibir_titulo()
        exibir_localizacao_atual()
        
        # Exibir status do personagem
        print(f"❤️  Vida: {current_player.vida_atual}/{current_player.vida_maxima}")
        print(f"⭐ XP: {current_player.experiencia} | 💪 Força: {current_player.forca}")
        print()
        
        # Exibir opções de movimento
        adjacent_chunks = exibir_opcoes_movimento()
        
        print()
        print("🎮 OPÇÕES DO JOGO:")
        print("1-4. Mover para direção")
        print("5. 💾 Salvar progresso")
        print("6. 📊 Ver status detalhado")
        print("7. 🔙 Voltar ao menu principal")
        print()
        
        try:
            opcao = input("🎯 Escolha uma opção: ").strip()
            
            if opcao in ['1', '2', '3', '4']:
                # Movimento
                if adjacent_chunks:
                    indice = int(opcao) - 1
                    if 0 <= indice < len(adjacent_chunks):
                        chunk_id, bioma = adjacent_chunks[indice]
                        
                        # Verificar se há mudança de bioma
                        current_bioma = None
                        try:
                            # Buscar o bioma atual do chunk onde o jogador está
                            current_chunk = interface_service.get_chunk_by_id(extract_chunk_id_from_location(current_player.localizacao))
                            if current_chunk:
                                current_bioma = current_chunk.id_bioma
                        except Exception:
                            # Se não conseguir determinar o bioma atual, assumir que há mudança
                            current_bioma = None
                        
                        print(f"🚶 Movendo...")
                        
                        # Usar InterfaceService Singleton para mover
                        updated_player = interface_service.move_player_to_chunk(current_player, chunk_id)
                        if updated_player:
                            current_player = updated_player
                            set_current_player(updated_player)
                            
                            # Informar apenas se houve mudança de bioma
                            if current_bioma and current_bioma != bioma:
                                print(f"✅ Chegou em {bioma}!")
                            elif not current_bioma:
                                # Se não conseguimos determinar o bioma anterior, sempre informar
                                print(f"✅ Chegou em {bioma}!")
                            else:
                                print(f"✅ Movimento realizado!")
                            
                            input("⏳ Pressione Enter para continuar...")
                        else:
                            print(f"❌ Erro ao mover!")
                            input("⏳ Pressione Enter para continuar...")
                    else:
                        print(f"{Fore.RED}❌ Opção inválida!{Fore.RESET}")
                        input("⏳ Pressione Enter para continuar...")
                else:
                    print(f"{Fore.YELLOW}⚠️  Nenhuma direção disponível{Fore.RESET}")
                    input("⏳ Pressione Enter para continuar...")
                    
            elif opcao == "5":
                # Salvar progresso
                if interface_service.save_player(current_player):
                    current_player = interface_service.get_player_by_id(current_player.id_player)
                    set_current_player(current_player)
                    print(f"{Fore.GREEN}✅ Progresso salvo com sucesso!{Fore.RESET}")
                else:
                    print(f"{Fore.RED}❌ Erro ao salvar progresso!{Fore.RESET}")
                input("⏳ Pressione Enter para continuar...")
                
            elif opcao == "6":
                # Ver status detalhado
                clear_terminal()
                display_player_status()
                input("\n⏳ Pressione Enter para continuar...")
                
            elif opcao == "7":
                # Voltar ao menu principal
                print("🔙 Voltando ao menu principal...")
                break
                
            else:
                print(f"{Fore.RED}❌ Opção inválida!{Fore.RESET}")
                input("⏳ Pressione Enter para continuar...")
                
        except ValueError:
            print(f"{Fore.RED}❌ Digite apenas números válidos!{Fore.RESET}")
            input("⏳ Pressione Enter para continuar...")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⚠️  Jogo interrompido.{Fore.RESET}")
            break

def ver_status_detalhado():
    """Exibe status detalhado do personagem atual"""
    clear_terminal()
    display_player_status()
    input("\n⏳ Pressione Enter para voltar ao menu...")

def salvar_progresso():
    """Salva o progresso do personagem atual"""
    current_player = get_current_player()
    if not current_player:
        print(f"{Fore.RED}❌ Nenhum personagem ativo!{Fore.RESET}")
        input("⏳ Pressione Enter para continuar...")
        return
    
    interface_service = InterfaceService.get_instance()
    if interface_service.save_player(current_player):
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
    
    # Usar InterfaceService Singleton
    interface_service = InterfaceService.get_instance()
    players = interface_service.get_all_players()
    
    if not players:
        print(f"{Fore.YELLOW}⚠️  Nenhum personagem encontrado!{Fore.RESET}")
        print("Crie um novo personagem primeiro.")
        input("⏳ Pressione Enter para continuar...")
        return
    
    print("Personagens disponíveis:")
    print()
    
    for i, player in enumerate(players, 1):
        print(f"{i}. {player.nome} (Vida: {player.vida_atual}/{player.vida_maxima} | XP: {player.experiencia} | Força: {player.forca})")
    
    print()
    try:
        escolha = input("🎯 Digite o número do personagem (ou 'c' para cancelar): ").strip()
        
        if escolha.lower() == 'c':
            return
        
        indice = int(escolha) - 1
        
        if 0 <= indice < len(players):
            player = players[indice]
            
            # Verificar se é o personagem atual
            current_player = get_current_player()
            current_id = current_player.id_player if current_player else None
            
            if current_id and player.id_player == current_id:
                print(f"{Fore.YELLOW}⚠️  '{player.nome}' já é o personagem ativo!{Fore.RESET}")
                input("⏳ Pressione Enter para continuar...")
                return
            
            # Definir personagem
            set_current_player(player)
            print(f"{Fore.GREEN}✅ Personagem '{player.nome}' selecionado com sucesso!{Fore.RESET}")
            input("⏳ Pressione Enter para continuar...")
            return  # Sair da função e voltar ao menu principal
        else:
            print(f"{Fore.RED}❌ Número inválido! Digite um número entre 1 e {len(players)}.{Fore.RESET}")
            input("⏳ Pressione Enter para continuar...")
            return
            
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
    
    print(f"\n⚙️ Status iniciais:")
    print(f"❤️  Vida máxima: 100")
    print(f"💪 Força inicial: 10")
    print(f"⭐ XP inicial: 0")
    print(f"📍 Localização inicial: Deserto")
    
    # Usar InterfaceService Singleton
    interface_service = InterfaceService.get_instance()
    new_player = interface_service.create_player(nome, vida_maxima=100, forca=10)
    
    if new_player:
        print(f"\n{Fore.GREEN}✅ Personagem '{nome}' criado com sucesso!{Fore.RESET}")
        escolha = input("🎮 Deseja selecionar este personagem agora? (s/n): ").strip().lower()
        
        if escolha == 's':
            set_current_player(new_player)
    else:
        print(f"{Fore.RED}❌ Erro ao criar personagem ou nome já existe!{Fore.RESET}")
        
    input("⏳ Pressione Enter para continuar...")

def listar_jogadores():
    """Lista todos os personagens"""
    clear_terminal()
    print("📋 LISTA DE PERSONAGENS")
    print("=" * 70)
    print()
    
    # Usar InterfaceService Singleton
    interface_service = InterfaceService.get_instance()
    players = interface_service.get_all_players()
    
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
                current_id = current_player.id_player if current_player else None
                
                print("Personagens disponíveis:")
                for i, player in enumerate(players, 1):
                    status_icon = "🎮" if player.id_player == current_id else "👤"
                    print(f"{i}. {status_icon} {player.nome} (Vida: {player.vida_atual}/{player.vida_maxima} | XP: {player.experiencia} | Força: {player.forca})")
                
                print()
                
                while True:
                    try:
                        escolha = input("🎯 Digite o número do personagem (ou 'c' para cancelar): ").strip()
                        
                        if escolha.lower() == 'c':
                            break
                        
                        indice = int(escolha) - 1
                        
                        if 0 <= indice < len(players):
                            player = players[indice]
                            
                            # Verificar se é o personagem atual
                            if current_id and player.id_player == current_id:
                                print(f"{Fore.YELLOW}⚠️  '{player.nome}' já é o personagem ativo!{Fore.RESET}")
                                input("⏳ Pressione Enter para continuar...")
                                return
                            
                            # Definir personagem
                            set_current_player(player)
                            print(f"{Fore.GREEN}✅ Personagem '{player.nome}' selecionado com sucesso!{Fore.RESET}")
                            input("⏳ Pressione Enter para continuar...")
                            return  # Sair da função e voltar ao menu principal
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
                current_id = current_player.id_player if current_player else None
                
                print("Personagens disponíveis para deletar:")
                for i, player in enumerate(players, 1):
                    status_icon = "🎮" if player.id_player == current_id else "👤"
                    print(f"{i}. {status_icon} {player.nome} (Vida: {player.vida_atual}/{player.vida_maxima} | XP: {player.experiencia} | Força: {player.forca})")
                
                print()
                
                while True:
                    try:
                        escolha = input("🗑️  Digite o número do personagem para deletar (ou 'c' para cancelar): ").strip()
                        
                        if escolha.lower() == 'c':
                            break
                        
                        indice = int(escolha) - 1
                        
                        if 0 <= indice < len(players):
                            player = players[indice]
                            
                            # Verificar se é o personagem atual
                            if current_id and player.id_player == current_id:
                                print(f"{Fore.RED}❌ Não é possível deletar o personagem ativo '{player.nome}'!{Fore.RESET}")
                                print("💡 Dica: Troque de personagem primeiro ou saia da sessão.")
                                input("⏳ Pressione Enter para continuar...")
                                return
                            
                            # Confirmar deleção
                            if confirm_player_deletion(player.nome):
                                # Deletar personagem
                                if interface_service.delete_player(player.id_player):
                                    print(f"{Fore.GREEN}✅ Personagem '{player.nome}' deletado com sucesso!{Fore.RESET}")
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
        
        # Usar InterfaceService Singleton para salvar
        interface_service = InterfaceService.get_instance()
        interface_service.save_player(current_player)
        clear_current_player()
    
    print("🚪 Saindo do Minecraft")
    print("Até a próxima! 🎮")

def extract_chunk_id_from_location(location: str) -> int:
    """
    Extract chunk ID from location string like 'Mapa 1 - Chunk 364'
    
    Args:
        location: Location string in format 'Mapa X - Chunk Y'
        
    Returns:
        Chunk ID as integer
        
    Raises:
        ValueError: If location format is invalid
    """
    if not location:
        raise ValueError("Location is empty")
        
    # Try to extract chunk ID using regex
    match = re.search(r'Chunk (\d+)', location)
    if match:
        return int(match.group(1))
    
    # If no match found, try to convert the entire string to int (backwards compatibility)
    try:
        return int(location)
    except ValueError:
        raise ValueError(f"Cannot extract chunk ID from location: {location}")
