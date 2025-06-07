import os
import time
from colorama import Fore, init


init(autoreset=True)

CREEPER_ART = [
    "⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️",
    "⬛️📗📗📗📗📗📗📗📗⬛️",
    "⬛️📗⬛️⬛️📗📗⬛️⬛️📗⬛️",
    "⬛️📗⬛️⬛️📗📗⬛️⬛️📗⬛️",
    "⬛️📗📗📗⬛️⬛️📗📗📗⬛️",
    "⬛️📗📗⬛️⬛️⬛️⬛️📗📗⬛️",
    "⬛️📗📗⬛️📗📗⬛️📗📗⬛️",
    "⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️",
    "⬛️📗📗📗📗📗⬛️",
    "⬛️📗📗📗📗📗⬛️",
    "⬛️📗📗📗📗📗⬛️",
    "⬛️📗📗📗📗📗⬛️",
    "⬛️⬛️⬛️⬛️⬛️|⬛️⬛️⬛️⬛️⬛️",
    "⬛️📗📗📗📗|📗📗📗📗⬛️",
    "⬛️📗📗📗📗|📗📗📗📗⬛️",
    "⬛️⬛️⬛️⬛️⬛️|⬛️⬛️⬛️⬛️⬛️"
]


def mostrar_creeper(posicao):
    """Exibe o Creeper na posição especificada."""
    for linha in CREEPER_ART:
        print(" " * posicao + linha)

def explodir_creeper(posicao):
    """Anima a explosão do Creeper."""
    explosao = ["💥" * 10 for _ in range(16)]
    for _ in range(3):
        time.sleep(0.2)
        for linha in explosao:
            print(" " * posicao + linha)
        time.sleep(0.2)
    time.sleep(3)

def mover_creeper_para_direita():
    """Anima o Creeper se movendo para a direita e explodindo."""
    largura_terminal = os.get_terminal_size().columns
    largura_creeper = 10 
    meio_tela = largura_terminal // 2 - largura_creeper // 2
    
    for posicao in range(meio_tela + 1):
        mostrar_creeper(posicao)
        time.sleep(0.05)

    # Piscar e explodir o Creeper
    for _ in range(3):
        time.sleep(0.3)
        mostrar_creeper(meio_tela)
        time.sleep(0.3)
    
    explodir_creeper(meio_tela)
    time.sleep(1)

def tela_inicial():
    mover_creeper_para_direita()
    print("################")