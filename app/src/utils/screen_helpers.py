import os

def clear_terminal():
    """Limpa o terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def players_status(player):
    print(f"Nome: {player[1]}")
    print(f"Vida Maxima: {player[2]}")
    print(f"Vida Atual: {player[3]}")
    print(f"Pontos de Experiencia: {player[4]}")
    print(f"Força: {player[5]}")
    print(" ")