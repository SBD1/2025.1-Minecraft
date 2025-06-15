#!/bin/bash

# Script para construir a documentação localmente

echo "🔨 Construindo documentação do MINECRAFT - FGA - 2025/1..."

# Verificar se estamos no diretório correto
if [ ! -f "Makefile" ]; then
    echo "❌ Erro: Execute este script do diretório docs/"
    exit 1
fi

# Instalar dependências se necessário
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Limpar build anterior
echo "🧹 Limpando build anterior..."
make clean

# Construir documentação
echo "🏗️  Construindo documentação HTML..."
make html

# Verificar se o build foi bem-sucedido
if [ $? -eq 0 ]; then
    echo "✅ Documentação construída com sucesso!"
    echo "📁 Arquivos gerados em: build/html/"
    echo "🌐 Para visualizar, abra: build/html/index.html"
    
    # Perguntar se quer abrir no navegador
    read -p "🚀 Abrir no navegador? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v xdg-open > /dev/null; then
            xdg-open build/html/index.html
        elif command -v open > /dev/null; then
            open build/html/index.html
        else
            echo "⚠️  Não foi possível abrir automaticamente. Abra manualmente: build/html/index.html"
        fi
    fi
else
    echo "❌ Erro ao construir documentação!"
    exit 1
fi 