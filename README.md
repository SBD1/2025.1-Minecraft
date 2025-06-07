# 🟩 2025.1 - Minecraft em Python

Bem-vindo ao projeto **Minecraft Legends**, desenvolvido para a disciplina de Sistemas de Banco de Dados 1 (SBD1) — 2025.1.

Este projeto recria o Minecraft Legends utilizando SQL e Python, com ambiente isolado via Docker para facilitar a execução e portabilidade.

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

## ❌ Como sair

Para sair do terminal interativo:

- Pressione `Ctrl + D`
- Ou digite `exit` e pressione `Enter`

Para parar os containers:

```bash
docker compose down
```


---

## 👥 Contribuindo

Sinta-se à vontade para abrir issues, sugestões ou enviar pull requests!


## ✍️ Créditos

Projeto desenvolvido por alunos da disciplina **SBD1 – 2025.1**.  
Professor: *Mauricio Serrano*  
Instituição: *Universidade de Brasília*

---

## 📄 Licença

Este projeto é licenciado sob a [MIT License](LICENSE).
