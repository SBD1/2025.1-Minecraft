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

.. image:: _static/create-character.png
   :alt: Criando personagem
   :align: center

Navegando pelo Menu
------------------

O menu principal oferece as seguintes opções:

* **🎮 Iniciar jogo** - Inicia uma sessão de jogo (em desenvolvimento)
* **📊 Ver status detalhado** - Mostra informações completas do personagem
* **💾 Salvar progresso** - Salva as alterações no banco de dados
* **👥 Trocar personagem** - Permite trocar para outro personagem
* **📋 Lista de personagens** - Visualiza todos os personagens
* **➕ Criar novo personagem** - Cria um novo personagem
* **🚪 Sair** - Sai do jogo

Gerenciando Personagens
-----------------------

Listando Personagens
^^^^^^^^^^^^^^^^^^^^

#. Selecione **5. 📋 Lista de personagens**
#. Você verá uma visualização em grid de todos os personagens
#. Cada personagem mostra:
   * Nome
   * Vida atual/máxima
   * XP
   * Força
   * Localização atual

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
   * Vida atual e máxima
   * XP e força
   * Localização (bioma, mapa e turno)
   * Status de vida

Salvando Progresso
------------------

O jogo salva automaticamente quando você:
* Sai do jogo
* Troca de personagem

Para salvar manualmente:
#. Selecione **3. 💾 Salvar progresso**
#. Confirme que os dados foram salvos

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
* :doc:`api_reference` - Explore a documentação da API
* :doc:`database` - Entenda a estrutura do banco de dados 