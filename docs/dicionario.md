# Dicionário de dados

## Introdução

Um **dicionário de dados** é um recurso fundamental em projetos de banco de dados, pois descreve detalhadamente os elementos que compõem o sistema, como tabelas, campos, tipos de dados e restrições. Ele funciona como uma espécie de manual técnico que **centraliza informações** sobre os dados, garantindo consistência, padronização e melhor comunicação entre os envolvidos no projeto. Além disso, o dicionário de dados **facilita a documentação**, uma vez que registra os significados, formatos e possíveis valores de cada atributo. Com isso, ele não apenas **apoia o desenvolvimento** e a manutenção do sistema, mas também **favorece a integração** entre equipes de desenvolvimento, análise e usuários finais, promovendo clareza e evitando ambiguidades no uso dos dados.

O dicionário de dados deste projeto é composto pelas seguintes colunas:

- **Atributo**: Nome do campo ou característica que representa uma informação específica armazenada na base de dados.
- **Obrigatoriedade**: Indica se o preenchimento do atributo é obrigatório ou opcional dentro do sistema.
- **Tipo**: Define o formato do dado, como texto (string), número inteiro (int), decimal, data, entre outros.
- **Tamanho**: Indica a capacidade máxima ou o número de caracteres que o dado pode conter.
- **Descrição**: Explica detalhadamente o significado do atributo ou entidade e seu papel dentro do contexto do jogo.
- **Exemplo**: Fornece um valor ilustrativo para ajudar a entender como o atributo é utilizado na prática.



# Dicionário de dados

## Entidade: Entidade  
#### Descrição: Representa qualquer ser do jogo (jogador, mob, vilão ou criatura).

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição                             | Exemplo        |
| ------------ | --------------- | -------- | ------- | ------------------------------------- | -------------- |
| id_entidade  | Obrigatório     | int      | 4       | Identificador da entidade             | 1              |
| id_bioma     | Obrigatório     | int      | 4       | Bioma onde a entidade se encontra     | 2              |
| id_inventario| Obrigatório     | int      | 4       | Inventário da entidade                | 5              |
| armadura     | Opcional        | varchar  | 50      | Armadura equipada                     | Ferro          |
| forca        | Opcional        | int      | 4       | Força da entidade                     | 20             |
| vida_atual   | Obrigatório     | int      | 4       | Vida atual                            | 30             |
| vida_max     | Obrigatório     | int      | 4       | Vida máxima                           | 40             |
| nome         | Obrigatório     | varchar  | 100     | Nome da entidade                      | Zumbi          |

## Entidade: Item  
#### Descrição: Representa itens no jogo (equipamentos, materiais, etc).

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição                                     | Exemplo              |
| ------------ | --------------- | -------- | ------- | --------------------------------------------- | -------------------- |
| id_item      | Obrigatório     | int      | 4       | Identificador do item                         | 10                   |
| nome         | Obrigatório     | varchar  | 100     | Nome do item                                  | Espada de Ferro      |
| dano         | Opcional        | int      | 4       | Dano causado pelo item                        | 7                    |
| durabilidade | Opcional        | int      | 4       | Quantidade de usos antes de quebrar           | 250                  |
| encantavel   | Obrigatório     | boolean  | 1       | Define se pode ser encantado                  | true                 |
| craftavel    | Obrigatório     | boolean  | 1       | Define se pode ser craftado                   | true                 |
| id_item      | Opcional        | int      | 4       | Item necessário na receita (auto-relacionado) | 5                    |
| receita      | Opcional        | varchar  | 500     | Receita de criação                            | 2x madeira, 1x ferro |

## Entidade: Inventário  
#### Descrição: Armazena os itens, slots e crafting de uma entidade.

| Atributo        | Obrigatoriedade | Tipo     | Tamanho | Descrição                             | Exemplo |
| --------------- | --------------- | -------- | ------- | ------------------------------------- | ------- |
| id_inventario   | Obrigatório     | int      | 4       | Identificador do inventário           | 5       |
| id_entidade     | Obrigatório     | int      | 4       | Entidade dona do inventário           | 1       |
| ArmaduraSlots   | Opcional        | int      | 4       | Quantidade de slots de armadura       | 4       |
| StorageSlots    | Opcional        | int      | 4       | Quantidade de slots de armazenamento  | 20      |
| Crafting        | Opcional        | int      | 4       | Slots para crafting                   | 4       |
| Não_craftavel   | Opcional        | boolean  | 1       | Se o item não é craftável             | false   |
| id_item         | Opcional        | int      | 4       | Item contido no inventário            | 7       |

## Entidade: Baú  
#### Descrição: Representa um baú com inventário próprio.

| Atributo        | Obrigatoriedade | Tipo     | Tamanho | Descrição                         | Exemplo |
| --------------- | --------------- | -------- | ------- | --------------------------------- | ------- |
| id_item         | Obrigatório     | int      | 4       | Item que representa o baú         | 12      |
| id_inventario   | Obrigatório     | int      | 4       | Inventário contido no baú         | 9       |

## Entidade: Mob  
#### Descrição: Criaturas vivas no mundo, podendo ser hostis ou não.

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição              | Exemplo  |
| ------------ | --------------- | -------- | ------- | ---------------------- | -------- |
| id_entidade  | Obrigatório     | int      | 4       | Entidade associada     | 3        |
| tipoMob      | Obrigatório     | varchar  | 50      | Tipo de mob            | Hostil   |
| tmpRespawn   | Opcional        | int      | 4       | Tempo para reaparecer  | 30       |

## Entidade: Player  
#### Descrição: Jogador controlado por humano.

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição                         | Exemplo |
| ------------ | --------------- | -------- | ------- | --------------------------------- | ------- |
| id_entidade  | Obrigatório     | int      | 4       | Entidade associada                | 1       |
| fome         | Obrigatório     | int      | 4       | Nível de fome do jogador          | 10      |
| xp           | Obrigatório     | int      | 4       | Nível de experiência              | 42      |

## Entidade: Bioma  
#### Descrição: Região ecológica com clima, fauna e flora específicos.

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição                     | Exemplo     |
| ------------ | --------------- | -------- | ------- | ----------------------------- | ----------- |
| id_bioma     | Obrigatório     | int      | 4       | Identificador do bioma        | 5           |
| tipoBioma    | Obrigatório     | varchar  | 50      | Tipo do bioma                 | Floresta    |
| período      | Obrigatório     | varchar  | 20      | Período do dia                | Noite       |

## Entidade: Fauna  
#### Descrição: Animais presentes em um bioma.

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição                | Exemplo  |
| ------------ | --------------- | -------- | ------- | ------------------------ | -------- |
| id_bioma     | Obrigatório     | int      | 4       | Bioma de ocorrência       | 2        |
| especieFauna | Obrigatório     | varchar  | 100     | Espécie animal presente   | Lobo     |

## Entidade: Flora  
#### Descrição: Plantas presentes em um bioma.

| Atributo      | Obrigatoriedade | Tipo     | Tamanho | Descrição                | Exemplo   |
| ------------- | --------------- | -------- | ------- | ------------------------ | --------- |
| id_bioma      | Obrigatório     | int      | 4       | Bioma de ocorrência       | 3         |
| especieFlora  | Obrigatório     | varchar  | 100     | Espécie vegetal presente  | Carvalho  |

## Entidade: Estrutura  
#### Descrição: Construções presentes nos biomas do jogo.

| Atributo       | Obrigatoriedade | Tipo     | Tamanho | Descrição                        | Exemplo           |
| -------------- | --------------- | -------- | ------- | -------------------------------- | ----------------- |
| id_estrutura   | Obrigatório     | int      | 4       | Identificador da estrutura       | 1                 |
| id_bioma       | Obrigatório     | int      | 4       | Bioma onde aparece               | 2                 |
| tipo_estrutura | Obrigatório     | varchar  | 50      | Tipo da estrutura                | Vila              |
| prob_geração   | Obrigatório     | decimal  | 5,2     | Probabilidade de ser gerada      | 0.25              |

## Entidade: Encantamento

#### Descrição: Melhorias mágicas aplicáveis a itens ou jogadores.

| Atributo                         | Obrigatoriedade | Tipo     | Tamanho | Descrição                                 | Exemplo           |
| -------------------------------- | --------------- | -------- | ------- | ----------------------------------------- | ----------------- |
| id_encantamento                 | Obrigatório     | int      | 4       | Identificador do encantamento             | 1                 |
| nome                            | Obrigatório     | varchar  | 100     | Nome do encantamento                      | Proteção          |
| boost                           | Obrigatório     | varchar  | 100     | Efeito do encantamento                    | +5 Defesa         |
| aplicavel_player                | Obrigatório     | boolean  | 1       | Pode ser aplicado ao jogador              | true              |
| atributo_afetado                | Obrigatório     | varchar  | 100     | Atributo modificado                       | defesa            |
| ids_itens_necessários           | Opcional        | varchar  | 500     | Itens exigidos para aplicar               | 3,4               |
| ids_encantamentos_incompativeis | Opcional        | varchar  | 500     | Encantamentos incompatíveis               | 2,5               |
| ids_itens_aplicaveis            | Opcional        | varchar  | 500     | Itens que podem receber esse encantamento | 1,6               |

## Entidade: Hostil  
#### Descrição: Entidade com comportamento agressivo.

| Atributo    | Obrigatoriedade | Tipo | Tamanho | Descrição               | Exemplo |
| ----------- | --------------- | ---- | ------- | ----------------------- | ------- |
| id_entidade | Obrigatório     | int  | 4       | FK para Entidade        | 3       |

## Entidade: NãoHostil  
#### Descrição: Entidade pacífica.

| Atributo    | Obrigatoriedade | Tipo | Tamanho | Descrição               | Exemplo |
| ----------- | --------------- | ---- | ------- | ----------------------- | ------- |
| id_entidade | Obrigatório     | int  | 4       | FK para Entidade        | 4       |

## Entidade: Villager  
#### Descrição: Entidade com função social (comércio, aldeia).

| Atributo    | Obrigatoriedade | Tipo | Tamanho | Descrição               | Exemplo |
| ----------- | --------------- | ---- | ------- | ----------------------- | ------- |
| id_entidade | Obrigatório     | int  | 4       | FK para Entidade        | 6       |

## Entidade: Lobo  
#### Descrição: Entidade animal que pode ser domesticada.

| Atributo    | Obrigatoriedade | Tipo | Tamanho | Descrição               | Exemplo |
| ----------- | --------------- | ---- | ------- | ----------------------- | ------- |
| id_entidade | Obrigatório     | int  | 4       | FK para Entidade        | 8       |
| fome        | Obrigatório     | int  | 4       | Nível de fome do lobo   | 12      |




# Versões
| Data       | Versão | Descrição                          | Autor                    | Revisão|
|------------|--------|------------------------------------|--------------------------|----|
| 01/05/2025 | **1.0** | Versão inicial do Dicionário de dados | Yan Guimarães Nathan Vitor Valério João Zarbiélli Karolina Vieira  | Yan Guimarães Nathan Batista Vitor Valério João Zarbiélli Karolina |
