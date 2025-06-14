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
        print(f"✓ Arquivo SQL executado com sucesso: {file_path}")
        return True
    except Exception as e:
        print(f"✗ Erro ao executar arquivo SQL {file_path}: {str(e)}")
        return False

def check_database_connection():
    """Verifica se é possível conectar ao banco de dados"""
    try:
        conn = connection_db()
        conn.close()
        print("✓ Conexão com o banco de dados estabelecida")
        return True
    except Exception as e:
        print(f"✗ Erro ao conectar com o banco de dados: {str(e)}")
        return False

def check_tables_exist():
    """Verifica se as tabelas principais existem no banco"""
    try:
        conn = connection_db()
        cursor = conn.cursor()
        
        # Lista das tabelas principais que devem existir
        required_tables = ['bioma', 'mapa', 'chunk', 'jogador', 'inventario']
        
        for table in required_tables:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                );
            """, (table,))
            
            exists = cursor.fetchone()[0]
            if not exists:
                cursor.close()
                conn.close()
                print(f"✗ Tabela '{table}' não encontrada")
                return False
        
        cursor.close()
        conn.close()
        print("✓ Todas as tabelas necessárias existem")
        return True
    except Exception as e:
        print(f"✗ Erro ao verificar tabelas: {str(e)}")
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
            print(f"✓ Mapa com 1000 chunks já existe (Dia: {day_chunks}, Noite: {night_chunks})")
            return True
        else:
            print(f"⚠ Mapa com 1000 chunks não encontrado (Dia: {day_chunks}, Noite: {night_chunks})")
            return False
    except Exception as e:
        print(f"✗ Erro ao verificar mapa com 1000 chunks: {str(e)}")
        return False

def check_data_seeded():
    """Verifica se os dados iniciais (seed) já foram inseridos"""
    try:
        conn = connection_db()
        cursor = conn.cursor()
        
        # Verifica se existem dados básicos nas tabelas principais
        cursor.execute("SELECT COUNT(*) FROM bioma;")
        bioma_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM mapa;")
        mapa_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM chunk;")
        chunk_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        if bioma_count > 0 and mapa_count > 0 and chunk_count > 0:
            print("✓ Dados iniciais (seed) já existem no banco")
            return True
        else:
            print("⚠ Dados iniciais (seed) não encontrados")
            return False
    except Exception as e:
        print(f"✗ Erro ao verificar dados iniciais: {str(e)}")
        return False

def initialize_database():
    """Inicializa o banco de dados executando os scripts SQL necessários"""
    print("Inicializando banco de dados...")
    
    # Caminhos dos arquivos SQL (relativos ao diretório /app no container)
    base_path = "/app/db"
    
    ddl_path = os.path.join(base_path, "ddl.sql")
    dml_1000_chunks_path = os.path.join(base_path, "dml_1000_chunks.sql")
    dml_path = os.path.join(base_path, "dml.sql")
    
    try:
        conn = connection_db()
        
        # Executa DDL (criação das tabelas)
        if os.path.exists(ddl_path):
            if not execute_sql_file(conn, ddl_path):
                conn.close()
                return False
        else:
            print(f"✗ Arquivo DDL não encontrado: {ddl_path}")
            conn.close()
            return False
        
        # Tenta executar o script com 1000 chunks primeiro
        if os.path.exists(dml_1000_chunks_path):
            print("🗺️ Executando script com mapa de 1000 chunks...")
            if not execute_sql_file(conn, dml_1000_chunks_path):
                print("⚠ Erro ao executar script de 1000 chunks, tentando script básico...")
                # Se falhar, tenta o script básico
                if os.path.exists(dml_path):
                    if not execute_sql_file(conn, dml_path):
                        conn.close()
                        return False
                else:
                    print(f"✗ Arquivo DML básico não encontrado: {dml_path}")
                    conn.close()
                    return False
        else:
            # Se não existir o script de 1000 chunks, usa o básico
            if os.path.exists(dml_path):
                if not execute_sql_file(conn, dml_path):
                    conn.close()
                    return False
            else:
                print(f"✗ Arquivo DML não encontrado: {dml_path}")
                conn.close()
                return False
        
        conn.close()
        print("Banco de dados inicializado com sucesso!")
        return True
        
    except Exception as e:
        print(f"✗ Erro durante a inicialização do banco: {str(e)}")
        return False

def setup_database():
    """Função principal para configurar o banco de dados antes da execução do app"""
    print("Verificando configuração do banco de dados...")
    
    # 1. Verifica conexão com o banco
    if not check_database_connection():
        print("Falha na conexão com o banco de dados. Verifique se o serviço está rodando.")
        sys.exit(1)
    
    # 2. Verifica se as tabelas existem
    tables_exist = check_tables_exist()
    
    # 3. Verifica se os dados iniciais existem
    data_exists = check_data_seeded()
    
    # 4. Verifica se o mapa com 1000 chunks existe
    map_1000_exists = check_map_with_1000_chunks()
    
    # 5. Se tabelas não existem, dados não existem, ou mapa não tem 1000 chunks, inicializa o banco
    if not tables_exist or not data_exists or not map_1000_exists:
        print("🔄 Inicializando estrutura e dados do banco...")
        if not initialize_database():
            print("❌ Falha na inicialização do banco de dados.")
            sys.exit(1)
    else:
        print("✅ Banco de dados já configurado e pronto para uso!")
    
    print("=" * 50)