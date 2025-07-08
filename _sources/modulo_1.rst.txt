.. _modulo-1:

Módulo 1
=================

Assista aos vídeos explicativos do Módulo 1 para aprofundar seus conhecimentos:

* `Link para o primeiro vídeo do Módulo 1 <https://www.youtube.com/embed/RdbeW6n8fk0>`_
* `Link para o segundo vídeo do Módulo 1 <https://www.youtube.com/watch?v=jHNbsm4IbuQ>`_

.. _diagrama-entidade-relacionamento-der:

Diagrama Entidade-Relacionamento (DER)
--------------------------------------

Este documento detalha o **Diagrama Entidade-Relacionamento (DER)**, uma ferramenta essencial para a modelagem e compreensão da estrutura de bancos de dados.


O **Diagrama Entidade-Relacionamento (DER)** é uma representação gráfica utilizada para modelar a estrutura lógica de bancos de dados, permitindo visualizar como os dados se organizam e se conectam. Por meio de **entidades**, que representam elementos do mundo real como pessoas, objetos ou conceitos, e de **atributos**, que descrevem as propriedades dessas entidades, o DER torna-se essencial para o planejamento e entendimento de sistemas de informação.

Além disso, os **relacionamentos** entre as entidades são representados por linhas e símbolos que indicam como os dados se associam entre si, evidenciando **cardinalidades**, como "um para muitos" ou "muitos para muitos". Com isso, é possível compreender de forma clara as dependências e conexões entre os elementos do banco de dados, favorecendo tanto a criação quanto a manutenção de estruturas coerentes e funcionais.


.. image:: ../images/minecraft_legends_4.png
   :alt: Diagrama Entidade-Relacionamento (DER) versão 2.0
   :align: center


.. _Modelo-Relacional:

Modelo Relacional
-----------------



O modelo relacional organiza os dados em **tabelas** (relações) compostas por linhas e colunas, onde cada coluna representa um **atributo** e cada linha representa um **registro**. A estrutura é baseada em **chaves primárias (PK)** para identificar registros de forma única e **chaves estrangeiras (FK)** para conectar diferentes tabelas, garantindo a **integridade dos dados**.



Além disso, o modelo permite a manipulação eficiente das informações por meio da linguagem **SQL**, facilitando consultas, inserções e atualizações. Sua flexibilidade e clareza na estruturação fazem com que seja amplamente utilizado em sistemas de banco de dados, promovendo a organização, consistência e escalabilidade das informações armazenadas.



.. image:: ../images/modelorelaciona.png
   :alt: Modelo Relacional 2.0
   :align: center

.. _dicionario-de-dados:

Dicionário de Dados Completo
----------------------------

Este dicionário detalha a estrutura do banco de dados, incluindo todas as tabelas, seus atributos, tipos de dados, chaves e descrições baseadas no diagrama relacional.

Tabelas de Personagens e Entidades Vivas
****************************************

Tabela: Heroi
-----------------
Armazena os dados principais do jogador/herói.

+----------------+-----------------+-------------------------+-----------------------------------------+-----------------------------------+
| Nome do Campo  | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                               | Observações                       |
+================+=================+=========================+=========================================+===================================+
| ``ID_jogador`` | PK              | INTEGER                 | Identificador único para cada herói.    | Chave Primária.                   |
+----------------+-----------------+-------------------------+-----------------------------------------+-----------------------------------+
| ``nome``       |                 | VARCHAR(100)            | Nome do herói.                          |                                   |
+----------------+-----------------+-------------------------+-----------------------------------------+-----------------------------------+
| ``vida_max``   |                 | INTEGER                 | Pontos de vida máximos do herói.        |                                   |
+----------------+-----------------+-------------------------+-----------------------------------------+-----------------------------------+
| ``vida_atual`` |                 | INTEGER                 | Pontos de vida atuais do herói.         |                                   |
+----------------+-----------------+-------------------------+-----------------------------------------+-----------------------------------+
| ``XP``         |                 | INTEGER                 | Pontos de experiência do herói.         |                                   |
+----------------+-----------------+-------------------------+-----------------------------------------+-----------------------------------+
| ``forca``      |                 | INTEGER                 | Atributo de força do herói.             |                                   |
+----------------+-----------------+-------------------------+-----------------------------------------+-----------------------------------+
| ``numero_chunk``| FK              | INTEGER                 | Identificador do chunk onde o herói se  | Refere-se  ``Chunk.Numero_chunk``|
|                |                 |                         | encontra.                               |                                   |
+----------------+-----------------+-------------------------+-----------------------------------------+-----------------------------------+

Tabela: Aldeao
------------------
Armazena dados sobre os personagens aldeões (NPCs).

+---------------+-----------------+-------------------------+----------------------------------+-----------------------------------+
| Nome do Campo | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                        | Observações                       |
+===============+=================+=========================+==================================+===================================+
| ``ID_aldeao`` | PK              | INTEGER                 | Identificador único do aldeão.   | Chave Primária                    |
+---------------+-----------------+-------------------------+----------------------------------+-----------------------------------+
| ``Nome``      |                 | VARCHAR(100)            | Nome do aldeão.                  |                                   |
+---------------+-----------------+-------------------------+----------------------------------+-----------------------------------+
| ``Tipo``      |                 | VARCHAR(50)             | Tipo ou profissão do aldeão.     |                                   |
+---------------+-----------------+-------------------------+----------------------------------+-----------------------------------+
| ``ID_casa``   | FK              | INTEGER                 | Casa onde o aldeão vive.         | Refere-se  ``Casa_aldeao.ID_casa``|
+---------------+-----------------+-------------------------+----------------------------------+-----------------------------------+

Tabela: Chefao
------------------
Informações sobre os chefões (Bosses) do jogo.

+---------------+-----------------+-------------------------+------------------------------------------+-------------------+
| Nome do Campo | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                                | Observações       |
+===============+=================+=========================+==========================================+===================+
| ``Nome``      | PK              | VARCHAR(100)            | Nome e identificador único do chefão.    | Chave Primária.   |
+---------------+-----------------+-------------------------+------------------------------------------+-------------------+
| ``Descricao`` |                 | TEXT                    | Descrição e lore do chefão.              |                   |
+---------------+-----------------+-------------------------+------------------------------------------+-------------------+

Tabela: Tropa
-----------------
Define os arquétipos de tropas que podem existir no jogo.

+------------------------+-----------------+-------------------------+------------------------------------------------------+----------------------------------------------+
| Nome do Campo          | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                                            | Observações                                  |
+========================+=================+=========================+======================================================+==============================================+
| ``Nome``               | PK              | VARCHAR(100)            | Nome e identificador único do tipo de tropa.         | Chave Primária.                              |
+------------------------+-----------------+-------------------------+------------------------------------------------------+----------------------------------------------+
| ``Forca``              |                 | INTEGER                 | Atributo de força base da tropa.                     |                                              |
+------------------------+-----------------+-------------------------+------------------------------------------------------+----------------------------------------------+
| ``Especialidade``      |                 | VARCHAR(100)            | Habilidade ou característica especial da tropa.      |                                              |
+------------------------+-----------------+-------------------------+------------------------------------------------------+----------------------------------------------+
| ``Max_alvos``          |                 | INTEGER                 | Número máximo de alvos que a tropa pode atingir.     |                                              |
+------------------------+-----------------+-------------------------+------------------------------------------------------+----------------------------------------------+
| ``Vida_max``           |                 | INTEGER                 | Pontos de vida máximos padrão para este tipo de tropa.|                                             |
+------------------------+-----------------+-------------------------+------------------------------------------------------+----------------------------------------------+
| ``Descricao``          |                 | TEXT                    | Descrição da tropa.                                  |                                              |
+------------------------+-----------------+-------------------------+------------------------------------------------------+----------------------------------------------+
| ``ID_instancia_tropa`` | FK              | INTEGER                 | Chave estrangeira para a tabela de instâncias.       | Refere-se  Instancia_tropa.ID_instancia_tropa|
+------------------------+-----------------+-------------------------+------------------------------------------------------+----------------------------------------------+

Tabela: Instancia_tropa
---------------------------
Representa uma unidade ou grupo específico de uma tropa no mapa.

+------------------------+-----------------+-------------------------+---------------------------------------------+------------------------------------+
| Nome do Campo          | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                                   | Observações                        |
+========================+=================+=========================+=============================================+====================================+
| ``ID_instancia_tropa`` | PK              | INTEGER                 | Identificador único da instância da tropa.  | Chave Primária.                    |
+------------------------+-----------------+-------------------------+---------------------------------------------+====================================+
| ``Nome_tropa``         | FK              | VARCHAR(100)            | Nome do tipo de tropa.                      | Refere-se a ``Tropa.Nome``.        |
+------------------------+-----------------+-------------------------+---------------------------------------------+------------------------------------+
| ``Vida_max``           |                 | INTEGER                 | Pontos de vida máximos desta instância.     |                                    |
+------------------------+-----------------+-------------------------+---------------------------------------------+------------------------------------+
| ``Vida_atual``         |                 | INTEGER                 | Pontos de vida atuais desta instância.      |                                    |
+------------------------+-----------------+-------------------------+---------------------------------------------+------------------------------------+
| ``Numero_chunk``       | FK              | INTEGER                 | Chunk onde a instância da tropa está        | Refere-se a ``Chunk.Numero_chunk``.|
|                        |                 |                         | localizada.                                 |                                    |
+------------------------+-----------------+-------------------------+---------------------------------------------+------------------------------------+

Tabela: Piglin
------------------
Representa um tipo de inimigo ou NPC específico do jogo.

+-----------------+-----------------+-------------------------+---------------------------------------------+------------------------------------+
| Nome do Campo   | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                                   | Observações                        |
+=================+=================+=========================+=============================================+====================================+
| ``ID_piglin``   | PK              | INTEGER                 | Identificador único do Piglin.              | Chave Primária.                    |
+-----------------+-----------------+-------------------------+---------------------------------------------+------------------------------------+
| ``Forca``       |                 | INTEGER                 | Atributo de força do Piglin.                |                                    |
+-----------------+-----------------+-------------------------+---------------------------------------------+------------------------------------+
| ``Vida_max``    |                 | INTEGER                 | Pontos de vida máximos do Piglin.           |                                    |
+-----------------+-----------------+-------------------------+---------------------------------------------+------------------------------------+
| ``Vida_atual``  |                 | INTEGER                 | Pontos de vida atuais do Piglin.            |                                    |
+-----------------+-----------------+-------------------------+---------------------------------------------+------------------------------------+
|``Nome_fortaleza``| FK              | VARCHAR(100)            | Fortaleza à qual o Piglin está associado.   | Refere-se a ``Fortaleza.Nome``.   |
+-----------------+-----------------+-------------------------+---------------------------------------------+------------------------------------+
| ``Nome_chefao`` | FK              | VARCHAR(100)            | Chefão que comanda o Piglin.                | Refere-se a ``Chefao.Nome``.       |
+-----------------+-----------------+-------------------------+---------------------------------------------+------------------------------------+
| ``numero_chunk``| FK              | INTEGER                 | Chunk onde o Piglin se encontra.            | Refere-se a ``Chunk.Numero_chunk`` |
+-----------------+-----------------+-------------------------+---------------------------------------------+------------------------------------+

Tabela: Fantasma_construtor e Fantasma_minerador
------------------------------------------------------
Representam papéis ou habilidades especiais que o jogador pode assumir.

+-------------------+-----------------+-------------------------+-------------------------------------------+-----------------------------------------------------+
| Nome do Campo     | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                                 | Observações                                         |
+===================+=================+=========================+===========================================+=====================================================+
| ``ID_construtor`` | PK              | INTEGER                 | Identificador único da entidade construtora.| Chave Primária da tabela ``Fantasma_construtor``. |
+-------------------+-----------------+-------------------------+-------------------------------------------+-----------------------------------------------------+
| ``ID_minerador``  | PK              | INTEGER                 | Identificador único da entidade mineradora. | Chave Primária da tabela ``Fantasma_minerador``.  |
+-------------------+-----------------+-------------------------+-------------------------------------------+-----------------------------------------------------+
| ``ID_jogador``    | FK              | INTEGER                 | Jogador que assume este papel.            | Refere-se a ``Heroi.ID_jogador``.                   |
+-------------------+-----------------+-------------------------+-------------------------------------------+-----------------------------------------------------+

Tabela: Anfitriao
-------------------
Provavelmente representa uma entidade que hospeda ou inicia um evento ou missão.

+---------------+-----------------+-------------------------+------------------------------------------+-------------------+
| Nome do Campo | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                                | Observações       |
+===============+=================+=========================+==========================================+===================+
| ``Nome``      | PK              | VARCHAR(100)            | Nome e identificador único do anfitrião. | Chave Primária.   |
+---------------+-----------------+-------------------------+------------------------------------------+-------------------+
| ``Descricao`` |                 | TEXT                    | Descrição do papel do anfitrião.         |                   |
+---------------+-----------------+-------------------------+------------------------------------------+-------------------+

Tabelas de Mundo e Ambiente
***************************

Tabela: Mapa
----------------
Define os mapas do jogo.

+----------------+-----------------+-------------------------+------------------------------------------+--------------------------+
| Nome do Campo  | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                                | Observações              |
+================+=================+=========================+==========================================+==========================+
| ``Nome``       | PK              | VARCHAR(100)            | Nome e identificador do mapa.            | Chave Primária Composta. |
+----------------+-----------------+-------------------------+------------------------------------------+--------------------------+
| ``Tumo``       | PK              | VARCHAR(100)            | Turno ou estado específico do mapa.      | Chave Primária Composta. |
+----------------+-----------------+-------------------------+------------------------------------------+--------------------------+
|``numero_chunk``| FK              | INTEGER                 | Chave estrangeira para a tabela de chunks.|   ``Chunk.Numero_chunk``|
+----------------+-----------------+-------------------------+------------------------------------------+--------------------------+

Tabela: Chunk
-----------------
Representa uma porção ou área do mapa do jogo.

+----------------+-----------------+-------------------------+-------------------------------------------+-----------------------------------+
| Nome do Campo  | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                                 | Observações                       |
+================+=================+=========================+===========================================+===================================+
|``Numero_chunk``| PK              | INTEGER                 | Identificador único para cada chunk.      | Primária.                         |
+----------------+-----------------+-------------------------+-------------------------------------------+-----------------------------------+
|``id_mapa_nome``| FK              | VARCHAR(100)            | Nome do mapa ao qual o chunk pertence.    | Refere-se a ``Mapa.Nome``.        |
+----------------+-----------------+-------------------------+-------------------------------------------+-----------------------------------+
|``id_mapa_tumo``| FK              | VARCHAR(100)            | Turno do mapa ao qual o chunk pertence.   | Refere-se a ``Mapa.Tumo``.        |
+----------------+-----------------+-------------------------+-------------------------------------------+-----------------------------------+
| ``id_bioma``   | FK              | VARCHAR(100)            | Bioma predominante no chunk.              | Refere-se a ``Bioma.Nome_bioma``. |
+----------------+-----------------+-------------------------+-------------------------------------------+-----------------------------------+
| ``Acessivel``  |                 | BOOLEAN                 | Indica se o chunk é acessível ao jogador. |                                   |
+----------------+-----------------+-------------------------+-------------------------------------------+-----------------------------------+

Tabela: Bioma
-----------------
Armazena os diferentes tipos de biomas do mundo.

+--------------+-----------------+-------------------------+-----------------------------------------+------------------+
| Nome do Campo| Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                               | Observações      |
+==============+=================+=========================+=========================================+==================+
|``Nome_bioma``| PK              | VARCHAR(100)            | Nome e identificador único do bioma.    | Chave Primária.  |
+--------------+-----------------+-------------------------+-----------------------------------------+------------------+
| ``Descricao``|                 | TEXT                    | Descrição do bioma.                     |                  |
+--------------+-----------------+-------------------------+-----------------------------------------+------------------+

Tabelas de Estruturas e Construções
***********************************

Tabela: Vila_aldeao
-----------------------
Armazena informações sobre as vilas de aldeões.

+------------------+-----------------+-------------------------+------------------------------------------+-----------------------------------+
| Nome do Campo    | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                                | Observações                       |
+==================+=================+=========================+==========================================+===================================+
| ``Nome``         | PK              | VARCHAR(100)            | Nome e identificador único da vila.      | Chave Primária.                   |
+------------------+-----------------+-------------------------+------------------------------------------+-----------------------------------+
|``Descricao_vila``|                 | TEXT                    | Descrição da vila.                       |                                   |
+------------------+-----------------+-------------------------+------------------------------------------+-----------------------------------+
| ``numero_chunk`` | FK              | INTEGER                 | Chunk onde a vila está localizada.       | Refere-se a ``Chunk.Numero_chunk``|
+------------------+-----------------+-------------------------+------------------------------------------+-----------------------------------+

Tabela: Casa_aldeao
-----------------------
Representa as casas dentro de uma vila.

+------------------+-----------------+-------------------------+-----------------------------------+-----------------------------------+
| Nome do Campo    | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                         | Observações                       |
+==================+=================+=========================+===================================+===================================+
| ``ID_casa``      | PK              | INTEGER                 | Identificador único da casa.      | Chave Primária.                   |
+------------------+-----------------+-------------------------+-----------------------------------+-----------------------------------+
|``Descricao_casa``|                 | TEXT                    | Descrição da casa.                |                                   |
+------------------+-----------------+-------------------------+-----------------------------------+-----------------------------------+
| ``Nome_vila``    | FK              | VARCHAR(100)            | Vila à qual a casa pertence.      | Refere-se a ``Vila_aldeao.Nome``. |
+------------------+-----------------+-------------------------+-----------------------------------+-----------------------------------+

Tabela: Fortaleza
-------------------
Armazena informações sobre fortalezas.

+---------------+-----------------+-------------------------+---------------------------------------------+-----------------------------+
| Nome do Campo | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                                   | Observações                 |
+===============+=================+=========================+=============================================+=============================+
| ``Nome``      | PK              | VARCHAR(100)            | Nome e identificador único da fortaleza.    | Chave Primária Composta.    |
+---------------+-----------------+-------------------------+---------------------------------------------+-----------------------------+
| ``Cla``       | PK              | VARCHAR(100)            | Clã ou facção que controla a fortaleza.     | Chave Primária Composta.    |
+---------------+-----------------+-------------------------+---------------------------------------------+-----------------------------+
| ``Nome_chefao`` | FK            | VARCHAR(100)            | Chefão que comanda a fortaleza.             | Refere-se a ``Chefao.Nome``.|
+---------------+-----------------+-------------------------+---------------------------------------------+-----------------------------+

Tabela: Estrutura
-------------------
Tabela genérica para diferentes tipos de estruturas construídas no jogo.

+-------------------+-----------------+-------------------------+--------------------------------------------------+---------------------------------+
| Nome do Campo     | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                                        | Observações                     |
+===================+=================+=========================+==================================================+=================================+
| ``Nome``          | PK              | VARCHAR(100)            | Nome e identificador da estrutura.               | Chave Primária.                 |
+-------------------+-----------------+-------------------------+--------------------------------------------------+---------------------------------+
| ``Cla``           |                 | VARCHAR(100)            | Clã ou facção proprietária da estrutura.         |                                 |
+-------------------+-----------------+-------------------------+--------------------------------------------------+---------------------------------+
|``Nome_fortaleza`` | FK              | VARCHAR(100)            | Fortaleza à qual a estrutura pode estar associada. | Refere-se a ``Fortaleza.Nome``|
+-------------------+-----------------+-------------------------+--------------------------------------------------+---------------------------------+

Tabelas de Construções Específicas
----------------------------------
Estas tabelas herdam ou se relacionam com a tabela Estrutura.

* **Muros**
    * ``ID_muro`` (PK): Identificador do muro.
    * ``Material``: Material de que o muro é feito.
    * ``Fraqueza``: Fraqueza do muro.

* **Torre_Arqueira**
    * ``ID_torre_arqueiro`` (PK): Identificador da torre.
    * ``Dano``: Dano causado pela torre.
    * ``Max_alvos``: Número máximo de alvos.
    * ``Alcance``: Alcance dos ataques.

* **Ponte**
    * ``ID_construcao`` (PK): Identificador da ponte.
    * ``Descricao``: Descrição da ponte.
    * ``Numero_chunk`` (FK): Chunk onde se localiza.

* **Totem_tropa**
    * ``ID_construcao`` (PK): Identificador do totem.
    * ``Descricao``: Descrição do totem.

* **Fornalha**
    * ``ID_fornalha`` (PK): Identificador da fornalha.
    * ``Piglins_por_rodada``: Capacidade de processamento.

* **Portal**
    * ``ID_portal`` (PK): Identificador do portal.
    * ``Status``: Status atual do portal (e.g., Ativo, Inativo).

Tabelas de Itens e Interação
*****************************

Tabela: Inventario
--------------------
Representa o inventário, que pode ser de um herói ou de um baú.

+-----------------+-----------------+-------------------------+---------------------------------------------------+-----------------------------------+
| Nome do Campo   | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                                         | Observações                       |
+=================+=================+=========================+===================================================+===================================+
|``ID_inventario``| PK              | INTEGER                 | Identificador único do inventário.                | Chave Primária.                   |
+-----------------+-----------------+-------------------------+---------------------------------------------------+-----------------------------------+
| ``ID_heroi``    |                 | INTEGER                 | Herói proprietário do inventário (se aplicável).  | Refere-se a ``Heroi.ID_jogador``. |
+-----------------+-----------------+-------------------------+---------------------------------------------------+-----------------------------------+
| ``ID_bau``      | FK              | INTEGER                 | Baú proprietário do inventário (se aplicável).    | Refere-se a ``Bau.ID_bau``.       |
+-----------------+-----------------+-------------------------+---------------------------------------------------+-----------------------------------+

Tabela: Bau
---------------
Representa um baú que pode conter itens.

+---------------+-----------------+-------------------------+----------------------------------+-------------------+
| Nome do Campo | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                        | Observações       |
+===============+=================+=========================+==================================+===================+
| ``ID_bau``    | PK              | INTEGER                 | Identificador único do baú.      | Chave Primária.   |
+---------------+-----------------+-------------------------+----------------------------------+-------------------+

Tabela: Item
----------------
Define os arquétipos de itens que podem existir no jogo.

+-----------------------+-----------------+-------------------------+--------------------------------------------------+------------------------------------------------+
| Nome do Campo         | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                                        | Observações                                    |
+=======================+=================+=========================+==================================================+================================================+
| ``ID_item``           | PK              | INTEGER                 | Identificador único do tipo de item.             | Chave Primária.                                |
+-----------------------+-----------------+-------------------------+--------------------------------------------------+------------------------------------------------+
| ``Tipo``              |                 | VARCHAR(50)             | Categoria do item (e.g., Arma, Poção)            |                                                |
+-----------------------+-----------------+-------------------------+--------------------------------------------------+------------------------------------------------+
| ``Nome``              |                 | VARCHAR(100)            | Nome do item.                                    |                                                |
+-----------------------+-----------------+-------------------------+--------------------------------------------------+------------------------------------------------+
|``ID_instancia_item``  | FK              | INTEGER                 | Relaciona-se com a instância específica do item. | Refere-se a``instancia_item.ID_instancia_item``|
+-----------------------+-----------------+-------------------------+--------------------------------------------------+------------------------------------------------+

Tabela: instancia_item
--------------------------

+-----------------------+-----------------+-------------------------+--------------------------------------------------+------------------------------------------+
| Nome do Campo         | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                                        | Observações                              |
+=======================+=================+=========================+==================================================+==========================================+
| ``ID_instancia_item`` | PK              | INTEGER                 | Identificador único da instância do item.        | Chave Primária.                          |
+-----------------------+-----------------+-------------------------+--------------------------------------------------+------------------------------------------+
| ``Uso``               |                 | INTEGER                 | Quantidade de usos restantes ou durabilidade.    |                                          |
+-----------------------+-----------------+-------------------------+--------------------------------------------------+------------------------------------------+
| ``Descricao``         |                 | TEXT                    | Descrição específica desta instância.            |                                          |
+-----------------------+-----------------+-------------------------+--------------------------------------------------+------------------------------------------+
| ``ID_inventario``     | FK              | INTEGER                 | Inventário onde o item está guardado.            | Refere-se a ``Inventario.ID_inventario`` |
+-----------------------+-----------------+-------------------------+--------------------------------------------------+------------------------------------------+
| ``ID_bau``            | FK              | INTEGER                 | Baú onde o item pode estar guardado.             | Refere-se a ``Bau.ID_bau``.              |
+-----------------------+-----------------+-------------------------+--------------------------------------------------+------------------------------------------+

Tabelas de Jogo e Missões
**************************

Tabela: Missao
------------------

+-----------------------+-----------------+-------------------------+--------------------------------------------------+-----------------------------------+
| Nome do Campo         | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                                        | Observações                       |
+=======================+=================+=========================+==================================================+===================================+
| ``ID_missao``         | PK              | INTEGER                 | Identificador único da missão.                   | Chave Primária.                   |
+-----------------------+-----------------+-------------------------+--------------------------------------------------+-----------------------------------+
| ``Prioridade``        |                 | VARCHAR(50)             | Nível de prioridade da missão.                   |                                   |
+-----------------------+-----------------+-------------------------+--------------------------------------------------+-----------------------------------+
| ``Descricao``         |                 | TEXT                    | Descrição detalhada dos objetivos da missão.     |                                   |
+-----------------------+-----------------+-------------------------+--------------------------------------------------+-----------------------------------+
|``Criterios_conclusao``|                 | TEXT                    | Condições para que a missão seja concluída.      |                                   |
+-----------------------+-----------------+-------------------------+--------------------------------------------------+-----------------------------------+
| ``XP``                |                 | INTEGER                 | Experiência ganha ao completar a missão.         |                                   |
+-----------------------+-----------------+-------------------------+--------------------------------------------------+-----------------------------------+
| ``ID_jogador``        | FK              | INTEGER                 | Identificador do jogador associado à missão.     | Refere-se a ``Heroi.ID_jogador``. |
+-----------------------+-----------------+-------------------------+--------------------------------------------------+-----------------------------------+

Tabela: Dialogo
-------------------
Armazena os textos de diálogo dos personagens.

+-----------------+-----------------+-------------------------+--------------------------------------------------+------------------------------------------+
| Nome do Campo   | Chave/Restrição | Tipo de Dado (Sugerido) | Descrição                                        | Observações                              |
+=================+=================+=========================+==================================================+==========================================+
| ``ID_dialogo``  | PK              | INTEGER                 | Identificador único para cada fala ou diálogo.   | Chave Primária.                          |
+-----------------+-----------------+-------------------------+--------------------------------------------------+------------------------------------------+
|``ID_personagem``| FK              | INTEGER                 | Identificador do personagem que fala.            | refere-se a ``Aldeao``, ``Chefao``, etc. |
+-----------------+-----------------+-------------------------+--------------------------------------------------+------------------------------------------+
| ``Texto``       |                 | TEXT                    | O conteúdo do diálogo.                           |                                          |
+-----------------+-----------------+-------------------------+--------------------------------------------------+------------------------------------------+

Tabelas de Especialização (Herança)
*************************************

+------------------+------------------------------------+-------------------------+-------------------------------------------------+
| Nome da Tabela   | Atributo                           | Tipo (Sugerido)         | Descrição                                       |
+==================+====================================+=========================+=================================================+
| ``Bob_mago``     | ``Habilidade_mago / Nivel``        | INTEGER                 | Nível da habilidade de mago do personagem.      |
+------------------+------------------------------------+-------------------------+-------------------------------------------------+
| ``Bob_construtor`` | ``Habilidade_construtor / Nivel``| INTEGER                 | Nível da habilidade de construtor do personagem.|
+------------------+------------------------------------+-------------------------+-------------------------------------------------+