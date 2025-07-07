#!/bin/bash

# Script para reinicializar o banco de dados do Minecraft
# Este script para e remove os containers existentes, remove os volumes
# e reinicia o banco com a estrutura organizada

echo "🎮 Reinicializando banco de dados do Minecraft..."

# Para e remove containers existentes
echo "📦 Parando containers existentes..."
docker-compose down -v

# Remove volumes para limpeza completa
echo "🧹 Removendo volumes..."
docker volume prune -f

# Reconstrói e inicia os containers
echo "🔧 Reconstruindo containers..."
docker-compose up --build -d

echo "⏳ Aguardando inicialização do banco..."
sleep 10

# Verifica se o banco está rodando
echo "🔍 Verificando status do banco..."
docker-compose ps

echo "✅ Banco de dados inicializado com sucesso!"
echo "📊 Estrutura organizada em fases:"
echo "   - Fase 1: Criação de usuários"
echo "   - Fase 2: Criação de schemas (tabelas e índices)"
echo "   - Fase 3: Inserção de dados"
echo ""
echo "🔗 Para conectar ao banco:"
echo "   Host: localhost"
echo "   Port: 5433"
echo "   Database: 2025_1_Minecraft"
echo "   User: postgres"
echo "   Password: password"
echo ""
echo "📋 Para verificar logs:"
echo "   docker-compose logs db"
