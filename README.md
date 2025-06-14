# 🟩 2025.1 - Minecraft em Python

Bem-vindo ao projeto **Minecraft Legends**, desenvolvido para a disciplina de Sistemas de Banco de Dados 1 (SBD1) — 2025.1.

Este projeto recria o Minecraft Legends utilizando SQL e Python, com ambiente isolado via Docker para facilitar a execução e portabilidade.

---

## 📚 Documentação

📖 **Documentação Completa**: [https://sbd1.github.io/2025.1-Minecraft/](https://sbd1.github.io/2025.1-Minecraft/)

A documentação inclui:
- 📋 Guias de instalação e início rápido
- 🎮 Guia completo do usuário
- 🔧 Referência da API e desenvolvimento
- 🗄️ Estrutura do banco de dados
- 🤝 Guia de contribuição

---

## 📸 Preview

> *(Adicione aqui um gif ou screenshot do jogo rodando, se desejar)*

---

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de ter os seguintes softwares instalados na sua máquina:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Como rodar o jogo

### 1. Clone e acesse este repositório em seu ambiente local

```bash
git clone https://github.com/SBD1/2025.1-Minecraft.git

cd 2025.1-Minecraft
```

### 2. Construa e suba os containers com Docker

```bash
docker compose up -d --build
```

### 3. Acesse o container interativamente

```bash
docker exec -it python_mine bash
```

### 4. Execute o jogo

```bash
python main.py
```

---

## 📖 Documentação Local

Para construir a documentação localmente:

```bash
# Instalar dependências
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

## ❌ Como sair

Para sair do terminal interativo:

- Pressione `Ctrl + D`
- Ou digite `exit` e pressione `Enter`

Para parar os containers:

```bash
docker compose down
```

---

## 🛠️ Desenvolvimento

### Estrutura do Projeto

```
2025.1-Minecraft/
├── app/                    # Aplicação principal
│   ├── main.py            # Ponto de entrada
│   └── src/               # Código fonte
│       ├── interface/     # Interface do usuário
│       └── utils/         # Utilitários
├── db/                    # Banco de dados
├── docs/                  # Documentação
└── docker-compose.yml     # Orquestração
```

### Contribuindo

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'feat: add nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

Para mais detalhes, consulte o [Guia de Contribuição](https://sbd1.github.io/2025.1-Minecraft/contributing.html).

---

## 👥 Contribuindo

Sinta-se à vontade para abrir issues, sugestões ou enviar pull requests!

Para contribuir, consulte nossa [documentação completa](https://sbd1.github.io/2025.1-Minecraft/contributing.html).

---

## ✍️ Créditos

Projeto desenvolvido por alunos da disciplina **SBD1 – 2025.1**.  
Professor: *Mauricio Serrano*  
Instituição: *Universidade de Brasília*

---

## 📄 Licença

Este projeto é licenciado sob a [MIT License](LICENSE).
