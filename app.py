from colorama import init, Fore, Style
import utils

init()

MINECRAFT = [
    f"{Fore.GREEN}███╗   ███╗██╗███╗   ██╗███████╗███████╗██████╗ ███████╗███████╗████████╗{Style.RESET_ALL}",
    f"{Fore.GREEN}████╗ ████║██║████╗  ██║██╔════╝██╔════╝██╔══██╗██╔══██║██╔════╝╚══██╔══╝{Style.RESET_ALL}",
    f"{Fore.GREEN}██╔████╔██║██║██╔██╗ ██║█████╗  ██║     ██████╔╝███████║█████╗     ██║   {Style.RESET_ALL}",
    f"{Fore.GREEN}██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██║     ██╔══██╗██╔══██║██╔══╝     ██║   {Style.RESET_ALL}",
    f"{Fore.GREEN}██║ ╚═╝ ██║██║██║ ╚████║███████╗███████╗██║  ██║██║  ██║██║        ██║   {Style.RESET_ALL}",
    f"{Fore.GREEN}╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   {Style.RESET_ALL}"
]

ESPADA_ART = [
    f"{Fore.GREEN}    ██    {Style.RESET_ALL}",
    f"{Fore.GREEN}    ██    {Style.RESET_ALL}",
    f"{Fore.GREEN}    ██    {Style.RESET_ALL}",
    f"{Fore.GREEN}    ██    {Style.RESET_ALL}",
    f"{Fore.GREEN}████████{Style.RESET_ALL}",
    f"{Fore.GREEN}████████{Style.RESET_ALL}",
    f"{Fore.GREEN}    ██    {Style.RESET_ALL}",
    f"{Fore.GREEN}    ██    {Style.RESET_ALL}",
    f"{Fore.GREEN}    ██    {Style.RESET_ALL}",
    f"{Fore.GREEN}    ██    {Style.RESET_ALL}"
]

# Exibir
for linha in MINECRAFT:
    print(linha)

print()  # Linha em branco para separar

for linha in ESPADA_ART:
    print(linha)

print(utils.soma(2, 3))