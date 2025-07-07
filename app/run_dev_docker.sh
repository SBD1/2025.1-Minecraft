#!/bin/bash
# Script para desenvolvimento com Docker

set -e

echo "🚀 Iniciando ambiente de desenvolvimento Minecraft"
echo "================================================"

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para cleanup
cleanup() {
    echo -e "\n${YELLOW}🛑 Parando containers de desenvolvimento...${NC}"
    docker-compose down
}

# Trap para cleanup em caso de interrupção
trap cleanup EXIT

# Verificar se docker-compose.yml existe
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ docker-compose.yml não encontrado!${NC}"
    echo -e "${YELLOW}💡 Certifique-se de estar no diretório correto${NC}"
    exit 1
fi

# Build e start dos serviços
echo -e "${YELLOW}🔨 Construindo e iniciando containers...${NC}"
docker-compose up --build -d postgres

echo -e "${YELLOW}⏳ Aguardando banco de dados...${NC}"
sleep 5

echo -e "${YELLOW}🚀 Iniciando aplicação...${NC}"
docker-compose up --build minecraft-dev

echo -e "\n${GREEN}✅ Ambiente de desenvolvimento iniciado!${NC}"
echo -e "${GREEN}🔗 Aplicação disponível em: http://localhost:8000${NC}"
echo -e "${GREEN}🗄️  PostgreSQL disponível em: localhost:5432${NC}"
