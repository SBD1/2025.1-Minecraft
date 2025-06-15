Guia do Usuário
==============

Este guia detalhado irá ajudá-lo a aproveitar ao máximo o MINECRAFT - FGA - 2025/1.

Interface do Jogo
-----------------

Tela Inicial
^^^^^^^^^^^

A tela inicial exibe:

* **Título do jogo** com bordas decorativas
* **Informações do personagem ativo** (se houver):
  * Nome do personagem
  * Vida atual/máxima
  * XP
  * Força
  * Localização atual (bioma, mapa, turno)
* **Menu principal** com opções numeradas

Menu Principal
^^^^^^^^^^^^^

O menu se adapta baseado no estado do jogo:

**Com personagem ativo:**
* 1. 🎮 Iniciar jogo
* 2. 📊 Ver status detalhado
* 3. 💾 Salvar progresso
* 4. 👥 Trocar personagem
* 5. 📋 Lista de personagens
* 6. ➕ Criar novo personagem
* 7. 🚪 Sair

**Sem personagem ativo:**
* 1. 👥 Selecionar personagem
* 2. ➕ Criar novo personagem
* 3. 📋 Lista de personagens
* 4. 🚪 Sair

Sistema de Personagens
----------------------

Criação de Personagens
^^^^^^^^^^^^^^^^^^^^^^

Para criar um novo personagem:

#. Selecione **6. ➕ Criar novo personagem**
#. Digite um nome único (não pode estar vazio)
#. O sistema criará automaticamente com:
   * **Vida máxima**: 100
   * **Vida atual**: 100
   * **XP**: 0
   * **Força**: 10
   * **Localização**: Chunk 1 (Deserto - Mapa_Principal - Dia)

**Restrições:**
* Nome deve ser único
* Nome não pode estar vazio
* Valores iniciais são fixos

Gerenciamento de Personagens
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lista de Personagens
"""""""""""""""""""

A lista exibe personagens em formato de grid:

* **Visualização em tabelas** lado a lado
* **Informações por personagem**:
  * Nome
  * Vida atual/máxima
  * XP
  * Força
  * Localização
* **Indicador de personagem ativo** (🎮)
* **Adaptação automática** ao tamanho do terminal

Seleção de Personagem
""""""""""""""""""""

#. Acesse a lista de personagens
#. Escolha **1. 🎮 Selecionar personagem**
#. Digite o número do personagem
#. O sistema carregará e ativará o personagem

**Validações:**
* Número deve ser válido
* Não permite selecionar personagem já ativo
* Confirma carregamento bem-sucedido

Deleção de Personagens
"""""""""""""""""""""

#. Acesse a lista de personagens
#. Escolha **2. 🗑️ Deletar personagem**
#. Digite o número do personagem
#. Confirme a operação

**Proteções:**
* Não permite deletar personagem ativo
* Requer confirmação explícita
* Ação irreversível

Sistema de Localização
----------------------

Biomas Disponíveis
^^^^^^^^^^^^^^^^^

O jogo inclui os seguintes biomas:

* **Deserto** - Ambiente árido
* **Oceano** - Águas azuis
* **Selva** - Vegetação densa
* **Floresta** - Árvores e natureza

Mapas e Turnos
^^^^^^^^^^^^^

* **Mapa Principal** - Mapa principal do jogo
* **Turnos**:
  * **Dia** - Iluminação clara
  * **Noite** - Ambiente noturno

Chunks
^^^^^^

Chunks são divisões do mundo:

* **Chunk 1**: Deserto (Mapa_Principal - Dia)
* **Chunk 2**: Oceano (Mapa_Principal - Dia)
* **Chunk 3**: Selva (Mapa_Principal - Noite)
* **Chunk 4**: Floresta (Mapa_Principal - Noite)

Sistema de Status
-----------------

Atributos do Personagem
^^^^^^^^^^^^^^^^^^^^^^

* **Vida Máxima**: Capacidade total de vida (padrão: 100)
* **Vida Atual**: Vida restante (0 = morte)
* **XP**: Experiência acumulada (padrão: 0)
* **Força**: Poder de ataque (padrão: 10)

Status Detalhado
^^^^^^^^^^^^^^^

Para ver informações completas:

#. Selecione **2. 📊 Ver status detalhado**
#. Visualize:
  * ID único do personagem
  * Nome completo
  * Vida atual/máxima
  * XP e força
  * Localização detalhada
  * Status de vida (vivo/morto)

Sistema de Persistência
-----------------------

Salvamento Automático
^^^^^^^^^^^^^^^^^^^^^

O jogo salva automaticamente quando:

* **Sai do jogo** - Salva antes de encerrar
* **Troca de personagem** - Salva o personagem atual
* **Executa ações importantes** - Salva progresso

Salvamento Manual
^^^^^^^^^^^^^^^^

Para salvar manualmente:

#. Selecione **3. 💾 Salvar progresso**
#. Confirme que os dados foram salvos
#. Verifique mensagem de sucesso

Banco de Dados
^^^^^^^^^^^^^

* **PostgreSQL** - Banco de dados principal
* **Docker** - Container isolado
* **Persistência** - Dados mantidos entre sessões
* **Backup automático** - Volume Docker preserva dados

Interface e Usabilidade
-----------------------

Cores e Emojis
^^^^^^^^^^^^^

O jogo utiliza:

* **Cores** - Diferenciação visual (verde, vermelho, amarelo)
* **Emojis** - Ícones intuitivos
* **Bordas** - Elementos decorativos
* **Formatação** - Texto bem estruturado

Navegação
^^^^^^^^^

* **Menus numerados** - Fácil seleção
* **Validação de entrada** - Previne erros
* **Mensagens claras** - Feedback constante
* **Opções de cancelamento** - Controle do usuário

Tratamento de Erros
^^^^^^^^^^^^^^^^^^^

* **Validação de entrada** - Números e texto
* **Mensagens de erro** - Explicações claras
* **Recuperação automática** - Continua funcionando
* **Logs informativos** - Rastreamento de problemas

Dicas e Truques
---------------

Dicas Gerais
^^^^^^^^^^^

* **Salve frequentemente** - Use o salvamento manual
* **Experimente personagens** - Crie vários para testar
* **Observe a localização** - Cada chunk tem características únicas
* **Use o status detalhado** - Mantenha-se informado

Boas Práticas
^^^^^^^^^^^^

* **Nomes únicos** - Evite conflitos
* **Backup regular** - Preserve seus dados
* **Teste funcionalidades** - Explore todas as opções
* **Reporte problemas** - Ajude a melhorar o jogo

Próximos Passos
---------------

Para aprofundar seus conhecimentos:

* :doc:`api_reference` - Documentação técnica
* :doc:`database` - Estrutura do banco de dados
* :doc:`development` - Como contribuir 