Banco de Dados
=============

Esta seção documenta a estrutura e configuração do banco de dados do Minecraft Legends.

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
* Inserção de chunks
* Inserção de personagens de exemplo
* Inserção de inventários de exemplo

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

Chunks
^^^^^^

.. code-block:: sql

   INSERT INTO Chunk (Numero_chunk, Id_bioma, Id_mapa_nome, Id_mapa_turno) VALUES
       (1, 'Deserto', 'Mapa_Principal', 'Dia'),
       (2, 'Oceano', 'Mapa_Principal', 'Dia'),
       (3, 'Selva', 'Mapa_Principal', 'Noite'),
       (4, 'Floresta', 'Mapa_Principal', 'Noite');

Personagens de Exemplo
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   INSERT INTO Jogador (Nome, Vida_max, Vida_atual, xp, forca, Id_Chunk_Atual) VALUES
       ('Player1', 100, 100, 0, 10, 1),
       ('Player2', 120, 120, 50, 12, 2);

Inventários de Exemplo
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   INSERT INTO Inventario (id_jogador, id_inventario, Instancia_Item, ArmaduraEquipada, ArmaEquipada) VALUES
       (1, 1, '{"item_id": 101, "quantidade": 5}', 'Capacete de Ferro', 'Espada de Diamante'),
       (2, 1, '{"item_id": 201, "quantidade": 1}', 'Armadura de Couro', 'Arco Longo');

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

Performance
-----------

Otimizações Implementadas
^^^^^^^^^^^^^^^^^^^^^^^^

* **Índices** em chaves estrangeiras
* **JOINs otimizados** com LEFT JOIN
* **Queries preparadas** com parâmetros
* **Conexões gerenciadas** com context managers

Monitoramento de Performance
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sql

   -- Verificar uso de índices
   EXPLAIN ANALYZE SELECT * FROM jogador WHERE id_chunk_atual = 1;
   
   -- Verificar tamanho das tabelas
   SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
   FROM pg_tables WHERE schemaname = 'public';

Próximos Passos
---------------

Para mais informações:

* :doc:`api_reference` - Documentação da API
* :doc:`development` - Guia de desenvolvimento
* :doc:`contributing` - Como contribuir 