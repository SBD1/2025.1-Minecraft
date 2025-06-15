Desenvolvimento
==============

Este guia irá ajudá-lo a configurar o ambiente de desenvolvimento e entender a arquitetura do projeto MINECRAFT - FGA - 2025/1.

Estrutura do Projeto
--------------------

.. code-block:: text

   2025.1-Minecraft/
   ├── app/                          # Aplicação principal
   │   ├── main.py                   # Ponto de entrada
   │   ├── Dockerfile                # Container da aplicação
   │   ├── requirements.txt          # Dependências Python
   │   ├── pytest.ini               # Configuração do pytest
   │   ├── run_tests.py             # Script de execução de testes
   │   └── src/                      # Código fonte
   │       ├── interface/            # Interface do usuário
   │       │   └── display.py        # Menus e exibição
   │       ├── services/             # Lógica de negócio
   │       │   ├── game_service.py   # Serviços do jogo
   │       │   └── interface_service.py # Serviços da interface
   │       ├── repositories/         # Acesso a dados
   │       │   ├── player_repository.py
   │       │   ├── chunk_repository.py
   │       │   ├── mapa_repository.py
   │       │   └── bioma_repository.py
   │       ├── models/               # Entidades de domínio
   │       │   ├── player.py         # Modelo do jogador
   │       │   ├── chunk.py          # Modelo do chunk
   │       │   ├── mapa.py           # Modelo do mapa
   │       │   └── bioma.py          # Modelo do bioma
   │       └── utils/                # Utilitários
   │           └── db_helpers.py     # Helpers do banco de dados
   ├── db/                           # Scripts do banco de dados
   │   ├── Dockerfile.db             # Container do PostgreSQL
   │   ├── ddl.sql                   # Definição das tabelas
   │   ├── trigger_SP.sql            # Triggers e stored procedures
   │   ├── dml.sql                   # Dados iniciais
   │   ├── dml_inst.sql              # Dados de instância
   │   └── create_user.sql           # Criação de usuários
   ├── docs/                         # Documentação
   │   ├── source/                   # Arquivos fonte do Sphinx
   │   ├── build/                    # Documentação gerada
   │   ├── architecture.md           # Documentação da arquitetura
   │   └── build_docs.sh             # Script de build
   ├── docker-compose.yml            # Orquestração dos containers
   └── README.md                     # Documentação principal

Arquitetura
-----------

Padrão de Arquitetura
^^^^^^^^^^^^^^^^^^^^^

O projeto segue uma arquitetura em camadas com padrão Repository:

* **Interface Layer** (``src/interface/``)
  * Interface com o usuário
  * Menus e exibição
  * Validação de entrada

* **Service Layer** (``src/services/``)
  * Lógica de negócio
  * Coordenação entre camadas
  * Validações de domínio

* **Repository Layer** (``src/repositories/``)
  * Acesso a dados
  * Persistência
  * Operações CRUD

* **Model Layer** (``src/models/``)
  * Entidades de domínio
  * Validações de modelo
  * Lógica de negócio específica

* **Utils Layer** (``src/utils/``)
  * Funções auxiliares
  * Conexão com banco
  * Utilitários gerais

Fluxo de Dados
^^^^^^^^^^^^^

.. image:: _static/architecture-flow.png
   :alt: Fluxo de Dados
   :align: center

1. **Interface** recebe entrada do usuário
2. **Service** processa a lógica de negócio
3. **Repository** executa operações no banco
4. **Model** representa as entidades
5. **Interface** exibe resultados

Padrão Repository
^^^^^^^^^^^^^^^^

Cada repositório implementa uma interface comum:

.. code-block:: python

   class PlayerRepository:
       def find_all(self) -> List[Player]
       def find_by_id(self, id: int) -> Optional[Player]
       def save(self, player: Player) -> Optional[Player]
       def delete(self, id: int) -> bool
       def find_by_name(self, name: str) -> Optional[Player]

Configuração do Ambiente
------------------------

Pré-requisitos
^^^^^^^^^^^^^

* Python 3.10+
* Docker e Docker Compose
* Git
* Editor de código (VS Code, PyCharm, etc.)

Configuração Local
^^^^^^^^^^^^^^^^^

#. Clone o repositório::

   git clone https://github.com/SBD1/2025.1-Minecraft.git
   cd 2025.1-Minecraft

#. Configure o ambiente virtual::

   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # ou
   venv\Scripts\activate     # Windows

#. Instale dependências::

   pip install -r app/requirements.txt

#. Inicie os containers::

   docker-compose up -d

#. Execute o jogo::

   python app/main.py

Desenvolvimento com Docker
^^^^^^^^^^^^^^^^^^^^^^^^^

Para desenvolvimento dentro do container:

#. Acesse o container::

   docker exec -it python_mine bash

#. Instale dependências de desenvolvimento::

   pip install sphinx sphinx-rtd-theme

#. Execute o jogo::

   python main.py

Estrutura do Código
-------------------

Módulo Models
^^^^^^^^^^^^

Entidades de domínio do jogo:

.. code-block:: python

   # Player - Representa um jogador
   class Player:
       def __init__(self, id_jogador, nome, vida_max, vida_atual, xp, forca, id_chunk_atual=None)
       
       def is_alive(self) -> bool
       def take_damage(self, damage: int) -> None
       def heal(self, amount: int) -> None
       def gain_xp(self, amount: int) -> None
   
   # Chunk - Representa uma divisão do mundo
   class Chunk:
       def __init__(self, numero_chunk, id_bioma, id_mapa_nome, id_mapa_turno)
   
   # Mapa - Representa um mapa do jogo
   class Mapa:
       def __init__(self, nome, turno)
   
   # Bioma - Representa um tipo de bioma
   class Bioma:
       def __init__(self, nome_bioma)

Módulo Repositories
^^^^^^^^^^^^^^^^^^

Acesso e persistência de dados:

.. code-block:: python

   # PlayerRepository - Operações com jogadores
   class PlayerRepository:
       def find_all(self) -> List[Player]
       def find_by_id(self, id: int) -> Optional[Player]
       def save(self, player: Player) -> Optional[Player]
       def delete(self, id: int) -> bool
       def find_by_name(self, name: str) -> Optional[Player]
   
   # ChunkRepository - Operações com chunks
   class ChunkRepository:
       def find_all(self) -> List[Chunk]
       def find_by_id(self, id: int) -> Optional[Chunk]
       def find_adjacent_chunks(self, chunk_id: int, turno: str) -> List[tuple]
   
   # MapaRepository - Operações com mapas
   class MapaRepository:
       def find_all(self) -> List[Mapa]
       def find_by_name_and_turn(self, nome: str, turno: str) -> Optional[Mapa]
   
   # BiomaRepository - Operações com biomas
   class BiomaRepository:
       def find_all(self) -> List[Bioma]
       def find_by_name(self, nome: str) -> Optional[Bioma]

Módulo Services
^^^^^^^^^^^^^^

Lógica de negócio e coordenação:

.. code-block:: python

   # InterfaceService - Coordena interface com repositórios
   class InterfaceService:
       def get_all_players(self) -> List[Player]
       def create_player(self, nome: str, vida_maxima: int, forca: int) -> Optional[Player]
       def save_player(self, player: Player) -> Optional[Player]
       def delete_player(self, player_id: int) -> bool
       def move_player_to_chunk(self, player: Player, chunk_id: int) -> Optional[Player]
       def get_adjacent_chunks(self, chunk_id: int, turno: str) -> List[tuple]
       def get_player_statistics(self) -> Dict[str, Any]
   
   # GameService - Lógica específica do jogo
   class GameService:
       def start_game(self, player: Player) -> bool
       def end_game(self, player: Player) -> bool
       def process_turn(self, player: Player) -> Dict[str, Any]

Módulo Interface
^^^^^^^^^^^^^^^

Interface com o usuário:

.. code-block:: python

   def tela_inicial():
       """Tela principal do jogo"""
   
   def menu_inicial():
       """Menu principal com opções"""
   
   def criar_jogador():
       """Interface de criação de personagem"""
   
   def listar_jogadores():
       """Lista personagens em grid"""
   
   def ver_status_detalhado():
       """Mostra informações completas do personagem"""
   
   def trocar_jogador():
       """Interface de troca de personagem"""
   
   def sair_jogo():
       """Encerra o jogo"""

Módulo Utils
^^^^^^^^^^^

Funções auxiliares:

.. code-block:: python

   def connection_db():
       """Cria conexão com PostgreSQL"""
   
   def setup_database():
       """Configura banco antes da execução"""
   
   def check_tables_exist():
       """Verifica se tabelas existem"""
   
   def initialize_database():
       """Inicializa estrutura e dados"""

Padrões de Código
-----------------

Convenções de Nomenclatura
^^^^^^^^^^^^^^^^^^^^^^^^^^

* **Funções**: snake_case (``criar_jogador``)
* **Variáveis**: snake_case (``current_player``)
* **Classes**: PascalCase (``PlayerSession``)
* **Constantes**: UPPER_CASE (``MAX_LIFE``)
* **Módulos**: snake_case (``player_manager``)

Documentação
^^^^^^^^^^^^

Use docstrings no formato Google:

.. code-block:: python

   def criar_personagem(nome: str, vida_max: int = 100) -> Optional[PlayerSession]:
       """Cria um novo personagem no banco de dados.
       
       Args:
           nome: Nome único do personagem
           vida_max: Vida máxima (padrão: 100)
       
       Returns:
           PlayerSession do personagem criado ou None se erro
       
       Raises:
           ValueError: Se nome for inválido
       """

Tratamento de Erros
^^^^^^^^^^^^^^^^^^^

Use try/except com mensagens específicas:

.. code-block:: python

   try:
       conn = connection_db()
       # Operações
   except psycopg2.Error as e:
       print(f"❌ Erro de banco: {e}")
   except Exception as e:
       print(f"❌ Erro inesperado: {e}")
   finally:
       conn.close()

Validação de Dados
^^^^^^^^^^^^^^^^^^

Valide sempre as entradas:

.. code-block:: python

   def validar_nome(nome: str) -> bool:
       """Valida nome do personagem"""
       if not nome or not nome.strip():
           return False
       if len(nome) > 100:
           return False
       return True

Testes
------

Estrutura de Testes
^^^^^^^^^^^^^^^^^^

O projeto possui uma estrutura completa de testes:

.. code-block:: text

   tests/
   ├── __init__.py
   ├── conftest.py                    # Configuração do pytest
   ├── test_bioma.py                  # Testes do modelo Bioma
   ├── test_chunk.py                  # Testes do modelo Chunk
   ├── test_mapa.py                   # Testes do modelo Mapa
   ├── test_integration.py            # Testes de integração
   ├── test_repository_pattern.py     # Testes do padrão Repository
   └── test_singleton.py              # Testes de padrões de design

Tipos de Testes
^^^^^^^^^^^^^^

**Testes Unitários**: Testam componentes isolados
.. code-block:: python

   def test_bioma_creation():
       """Testa criação de bioma"""
       bioma = Bioma("Deserto")
       assert bioma.nome_bioma == "Deserto"

   def test_player_damage():
       """Testa sistema de dano"""
       player = Player(1, "Teste", 100, 100, 0, 10)
       player.take_damage(20)
       assert player.vida_atual == 80

**Testes de Integração**: Testam interação entre camadas
.. code-block:: python

   def test_player_repository_integration():
       """Testa integração com banco de dados"""
       player = Player(1, "Teste", 100, 100, 0, 10)
       saved_player = player_repository.save(player)
       assert saved_player is not None
       assert saved_player.id_jogador == 1

**Testes de Padrões**: Testam implementação de padrões de design
.. code-block:: python

   def test_repository_pattern():
       """Testa padrão Repository"""
       players = player_repository.find_all()
       assert isinstance(players, list)

Executando Testes
^^^^^^^^^^^^^^^^

**Com Docker (Recomendado)**:
.. code-block:: bash

   # Executar todos os testes
   docker compose exec app python -m pytest tests/ -v
   
   # Executar com cobertura
   docker compose exec app python -m pytest tests/ --cov=src --cov-report=term-missing
   
   # Executar teste específico
   docker compose exec app python -m pytest tests/test_bioma.py::TestBioma::test_bioma_creation -v
   
   # Executar testes de integração
   docker compose exec app python -m pytest tests/test_integration.py -v

**Localmente**:
.. code-block:: bash

   # Instalar dependências
   pip install -r app/requirements.txt
   
   # Executar testes
   cd app
   python -m pytest tests/ -v

**Script de Testes**:
.. code-block:: bash

   # Usar script de execução
   cd app
   python run_tests.py

Configuração do Pytest
^^^^^^^^^^^^^^^^^^^^^

O projeto usa `pytest.ini` para configuração:

.. code-block:: ini

   [tool:pytest]
   testpaths = tests
   python_files = test_*.py
   python_classes = Test*
   python_functions = test_*
   addopts = 
       -v
       --tb=short
       --strict-markers
   markers =
       unit: Unit tests
       integration: Integration tests
       slow: Slow running tests

Cobertura de Código
^^^^^^^^^^^^^^^^^^

O projeto gera relatórios de cobertura:

.. code-block:: bash

   # Gerar relatório HTML
   docker compose exec app python -m pytest tests/ --cov=src --cov-report=html
   
   # Ver relatório no navegador
   open app/htmlcov/index.html

**Cobertura Atual**: O projeto mantém alta cobertura de código com relatórios enviados para Codecov.

Debugging
---------

Logs
^^^^

Use prints informativos para debug:

.. code-block:: python

   print(f"🔍 Debug: Criando personagem '{nome}'")
   print(f"🔍 Debug: Dados salvos: {player.to_dict()}")

Debug no Container
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Acessar container
   docker exec -it python_mine bash
   
   # Executar com debug
   python -u main.py
   
   # Ver logs
   docker-compose logs app

Debug no VS Code
^^^^^^^^^^^^^^^

Configure o launch.json:

.. code-block:: json

   {
       "version": "0.2.0",
       "configurations": [
           {
               "name": "Python: Minecraft",
               "type": "python",
               "request": "launch",
               "program": "${workspaceFolder}/app/main.py",
               "console": "integratedTerminal",
               "cwd": "${workspaceFolder}/app"
           }
       ]
   }

Deploy e CI/CD
--------------

GitHub Actions
^^^^^^^^^^^^^

Configure workflows para:

* **Testes automáticos**
* **Build da documentação**
* **Deploy no GitHub Pages**

.. code-block:: yaml

   name: Build Documentation
   on: [push, pull_request]
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Set up Python
           uses: actions/setup-python@v2
           with:
             python-version: 3.10
         - name: Install dependencies
           run: |
             pip install sphinx sphinx-rtd-theme
         - name: Build docs
           run: |
             cd docs
             make html

Deploy Automático
^^^^^^^^^^^^^^^^^

Configure deploy automático no GitHub Pages:

.. code-block:: yaml

   name: Deploy to GitHub Pages
   on:
     push:
       branches: [ main ]
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Deploy
           uses: peaceiris/actions-gh-pages@v3
           with:
             github_token: ${{ secrets.GITHUB_TOKEN }}
             publish_dir: ./docs/build/html

Versionamento
-------------

Semantic Versioning
^^^^^^^^^^^^^^^^^^

Use o padrão MAJOR.MINOR.PATCH:

* **MAJOR**: Mudanças incompatíveis
* **MINOR**: Novas funcionalidades
* **PATCH**: Correções de bugs

Changelog
^^^^^^^^^

Mantenha um CHANGELOG.md:

.. code-block:: markdown

   # Changelog
   
   ## [1.1.0] - 2025-01-XX
   ### Added
   - Sistema de grid para lista de personagens
   - Opção de deletar personagens
   
   ### Changed
   - Melhorada interface de seleção
   
   ### Fixed
   - Correção de mensagens duplicadas

Commits
^^^^^^^

Use commits semânticos:

* **feat**: Nova funcionalidade
* **fix**: Correção de bug
* **docs**: Documentação
* **style**: Formatação
* **refactor**: Refatoração
* **test**: Testes
* **chore**: Tarefas de manutenção

Exemplo: ``feat: add character deletion functionality``

Próximos Passos
---------------

Para continuar o desenvolvimento:

* :doc:`contributing` - Guia de contribuição
* :doc:`api_reference` - Documentação da API
* :doc:`database` - Estrutura do banco 