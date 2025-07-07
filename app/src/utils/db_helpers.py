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
    """Verifica se os dados iniciais foram inseridos"""
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
        
        cursor.close()
        conn.close()
        
        # Verificar se há pelo menos alguns dados
        if player_count == 0 and chunk_count == 0 and bioma_count == 0 and mapa_count == 0:
            print("Dados iniciais (seed) não encontrados")
            return False
        
        return True
        
    except Exception as e:
        print(f"Erro ao verificar dados iniciais: {str(e)}")
        return False

def initialize_database():
    """Inicializa o banco de dados com dados básicos"""
    try:
        conn = connection_db()
        
        # Executar scripts SQL na ordem correta
        execute_sql_file(conn, "db/ddl.sql")
        
        # Verificar se existe o arquivo de triggers antes de executar
        if os.path.exists("db/trigger_SP.sql"):
            execute_sql_file(conn, "db/trigger_SP.sql")
        
        execute_sql_file(conn, "db/dml.sql")
        
        # Verificar se existe o arquivo de instâncias antes de executar
        if os.path.exists("db/dml_inst.sql"):
            execute_sql_file(conn, "db/dml_inst.sql")
        
        print("Executando script com mapa de 1000 chunks...")
        if os.path.exists("db/dml_1000_chunks.sql"):
            execute_sql_file(conn, "db/dml_1000_chunks.sql")
        
        # Executar script adicional se existir
        if os.path.exists("db/create_user.sql"):
            execute_sql_file(conn, "db/create_user.sql")
        
        conn.close()
        print("Banco de dados inicializado com sucesso!")
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
    
    # Verificar estrutura das tabelas
    if not check_tables_exist():
        print("Inicializando estrutura e dados do banco...")
        if not initialize_database():
            print("Falha na inicialização do banco de dados.")
            return False
    
    # Verificar dados iniciais
    if not check_data_seeded():
        print("Inicializando dados básicos...")
        if not initialize_database():
            print("Falha na inicialização dos dados.")
            return False
    
    print("Banco de dados já configurado e pronto para uso!")
    return True
