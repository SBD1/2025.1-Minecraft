# Arquitetura do Projeto Minecraft Legends

## Visão Geral

O projeto Minecraft Legends utiliza uma arquitetura em camadas com o padrão Repository para separar a lógica de negócio da persistência de dados, e um InterfaceService para coordenar as ações da interface com os repositórios.

## Camadas da Arquitetura

### 1. Camada de Interface (Interface Layer)
- **Localização**: `app/src/interface/`
- **Responsabilidade**: Interface com o usuário, menus e exibição
- **Componentes**:
  - `display.py`: Interface principal do jogo
  - `screen_helpers.py`: Funções auxiliares de exibição

### 2. Camada de Serviços (Service Layer)
- **Localização**: `app/src/services/`
- **Responsabilidade**: Lógica de negócio e coordenação entre camadas
- **Componentes**:
  - `interface_service.py`: Coordena ações da interface com repositórios

### 3. Camada de Repositórios (Repository Layer)
- **Localização**: `app/src/repositories/`
- **Responsabilidade**: Acesso e persistência de dados
- **Componentes**:
  - `player_repository.py`: Operações com jogadores
  - `chunk_repository.py`: Operações com chunks
  - `mapa_repository.py`: Operações com mapas
  - `bioma_repository.py`: Operações com biomas

### 4. Camada de Modelos (Model Layer)
- **Localização**: `app/src/models/`
- **Responsabilidade**: Entidades de domínio
- **Componentes**:
  - `player.py`: Modelo do jogador
  - `chunk.py`: Modelo do chunk
  - `mapa.py`: Modelo do mapa
  - `bioma.py`: Modelo do bioma

### 5. Camada de Utilitários (Utils Layer)
- **Localização**: `app/src/utils/`
- **Responsabilidade**: Funções auxiliares e gerenciamento de sessão
- **Componentes**:
  - `player_manager.py`: Gerenciamento de sessão do jogador
  - `db_helpers.py`: Conexão com banco de dados

## Padrão Repository

### Estrutura
Cada repositório segue a estrutura:
```
Repository Interface (ABC)
├── find_all()
├── find_by_id()
├── save()
├── delete()
└── métodos específicos

Repository Implementation
├── Implementação PostgreSQL
├── Validações
└── Tratamento de transações
```

### Benefícios
- **Separação de Responsabilidades**: Lógica de negócio separada da persistência
- **Testabilidade**: Fácil mock dos repositórios para testes
- **Flexibilidade**: Possibilidade de trocar implementação de banco
- **Manutenibilidade**: Código mais organizado e fácil de manter

## InterfaceService

### Responsabilidades
- Coordenar ações entre interface e repositórios
- Implementar lógica de negócio
- Validar dados antes de persistir
- Fornecer métodos de alto nível para a interface

### Métodos Principais
```python
class InterfaceService:
    def get_all_players() -> List[Player]
    def create_player(nome, vida_maxima, forca) -> Optional[Player]
    def save_player(player) -> Optional[Player]
    def delete_player(player_id) -> bool
    def move_player_to_chunk(player, chunk_id) -> Optional[Player]
    def get_adjacent_chunks(chunk_id, turno) -> List[tuple]
    def get_player_statistics() -> Dict[str, Any]
```

## Fluxo de Dados

### Criação de Jogador
```
Interface → InterfaceService → PlayerRepository → Database
     ↑                              ↓
     └── Player Object ←────────────┘
```

### Movimento de Jogador
```
Interface → InterfaceService → ChunkRepository (valida chunk)
     ↑                              ↓
     └── Player Object ←────────────┘
                    ↓
            PlayerRepository (salva localização)
```

## Validações

### Nível de Repositório
- Validações de dados antes de persistir
- Verificação de integridade referencial
- Tratamento de transações (commit/rollback)

### Nível de Serviço
- Validações de negócio
- Verificação de regras de domínio
- Coordenação entre múltiplos repositórios

## Testes

### Estrutura de Testes
```
tests/
├── test_models/          # Testes dos modelos
├── test_repositories/    # Testes dos repositórios
├── test_services/        # Testes dos serviços
├── test_integration.py   # Testes de integração
└── test_interface/       # Testes da interface
```

### Tipos de Testes
- **Unitários**: Testam componentes isolados
- **Integração**: Testam interação entre camadas
- **Mock**: Simulam dependências externas

## Configuração do Banco

### Docker Compose
```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: minecraft_legends
      POSTGRES_USER: minecraft
      POSTGRES_PASSWORD: minecraft123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### Conexão
- **Host**: localhost:5432
- **Database**: minecraft_legends
- **User**: minecraft
- **Password**: minecraft123

## Convenções de Código

### Nomenclatura
- **Classes**: PascalCase (ex: `PlayerRepository`)
- **Métodos**: snake_case (ex: `find_by_id`)
- **Variáveis**: snake_case (ex: `player_id`)
- **Constantes**: UPPER_CASE (ex: `MAX_HEALTH`)

### Estrutura de Arquivos
- Um arquivo por classe principal
- Imports organizados por categoria
- Docstrings em todos os métodos públicos

### Tratamento de Erros
- Uso de try/catch com rollback em transações
- Mensagens de erro descritivas
- Logs para debugging

## Próximos Passos

### Melhorias Planejadas
1. **Cache**: Implementar cache para melhorar performance
2. **Logging**: Sistema de logs estruturado
3. **Configuração**: Arquivo de configuração centralizado
4. **API REST**: Interface REST para integração externa
5. **Eventos**: Sistema de eventos para desacoplamento

### Refatorações Futuras
1. **Dependency Injection**: Container de dependências
2. **Command Pattern**: Para operações complexas
3. **Observer Pattern**: Para notificações de mudanças
4. **Factory Pattern**: Para criação de objetos complexos 