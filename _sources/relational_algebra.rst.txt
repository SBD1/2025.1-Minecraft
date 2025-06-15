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

Consultas Relacionais no Banco Minecraft
----------------------------------------

**Seleciona todos os mapas**

.. code-block:: none

    Mapa

**Seleciona todos os biomas**

.. code-block:: none

   Bioma

**Seleciona todos os chunks**

.. code-block:: none

   Chunks

**Seleciona todos os jogadores**

.. code-block:: none

   Jogadores

**Seleciona todos os inventários**

.. code-block:: none

   nventários

Consultas Compostas
-------------------

**Consulta 1: Jogadores e sua Localização Atual**

.. code-block:: none

   π_{j.Nome, j.Vida_atual, j.xp, c.Numero_chunk, c.Id_bioma, c.Id_mapa_nome, c.Id_mapa_turno}
   (
       Jogador ⨝_{Jogador.Id_Chunk_Atual = Chunk.Numero_chunk} Chunk
   )

**Consulta 2: Inventário de Cada Jogador**

.. code-block:: none

   π_{j.Nome, i.Instancia_Item, i.ArmaduraEquipada, i.ArmaEquipada}
   (
       Inventario ⨝_{Inventario.id_jogador = Jogador.Id_Jogador} Jogador
   )

**Consulta 3: Detalhes Completos dos Chunks**

.. code-block:: none

   π_{c.Numero_chunk, b.NomeBioma, m.Nome, m.Turno}
   (
       (Chunk ⨝_{Chunk.Id_bioma = Bioma.NomeBioma} Bioma)
            ⨝_{Chunk.Id_mapa_nome = Mapa.Nome ∧ Chunk.Id_mapa_turno = Mapa.Turno} Mapa
   )
