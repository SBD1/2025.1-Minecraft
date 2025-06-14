Desenvolvimento
==============

Este guia irá ajudá-lo a configurar o ambiente de desenvolvimento e entender a arquitetura do projeto.

Estrutura do Projeto
--------------------

.. code-block:: text

   2025.1-Minecraft/
   ├── app/                          # Aplicação principal
   │   ├── main.py                   # Ponto de entrada
   │   ├── Dockerfile                # Container da aplicação
   │   ├── requirements.txt          # Dependências Python
   │   └── src/                      # Código fonte
   │       ├── interface/            # Interface do usuário
   │       │   └── display.py        # Menus e exibição
   │       └── utils/                # Utilitários
   │           ├── player_manager.py # Gerenciamento de personagens
   │           └── db_helpers.py     # Helpers do banco de dados
   ├── db/                           # Banco de dados
   │   ├── ddl.sql                   # Definição das tabelas
   │   ├── dml.sql                   # Dados iniciais
   │   ├── Dockerfile.db             # Container do banco
   │   └── create_user.sql           # Criação de usuários
   ├── docs/                         # Documentação
   │   ├── source/                   # Arquivos fonte do Sphinx
   │   └── build/                    # Documentação gerada
   ├── docker-compose.yml            # Orquestração dos containers
   └── README.md                     # Documentação principal

Arquitetura
-----------

Padrão de Arquitetura
^^^^^^^^^^^^^^^^^^^^^

O projeto segue uma arquitetura modular com separação clara de responsabilidades:

* **Interface Layer** (``interface/display.py``)
  * Menus e interação com usuário
  * Validação de entrada
  * Formatação de saída

* **Business Logic Layer** (``utils/player_manager.py``)
  * Lógica de negócio
  * Gerenciamento de estado
  * Operações de personagens

* **Data Access Layer** (``utils/db_helpers.py``)
  * Conexão com banco de dados
  * Execução de queries
  * Inicialização do banco

* **Data Layer** (``db/``)
  * Scripts SQL
  * Configuração do banco
  * Dados iniciais

Fluxo de Dados
^^^^^^^^^^^^^

.. image:: _static/architecture-flow.png
   :alt: Fluxo de Dados
   :align: center

1. **Interface** recebe entrada do usuário
2. **Business Logic** processa a lógica
3. **Data Access** executa operações no banco
4. **Interface** exibe resultados

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

Módulo player_manager
^^^^^^^^^^^^^^^^^^^^

Responsável pelo gerenciamento de personagens:

.. code-block:: python

   # Variável global para personagem ativo
   current_player: Optional[PlayerSession] = None
   
   # Classe principal
   @dataclass
   class PlayerSession:
       # Atributos do personagem
   
   # Funções de gerenciamento
   def set_current_player(player_data: PlayerSession) -> None:
       """Define o personagem ativo"""
   
   def get_current_player() -> Optional[PlayerSession]:
       """Retorna o personagem ativo"""
   
   def load_player_by_id(player_id: int) -> Optional[PlayerSession]:
       """Carrega personagem do banco"""

Módulo db_helpers
^^^^^^^^^^^^^^^^

Gerencia conexões e operações do banco:

.. code-block:: python

   def connection_db():
       """Cria conexão com PostgreSQL"""
   
   def setup_database():
       """Configura banco antes da execução"""
   
   def check_tables_exist():
       """Verifica se tabelas existem"""
   
   def initialize_database():
       """Inicializa estrutura e dados"""

Módulo display
^^^^^^^^^^^^^

Interface do usuário e menus:

.. code-block:: python

   def menu_inicial():
       """Menu principal do jogo"""
   
   def criar_jogador():
       """Interface de criação de personagem"""
   
   def listar_jogadores():
       """Lista personagens em grid"""
   
   def sair_jogo():
       """Encerra o jogo"""

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

Crie testes para funções críticas:

.. code-block:: python

   def test_criar_personagem():
       """Testa criação de personagem"""
       player = create_new_player("Teste", 100, 10)
       assert player is not None
       assert player.nome == "Teste"
       assert player.vida_max == 100

   def test_validar_nome():
       """Testa validação de nome"""
       assert validar_nome("João") == True
       assert validar_nome("") == False
       assert validar_nome("   ") == False

Executando Testes
^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Instalar pytest
   pip install pytest
   
   # Executar testes
   pytest tests/
   
   # Com cobertura
   pytest --cov=app tests/

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