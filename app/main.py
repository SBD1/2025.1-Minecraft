from src.interface.display import tela_inicial
from src.utils.db_helpers import setup_database

if __name__ == "__main__":
    # Verifica e configura o banco de dados antes de iniciar a aplicação
    setup_database()
    
    # Inicia a aplicação
    tela_inicial()


# Ver inventario
# andar