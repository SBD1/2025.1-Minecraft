Álgebra Relacional
==================

A álgebra relacional é uma linguagem formal utilizada para representar consultas em bancos de dados relacionais de forma matemática e precisa. Essa linguagem serve como base teórica para o SQL, especialmente para consultas (SELECT). Além de ajudar a entender o funcionamento interno dos sistemas de banco de dados, a álgebra relacional é útil para projetar, otimizar e validar consultas, oferecendo uma forma rigorosa e lógica de manipular dados. Seu uso é fundamental no ensino e na análise de bancos relacionais, por ser independente da linguagem de implementação.

Operadores Fundamentais
------------------------

- **Seleção (σ)**: Filtra linhas com base em uma condição.
- **Projeção (π)**: Seleciona colunas específicas.
- **União (∪)**: Junta duas relações com o mesmo esquema.
- **Diferença (−)**: Retorna tuplas que estão em uma relação mas não na outra.
- **Produto Cartesiano (×)**: Junta todas as combinações de tuplas das duas relações.
- **Junção (⨝)**: Combina tuplas de duas relações com base em uma condição.

Estrutura Atual do Banco de Dados
---------------------------------

O banco de dados do MINECRAFT - FGA - 2025/1 possui a seguinte estrutura:

.. code-block:: text

    Bioma (id_bioma, nome, descricao)
    Mapa (id_mapa, nome, turno)
    Chunk (id_chunk, id_bioma, id_mapa, x, y)
    Player (id_player, nome, vida_maxima, vida_atual, forca, localizacao, nivel, experiencia, current_chunk_id)
    Item (id_item, nome, tipo, poder, durabilidade)
    Inventario (id, player_id, item_id, quantidade)

Consultas Básicas
-----------------

**Seleciona todos os biomas**

.. code-block:: none

    π_{id_bioma, nome, descricao}(Bioma)

**Seleciona todos os mapas**

.. code-block:: none

    π_{id_mapa, nome, turno}(Mapa)

**Seleciona todos os chunks**

.. code-block:: none

    π_{id_chunk, id_bioma, id_mapa, x, y}(Chunk)

**Seleciona todos os jogadores**

.. code-block:: none

    π_{id_player, nome, vida_maxima, vida_atual, forca, localizacao, nivel, experiencia, current_chunk_id}(Player)

**Seleciona todos os itens**

.. code-block:: none

    π_{id_item, nome, tipo, poder, durabilidade}(Item)

**Seleciona todos os inventários**

.. code-block:: none

    π_{id, player_id, item_id, quantidade}(Inventario)

Consultas de Filtragem
---------------------

**Jogadores vivos (vida_atual > 0)**

.. code-block:: none

    σ_{vida_atual > 0}(Player)

**Chunks de um bioma específico (e.g., Oceano)**

.. code-block:: none

    σ_{id_bioma = 4}(Chunk)

**Mapas de dia**

.. code-block:: none

    σ_{turno = 'Dia'}(Mapa)

**Itens do tipo arma**

.. code-block:: none

    σ_{tipo = 'Arma'}(Item)

**Jogadores de nível alto (nível >= 5)**

.. code-block:: none

    σ_{nivel >= 5}(Player)

Consultas com Junções
--------------------

**Consulta 1: Jogadores e sua Localização Atual Detalhada**

.. code-block:: none

    π_{p.nome, p.vida_atual, p.nivel, p.experiencia, c.id_chunk, b.nome, m.nome, m.turno}
    (
        ((Player ⨝_{Player.current_chunk_id = Chunk.id_chunk} Chunk)
            ⨝_{Chunk.id_bioma = Bioma.id_bioma} Bioma)
            ⨝_{Chunk.id_mapa = Mapa.id_mapa} Mapa
    )

**Consulta 2: Inventário Completo de Cada Jogador**

.. code-block:: none

    π_{p.nome, i.nome, inv.quantidade, i.tipo, i.poder}
    (
        ((Player ⨝_{Player.id_player = Inventario.player_id} Inventario)
            ⨝_{Inventario.item_id = Item.id_item} Item)
    )

**Consulta 3: Detalhes Completos dos Chunks com Biomas e Mapas**

.. code-block:: none

    π_{c.id_chunk, c.x, c.y, b.nome, b.descricao, m.nome, m.turno}
    (
        ((Chunk ⨝_{Chunk.id_bioma = Bioma.id_bioma} Bioma)
            ⨝_{Chunk.id_mapa = Mapa.id_mapa} Mapa)
    )

**Consulta 4: Jogadores em Biomas Específicos**

.. code-block:: none

    π_{p.nome, p.nivel, b.nome}
    (
        ((Player ⨝_{Player.current_chunk_id = Chunk.id_chunk} Chunk)
            ⨝_{Chunk.id_bioma = Bioma.id_bioma} Bioma)
    )

Consultas de Agregação (Conceitual)
----------------------------------

**Contagem de Jogadores por Bioma**

.. code-block:: none

    γ_{b.nome, count(*)}
    (
        ((Player ⨝_{Player.current_chunk_id = Chunk.id_chunk} Chunk)
            ⨝_{Chunk.id_bioma = Bioma.id_bioma} Bioma)
    )

**Distribuição de Chunks por Mapa**

.. code-block:: none

    γ_{m.nome, m.turno, count(*)}
    (
        Chunk ⨝_{Chunk.id_mapa = Mapa.id_mapa} Mapa
    )

**Quantidade Total de Itens por Jogador**

.. code-block:: none

    γ_{p.nome, sum(inv.quantidade)}
    (
        Player ⨝_{Player.id_player = Inventario.player_id} Inventario
    )

Consultas Avançadas
------------------

**Consulta 5: Jogadores com Armas no Inventário**

.. code-block:: none

    π_{p.nome, i.nome, i.poder}
    (
        σ_{i.tipo = 'Arma'}
        (
            ((Player ⨝_{Player.id_player = Inventario.player_id} Inventario)
                ⨝_{Inventario.item_id = Item.id_item} Item)
        )
    )

**Consulta 6: Chunks Adjacentes (Baseado em Coordenadas)**

.. code-block:: none

    π_{c1.id_chunk, c2.id_chunk}
    (
        σ_{(|c1.x - c2.x| = 1 ∧ c1.y = c2.y) ∨ (|c1.y - c2.y| = 1 ∧ c1.x = c2.x)}
        (
            ρ_{c1}(Chunk) × ρ_{c2}(Chunk)
        )
    )

**Consulta 7: Jogadores em Mapas de Dia vs Noite**

.. code-block:: none

    π_{p.nome, m.turno}
    (
        ((Player ⨝_{Player.current_chunk_id = Chunk.id_chunk} Chunk)
            ⨝_{Chunk.id_mapa = Mapa.id_mapa} Mapa)
    )

**Consulta 8: Itens Mais Poderosos por Tipo**

.. code-block:: none

    π_{i.tipo, max(i.poder)}
    (
        σ_{i.poder IS NOT NULL}(Item)
    )

Consultas de Diferença e União
-----------------------------

**Jogadores que NÃO possuem itens**

.. code-block:: none

    π_{id_player, nome}(Player) − π_{player_id, nome}(Player ⨝_{Player.id_player = Inventario.player_id} Inventario)

**Chunks de Deserto OU Oceano**

.. code-block:: none

    σ_{id_bioma = 1}(Chunk) ∪ σ_{id_bioma = 4}(Chunk)

**Itens de Combate (Armas + Poções)**

.. code-block:: none

    σ_{tipo = 'Arma'}(Item) ∪ σ_{tipo = 'Poção'}(Item)

Consultas de Otimização de Jogabilidade
--------------------------------------

**Consulta 9: Jogadores Próximos (Mesmo Mapa)**

.. code-block:: none

    π_{p1.nome, p2.nome, m.nome}
    (
        σ_{p1.id_player ≠ p2.id_player}
        (
            ((((ρ_{p1}(Player) ⨝_{p1.current_chunk_id = c1.id_chunk} ρ_{c1}(Chunk))
                ⨝_{c1.id_mapa = m.id_mapa} Mapa)
                ⨝_{m.id_mapa = c2.id_mapa} ρ_{c2}(Chunk))
                ⨝_{c2.id_chunk = p2.current_chunk_id} ρ_{p2}(Player))
        )
    )

**Consulta 10: Recursos Disponíveis por Bioma**

.. code-block:: none

    π_{b.nome, i.nome, sum(inv.quantidade)}
    (
        ((((Player ⨝_{Player.current_chunk_id = Chunk.id_chunk} Chunk)
            ⨝_{Chunk.id_bioma = Bioma.id_bioma} Bioma)
            ⨝_{Player.id_player = Inventario.player_id} Inventario)
            ⨝_{Inventario.item_id = Item.id_item} Item)
    )

Equivalências de Consulta
------------------------

**Equivalência 1: Comutatividade da Junção**

.. code-block:: none

    Player ⨝_{Player.id_player = Inventario.player_id} Inventario
    ≡
    Inventario ⨝_{Inventario.player_id = Player.id_player} Player

**Equivalência 2: Seleção Antes da Junção**

.. code-block:: none

    σ_{vida_atual > 50}(Player ⨝_{Player.id_player = Inventario.player_id} Inventario)
    ≡
    σ_{vida_atual > 50}(Player) ⨝_{Player.id_player = Inventario.player_id} Inventario

**Equivalência 3: Projeção Distributiva**

.. code-block:: none

    π_{nome, quantidade}(Player ⨝_{Player.id_player = Inventario.player_id} Inventario)
    ≡
    π_{nome}(Player) ⨝_{Player.id_player = Inventario.player_id} π_{player_id, quantidade}(Inventario)

Considerações de Performance
---------------------------

1. **Índices Sugeridos**: Baseados nas junções mais comuns
   - `Player.current_chunk_id` → `Chunk.id_chunk`
   - `Chunk.id_bioma` → `Bioma.id_bioma`
   - `Chunk.id_mapa` → `Mapa.id_mapa`
   - `Inventario.player_id` → `Player.id_player`
   - `Inventario.item_id` → `Item.id_item`

2. **Ordenação de Operações**: Aplicar seleções antes das junções para reduzir o conjunto de dados

3. **Junções Mais Eficientes**: Usar índices nas chaves estrangeiras para acelerar as junções

4. **Projeção Precoce**: Selecionar apenas as colunas necessárias o mais cedo possível

Aplicações Práticas
------------------

Essas consultas em álgebra relacional são implementadas no sistema através de:

1. **Repositories**: Que encapsulam consultas específicas de cada entidade
2. **Services**: Que combinam múltiplas consultas para funcionalidades complexas
3. **Interface**: Que apresenta os dados resultantes para o usuário

A álgebra relacional serve como base teórica para:
- Otimização de consultas SQL
- Design de índices eficientes
- Validação de lógica de negócio
- Compreensão de relacionamentos entre entidades
