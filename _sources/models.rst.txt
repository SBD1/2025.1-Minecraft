Modelos
=======

O MINECRAFT - FGA - 2025/1 utiliza uma arquitetura baseada em models para representar as entidades do jogo. Esta abordagem garante separação de responsabilidades, reutilização de código e facilita a manutenção.

Estrutura de Models
------------------

.. code-block:: text

    app/src/models/
    ├── __init__.py          # Exporta todas as models
    ├── player.py            # Models do personagem (Player e PlayerSession)
    ├── chunk.py             # Model do chunk
    ├── bioma.py             # Model do bioma
    ├── mapa.py              # Model do mapa
    ├── item.py              # Model do item
    └── inventory.py         # Model do inventário

Player
------

A model ``Player`` representa um personagem principal do jogo com todos os seus atributos persistentes.

.. autoclass:: models.player.Player
   :members:
   :undoc-members:
   :show-inheritance:

**Exemplo de uso:**

.. code-block:: python

    from src.models.player import Player
    from src.models.inventory import InventoryEntry
    
    # Criar um personagem
    player = Player(
        id_player=1,
        nome="Steve",
        vida_maxima=100,
        vida_atual=85,
        forca=12,
        localizacao="Mapa 1 - Chunk 1",
        nivel=1,
        experiencia=150,
        current_chunk_id=1
    )
    
    # Verificar se está vivo
    if player.is_alive():
        print("Personagem está vivo!")
    
    # Aplicar dano
    sobreviveu = player.take_damage(20)
    
    # Ganhar experiência
    player.gain_experience(50)
    
    # Tentar subir de nível
    if player.level_up():
        print("Subiu de nível!")
    
    # Exibir barra de vida
    print(player.get_health_bar())

PlayerSession
-------------

A model ``PlayerSession`` representa um personagem ativo na sessão do jogo com informações otimizadas para performance.

.. autoclass:: models.player.PlayerSession
   :members:
   :undoc-members:
   :show-inheritance:

**Exemplo de uso:**

.. code-block:: python

    from src.models.player import PlayerSession
    
    # Criar uma sessão de personagem
    session = PlayerSession(
        id_player=1,
        nome="Steve",
        vida_max=100,
        vida_atual=85,
        xp=150,
        forca=12,
        id_chunk_atual=5,
        chunk_bioma="Oceano",
        chunk_mapa_nome="Mapa_Principal",
        chunk_mapa_turno="Dia"
    )
    
    # Verificar se pode se mover
    if session.can_move():
        print("Pode se mover!")
    
    # Obter localização formatada
    print(session.get_location_display())
    
    # Converter para dicionário
    data = session.to_dict()

Chunk
-----

A model ``Chunk`` representa um chunk do mapa do jogo com suas coordenadas e relacionamentos.

.. autoclass:: models.chunk.Chunk
   :members:
   :undoc-members:
   :show-inheritance:

**Exemplo de uso:**

.. code-block:: python

    from src.models.chunk import Chunk
    
    # Criar um chunk
    chunk = Chunk(
        id_chunk=1,
        id_bioma=2,  # ID do bioma Oceano
        id_mapa=1,   # ID do mapa principal
        x=10,
        y=15
    )
    
    # Verificar tipo de bioma por ID
    if chunk.id_bioma == 2:
        print("É um oceano!")
    
    # Obter nome formatado
    print(chunk.get_display_name())
    
    # Obter chunks adjacentes
    adjacentes = chunk.get_adjacent_chunk_ids()
    
    # Verificar se é dia ou noite baseado na coordenada
    if chunk.is_day():
        print("É dia neste chunk!")

Bioma
-----

A model ``Bioma`` representa um bioma do jogo com suas características.

.. autoclass:: models.bioma.Bioma
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: models.bioma.BiomaType
   :members:
   :undoc-members:
   :show-inheritance:

**Biomas Predefinidos:**

.. code-block:: python

    from src.models.bioma import BIOMAS_PREDEFINIDOS, BiomaType, Bioma
    
    # Usar bioma predefinido
    deserto = BIOMAS_PREDEFINIDOS[BiomaType.DESERTO]
    
    # Criar bioma personalizado
    bioma_custom = Bioma(
        id_bioma=5,
        nome="Tundra",
        descricao="Um bioma frio e gelado."
    )
    
    # Comparar biomas
    if deserto == bioma_custom:
        print("São o mesmo bioma!")

Mapa
----

A model ``Mapa`` representa um mapa do jogo com seus chunks e características temporais.

.. autoclass:: models.mapa.Mapa
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: models.mapa.TurnoType
   :members:
   :undoc-members:
   :show-inheritance:

**Exemplo de uso:**

.. code-block:: python

    from src.models.mapa import Mapa, TurnoType
    
    # Criar mapa
    mapa = Mapa(
        id_mapa=1,
        nome="Mapa_Principal",
        turno=TurnoType.DIA
    )
    
    # Verificar tipo de turno
    if mapa.is_day_map():
        print("É um mapa de dia!")
    
    # Obter informações de exibição
    info = mapa.get_display_info()
    
    # Buscar chunk específico (requer repository configurado)
    # mapa.set_chunk_repository(chunk_repository)
    # chunk = mapa.get_chunk_by_id(1)

Item
----

A model ``Item`` representa um item do jogo que pode ser coletado ou usado.

.. autoclass:: models.item.Item
   :members:
   :undoc-members:
   :show-inheritance:

**Exemplo de uso:**

.. code-block:: python

    from src.models.item import Item
    
    # Criar diferentes tipos de itens
    espada = Item(
        id_item=1,
        nome="Espada de Ferro",
        tipo="Arma",
        poder=8,
        durabilidade=200
    )
    
    pocao = Item(
        id_item=2,
        nome="Poção de Vida",
        tipo="Poção",
        poder=50,
        durabilidade=None  # Poções não têm durabilidade
    )
    
    madeira = Item(
        id_item=3,
        nome="Madeira",
        tipo="Material",
        poder=None,
        durabilidade=None
    )

InventoryEntry
--------------

A model ``InventoryEntry`` representa uma entrada no inventário de um jogador.

.. autoclass:: models.inventory.InventoryEntry
   :members:
   :undoc-members:
   :show-inheritance:

**Exemplo de uso:**

.. code-block:: python

    from src.models.inventory import InventoryEntry
    
    # Criar entrada de inventário
    entrada = InventoryEntry(
        id=1,
        player_id=1,
        item_id=3,  # Madeira
        quantidade=64
    )
    
    # Modificar quantidade
    entrada.quantidade += 32
    print(f"Nova quantidade: {entrada.quantidade}")

Relacionamentos do Banco de Dados
--------------------------------

As models refletem exatamente a estrutura do banco de dados:

.. code-block:: text

    Mapa (id_mapa, nome, turno) ← Chunk (id_mapa)
    Bioma (id_bioma, nome) ← Chunk (id_bioma)
    Chunk (id_chunk) ← Player (current_chunk_id)
    Player (id_player) ← Inventario (player_id)
    Item (id_item) ← Inventario (item_id)

**Características dos Relacionamentos:**

- **Mapa**: Chave primária simples (id_mapa) com constraint única (nome, turno)
- **Bioma**: Chave primária simples (id_bioma) com nome único
- **Chunk**: Chave primária simples (id_chunk) com FKs para Bioma e Mapa
- **Player**: Referencia Chunk através de current_chunk_id (pode ser NULL)
- **Item**: Chave primária simples (id_item) com nome único
- **Inventario**: Relacionamento N:M entre Player e Item com quantidades

Integração com o Sistema
------------------------

As models são utilizadas em conjunto com o sistema de gerenciamento de personagens:

.. code-block:: python

    from src.models.player import Player
    from src.utils.player_manager import get_current_player, set_current_player
    from src.services.interface_service import InterfaceService
    
    # Obter personagem ativo
    current_player = get_current_player()
    
    if current_player:
        print(f"Jogando com: {current_player.nome}")
        print(f"Localização: {current_player.localizacao}")
        print(f"Vida: {current_player.get_health_bar()}")
        
        # Usar interface service para operações
        interface_service = InterfaceService.get_instance()
        
        # Mover para outro chunk
        updated_player = interface_service.move_player_to_chunk(current_player, 2)
        
        # Salvar progresso
        interface_service.save_player(updated_player)

Vantagens da Arquitetura de Models
---------------------------------

1. **Separação de Responsabilidades**: Cada model tem responsabilidades bem definidas
2. **Reutilização**: Models podem ser usadas em diferentes partes do sistema
3. **Manutenibilidade**: Mudanças em uma model não afetam outras partes
4. **Testabilidade**: Cada model pode ser testada independentemente
5. **Documentação**: Models são auto-documentadas com docstrings
6. **Type Safety**: Uso de type hints para melhor desenvolvimento
7. **Fidelidade ao Banco**: Models refletem exatamente a estrutura do banco
8. **Performance**: PlayerSession otimizada para uso em sessões de jogo

Padrões de Uso
--------------

**Player vs PlayerSession:**
- Use ``Player`` para operações de persistência e dados completos
- Use ``PlayerSession`` para otimização de performance em sessões ativas

**Localização:**
- ``Player.localizacao`` armazena string formatada ("Mapa 1 - Chunk 1")
- ``Player.current_chunk_id`` armazena referência direta ao chunk
- ``PlayerSession`` inclui cache de informações do chunk para performance

**Inventário:**
- Relação N:M entre Player e Item através de InventoryEntry
- Suporte a quantidades e controle de unicidade por constraint

Exemplos Avançados
------------------

Para ver exemplos completos de uso das models em cenários reais, consulte os testes unitários e os services do sistema.

**Navegação entre Chunks:**

.. code-block:: python

    # Obter chunk atual do jogador
    current_chunk = interface_service.get_chunk_by_id(player.current_chunk_id)
    
    # Obter chunks adjacentes
    adjacent_chunks = interface_service.get_adjacent_chunks(current_chunk.id_chunk, 'Dia')
    
    # Mover para chunk adjacente
    if adjacent_chunks:
        next_chunk_id = adjacent_chunks[0][0]
        updated_player = interface_service.move_player_to_chunk(player, next_chunk_id)

**Progressão de Personagem:**

.. code-block:: python

    # Sistema de XP e level up
    player.gain_experience(50)
    
    while player.level_up():
        print(f"Subiu para nível {player.nivel}!")
        print(f"Nova vida máxima: {player.vida_maxima}")
        print(f"Nova força: {player.forca}")
    
    # Salvar progresso
    interface_service.save_player(player)
