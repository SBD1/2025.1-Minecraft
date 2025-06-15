Models
======

O Minecraft Legends utiliza uma arquitetura baseada em models para representar as entidades do jogo. Esta abordagem garante separação de responsabilidades, reutilização de código e facilita a manutenção.

Estrutura de Models
------------------

.. code-block:: text

    app/src/models/
    ├── __init__.py          # Exporta todas as models
    ├── player.py            # Model do personagem
    ├── chunk.py             # Model do chunk
    ├── bioma.py             # Model do bioma
    ├── mapa.py              # Model do mapa
    └── example_usage.py     # Exemplos de uso

PlayerSession
------------

A model ``PlayerSession`` representa um personagem ativo na sessão do jogo.

.. autoclass:: models.player.PlayerSession
   :members:
   :undoc-members:
   :show-inheritance:

**Exemplo de uso:**

.. code-block:: python

    from src.models.player import PlayerSession
    
    # Criar um personagem
    player = PlayerSession(
        id_jogador=1,
        nome="Steve",
        vida_max=100,
        vida_atual=85,
        xp=150,
        forca=12,
        id_chunk_atual=5,
        chunk_bioma="Floresta",
        chunk_mapa_nome="Mapa_Principal",
        chunk_mapa_turno="Dia"
    )
    
    # Verificar se está vivo
    if player.is_alive():
        print("Personagem está vivo!")
    
    # Aplicar dano
    sobreviveu = player.take_damage(20)
    
    # Exibir barra de vida
    print(player.get_health_bar())

Chunk
-----

A model ``Chunk`` representa um chunk do mapa do jogo.

.. autoclass:: models.chunk.Chunk
   :members:
   :undoc-members:
   :show-inheritance:

**Exemplo de uso:**

.. code-block:: python

    from src.models.chunk import Chunk
    
    # Criar um chunk
    chunk = Chunk(
        numero_chunk=1,
        id_bioma="Floresta",
        id_mapa_nome="Mapa_Principal",
        id_mapa_turno="Dia"
    )
    
    # Verificar tipo de bioma
    if chunk.is_forest():
        print("É uma floresta!")
    
    # Verificar se pertence a um mapa
    if chunk.belongs_to_map("Mapa_Principal", "Dia"):
        print("Pertence ao mapa principal de dia!")
    
    # Obter chunks adjacentes
    adjacentes = chunk.get_adjacent_chunk_ids()

Bioma
-----

A model ``Bioma`` representa um bioma do jogo.

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

    from src.models.bioma import BIOMAS_PREDEFINIDOS, BiomaType
    
    # Usar bioma predefinido
    deserto = BIOMAS_PREDEFINIDOS[BiomaType.DESERTO]
    
    # Obter tipo enum
    tipo = deserto.get_bioma_type()
    
    # Obter informações para exibição
    info = deserto.get_display_info()

Mapa
----

A model ``Mapa`` representa um mapa do jogo com seus chunks e características.

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
    from src.models.chunk import Chunk
    
    # Criar mapa
    mapa = Mapa(
        nome="Mapa_Principal",
        turno=TurnoType.DIA
    )
    
    # Criar chunks
    chunks = [
        Chunk(1, "Deserto", "Mapa_Principal", "Dia"),
        Chunk(2, "Floresta", "Mapa_Principal", "Dia"),
    ]
    
    # Associar chunks ao mapa
    mapa.set_chunks(chunks)
    
    # Buscar chunk por ID
    chunk = mapa.get_chunk_by_id(1)
    
    # Obter distribuição de biomas
    distribuicao = mapa.get_bioma_distribution()

Relacionamentos do Banco de Dados
--------------------------------

As models refletem exatamente a estrutura do banco de dados:

.. code-block:: text

    Mapa (Nome, Turno) ← Chunk (Id_mapa_nome, Id_mapa_turno)
    Bioma (NomeBioma) ← Chunk (Id_bioma)
    Chunk (Numero_chunk) ← Jogador (Id_Chunk_Atual)

**Características dos Relacionamentos:**

- **Mapa**: Chave primária composta (Nome, Turno)
- **Bioma**: Chave primária simples (NomeBioma)
- **Chunk**: Chave primária simples (Numero_chunk) com FKs para Bioma e Mapa
- **Jogador**: Referencia Chunk através de Id_Chunk_Atual

Integração com o Sistema
------------------------

As models são utilizadas em conjunto com o sistema de gerenciamento de personagens:

.. code-block:: python

    from src.models.player import PlayerSession
    from src.utils.player_manager import load_player_by_id, set_current_player
    
    # Carregar personagem do banco
    player = load_player_by_id(1)
    
    if player:
        # Definir como personagem ativo
        set_current_player(player)
        
        # Usar métodos da model
        print(f"Localização: {player.get_location_display()}")
        print(f"Barra de vida: {player.get_health_bar()}")

Vantagens da Arquitetura de Models
---------------------------------

1. **Separação de Responsabilidades**: Cada model tem responsabilidades bem definidas
2. **Reutilização**: Models podem ser usadas em diferentes partes do sistema
3. **Manutenibilidade**: Mudanças em uma model não afetam outras partes
4. **Testabilidade**: Cada model pode ser testada independentemente
5. **Documentação**: Models são auto-documentadas com docstrings
6. **Type Safety**: Uso de type hints para melhor desenvolvimento
7. **Fidelidade ao Banco**: Models refletem exatamente a estrutura do banco

Exemplos Completos
-----------------

Para ver exemplos completos de uso das models, execute:

.. code-block:: bash

    python -m app.src.models.example_usage

Este comando demonstra todas as funcionalidades das models com exemplos práticos baseados na estrutura real do banco de dados. 