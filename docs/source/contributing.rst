Contribuindo
============

Obrigado por considerar contribuir com o Minecraft Legends! Este guia irá ajudá-lo a começar.

Como Contribuir
---------------

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

Sugerindo Features
------------------

Template de Feature Request
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: markdown

   ## 💡 Feature Request
   
   **Problema que a feature resolve**
   Uma descrição clara e concisa do problema que a feature resolve.
   
   **Descrição da Solução**
   Uma descrição clara e concisa do que você quer que aconteça.
   
   **Alternativas Consideradas**
   Uma descrição clara e concisa de quaisquer soluções ou features alternativas que você considerou.
   
   **Contexto Adicional**
   Adicione qualquer outro contexto ou screenshots sobre a feature request aqui.

Critérios para Features
^^^^^^^^^^^^^^^^^^^^^^^

Features devem:

* **Resolver um problema real** ou adicionar valor significativo
* **Ser bem documentadas** com casos de uso claros
* **Seguir os padrões** do projeto
* **Incluir testes** quando aplicável
* **Ser compatíveis** com a arquitetura existente

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
   
   # Com cobertura
   pytest --cov=app --cov-report=html
   
   # Testes específicos
   pytest tests/test_player_manager.py

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
* Primeira linha com máximo 50 caracteres
* Descrição detalhada após linha em branco
* Referencie issues quando aplicável

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

Template de PR
^^^^^^^^^^^^^

.. code-block:: markdown

   ## 📝 Descrição
   
   Breve descrição das mudanças implementadas.
   
   ## 🔗 Issue Relacionada
   
   Closes #123
   
   ## 🧪 Testes
   
   - [ ] Testes unitários passando
   - [ ] Testes de integração passando
   - [ ] Funcionalidade testada manualmente
   
   ## 📸 Screenshots
   
   Se aplicável, adicione screenshots das mudanças.
   
   ## ✅ Checklist
   
   - [ ] Código segue os padrões do projeto
   - [ ] Documentação atualizada
   - [ ] Testes adicionados/atualizados
   - [ ] Commits seguem convenções
   - [ ] PR está atualizado com a main

Revisão de Código
-----------------

Critérios de Revisão
^^^^^^^^^^^^^^^^^^^^

* **Funcionalidade**: O código faz o que deveria?
* **Qualidade**: O código está bem escrito?
* **Testes**: Há testes adequados?
* **Documentação**: Está bem documentado?
* **Performance**: Há problemas de performance?
* **Segurança**: Há vulnerabilidades?

Comentários de Revisão
^^^^^^^^^^^^^^^^^^^^^^

Seja construtivo:

.. code-block:: markdown

   ✅ **Positivo**: "Boa implementação! O código está claro e bem estruturado."
   
   🔧 **Sugestão**: "Considere usar uma validação mais específica aqui."
   
   ❌ **Problema**: "Esta função pode causar problemas de performance com muitos dados."
   
   💡 **Idea**: "Que tal implementar cache para melhorar performance?"

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

Comunicação
-----------

Canais de Comunicação
^^^^^^^^^^^^^^^^^^^^^

* **GitHub Issues**: Para bugs e features
* **GitHub Discussions**: Para discussões gerais
* **Pull Requests**: Para contribuições de código
* **Email**: Para assuntos privados

Código de Conduta
^^^^^^^^^^^^^^^^^

* Seja respeitoso e inclusivo
* Foque no código, não na pessoa
* Seja construtivo em feedback
* Ajude outros contribuidores
* Respeite diferentes pontos de vista

Reconhecimento
--------------

Contribuidores
^^^^^^^^^^^^^

Todos os contribuidores são reconhecidos:

* No arquivo CONTRIBUTORS.md
* Na documentação
* Nos releases do GitHub
* No README do projeto

Como Ser Reconhecido
^^^^^^^^^^^^^^^^^^^^

* Contribuições significativas de código
* Melhorias importantes na documentação
* Reportes de bugs críticos
* Sugestões de features implementadas
* Ajuda na comunidade

Próximos Passos
---------------

Agora que você conhece como contribuir:

#. **Escolha** uma issue para trabalhar
#. **Configure** seu ambiente de desenvolvimento
#. **Desenvolva** sua contribuição
#. **Teste** suas mudanças
#. **Abra** um Pull Request

Obrigado por contribuir com o Minecraft Legends! 🎮

Para mais informações:

* :doc:`development` - Guia de desenvolvimento
* :doc:`api_reference` - Documentação da API
* :doc:`database` - Estrutura do banco 