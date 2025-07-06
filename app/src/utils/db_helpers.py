import psycopg2
import os
import sys

def connection_db():
    return psycopg2.connect(
        user="postgres",
        password="password",
        host="db",
        port="5432",
        database="2025_1_Minecraft"
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
        
        # Verifica se existem pelo menos 1000 chunks no mapa de dia
        cursor.execute("""
            SELECT COUNT(*) FROM chunk 
            WHERE id_mapa_nome = 'Mapa_Principal' AND id_mapa_turno = 'Dia'
        """)
        day_chunks = cursor.fetchone()[0]
        
        # Verifica se existem pelo menos 1000 chunks no mapa de noite
        cursor.execute("""
            SELECT COUNT(*) FROM chunk 
            WHERE id_mapa_nome = 'Mapa_Principal' AND id_mapa_turno = 'Noite'
        """)
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
        cursor.execute("SELECT COUNT(*) FROM Jogador")
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
        # Executar scripts SQL na ordem correta
        execute_sql_file("db/ddl.sql")
        execute_sql_file("db/trigger_SP.sql")
        execute_sql_file("db/dml.sql")
        execute_sql_file("db/dml_inst.sql")
        
        print("Executando script com mapa de 1000 chunks...")
        
        # Executar script adicional se existir
        try:
            execute_sql_file("db/create_user.sql")
        except FileNotFoundError:
            pass
        
        print("Banco de dados inicializado com sucesso!")
        return True
        
    except Exception as e:
        print(f"Falha na inicialização do banco de dados.")
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
