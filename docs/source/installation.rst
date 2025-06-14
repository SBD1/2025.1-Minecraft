Instalação
==========

Este guia irá ajudá-lo a configurar o ambiente Minecraft Legends em sua máquina local.

Pré-requisitos
--------------

Antes de começar, certifique-se de ter os seguintes softwares instalados:

* **Docker** (versão 20.10 ou superior)
* **Docker Compose** (versão 2.0 ou superior)
* **Git** (para clonar o repositório)

Instalação do Docker
--------------------

.. tabs::

   .. tab:: Windows

      #. Baixe o `Docker Desktop para Windows <https://www.docker.com/products/docker-desktop>`_
      #. Execute o instalador e siga as instruções
      #. Reinicie o computador se necessário
      #. Verifique a instalação::

         docker --version
         docker-compose --version

   .. tab:: macOS

      #. Baixe o `Docker Desktop para Mac <https://www.docker.com/products/docker-desktop>`_
      #. Arraste o Docker para a pasta Applications
      #. Abra o Docker Desktop
      #. Verifique a instalação::

         docker --version
         docker-compose --version

   .. tab:: Linux (Ubuntu/Debian)

      #. Atualize os pacotes::

         sudo apt update

      #. Instale dependências::

         sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release

      #. Adicione a chave GPG oficial do Docker::

         curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

      #. Configure o repositório::

         echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

      #. Instale o Docker::

         sudo apt update
         sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin

      #. Adicione seu usuário ao grupo docker::

         sudo usermod -aG docker $USER

      #. Reinicie a sessão e verifique::

         docker --version
         docker-compose --version

Clonando o Repositório
----------------------

#. Clone o repositório::

   git clone https://github.com/SBD1/2025.1-Minecraft.git

#. Acesse o diretório::

   cd 2025.1-Minecraft

Configuração do Ambiente
------------------------

#. Construa e inicie os containers::

   docker-compose up -d --build

#. Aguarde alguns segundos para que o banco de dados seja inicializado

#. Verifique se os containers estão rodando::

   docker-compose ps

Você deve ver algo como:

.. code-block:: bash

   NAME                    COMMAND                  SERVICE             STATUS              PORTS
   2025_1_Minecraft        "docker-entrypoint.s…"   db                  Up                  0.0.0.0:5433->5432/tcp
   python_mine            "python"                  app                 Up                  0.0.0.0:8000->8000/tcp

Verificação da Instalação
-------------------------

Para verificar se tudo está funcionando:

#. Acesse o container da aplicação::

   docker exec -it python_mine bash

#. Execute o jogo::

   python main.py

#. Você deve ver a tela inicial do Minecraft Legends

Se tudo estiver funcionando, você verá uma mensagem como:

.. code-block:: text

   ╔══════════════════════════════════════════════════╗
   ║         🟩 MINECRAFT - FGA - 2025/1              ║
   ║              Python Edition                      ║
   ╚══════════════════════════════════════════════════╝

Solução de Problemas
--------------------

Problema: Erro de conexão com banco de dados
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Sintomas**: Mensagem "Falha na conexão com o banco de dados"

**Solução**:

#. Verifique se os containers estão rodando::

   docker-compose ps

#. Se não estiverem, reinicie::

   docker-compose down
   docker-compose up -d

#. Aguarde alguns segundos e tente novamente

Problema: Porta 5433 já em uso
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Sintomas**: Erro ao subir containers

**Solução**:

#. Edite o arquivo ``docker-compose.yml`` e mude a porta::

   ports:
     - "5434:5432"  # Mude de 5433 para 5434

#. Reinicie os containers::

   docker-compose down
   docker-compose up -d

Problema: Permissões no Linux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Sintomas**: Erro de permissão ao executar docker

**Solução**:

#. Adicione seu usuário ao grupo docker::

   sudo usermod -aG docker $USER

#. Faça logout e login novamente

#. Ou execute com sudo (não recomendado)::

   sudo docker-compose up -d

Próximos Passos
---------------

Após a instalação bem-sucedida, você pode:

* :doc:`quickstart` - Começar a usar o jogo
* :doc:`user_guide` - Aprender sobre as funcionalidades
* :doc:`development` - Contribuir com o desenvolvimento 