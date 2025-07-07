import psycopg2
import os
import sys

def connection_db():
    # Configurar parâmetros via variáveis de ambiente para suportar conexões locais e Docker
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "password")
    host = os.getenv("DB_HOST", "db")
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME", "2025_1_Minecraft")
    return psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )

def execute_sql_file(conn, file_path):
    """Executa um arquivo SQL no banco de dados"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        cursor = conn.cursor()
        cursor.execute(sql_content)
        conn.commit()
        cursor.close()
        print(f"Arquivo SQL executado com sucesso: {file_path}")
        return True
    except Exception as e:
        print(f"Erro ao executar arquivo SQL {file_path}: {str(e)}")
        return False

def check_database_connection():
    """Verifica se é possível conectar ao banco de dados"""
    try:
        conn = connection_db()
        conn.close()
        print("Conexão com o banco de dados estabelecida")
        return True
    except Exception as e:
        print(f"Erro ao conectar com o banco de dados: {str(e)}")
        return False

def check_tables_exist():
    """Verifica se as tabelas principais existem no banco usando repositórios"""
    try:
        # Importação local para evitar importação circular
        from ..repositories import BiomaRepositoryImpl, MapaRepositoryImpl, ChunkRepositoryImpl
        
        bioma_repo = BiomaRepositoryImpl()
        mapa_repo = MapaRepositoryImpl()
        chunk_repo = ChunkRepositoryImpl()

        # Verifica se as tabelas têm pelo menos um registro
        if not bioma_repo.find_all() or not mapa_repo.find_all() or not chunk_repo.find_all():
            print("Algumas tabelas não têm registros")
            return False

        print("Todas as tabelas necessárias têm registros")
        return True
    except Exception as e:
        print(f"Erro ao verificar tabelas: {str(e)}")
        return False

def check_new_structure_tables():
    """Verifica se todas as tabelas da nova estrutura existem"""
    try:
        conn = connection_db()
        cursor = conn.cursor()
        
        # Lista de tabelas esperadas na nova estrutura
        expected_tables = [
            'bioma', 'mapa', 'item', 'chunk', 'player', 
            'inventario', 'fantasma', 'pontes', 'totem', 'aldeao'
        ]
        
        for table in expected_tables:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_name = %s
                )
            """, (table,))
            
            exists = cursor.fetchone()[0]
            if not exists:
                print(f"Tabela '{table}' não encontrada")
                cursor.close()
                conn.close()
                return False
        
        cursor.close()
        conn.close()
        print("Todas as tabelas da nova estrutura existem")
        return True
        
    except Exception as e:
        print(f"Erro ao verificar estrutura das tabelas: {str(e)}")
        return False

def check_map_with_1000_chunks():
    """Verifica se o mapa com 1000 chunks já foi criado"""
    try:
        conn = connection_db()
        cursor = conn.cursor()
        
        # Buscar ID dos mapas Dia e Noite
        cursor.execute("""
            SELECT id_mapa FROM mapa 
            WHERE nome = 'Mapa_Principal' AND turno = 'Dia'
        """)
        day_map = cursor.fetchone()
        
        cursor.execute("""
            SELECT id_mapa FROM mapa 
            WHERE nome = 'Mapa_Principal' AND turno = 'Noite'
        """)
        night_map = cursor.fetchone()
        
        day_chunks = 0
        night_chunks = 0
        
        if day_map:
            cursor.execute("""
                SELECT COUNT(*) FROM chunk WHERE id_mapa = %s
            """, (day_map[0],))
            day_chunks = cursor.fetchone()[0]
        
        if night_map:
            cursor.execute("""
                SELECT COUNT(*) FROM chunk WHERE id_mapa = %s
            """, (night_map[0],))
            night_chunks = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        if day_chunks >= 1000 and night_chunks >= 1000:
            print(f"Mapa com 1000 chunks já existe (Dia: {day_chunks}, Noite: {night_chunks})")
            return True
        else:
            print(f"Mapa com 1000 chunks não encontrado (Dia: {day_chunks}, Noite: {night_chunks})")
            return False
    except Exception as e:
        print(f"Erro ao verificar mapa com 1000 chunks: {str(e)}")
        return False

def check_data_seeded():
    """Verifica se os dados iniciais foram inseridos (incluindo novas tabelas)"""
    try:
        conn = connection_db()
        cursor = conn.cursor()
        
        # Verificar se há dados nas tabelas principais
        cursor.execute("SELECT COUNT(*) FROM Player")
        player_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Chunk")
        chunk_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Bioma")
        bioma_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Mapa")
        mapa_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Item")
        item_count = cursor.fetchone()[0]
        
        # Verificar novas tabelas
        cursor.execute("SELECT COUNT(*) FROM fantasma")
        fantasma_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM pontes")
        pontes_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM totem")
        totem_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Aldeao")
        aldeao_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        # Verificar se há pelo menos alguns dados nas tabelas básicas
        if bioma_count == 0 or mapa_count == 0 or item_count == 0:
            print("Dados iniciais básicos não encontrados")
            return False
        
        print(f"Dados encontrados - Players: {player_count}, Chunks: {chunk_count}, "
              f"Biomas: {bioma_count}, Mapas: {mapa_count}, Items: {item_count}, "
              f"Fantasmas: {fantasma_count}, Pontes: {pontes_count}, Totens: {totem_count}, "
              f"Aldeões: {aldeao_count}")
        
        return True
        
    except Exception as e:
        print(f"Erro ao verificar dados iniciais: {str(e)}")
        return False

def initialize_database():
    """Inicializa o banco de dados com a nova estrutura organizada"""
    try:
        conn = connection_db()
        
        # Executar scripts SQL na ordem correta da nova estrutura
        script_order = [
            # Fase 1: Usuários
            "db/init/01_users/create_users.sql",
            
            # Fase 2: Schema
            "db/init/02_schema/01_drop_tables.sql",
            "db/init/02_schema/02_base_tables.sql",
            "db/init/02_schema/03_dependent_tables.sql",
            "db/init/02_schema/03_9_aldeao_table.sql",
            "db/init/02_schema/04_relationship_tables.sql",
            "db/init/02_schema/05_game_tables.sql",
            "db/init/02_schema/06_indexes.sql",
            
            # Fase 3: Dados
            "db/init/03_data/01_basic_data.sql",
            "db/init/03_data/02_chunks.sql",
            "db/init/03_data/03_players.sql",
            "db/init/03_data/03_5_aldeao_data.sql",
            "db/init/03_data/04_inventory.sql",
            "db/init/03_data/05_game_data.sql"
        ]
        
        for script_path in script_order:
            if os.path.exists(script_path):
                if not execute_sql_file(conn, script_path):
                    print(f"Falha ao executar {script_path}")
                    return False
            else:
                print(f"Arquivo não encontrado: {script_path}")
        
        conn.close()
        print("Banco de dados inicializado com sucesso usando nova estrutura!")
        return True
        
    except Exception as e:
        print(f"Falha na inicialização do banco de dados: {str(e)}")
        return False

def setup_database():
    """Configura o banco de dados antes da execução da aplicação"""
    print("Verificando configuração do banco de dados...")
    
    # Verificar conexão
    if not check_database_connection():
        print("Erro: Não foi possível conectar ao banco de dados")
        return False
    
    # Verificar estrutura das tabelas da nova organização
    if not check_new_structure_tables():
        print("Inicializando estrutura e dados do banco com nova organização...")
        if not initialize_database():
            print("Falha na inicialização do banco de dados.")
            return False
    
    # Verificar se há dados nas tabelas (fallback para método antigo se necessário)
    if not check_data_seeded():
        try:
            # Tentar usar repositórios se estiverem disponíveis
            if not check_tables_exist():
                print("Inicializando dados básicos...")
                if not initialize_database():
                    print("Falha na inicialização dos dados.")
                    return False
        except Exception as e:
            print(f"Repositórios não disponíveis, usando verificação direta: {str(e)}")
    
    print("Banco de dados configurado e pronto para uso!")
    return True
