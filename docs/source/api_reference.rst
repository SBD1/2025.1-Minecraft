Referência da API
================

Esta seção documenta as APIs e módulos do MINECRAFT - FGA - 2025/1.

Módulos Principais
-----------------

.. toctree::
   :maxdepth: 2

   modules/models
   modules/repositories
   modules/services
   modules/interface
   modules/utils

Módulo Models
------------

.. automodule:: models.player
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: models.chunk
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: models.mapa
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: models.bioma
   :members:
   :undoc-members:
   :show-inheritance:

Player
^^^^^^

.. autoclass:: models.player.Player
   :members:
   :undoc-members:
   :show-inheritance:

Chunk
^^^^^

.. autoclass:: models.chunk.Chunk
   :members:
   :undoc-members:
   :show-inheritance:

Mapa
^^^^

.. autoclass:: models.mapa.Mapa
   :members:
   :undoc-members:
   :show-inheritance:

Bioma
^^^^^

.. autoclass:: models.bioma.Bioma
   :members:
   :undoc-members:
   :show-inheritance:

Módulo Repositories
------------------

.. automodule:: repositories.player_repository
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: repositories.chunk_repository
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: repositories.mapa_repository
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: repositories.bioma_repository
   :members:
   :undoc-members:
   :show-inheritance:

PlayerRepository
^^^^^^^^^^^^^^^

.. autoclass:: repositories.player_repository.PlayerRepository
   :members:
   :undoc-members:
   :show-inheritance:

ChunkRepository
^^^^^^^^^^^^^^

.. autoclass:: repositories.chunk_repository.ChunkRepository
   :members:
   :undoc-members:
   :show-inheritance:

MapaRepository
^^^^^^^^^^^^^

.. autoclass:: repositories.mapa_repository.MapaRepository
   :members:
   :undoc-members:
   :show-inheritance:

BiomaRepository
^^^^^^^^^^^^^^

.. autoclass:: repositories.bioma_repository.BiomaRepository
   :members:
   :undoc-members:
   :show-inheritance:

Módulo Services
--------------

.. automodule:: services.interface_service
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: services.game_service
   :members:
   :undoc-members:
   :show-inheritance:

InterfaceService
^^^^^^^^^^^^^^^

.. autoclass:: services.interface_service.InterfaceService
   :members:
   :undoc-members:
   :show-inheritance:

GameService
^^^^^^^^^^

.. autoclass:: services.game_service.GameService
   :members:
   :undoc-members:
   :show-inheritance:

Módulo player_manager
--------------------

.. automodule:: utils.player_manager
   :members:
   :undoc-members:
   :show-inheritance:

PlayerSession
^^^^^^^^^^^^

.. autoclass:: utils.player_manager.PlayerSession
   :members:
   :undoc-members:
   :show-inheritance:

Funções de Gerenciamento
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: utils.player_manager.set_current_player

.. autofunction:: utils.player_manager.get_current_player

.. autofunction:: utils.player_manager.clear_current_player

.. autofunction:: utils.player_manager.load_player_by_id

.. autofunction:: utils.player_manager.refresh_current_player

.. autofunction:: utils.player_manager.save_player_changes

.. autofunction:: utils.player_manager.get_all_players

.. autofunction:: utils.player_manager.create_new_player

.. autofunction:: utils.player_manager.delete_player

.. autofunction:: utils.player_manager.confirm_player_deletion

Funções de Exibição
^^^^^^^^^^^^^^^^^^^

.. autofunction:: utils.player_manager.display_player_status

.. autofunction:: utils.player_manager.get_player_status_lines

.. autofunction:: utils.player_manager.display_players_grid

Módulo db_helpers
-----------------

.. automodule:: utils.db_helpers
   :members:
   :undoc-members:
   :show-inheritance:

Conexão com Banco
^^^^^^^^^^^^^^^^

.. autofunction:: utils.db_helpers.connection_db

Execução de SQL
^^^^^^^^^^^^^^

.. autofunction:: utils.db_helpers.execute_sql_file

Verificações
^^^^^^^^^^^

.. autofunction:: utils.db_helpers.check_database_connection

.. autofunction:: utils.db_helpers.check_tables_exist

.. autofunction:: utils.db_helpers.check_data_seeded

Inicialização
^^^^^^^^^^^^

.. autofunction:: utils.db_helpers.initialize_database

.. autofunction:: utils.db_helpers.setup_database

Módulo display
--------------

.. automodule:: interface.display
   :members:
   :undoc-members:
   :show-inheritance:

Interface Principal
^^^^^^^^^^^^^^^^^^

.. autofunction:: interface.display.tela_inicial

.. autofunction:: interface.display.exibir_titulo

.. autofunction:: interface.display.exibir_jogador_atual

.. autofunction:: interface.display.menu_inicial

Funções de Jogo
^^^^^^^^^^^^^^

.. autofunction:: interface.display.iniciar_jogo

.. autofunction:: interface.display.ver_status_detalhado

.. autofunction:: interface.display.salvar_progresso

.. autofunction:: interface.display.trocar_jogador

.. autofunction:: interface.display.selecionar_jogador

Gerenciamento de Personagens
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: interface.display.criar_jogador

.. autofunction:: interface.display.listar_jogadores

.. autofunction:: interface.display.sair_jogo

Utilitários
^^^^^^^^^^^

.. autofunction:: interface.display.clear_terminal

.. autofunction:: interface.display.mostrar_creeper

.. autofunction:: interface.display.mover_creeper_para_direita

Módulo Utils
------------

.. automodule:: utils.db_helpers
   :members:
   :undoc-members:
   :show-inheritance:

Conexão com Banco
^^^^^^^^^^^^^^^^

.. autofunction:: utils.db_helpers.connection_db

Execução de SQL
^^^^^^^^^^^^^^

.. autofunction:: utils.db_helpers.execute_sql_file

Verificações
^^^^^^^^^^^

.. autofunction:: utils.db_helpers.check_database_connection

.. autofunction:: utils.db_helpers.check_tables_exist

.. autofunction:: utils.db_helpers.check_data_seeded

Inicialização
^^^^^^^^^^^^

.. autofunction:: utils.db_helpers.initialize_database

.. autofunction:: utils.db_helpers.setup_database

Estrutura de Dados
------------------

Player
^^^^^^

A classe ``Player`` representa um jogador no jogo:

.. code-block:: python

   class Player:
       def __init__(self, id_jogador: int, nome: str, vida_max: int, 
                    vida_atual: int, xp: int, forca: int, 
                    id_chunk_atual: Optional[int] = None):
           self.id_jogador = id_jogador
           self.nome = nome
           self.vida_max = vida_max
           self.vida_atual = vida_atual
           self.xp = xp
           self.forca = forca
           self.id_chunk_atual = id_chunk_atual

Atributos:
* ``id_jogador``: ID único do personagem no banco
* ``nome``: Nome do personagem
* ``vida_max``: Vida máxima
* ``vida_atual``: Vida atual
* ``xp``: Experiência acumulada
* ``forca``: Força do personagem
* ``id_chunk_atual``: ID do chunk atual

Métodos:
* ``is_alive()``: Verifica se está vivo
* ``take_damage(damage)``: Aplica dano
* ``heal(amount)``: Cura o personagem
* ``gain_xp(amount)``: Adiciona experiência

Chunk
^^^^^

A classe ``Chunk`` representa uma divisão do mundo:

.. code-block:: python

   class Chunk:
       def __init__(self, numero_chunk: int, id_bioma: str, 
                    id_mapa_nome: str, id_mapa_turno: str):
           self.numero_chunk = numero_chunk
           self.id_bioma = id_bioma
           self.id_mapa_nome = id_mapa_nome
           self.id_mapa_turno = id_mapa_turno

Mapa
^^^^

A classe ``Mapa`` representa um mapa do jogo:

.. code-block:: python

   class Mapa:
       def __init__(self, nome: str, turno: str):
           self.nome = nome
           self.turno = turno

Bioma
^^^^^

A classe ``Bioma`` representa um tipo de bioma:

.. code-block:: python

   class Bioma:
       def __init__(self, nome_bioma: str):
           self.nome_bioma = nome_bioma

Padrões de Uso
--------------

Gerenciamento de Jogadores
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Criar jogador
   player = Player(1, "João", 100, 100, 0, 10)
   
   # Salvar no banco
   saved_player = player_repository.save(player)
   
   # Carregar jogador
   loaded_player = player_repository.find_by_id(1)
   
   # Aplicar dano
   loaded_player.take_damage(20)
   
   # Salvar alterações
   player_repository.save(loaded_player)

Gerenciamento de Chunks
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Buscar chunk
   chunk = chunk_repository.find_by_id(1)
   
   # Buscar chunks adjacentes
   adjacent_chunks = chunk_repository.find_adjacent_chunks(1, "Dia")
   
   # Mover jogador para chunk
   player.id_chunk_atual = chunk.numero_chunk
   player_repository.save(player)

Uso dos Services
^^^^^^^^^^^^^^^

.. code-block:: python

   # Usar InterfaceService
   interface_service = InterfaceService()
   
   # Criar jogador via service
   player = interface_service.create_player("João", 100, 10)
   
   # Mover jogador
   interface_service.move_player_to_chunk(player, 1)
   
   # Obter estatísticas
   stats = interface_service.get_player_statistics()

Próximos Passos
---------------

Para mais informações:

* :doc:`database` - Estrutura do banco de dados
* :doc:`development` - Guia de desenvolvimento
* :doc:`contributing` - Como contribuir 