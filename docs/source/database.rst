Banco de Dados
=============

Esta seção documenta a estrutura e configuração do banco de dados do MINECRAFT - FGA - 2025/1.

Visão Geral
-----------

O projeto utiliza **PostgreSQL** como banco de dados principal, executando em um container Docker para facilitar a portabilidade e isolamento.

Configuração
------------

Docker Compose
^^^^^^^^^^^^^

.. code-block:: yaml

   db:
     build:
       context: ./db
       dockerfile: Dockerfile.db
     container_name: 2025_1_Minecraft
     environment:
       POSTGRES_USER: postgres
       POSTGRES_PASSWORD: password
       POSTGRES_DB: 2025_1_Minecraft
     ports:
       - "5433:5432"
     volumes:
       - ./db/ddl.sql:/docker-entrypoint-initdb.d/1_ddl.sql
       - ./db/trigger_SP.sql:/docker-entrypoint-initdb.d/2_trigger_SP.sql
       - ./db/dml.sql:/docker-entrypoint-initdb.d/3_dml.sql
       - ./db/dml_inst.sql:/docker-entrypoint-initdb.d/4_dml_inst.sql
       - ./db/create_user.sql:/docker-entrypoint-initdb.d/5_create_user.sql
       - db_data:/var/lib/postgresql/data

Conexão
^^^^^^^

.. code-block:: python

   def connection_db():
       return psycopg2.connect(
           user="postgres",
           password="password",
           host="db",
           port="5432",
           database="2025_1_Minecraft"
       )

Estrutura do Banco
------------------

Tabelas Principais
^^^^^^^^^^^^^^^^^

Bioma
"""""

Armazena os diferentes biomas do mundo.

.. code-block:: sql

   CREATE TABLE Bioma (
       NomeBioma VARCHAR(100) PRIMARY KEY NOT NULL
   );

**Dados iniciais:**
* Deserto
* Oceano
* Selva
* Floresta

Mapa
""""

Define os mapas e seus turnos.

.. code-block:: sql

   CREATE TABLE Mapa (
       Nome VARCHAR(100) NOT NULL,
       Turno VARCHAR(50) NOT NULL,
       PRIMARY KEY (Nome, Turno)
   );

**Dados iniciais:**
* Mapa_Principal - Dia
* Mapa_Principal - Noite

Chunk
"""""

Representa as divisões do mundo (chunks).

.. code-block:: sql

   CREATE TABLE Chunk (
       Numero_chunk INTEGER PRIMARY KEY NOT NULL,
       Id_bioma VARCHAR(100) NOT NULL,
       Id_mapa_nome VARCHAR(100) NOT NULL,
       Id_mapa_turno VARCHAR(50) NOT NULL,
       FOREIGN KEY (Id_bioma) REFERENCES Bioma(NomeBioma),
       FOREIGN KEY (Id_mapa_nome, Id_mapa_turno) REFERENCES Mapa(Nome, Turno)
   );

**Dados iniciais:**
* Chunk 1: Deserto (Mapa_Principal - Dia)
* Chunk 2: Oceano (Mapa_Principal - Dia)
* Chunk 3: Selva (Mapa_Principal - Noite)
* Chunk 4: Floresta (Mapa_Principal - Noite)

Jogador
"""""""

Armazena os dados dos personagens.

.. code-block:: sql

   CREATE TABLE Jogador (
       Id_Jogador SERIAL PRIMARY KEY,
       Nome VARCHAR(100) NOT NULL,
       Vida_max INT NOT NULL,
       Vida_atual INT NOT NULL,
       xp INT NOT NULL,
       forca INT NOT NULL,
       Id_Chunk_Atual INTEGER,
       FOREIGN KEY (Id_Chunk_Atual) REFERENCES Chunk(Numero_chunk)
   );

**Atributos:**
* ``Id_Jogador``: Chave primária auto-incrementada
* ``Nome``: Nome único do personagem
* ``Vida_max``: Vida máxima (padrão: 100)
* ``Vida_atual``: Vida atual
* ``xp``: Experiência acumulada (padrão: 0)
* ``forca``: Força do personagem (padrão: 10)
* ``Id_Chunk_Atual``: Localização atual (FK para Chunk)

Inventario
""""""""""

Sistema de inventário dos personagens.

.. code-block:: sql

   CREATE TABLE Inventario (
       id_jogador INT NOT NULL,
       id_inventario INT NOT NULL,
       Instancia_Item TEXT,
       ArmaduraEquipada VARCHAR(100),
       ArmaEquipada VARCHAR(100),
       PRIMARY KEY (id_jogador, id_inventario),
       FOREIGN KEY (id_jogador) REFERENCES Jogador(Id_Jogador)
   );

**Atributos:**
* ``id_jogador``: Referência ao personagem (FK)
* ``id_inventario``: ID do inventário
* ``Instancia_Item``: Itens em formato JSON
* ``ArmaduraEquipada``: Armadura atual
* ``ArmaEquipada``: Arma atual

Diagrama ER
-----------

.. image:: _static/er-diagram.png
   :alt: Diagrama Entidade-Relacionamento
   :align: center

Relacionamentos
--------------

Bioma → Chunk
^^^^^^^^^^^^

* Um bioma pode ter múltiplos chunks
* Relacionamento 1:N
* Chave estrangeira: ``Chunk.Id_bioma``

Mapa → Chunk
^^^^^^^^^^^

* Um mapa/turno pode ter múltiplos chunks
* Relacionamento 1:N
* Chave estrangeira composta: ``Chunk.Id_mapa_nome, Id_mapa_turno``

Chunk → Jogador
^^^^^^^^^^^^^^

* Um chunk pode ter múltiplos jogadores
* Relacionamento 1:N
* Chave estrangeira: ``Jogador.Id_Chunk_Atual``

Jogador → Inventario
^^^^^^^^^^^^^^^^^^^^

* Um jogador pode ter múltiplos inventários
* Relacionamento 1:N
* Chave estrangeira: ``Inventario.id_jogador``

Índices
-------

Para otimização de performance:

.. code-block:: sql

   CREATE INDEX idx_chunk_id_bioma ON Chunk (Id_bioma);
   CREATE INDEX idx_chunk_id_mapa ON Chunk (Id_mapa_nome, Id_mapa_turno);
   CREATE INDEX idx_inventario_id_jogador ON Inventario (id_jogador);
   CREATE INDEX idx_jogador_id_chunk_atual ON Jogador (Id_Chunk_Atual);

Scripts de Inicialização
-----------------------

DDL (Data Definition Language)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arquivo: ``db/ddl.sql``

* Criação das tabelas
* Definição de constraints
* Criação de índices
* Configuração de chaves estrangeiras

DML (Data Manipulation Language)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arquivo: ``db/dml.sql``

* Inserção de biomas
* Inserção de mapas
* Inserção de chunks básicos (4 chunks)
* Inserção de personagens de exemplo
* Inserção de inventários de exemplo

DML com 1000 Chunks
^^^^^^^^^^^^^^^^^^^

Arquivo: ``db/dml_1000_chunks.sql``

* Inserção de biomas
* Inserção de mapas
* **Geração automática de 2000 chunks** (1000 para dia + 1000 para noite)
* Distribuição inteligente dos biomas:
  * **Oceano**: Bordas do mapa (~10% da área)
  * **Deserto**: Centro do mapa (~8% da área total, ~20% da área útil)
  * **Selva e Floresta**: Resto do mapa em padrão xadrez (~82% da área)
* Inserção de personagens de exemplo
* Inserção de inventários de exemplo

Sistema de Verificação Automática
--------------------------------

O sistema agora inclui verificações automáticas durante a inicialização:

Verificação de Tabelas
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   def check_tables_exist():
       """Verifica se as tabelas principais existem no banco"""
       required_tables = ['bioma', 'mapa', 'chunk', 'jogador', 'inventario']
       # Verifica cada tabela individualmente

Verificação de Dados Iniciais
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   def check_data_seeded():
       """Verifica se os dados iniciais (seed) já foram inseridos"""
       # Verifica contagem de biomas, mapas e chunks

Verificação do Mapa com 1000 Chunks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   def check_map_with_1000_chunks():
       """Verifica se o mapa com 1000 chunks já foi criado"""
       # Verifica se existem pelo menos 1000 chunks em cada turno

Lógica de Inicialização
^^^^^^^^^^^^^^^^^^^^^^^

O sistema segue esta ordem de prioridade:

1. **Verifica conexão** com o banco de dados
2. **Verifica existência** das tabelas
3. **Verifica dados iniciais** (biomas, mapas, chunks básicos)
4. **Verifica mapa com 1000 chunks** (dia e noite)
5. **Inicializa se necessário**:
   - Tenta executar ``dml_1000_chunks.sql`` primeiro
   - Se falhar, executa ``dml.sql`` como fallback

Estrutura do Mapa de 1000 Chunks
--------------------------------

Distribuição dos Biomas
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Oceano  Oceano  Oceano  Oceano  Oceano
   Oceano  Selva   Floresta Selva   Oceano
   Oceano  Floresta Deserto Floresta Oceano
   Oceano  Selva   Deserto  Selva   Oceano
   Oceano  Oceano  Oceano  Oceano  Oceano

**Estatísticas típicas:**
* **Total de chunks**: 2000 (1000 dia + 1000 noite)
* **Deserto**: ~82 chunks (área 9x9 no centro)
* **Oceano**: ~97 chunks (bordas)
* **Selva**: ~409 chunks (padrão xadrez)
* **Floresta**: ~410 chunks (padrão xadrez)

Geração Automática
^^^^^^^^^^^^^^^^^

O script usa PL/pgSQL para gerar chunks automaticamente:

.. code-block:: sql

   DO $$
   DECLARE
       chunk_id INTEGER := 1;
       map_size INTEGER := 32;
       center_start INTEGER := 12;
       center_end INTEGER := 20;
   BEGIN
       -- Gera chunks para dia e noite
       -- Aplica lógica de distribuição de biomas
   END
   $$ LANGUAGE plpgsql;

Dados Iniciais
--------------

Biomas
^^^^^^

.. code-block:: sql

   INSERT INTO Bioma (NomeBioma) VALUES
       ('Deserto'),
       ('Oceano'),
       ('Selva'),
       ('Floresta');

Mapas
^^^^^

.. code-block:: sql

   INSERT INTO Mapa (Nome, Turno) VALUES
       ('Mapa_Principal', 'Dia'),
       ('Mapa_Principal', 'Noite');

Chunks (Básico - 4 chunks)
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   INSERT INTO Chunk (Numero_chunk, Id_bioma, Id_mapa_nome, Id_mapa_turno) VALUES
       (1, 'Deserto', 'Mapa_Principal', 'Dia'),
       (2, 'Oceano', 'Mapa_Principal', 'Dia'),
       (3, 'Selva', 'Mapa_Principal', 'Noite'),
       (4, 'Floresta', 'Mapa_Principal', 'Noite');

Chunks (Completo - 2000 chunks)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Gerados automaticamente pelo script ``dml_1000_chunks.sql``:

* **Chunks 1-1000**: Mapa de dia
* **Chunks 1001-2000**: Mapa de noite
* **Distribuição**: Oceano nas bordas, deserto no centro, selva/floresta alternando

Personagens de Exemplo
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   INSERT INTO Jogador (Nome, Vida_max, Vida_atual, xp, forca, Id_Chunk_Atual) VALUES
       ('Player1', 100, 100, 0, 10, 1),
       ('Player2', 120, 120, 50, 12, 2),
       ('Player3', 110, 110, 25, 11, 3);

Inventários de Exemplo
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   INSERT INTO Inventario (id_jogador, id_inventario, Instancia_Item, ArmaduraEquipada, ArmaEquipada) VALUES
       (1, 1, '{"item_id": 101, "quantidade": 5}', 'Capacete de Ferro', 'Espada de Diamante'),
       (2, 1, '{"item_id": 201, "quantidade": 1}', 'Armadura de Couro', 'Arco Longo'),
       (3, 1, '{"item_id": 301, "quantidade": 3}', 'Armadura de Ouro', 'Machado de Pedra');

Queries Comuns
--------------

Buscar Personagem com Localização
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   SELECT 
       j.id_jogador, j.nome, j.vida_max, j.vida_atual, 
       j.xp, j.forca, j.id_chunk_atual,
       c.id_bioma, c.id_mapa_nome, c.id_mapa_turno
   FROM jogador j
   LEFT JOIN chunk c ON j.id_chunk_atual = c.numero_chunk
   WHERE j.id_jogador = %s;

Listar Todos os Personagens
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   SELECT id_jogador, nome, vida_max, vida_atual, xp, forca, id_chunk_atual
   FROM jogador 
   ORDER BY nome;

Verificar Nome Único
^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   SELECT COUNT(*) FROM jogador WHERE LOWER(nome) = LOWER(%s);

Atualizar Dados do Personagem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   UPDATE jogador 
   SET vida_atual = %s, xp = %s, forca = %s, id_chunk_atual = %s
   WHERE id_jogador = %s;

Verificar Mapa com 1000 Chunks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   -- Verificar chunks do mapa de dia
   SELECT COUNT(*) FROM chunk 
   WHERE id_mapa_nome = 'Mapa_Principal' AND id_mapa_turno = 'Dia';
   
   -- Verificar chunks do mapa de noite
   SELECT COUNT(*) FROM chunk 
   WHERE id_mapa_nome = 'Mapa_Principal' AND id_mapa_turno = 'Noite';
   
   -- Verificar distribuição de biomas
   SELECT id_bioma, COUNT(*) as quantidade 
   FROM chunk 
   WHERE id_mapa_turno = 'Dia' 
   GROUP BY id_bioma 
   ORDER BY quantidade DESC;

Backup e Restauração
-------------------

Backup Automático
^^^^^^^^^^^^^^^^

O Docker Compose configura um volume persistente:

.. code-block:: yaml

   volumes:
     - db_data:/var/lib/postgresql/data

Isso garante que os dados persistem entre reinicializações dos containers.

Backup Manual
^^^^^^^^^^^^

Para fazer backup manual:

.. code-block:: bash

   # Backup completo
   docker exec 2025_1_Minecraft pg_dump -U postgres 2025_1_Minecraft > backup.sql
   
   # Backup apenas dados
   docker exec 2025_1_Minecraft pg_dump -U postgres --data-only 2025_1_Minecraft > data_backup.sql

Restauração
^^^^^^^^^^^

Para restaurar um backup:

.. code-block:: bash

   # Restaurar backup completo
   docker exec -i 2025_1_Minecraft psql -U postgres 2025_1_Minecraft < backup.sql
   
   # Restaurar apenas dados
   docker exec -i 2025_1_Minecraft psql -U postgres 2025_1_Minecraft < data_backup.sql

Monitoramento
-------------

Verificar Status
^^^^^^^^^^^^^^^

.. code-block:: bash

   # Status dos containers
   docker-compose ps
   
   # Logs do banco
   docker-compose logs db
   
   # Conectar ao banco
   docker exec -it 2025_1_Minecraft psql -U postgres -d 2025_1_Minecraft

Verificar Tabelas
^^^^^^^^^^^^^^^^

.. code-block:: sql

   -- Listar tabelas
   \dt
   
   -- Verificar dados
   SELECT COUNT(*) FROM jogador;
   SELECT COUNT(*) FROM chunk;
   SELECT COUNT(*) FROM bioma;

Verificar Mapa Completo
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   -- Verificar total de chunks
   SELECT COUNT(*) as total_chunks FROM chunk;
   
   -- Verificar chunks por turno
   SELECT id_mapa_turno, COUNT(*) as chunks 
   FROM chunk 
   GROUP BY id_mapa_turno;
   
   -- Verificar distribuição de biomas
   SELECT id_bioma, COUNT(*) as quantidade 
   FROM chunk 
   GROUP BY id_bioma 
   ORDER BY quantidade DESC;

Performance
-----------

Otimizações Implementadas
^^^^^^^^^^^^^^^^^^^^^^^^

* **Índices** em chaves estrangeiras
* **JOINs otimizados** com LEFT JOIN
* **Queries preparadas** com parâmetros
* **Conexões gerenciadas** com context managers
* **Verificações automáticas** de integridade

Monitoramento de Performance
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   -- Verificar uso de índices
   EXPLAIN ANALYZE SELECT * FROM jogador WHERE id_chunk_atual = 1;
   
   -- Verificar tamanho das tabelas
   SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
   FROM pg_tables WHERE schemaname = 'public';
   
   -- Verificar performance de queries no mapa
   EXPLAIN ANALYZE SELECT COUNT(*) FROM chunk WHERE id_mapa_turno = 'Dia';

Próximos Passos
---------------

Para mais informações:

* :doc:`api_reference` - Documentação da API
* :doc:`development` - Guia de desenvolvimento
* :doc:`contributing` - Como contribuir

Sistema de Jogo
---------------

Visão Geral
-----------

O MINECRAFT - FGA - 2025/1 implementa um sistema de jogo baseado em chunks e biomas, onde os personagens podem se mover entre diferentes áreas do mapa.

Localização dos Personagens
---------------------------

Sistema de Chunks
^^^^^^^^^^^^^^^^

* Cada personagem está localizado em um **chunk específico**
* Os chunks são numerados de 1 a 2000 (1000 para dia + 1000 para noite)
* A localização é persistida no banco de dados via `id_chunk_atual`

Biomas Disponíveis
^^^^^^^^^^^^^^^^^

* **🏜️ Deserto**: Área central do mapa (~8% da área total)
* **🌊 Oceano**: Bordas do mapa (~10% da área)
* **🌴 Selva**: Interior do mapa (~41% da área)
* **🌲 Floresta**: Interior do mapa (~41% da área)

Turnos
^^^^^^

* **☀️ Dia**: Chunks 1-1000
* **🌙 Noite**: Chunks 1001-2000

Inicialização de Personagens
---------------------------

Novos Personagens
^^^^^^^^^^^^^^^^

* **Localização inicial**: Deserto (chunk 364)
* **Vida máxima**: 100
* **Força inicial**: 10
* **XP inicial**: 0

Personagens Existentes
^^^^^^^^^^^^^^^^^^^^

* **Carregam** a localização onde estavam por último
* **Se não tiverem localização**: São colocados no deserto automaticamente

Sistema de Movimento
-------------------

Chunks Adjacentes
^^^^^^^^^^^^^^^^

O sistema calcula chunks adjacentes baseado em:

.. code-block:: sql

   -- Movimento horizontal e vertical
   numero_chunk IN (
       %s - 1, %s + 1,  -- Horizontal
       %s - 32, %s + 32  -- Vertical (mapa 32x32)
   )

Lógica de Movimento
^^^^^^^^^^^^^^^^^

1. **Verifica chunks adjacentes** no mesmo turno
2. **Exibe opções disponíveis** com bioma e chunk ID
3. **Move o personagem** para o chunk selecionado
4. **Atualiza sessão e banco** simultaneamente

Interface de Jogo
----------------

Tela Principal
^^^^^^^^^^^^

.. code-block:: text

   ╔══════════════════════════════════════════════════╗
   ║         🟩 MINECRAFT - FGA - 2025/1              ║
   ║              Python Edition                      ║
   ╚══════════════════════════════════════════════════╝

   ============================================================
   🎮 JOGANDO COM: TestePlayer
   ============================================================
   🏜️ BIOMA: Deserto
   ☀️ TURNO: Dia
   📍 CHUNK: 364
   ============================================================
   ❤️  Vida: 100/100
   ⭐ XP: 0 | 💪 Força: 10

   🚶 OPÇÕES DE MOVIMENTO:
   ----------------------------------------
   1. 🌲 Floresta (Chunk 363)
   2. 🏜️ Deserto (Chunk 365)
   3. 🌲 Floresta (Chunk 332)
   4. 🏜️ Deserto (Chunk 396)

   🎮 OPÇÕES DO JOGO:
   1-4. Mover para direção
   5. 💾 Salvar progresso
   6. 📊 Ver status detalhado
   7. 🔙 Voltar ao menu principal

Opções de Movimento
^^^^^^^^^^^^^^^^^^

* **1-4**: Mover para chunks adjacentes
* **5**: Salvar progresso atual
* **6**: Ver status detalhado do personagem
* **7**: Voltar ao menu principal

Sistema de Sessão
----------------

PlayerSession
^^^^^^^^^^^^

.. code-block:: python

   @dataclass
   class PlayerSession:
       id_jogador: int
       nome: str
       vida_max: int
       vida_atual: int
       xp: int
       forca: int
       id_chunk_atual: Optional[int] = None
       chunk_bioma: Optional[str] = None
       chunk_mapa_nome: Optional[str] = None
       chunk_mapa_turno: Optional[str] = None

Gerenciamento de Estado
^^^^^^^^^^^^^^^^^^^^^^

* **Carregamento**: Dados completos do banco + chunk atual
* **Movimento**: Atualização simultânea de sessão e banco
* **Persistência**: Salvamento automático ao sair do jogo

Funções de Movimento
-------------------

get_adjacent_chunks()
^^^^^^^^^^^^^^^^^^^^

Busca chunks adjacentes ao chunk atual:

.. code-block:: python

   def get_adjacent_chunks(chunk_id: int, turno: str = 'Dia') -> List[Tuple[int, str]]:
       """Retorna os chunks adjacentes ao chunk atual"""
       # Retorna lista de tuplas (chunk_id, bioma)

move_player_to_chunk()
^^^^^^^^^^^^^^^^^^^^^

Move o personagem para um novo chunk:

.. code-block:: python

   def move_player_to_chunk(chunk_id: int) -> bool:
       """Move o personagem atual para um novo chunk"""
       # Atualiza tanto a sessão quanto o banco de dados

ensure_player_location()
^^^^^^^^^^^^^^^^^^^^^^^

Garante que o personagem tem localização válida:

.. code-block:: python

   def ensure_player_location() -> bool:
       """Garante que o personagem atual tem uma localização válida"""
       # Se não tiver, coloca no deserto

Queries de Movimento
-------------------

Buscar Chunks Adjacentes
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   SELECT numero_chunk, id_bioma
   FROM chunk 
   WHERE id_mapa_turno = 'Dia' 
   AND numero_chunk IN (
       364 - 1, 364 + 1,  -- Horizontal
       364 - 32, 364 + 32  -- Vertical
   )
   ORDER BY numero_chunk;

Mover Personagem
^^^^^^^^^^^^^^^

.. code-block:: sql

   UPDATE jogador 
   SET id_chunk_atual = %s
   WHERE id_jogador = %s;

Buscar Chunk de Deserto
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   SELECT numero_chunk
   FROM chunk 
   WHERE id_bioma = 'Deserto' AND id_mapa_turno = 'Dia'
   LIMIT 1;

Exemplos de Uso
--------------

Criar Personagem no Deserto
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Criar personagem (automaticamente no deserto)
   new_player = create_new_player("Aventureiro", 100, 10)
   
   # Verificar localização
   print(f"Localização: {new_player.chunk_bioma}")
   # Saída: Localização: Deserto

Mover Personagem
^^^^^^^^^^^^^^^

.. code-block:: python

   # Buscar chunks adjacentes
   adjacent = get_adjacent_chunks(364, 'Dia')
   # Resultado: [(363, 'Floresta'), (365, 'Deserto'), ...]
   
   # Mover para floresta
   success = move_player_to_chunk(363)
   if success:
       print("Movido para Floresta!")

Verificar Localização
^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   -- Verificar onde está um personagem
   SELECT 
       j.nome, j.id_chunk_atual,
       c.id_bioma, c.id_mapa_turno
   FROM jogador j
   LEFT JOIN chunk c ON j.id_chunk_atual = c.numero_chunk
   WHERE j.nome = 'TestePlayer';

Monitoramento de Jogo
--------------------

Verificar Movimento
^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   -- Histórico de localizações (se implementado)
   SELECT 
       j.nome, j.id_chunk_atual,
       c.id_bioma, c.id_mapa_turno
   FROM jogador j
   LEFT JOIN chunk c ON j.id_chunk_atual = c.numero_chunk
   ORDER BY j.nome;

Estatísticas de Biomas
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   -- Personagens por bioma
   SELECT 
       c.id_bioma, COUNT(*) as personagens
   FROM jogador j
   JOIN chunk c ON j.id_chunk_atual = c.numero_chunk
   GROUP BY c.id_bioma
   ORDER BY personagens DESC;

Performance
-----------

Otimizações de Movimento
^^^^^^^^^^^^^^^^^^^^^^^

* **JOIN otimizado** para carregar dados do chunk
* **Índices** em `numero_chunk` e `id_mapa_turno`
* **Sessão em memória** para evitar queries desnecessárias
* **Atualização em lote** de sessão e banco

Monitoramento de Performance
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   -- Verificar performance de busca de chunks adjacentes
   EXPLAIN ANALYZE 
   SELECT numero_chunk, id_bioma
   FROM chunk 
   WHERE id_mapa_turno = 'Dia' 
   AND numero_chunk IN (364-1, 364+1, 364-32, 364+32);

Próximos Passos
---------------

Para mais informações:

* :doc:`api_reference` - Documentação da API
* :doc:`development` - Guia de desenvolvimento
* :doc:`contributing` - Como contribuir 
