Início Rápido
=============

Este guia irá ajudá-lo a começar rapidamente com o MINECRAFT - FGA - 2025/1.

Primeira Execução
-----------------

#. **Inicie os containers** (se ainda não estiverem rodando)::

   docker-compose up -d

#. **Acesse o container**::

   docker exec -it python_mine bash

#. **Execute o jogo**::

   python main.py

Criando seu Primeiro Personagem
------------------------------

#. Na tela inicial, você verá o menu principal
#. Selecione a opção **6. ➕ Criar novo personagem**
#. Digite um nome para seu personagem
#. Confirme a criação
#. Escolha se deseja selecionar o personagem agora

.. note::
   Novos personagens começam no **Chunk 1** do **Mapa 1** durante o **Dia**, em um ambiente que pode ser qualquer bioma (Deserto, Selva, Floresta, ou Oceano).

Navegando pelo Menu
------------------

O menu principal oferece as seguintes opções:

* **🎮 Iniciar jogo** - Inicia uma sessão de jogo com sistema de movimento
* **📊 Ver status detalhado** - Mostra informações completas do personagem
* **💾 Salvar progresso** - Salva as alterações no banco de dados
* **👥 Trocar personagem** - Permite trocar para outro personagem
* **📋 Lista de personagens** - Visualiza todos os personagens
* **➕ Criar novo personagem** - Cria um novo personagem
* **🚪 Sair** - Sai do jogo

Sistema de Movimento
--------------------

Quando você inicia o jogo, pode mover seu personagem:

#. Selecione **🎮 Iniciar jogo**
#. Você verá as opções de movimento com direções:
   * **⬆️ Cima** - Move para chunk acima
   * **⬇️ Baixo** - Move para chunk abaixo
   * **⬅️ Esquerda** - Move para chunk à esquerda
   * **➡️ Direita** - Move para chunk à direita
#. Escolha uma direção (1-4)
#. O sistema informará se houve mudança de bioma

**Exemplo de movimento:**

.. code-block:: text

   🚶 OPÇÕES DE MOVIMENTO:
   ----------------------------------------
   1. ⬆️ Cima - 🌊 Oceano (Chunk 2)
   2. ⬇️ Baixo - 🌴 Selva (Chunk 4)
   3. ⬅️ Esquerda - 🏜️ Deserto (Chunk 1)
   4. ➡️ Direita - 🌲 Floresta (Chunk 3)

.. note::
   **Novidade**: Agora o sistema exibe o **nome do bioma** em vez do ID numérico! Você verá "🌊 Oceano" em vez de "BIOMA: 4".

Biomas Disponíveis
------------------

O mundo do jogo possui 4 biomas diferentes:

* **🏜️ Deserto** (ID: 1) - Um bioma árido com pouca vegetação
* **🌴 Selva** (ID: 2) - Um bioma tropical denso e úmido
* **🌲 Floresta** (ID: 3) - Um bioma com muitas árvores e vida selvagem
* **🌊 Oceano** (ID: 4) - Um vasto bioma de água salgada

Cada bioma oferece uma experiência visual e narrativa diferente durante a exploração.

Gerenciando Personagens
-----------------------

Listando Personagens
^^^^^^^^^^^^^^^^^^^^

#. Selecione **5. 📋 Lista de personagens**
#. Você verá uma visualização em grid de todos os personagens
#. Cada personagem mostra:
   * Nome
   * Vida atual/máxima com barra visual colorida
   * XP
   * Força
   * Localização atual (formato: "Mapa X - Chunk Y")

Selecionando um Personagem
^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Na lista de personagens, escolha **1. 🎮 Selecionar personagem**
#. Digite o número do personagem desejado
#. O personagem será carregado e se tornará o ativo

Deletando um Personagem
^^^^^^^^^^^^^^^^^^^^^^^

#. Na lista de personagens, escolha **2. 🗑️ Deletar personagem**
#. Digite o número do personagem a ser deletado
#. Confirme a operação
#. **Nota**: Não é possível deletar o personagem ativo

Verificando o Status
-------------------

Para ver informações detalhadas do seu personagem:

#. Selecione **2. 📊 Ver status detalhado**
#. Você verá:
   * Nome e ID do personagem
   * Vida atual e máxima com barra visual
   * XP e força
   * Localização detalhada (bioma, mapa e turno)
   * Status de vida

**Exemplo de status:**

.. code-block:: text

   📊 STATUS DO PERSONAGEM:
   ========================================
   👤 Nome: Steve
   🆔 ID: 1
   ❤️  Vida: 85/100 [████████████████████░░░]
   ⚡ Força: 12
   🎯 XP: 150
   📍 Localização: 🌊 Oceano (Mapa 1 - Dia)
   ✅ Status: Vivo

Salvando Progresso
------------------

O jogo salva automaticamente quando você:
* Sai do jogo
* Troca de personagem
* Move seu personagem

Para salvar manualmente:
#. Selecione **3. 💾 Salvar progresso**
#. Confirme que os dados foram salvos

.. tip::
   **Novidade**: O sistema agora salva tanto a localização formatada ("Mapa X - Chunk Y") quanto o ID do chunk atual para melhor performance.

Resolução de Problemas
----------------------

**Erro ao Mover Personagem**

Se você receber um erro relacionado à localização do personagem:

#. Verifique se o personagem tem uma localização válida no status
#. Tente salvar o progresso manualmente
#. Se o problema persistir, crie um novo personagem

**Bioma Não Aparece**

Se o bioma aparecer como número em vez do nome:

#. Isso pode indicar um problema temporário de conexão
#. Tente mover para outro chunk e voltar
#. Reinicie o jogo se necessário

**Problemas de Performance**

Para melhor performance:

#. Salve o progresso regularmente
#. Evite criar muitos personagens desnecessários
#. Use a funcionalidade de deletar personagens antigos

Estrutura do Mundo
------------------

O mundo do jogo é organizado da seguinte forma:

* **Mapas**: Cada mapa tem um nome e um turno (Dia/Noite)
* **Chunks**: Cada chunk pertence a um mapa e tem um bioma
* **Coordenadas**: Chunks são organizados em grid com coordenadas X,Y
* **Biomas**: Cada chunk tem um bioma que define sua aparência e características

**Navegação:**

* Chunks são numerados sequencialmente (1, 2, 3, ...)
* Movimento entre chunks adjacentes é possível
* Localização é exibida como "Mapa X - Chunk Y"

Saindo do Jogo
--------------

Para sair do jogo:

#. Selecione **7. 🚪 Sair**
#. O jogo salvará automaticamente seu progresso
#. Você verá uma mensagem de confirmação

Para sair do container Docker:

#. Digite ``exit`` ou pressione ``Ctrl+D``

Para parar os containers:

#. No terminal host::

   docker-compose down

Próximos Passos
---------------

Agora que você conhece o básico:

* :doc:`user_guide` - Aprenda sobre funcionalidades avançadas
* :doc:`models` - Entenda a estrutura dos dados do jogo
* :doc:`api_reference` - Explore a documentação da API
* :doc:`database` - Entenda a estrutura do banco de dados
* :doc:`relational_algebra` - Aprenda sobre as consultas do sistema

Funcionalidades Avançadas
-------------------------

Para usuários que desejam explorar mais funcionalidades:

**Desenvolvimento:**

* Examine o código em ``app/src/models/`` para entender a estrutura dos dados
* Verifique os repositories em ``app/src/repositories/`` para consultas customizadas
* Analise os services em ``app/src/services/`` para lógica de negócio

**Banco de Dados:**

* Conecte-se diretamente ao PostgreSQL para consultas avançadas
* Explore os arquivos SQL em ``db/`` para entender a estrutura
* Use as consultas de álgebra relacional para análise de dados

**Testes:**

* Execute ``python -m pytest`` para rodar os testes unitários
* Verifique os testes em ``tests/`` para exemplos de uso
* Adicione novos testes ao modificar funcionalidades
