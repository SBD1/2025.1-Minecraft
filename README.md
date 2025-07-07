# 2025.1 - MINECRAFT - FGA - 2025/1

[![Tests](https://github.com/SBD1/2025.1-Minecraft/actions/workflows/tests.yml/badge.svg)](https://github.com/SBD1/2025.1-Minecraft/actions/workflows/tests.yml)
[![Documentation](https://github.com/SBD1/2025.1-Minecraft/actions/workflows/docs.yml/badge.svg)](https://github.com/SBD1/2025.1-Minecraft/actions/workflows/docs.yml)
[![Codecov](https://codecov.io/gh/SBD1/2025.1-Minecraft/branch/main/graph/badge.svg)](https://codecov.io/gh/SBD1/2025.1-Minecraft)

O **MINECRAFT - FGA - 2025/1**, foi desenvolvido para a disciplina de Sistemas de Banco de Dados 1 (SBD1) — 2025.1.

Este projeto implementa um jogo baseado no MINECRAFT utilizando Python e PostgreSQL, com uma arquitetura em camadas bem definida e ambiente isolado via Docker.

---

## Documentação

**Documentação Completa**: [https://sbd1.github.io/2025.1-Minecraft/](https://sbd1.github.io/2025.1-Minecraft/)

A documentação inclui:
- Guias de instalação e início rápido
- Guia completo do usuário
- Referência da API e desenvolvimento
- Estrutura do banco de dados
- Guia de contribuição

---

## Arquitetura do Projeto

O projeto utiliza uma arquitetura em camadas com padrão Repository:

- **Interface Layer** (`app/src/interface/`): Interface com o usuário (terminal)
- **Service Layer** (`app/src/services/`): Lógica de negócio
- **Repository Layer** (`app/src/repositories/`): Acesso a dados
- **Model Layer** (`app/src/models/`): Entidades de domínio
- **Utils Layer** (`app/src/utils/`): Funções auxiliares

### Modelos Implementados
- **Player**: Gerenciamento de jogadores com estatísticas
- **Chunk**: Sistema de chunks do mundo
- **Mapa**: Gerenciamento do mapa do jogo
- **Bioma**: Diferentes tipos de biomas

---

## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes softwares instalados na sua máquina:

- [Docker](https://www.docker.com/) (versão 20.10+)
- [Docker Compose](https://docs.docker.com/compose/) (versão 2.0+)

---

## Como executar o jogo

### 1. Clone e acesse este repositório

```bash
git clone https://github.com/SBD1/2025.1-Minecraft.git
cd 2025.1-Minecraft
```

### 2. Construa e suba os containers

```bash
docker compose up -d --build
```

### 3. Acesse o container da aplicação

```bash
docker exec -it python_mine bash
```

### 4. Execute o jogo

```bash
python main.py
```

---

## Executando os Testes

### Executar todos os testes
```bash
docker compose exec app python -m pytest tests/ -v
```

### Executar com cobertura de código
```bash
docker compose exec app python -m pytest tests/ --cov=src --cov-report=term-missing
```

### Executar testes por categoria
```bash
# Testes de models
docker compose exec app python -m pytest tests/model/ -v

# Testes de repositórios
docker compose exec app python -m pytest tests/repositorio/ -v

# Testes de serviços
docker compose exec app python -m pytest tests/servicos/ -v

# Testes de integração
docker compose exec app python -m pytest tests/servicos/test_integration.py -v
```

### Executar teste específico
```bash
docker compose exec app python -m pytest tests/model/test_bioma.py::TestBioma::test_bioma_creation -v
```

### Executar testes com relatório detalhado
```bash
docker compose exec app python -m pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
```

---

## Documentação Local

Para construir a documentação localmente:

```bash
# Instalar dependências da documentação
pip install sphinx sphinx-rtd-theme

# Construir documentação
cd docs
./build_docs.sh
```

Ou manualmente:

```bash
cd docs
make html
```

A documentação será gerada em `docs/build/html/`.

---

## Desenvolvimento

### Estrutura do Projeto

```
2025.1-Minecraft/
├── app/                   # Aplicação principal
│   ├── main.py            # Ponto de entrada
│   ├── requirements.txt   # Dependências Python
│   ├── Dockerfile          # Container da aplicação
│   ├── tests/             # Testes unitários e integração
│   │   ├── model/         # Testes de models
│   │   │   ├── test_bioma.py
│   │   │   ├── test_chunk.py
│   │   │   └── test_mapa.py
│   │   ├── repositorio/   # Testes de repositórios
│   │   │   └── test_repository_pattern.py
│   │   ├── servicos/      # Testes de serviços
│   │   │   ├── test_integration.py
│   │   │   └── test_singleton.py
│   │   ├── utils/         # Testes de utilitários (futuro)
│   │   ├── conftest.py    # Configuração compartilhada
│   │   └── __init__.py
│   └── src/               # Código fonte
│       ├── interface/     # Interface do usuário
│       │   └── display.py
│       ├── services/      # Lógica de negócio
│       │   ├── game_service.py
│       │   └── interface_service.py
│       ├── repositories/  # Acesso a dados
│       │   ├── player_repository.py
│       │   ├── chunk_repository.py
│       │   ├── mapa_repository.py
│       │   └── bioma_repository.py
│       ├── models/       # Entidades de domínio
│       │   ├── player.py
│       │   ├── chunk.py
│       │   ├── mapa.py
│       │   └── bioma.py
│       └── utils/        # Utilitários
│           └── db_helpers.py
├── db/                   # Scripts do banco de dados
│   ├── Dockerfile.db      # Container do PostgreSQL
│   ├── init_database.sh   # Script de inicialização
│   ├── README_STRUCTURE.md # Documentação da nova estrutura
│   ├── init/             # Estrutura organizada de inicialização
│   │   ├── 01_users/     # Criação de usuários
│   │   ├── 02_schema/    # Definição de tabelas e índices
│   │   └── 03_data/      # Inserção de dados
│   └── dql.sql           # Consultas de exemplo
├── docs/                 # Documentação
│   ├── source/           # Arquivos fonte da documentação
│   ├── build/            # Documentação gerada
│   └── architecture.md   # Documentação da arquitetura
└── docker-compose.yml    # Orquestração dos containers
```

### Dependências

#### Python (app/requirements.txt)
- `psycopg2-binary==2.9.9`: Driver PostgreSQL
- `colorama==0.4.6`: Cores no terminal
- `pytest==7.4.3`: Framework de testes
- `pytest-cov==4.1.0`: Cobertura de código
- `pytest-mock==3.12.0`: Mocking para testes

#### Documentação (docs/requirements.txt)
- `sphinx`: Gerador de documentação
- `sphinx-rtd-theme`: Tema Read the Docs

### Padrões de Código

- **Arquitetura**: Camadas com padrão Repository
- **Testes**: Cobertura completa com pytest
- **Banco**: PostgreSQL com triggers e stored procedures
- **Containerização**: Docker para desenvolvimento e produção

---

## Terminar execução

Para sair do terminal interativo:
- Pressione `Ctrl + D`
- Ou digite `exit` e pressione `Enter`

Para parar os containers:
```bash
docker compose down
```

Para parar e remover volumes (cuidado: apaga dados):
```bash
docker compose down -v
```

---

## Créditos

Disciplina **SBD1 – 2025.1**.  
Professor: *Mauricio Serrano*  
Instituição: *Universidade de Brasília*
Alunos:
    - João Lucas Fragoso Zarbiélli
    - Karolina
    - Nathan
    - Victor Hoffmann
    - Yan Sousa Guimaraes

---

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE).
