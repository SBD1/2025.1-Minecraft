Referência da API
================

Esta seção documenta as APIs e módulos do Minecraft Legends.

Módulos Principais
-----------------

.. toctree::
   :maxdepth: 2

   modules/player_manager
   modules/db_helpers
   modules/display

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

Estrutura de Dados
------------------

PlayerSession
^^^^^^^^^^^^

A classe ``PlayerSession`` representa um personagem ativo na sessão:

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

Atributos:
* ``id_jogador``: ID único do personagem no banco
* ``nome``: Nome do personagem
* ``vida_max``: Vida máxima
* ``vida_atual``: Vida atual
* ``xp``: Experiência acumulada
* ``forca``: Força do personagem
* ``id_chunk_atual``: ID do chunk atual
* ``chunk_bioma``: Nome do bioma atual
* ``chunk_mapa_nome``: Nome do mapa atual
* ``chunk_mapa_turno``: Turno atual (Dia/Noite)

Métodos:
* ``to_dict()``: Converte para dicionário
* ``is_alive()``: Verifica se está vivo
* ``take_damage(damage)``: Aplica dano
* ``heal(amount)``: Cura o personagem
* ``gain_xp(amount)``: Adiciona experiência

Padrões de Uso
--------------

Gerenciamento de Sessão
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Carregar personagem
   player = load_player_by_id(1)
   set_current_player(player)
   
   # Verificar personagem ativo
   current = get_current_player()
   if current:
       print(f"Personagem ativo: {current.nome}")
   
   # Limpar sessão
   clear_current_player()

Criação de Personagem
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Criar novo personagem
   new_player = create_new_player("Nome", vida_max=100, forca=10)
   if new_player:
       set_current_player(new_player)

Salvamento de Dados
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Salvar alterações
   if save_player_changes():
       print("Dados salvos com sucesso!")
   
   # Atualizar dados do banco
   refresh_current_player()

Exibição de Status
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Exibir status detalhado
   display_player_status()
   
   # Obter linhas de status
   lines = get_player_status_lines(player)
   
   # Exibir grid de personagens
   players = get_all_players()
   display_players_grid(players)

Tratamento de Erros
-------------------

Conexão com Banco
^^^^^^^^^^^^^^^^

.. code-block:: python

   try:
       conn = connection_db()
       # Operações com banco
   except Exception as e:
       print(f"Erro de conexão: {e}")
   finally:
       conn.close()

Validação de Dados
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Validar nome único
   players = get_all_players()
   if any(p[1].lower() == nome.lower() for p in players):
       print("Nome já existe!")
   
   # Validar personagem ativo
   current = get_current_player()
   if not current:
       print("Nenhum personagem ativo!")

Exemplos Práticos
-----------------

Exemplo Completo de Criação
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   def criar_e_selecionar_personagem(nome: str):
       """Cria um personagem e o seleciona automaticamente"""
       
       # Verificar se nome é válido
       if not nome.strip():
           print("Nome não pode estar vazio!")
           return False
       
       # Verificar se nome já existe
       players = get_all_players()
       if any(p[1].lower() == nome.lower() for p in players):
           print("Nome já existe!")
           return False
       
       # Criar personagem
       new_player = create_new_player(nome)
       if not new_player:
           print("Erro ao criar personagem!")
           return False
       
       # Selecionar personagem
       set_current_player(new_player)
       print(f"Personagem '{nome}' criado e selecionado!")
       return True

Exemplo de Backup de Dados
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   def backup_personagem(player_id: int):
       """Faz backup dos dados de um personagem"""
       
       # Carregar personagem
       player = load_player_by_id(player_id)
       if not player:
           print("Personagem não encontrado!")
           return None
       
       # Converter para dicionário
       backup_data = player.to_dict()
       
       # Salvar em arquivo (exemplo)
       import json
       with open(f"backup_{player_id}.json", "w") as f:
           json.dump(backup_data, f, indent=2)
       
       print(f"Backup criado: backup_{player_id}.json")
       return backup_data

Exemplo de Sistema de Combate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   def combate_simples(atacante: PlayerSession, defensor: PlayerSession, dano: int):
       """Sistema simples de combate"""
       
       # Aplicar dano
       if defensor.take_damage(dano):
           print(f"{defensor.nome} sofreu {dano} de dano!")
           print(f"Vida restante: {defensor.vida_atual}/{defensor.vida_max}")
       else:
           print(f"{defensor.nome} foi derrotado!")
       
       # Salvar alterações
       save_player_changes()
       
       return defensor.is_alive()

Próximos Passos
---------------

Para mais informações:

* :doc:`database` - Estrutura do banco de dados
* :doc:`development` - Guia de desenvolvimento
* :doc:`contributing` - Como contribuir 