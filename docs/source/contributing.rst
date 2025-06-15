Contribuindo
============

Tipos de Contribuição
^^^^^^^^^^^^^^^^^^^^^

Aceitamos diferentes tipos de contribuição:

* **🐛 Bug Reports** - Reportar problemas encontrados
* **💡 Feature Requests** - Sugerir novas funcionalidades
* **📝 Documentation** - Melhorar documentação
* **🔧 Code Changes** - Implementar melhorias
* **🧪 Testing** - Testar e validar funcionalidades
* **🎨 UI/UX** - Melhorar interface do usuário

Processo de Contribuição
^^^^^^^^^^^^^^^^^^^^^^^^

#. **Fork** o repositório
#. **Clone** seu fork localmente
#. **Crie** uma branch para sua feature
#. **Desenvolva** suas mudanças
#. **Teste** suas alterações
#. **Commit** suas mudanças
#. **Push** para sua branch
#. **Abra** um Pull Request

Reportando Bugs
---------------

Template de Bug Report
^^^^^^^^^^^^^^^^^^^^^

Use o template de issue para bugs:

.. code-block:: markdown

   ## 🐛 Bug Report
   
   **Descrição do Bug**
   Uma descrição clara e concisa do que aconteceu.
   
   **Para Reproduzir**
   Passos para reproduzir o comportamento:
   1. Vá para '...'
   2. Clique em '...'
   3. Role até '...'
   4. Veja o erro
   
   **Comportamento Esperado**
   Uma descrição clara do que deveria acontecer.
   
   **Screenshots**
   Se aplicável, adicione screenshots para ajudar a explicar o problema.
   
   **Ambiente:**
   - OS: [ex: Windows, macOS, Linux]
   - Python: [ex: 3.10.0]
   - Docker: [ex: 20.10.0]
   
   **Contexto Adicional**
   Adicione qualquer outro contexto sobre o problema aqui.

Informações Necessárias
^^^^^^^^^^^^^^^^^^^^^^^

Para bugs, inclua sempre:

* **Descrição detalhada** do problema
* **Passos para reproduzir**
* **Comportamento esperado vs atual**
* **Screenshots** (se aplicável)
* **Informações do ambiente**
* **Logs de erro** (se disponível)


Desenvolvimento
--------------

Configuração do Ambiente
^^^^^^^^^^^^^^^^^^^^^^^^

#. **Fork e clone**::

   git clone https://github.com/SEU_USUARIO/2025.1-Minecraft.git
   cd 2025.1-Minecraft

#. **Configure o ambiente**::

   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   pip install -r app/requirements.txt

#. **Inicie os containers**::

   docker-compose up -d

#. **Teste a instalação**::

   python app/main.py

Criando uma Branch
^^^^^^^^^^^^^^^^^

Use branches descritivas:

.. code-block:: bash

   # Para novas features
   git checkout -b feat/nova-funcionalidade
   
   # Para correções
   git checkout -b fix/correcao-bug
   
   # Para documentação
   git checkout -b docs/melhorar-docs

Padrões de Código
-----------------

Estilo de Código
^^^^^^^^^^^^^^^^

Siga o PEP 8 para Python:

.. code-block:: python

   # ✅ Bom
   def criar_personagem(nome: str, vida_max: int = 100) -> Optional[PlayerSession]:
       """Cria um novo personagem."""
       if not nome.strip():
           return None
       
       return PlayerSession(
           nome=nome,
           vida_max=vida_max,
           vida_atual=vida_max
       )
   
   # ❌ Ruim
   def criar_personagem(nome,vida_max=100):
       if nome=="":
           return None
       return PlayerSession(nome=nome,vida_max=vida_max,vida_atual=vida_max)

Documentação
^^^^^^^^^^^^

Use docstrings no formato Google:

.. code-block:: python

   def calcular_dano(base: int, modificador: float = 1.0) -> int:
       """Calcula o dano baseado em valores e modificadores.
       
       Args:
           base: Dano base do ataque
           modificador: Multiplicador de dano (padrão: 1.0)
       
       Returns:
           Dano final calculado
       
       Raises:
           ValueError: Se base for negativo
       
       Example:
           >>> calcular_dano(10, 1.5)
           15
       """
       if base < 0:
           raise ValueError("Dano base não pode ser negativo")
       
       return int(base * modificador)

Tratamento de Erros
^^^^^^^^^^^^^^^^^^^

Use exceções específicas:

.. code-block:: python

   class PersonagemError(Exception):
       """Exceção base para erros de personagem."""
       pass
   
   class NomeDuplicadoError(PersonagemError):
       """Exceção para nomes duplicados."""
       pass
   
   def criar_personagem(nome: str) -> PlayerSession:
       if nome_existe(nome):
           raise NomeDuplicadoError(f"Nome '{nome}' já existe")
       
       # Criação do personagem...

Testes
------

Organização dos Testes
^^^^^^^^^^^^^^^^^^^^^

Os testes estão organizados em subpastas por categoria:

* **``tests/model/``**: Testes de models (Player, Chunk, Mapa, Bioma)
* **``tests/repositorio/``**: Testes de repositórios e padrão Repository  
* **``tests/servicos/``**: Testes de serviços e integração
* **``tests/utils/``**: Testes de utilitários (preparado para futuro)

Ao adicionar novos testes, coloque-os na pasta apropriada:

.. code-block:: python

   # Para novos models
   tests/model/test_novo_model.py
   
   # Para novos repositórios
   tests/repositorio/test_novo_repository.py
   
   # Para novos serviços
   tests/servicos/test_novo_service.py
   
   # Para novos utilitários
   tests/utils/test_novo_utils.py

Escrevendo Testes
^^^^^^^^^^^^^^^^

Crie testes para novas funcionalidades:

.. code-block:: python

   import pytest
   from utils.player_manager import PlayerSession, criar_personagem
   
   def test_criar_personagem_sucesso():
       """Testa criação bem-sucedida de personagem."""
       player = criar_personagem("Teste", 100)
       
       assert player is not None
       assert player.nome == "Teste"
       assert player.vida_max == 100
       assert player.vida_atual == 100
   
   def test_criar_personagem_nome_vazio():
       """Testa criação com nome vazio."""
       with pytest.raises(ValueError):
           criar_personagem("")
   
   def test_criar_personagem_nome_duplicado():
       """Testa criação com nome duplicado."""
       criar_personagem("Teste")
       
       with pytest.raises(NomeDuplicadoError):
           criar_personagem("Teste")

Executando Testes
^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Instalar pytest
   pip install pytest pytest-cov
   
   # Executar todos os testes
   pytest
   
   # Executar testes por categoria
   pytest tests/model/ -v
   pytest tests/repositorio/ -v
   pytest tests/servicos/ -v
   
   # Com cobertura
   pytest --cov=app --cov-report=html
   
   # Testes específicos
   pytest tests/model/test_player_manager.py

Commits
-------

Convenções de Commit
^^^^^^^^^^^^^^^^^^^^

Use commits semânticos:

* **feat**: Nova funcionalidade
* **fix**: Correção de bug
* **docs**: Documentação
* **style**: Formatação (espaços, ponto e vírgula, etc.)
* **refactor**: Refatoração de código
* **test**: Adicionando ou corrigindo testes
* **chore**: Tarefas de manutenção

Exemplos:

.. code-block:: bash

   feat: add character deletion functionality
   fix: resolve duplicate session exit message
   docs: update installation guide
   style: fix indentation in display.py
   refactor: simplify player loading logic
   test: add tests for character creation
   chore: update dependencies

Mensagens de Commit
^^^^^^^^^^^^^^^^^^

* Use o imperativo ("add" não "added")
* Máximo 50 caracteres

.. code-block:: bash

   feat: add character deletion functionality
   
   - Add delete_player function to player_manager
   - Add confirmation dialog for deletion
   - Prevent deletion of active character
   - Add tests for deletion functionality
   
   Closes #123

Pull Requests
-------------

Criando um PR
^^^^^^^^^^^^

#. **Atualize** sua branch com a main::

   git checkout main
   git pull origin main
   git checkout sua-branch
   git rebase main

#. **Teste** suas mudanças::

   python -m pytest
   python app/main.py

#. **Push** suas mudanças::

   git push origin sua-branch

#. **Abra o PR** no GitHub


Documentação
------------

Atualizando Documentação
^^^^^^^^^^^^^^^^^^^^^^^

Para mudanças que afetam a documentação:

#. **Atualize** os arquivos .rst relevantes
#. **Gere** a documentação::

   cd docs
   make html

#. **Verifique** se está correto::

   open build/html/index.html

#. **Commit** as mudanças::

   git add docs/
   git commit -m "docs: update API documentation"

Estrutura de Documentação
^^^^^^^^^^^^^^^^^^^^^^^^^

* **installation.rst**: Guias de instalação
* **quickstart.rst**: Início rápido
* **user_guide.rst**: Guia do usuário
* **api_reference.rst**: Documentação da API
* **database.rst**: Estrutura do banco
* **development.rst**: Guia de desenvolvimento
* **contributing.rst**: Este guia

Para mais informações:

* :doc:`development` - Guia de desenvolvimento
* :doc:`api_reference` - Documentação da API
* :doc:`database` - Estrutura do banco 
