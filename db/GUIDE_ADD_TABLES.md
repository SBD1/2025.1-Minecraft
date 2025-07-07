# 📋 Guia Completo: Adicionando Novas Tabelas ao Banco de Dados

## 🔍 Passo 1: Análise e Planejamento

### 1.1 Verificar Estrutura Atual
```bash
# Listar arquivos existentes
ls -la db/init/02_schema/
ls -la db/init/03_data/
```

### 1.2 Analisar Dependências
Pergunte-se:
- **Minha tabela depende de outras?** (Foreign Keys)
- **Outras tabelas vão depender dela?**
- **Onde ela se encaixa na sequência?**

### 1.3 Categorizar a Tabela
- **Básica**: Sem dependências (ex: Bioma, Mapa, Item)
- **Dependente**: Depende de tabelas básicas (ex: Chunk, Player)
- **Relacionamento**: Liga duas tabelas (ex: Inventario)
- **Específica**: Funcionalidade do jogo (ex: fantasma, pontes)

## 🛠️ Passo 2: Criação da Tabela

### 2.1 Definir Numeração
Baseado na sequência atual:
```
02_schema/
├── 01_drop_tables.sql
├── 02_base_tables.sql         # Sem dependências
├── 03_dependent_tables.sql    # Dependem de básicas
├── 03_5_aldeao_table.sql      # Nova tabela dependente
├── 04_relationship_tables.sql # Relacionamentos
├── 05_game_tables.sql         # Específicas do jogo
└── 06_indexes.sql             # Índices
```

### 2.2 Criar Arquivo de Schema
```sql
-- Exemplo: db/init/02_schema/03_5_aldeao_table.sql
CREATE TABLE Aldeao (
    id_aldeao SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    profissao VARCHAR(50) NOT NULL,
    nivel_profissao INT NOT NULL DEFAULT 1,
    vida_maxima INT NOT NULL DEFAULT 20,
    vida_atual INT NOT NULL DEFAULT 20,
    id_chunk INT REFERENCES Chunk(id_chunk) ON DELETE SET NULL ON UPDATE CASCADE,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 Passo 3: Atualizar Dependências

### 3.1 Atualizar DROP TABLE
```sql
-- db/init/02_schema/01_drop_tables.sql
DROP TABLE IF EXISTS Inventario, Item, Player, Chunk, Mapa, Bioma, fantasma, pontes, totem, Aldeao CASCADE;
```

### 3.2 Adicionar Índices
```sql
-- db/init/02_schema/06_indexes.sql
CREATE INDEX idx_aldeao_chunk ON Aldeao(id_chunk);
CREATE INDEX idx_aldeao_profissao ON Aldeao(profissao);
CREATE INDEX idx_aldeao_ativo ON Aldeao(ativo);
```

## 📊 Passo 4: Criar Dados Iniciais

### 4.1 Criar Arquivo de Dados
```sql
-- db/init/03_data/03_5_aldeao_data.sql
INSERT INTO Aldeao (nome, profissao, nivel_profissao, vida_maxima, vida_atual, id_chunk, ativo)
VALUES
  ('João Ferreiro', 'Ferreiro', 3, 25, 25, 1, TRUE),
  ('Maria Fazendeira', 'Fazendeira', 2, 20, 20, 2, TRUE)
ON CONFLICT (nome) DO NOTHING;
```

### 4.2 Seguir Numeração Sequencial
```
03_data/
├── 01_basic_data.sql
├── 02_chunks.sql
├── 03_players.sql
├── 03_5_aldeao_data.sql      # Nova tabela
├── 04_inventory.sql
└── 05_game_data.sql
```

## 🐳 Passo 5: Atualizar Docker Compose

### 5.1 Adicionar Volumes
```yaml
volumes:
  # Estrutura organizada e faseada
  - ./db/init/02_schema/03_5_aldeao_table.sql:/docker-entrypoint-initdb.d/04_5_aldeao_table.sql
  - ./db/init/03_data/03_5_aldeao_data.sql:/docker-entrypoint-initdb.d/10_5_aldeao_data.sql
```

### 5.2 Manter Numeração Sequencial
```yaml
# Schema
04_dependent_tables.sql
04_5_aldeao_table.sql         # Nova tabela
05_relationship_tables.sql

# Data
10_players.sql
10_5_aldeao_data.sql          # Novos dados
11_inventory.sql
```

## 🔧 Passo 6: Atualizar db_helpers.py

### 6.1 Adicionar na Lista de Verificação
```python
expected_tables = [
    'bioma', 'mapa', 'item', 'chunk', 'player', 
    'inventario', 'fantasma', 'pontes', 'totem', 'aldeao'  # Nova tabela
]
```

### 6.2 Atualizar Verificação de Dados
```python
cursor.execute("SELECT COUNT(*) FROM Aldeao")
aldeao_count = cursor.fetchone()[0]

print(f"Aldeões: {aldeao_count}")
```

### 6.3 Atualizar Script Order
```python
script_order = [
    # Schema
    "db/init/02_schema/03_5_aldeao_table.sql",  # Nova tabela
    
    # Data
    "db/init/03_data/03_5_aldeao_data.sql",    # Novos dados
]
```

## 📝 Passo 7: Atualizar Consultas

### 7.1 Adicionar no DQL
```sql
-- db/dql.sql
SELECT * FROM Aldeao;

-- Consulta com JOINs
SELECT
    a.nome AS Nome_Aldeao,
    a.profissao AS Profissao,
    c.x AS Chunk_X,
    c.y AS Chunk_Y,
    b.nome AS Bioma
FROM Aldeao a
JOIN Chunk c ON a.id_chunk = c.id_chunk
JOIN Bioma b ON c.id_bioma = b.id_bioma
WHERE a.ativo = TRUE;
```

## 🧪 Passo 8: Testar e Validar

### 8.1 Executar Inicialização
```bash
# Método 1: Script automatizado
./db/init_database.sh

# Método 2: Manual
docker-compose down -v
docker-compose up --build -d
```

### 8.2 Verificar Logs
```bash
# Verificar logs do banco
docker-compose logs db

# Verificar se containers estão rodando
docker-compose ps
```

### 8.3 Testar Conexão
```bash
# Conectar ao banco
psql -h localhost -p 5433 -U postgres -d 2025_1_Minecraft

# Verificar tabelas
\dt

# Testar dados
SELECT COUNT(*) FROM Aldeao;
```

## ✅ Passo 9: Checklist Final

### 9.1 Arquivos Criados/Modificados
- [ ] `02_schema/XX_nova_tabela.sql` - Schema da nova tabela
- [ ] `03_data/XX_nova_tabela_data.sql` - Dados iniciais
- [ ] `01_drop_tables.sql` - Adicionada nova tabela
- [ ] `06_indexes.sql` - Adicionados índices
- [ ] `docker-compose.yml` - Volumes atualizados
- [ ] `db_helpers.py` - Verificações atualizadas
- [ ] `dql.sql` - Consultas de exemplo

### 9.2 Numeração Sequencial
- [ ] Schema: Numeração respeita dependências
- [ ] Data: Numeração corresponde ao schema
- [ ] Docker: Volumes em ordem sequencial

### 9.3 Testes
- [ ] Banco inicializa sem erros
- [ ] Tabela criada corretamente
- [ ] Dados inseridos com sucesso
- [ ] Consultas funcionam
- [ ] Aplicação Python conecta

## 🎯 Exemplo Completo: Tabela "Missao"

### Schema (02_schema/05_5_missao_table.sql)
```sql
CREATE TABLE Missao (
    id_missao SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    recompensa_xp INT NOT NULL DEFAULT 0,
    recompensa_item_id INT REFERENCES Item(id_item),
    status VARCHAR(20) NOT NULL DEFAULT 'ativa',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Dados (03_data/05_5_missao_data.sql)
```sql
INSERT INTO Missao (nome, descricao, tipo, recompensa_xp, recompensa_item_id, status)
VALUES
  ('Primeira Mineração', 'Colete 10 blocos de pedra', 'mineracao', 50, 1, 'ativa'),
  ('Explorador', 'Visite 5 chunks diferentes', 'exploracao', 100, 2, 'ativa')
ON CONFLICT (nome) DO NOTHING;
```

### Docker Volume
```yaml
- ./db/init/02_schema/05_5_missao_table.sql:/docker-entrypoint-initdb.d/06_5_missao_table.sql
- ./db/init/03_data/05_5_missao_data.sql:/docker-entrypoint-initdb.d/12_5_missao_data.sql
```

## 🚀 Pronto!

Seguindo este guia, você pode adicionar qualquer nova tabela mantendo a estrutura organizada e funcionando corretamente!
