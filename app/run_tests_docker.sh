#!/bin/bash
# Script para executar testes em container Docker

set -e

echo "🧪 Executando testes do Minecraft em container Docker"
echo "=================================================="

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para cleanup
cleanup() {
    echo -e "\n${YELLOW}🧹 Limpando containers...${NC}"
    docker-compose -f docker-compose.test.yml down --volumes 2>/dev/null || true
}

# Trap para cleanup em caso de interrupção
trap cleanup EXIT

# Build da imagem de testes
echo -e "${YELLOW}🔨 Construindo imagem de testes...${NC}"
docker-compose -f docker-compose.test.yml build minecraft-tests

# Executar testes
echo -e "${YELLOW}🚀 Executando testes...${NC}"
if docker-compose -f docker-compose.test.yml run --rm minecraft-tests; then
    echo -e "\n${GREEN}✅ Todos os testes passaram!${NC}"
    
    # Copiar artefatos do container
    echo -e "${YELLOW}📦 Copiando artefatos de teste...${NC}"
    
    # Criar diretório local para artefatos se não existir
    mkdir -p ./test-reports
    
    # Copiar artefatos usando docker cp
    CONTAINER_ID=$(docker-compose -f docker-compose.test.yml ps -q minecraft-tests 2>/dev/null | head -1)
    if [ ! -z "$CONTAINER_ID" ]; then
        docker cp $CONTAINER_ID:/app/htmlcov ./test-reports/ 2>/dev/null || echo "htmlcov não encontrado"
        docker cp $CONTAINER_ID:/app/coverage.xml ./test-reports/ 2>/dev/null || echo "coverage.xml não encontrado"
        docker cp $CONTAINER_ID:/app/test-results.xml ./test-reports/ 2>/dev/null || echo "test-results.xml não encontrado"
        docker cp $CONTAINER_ID:/app/.pytest_cache ./test-reports/ 2>/dev/null || echo ".pytest_cache não encontrado"
    fi
    
    echo -e "${GREEN}📊 Artefatos salvos em: ./test-reports/${NC}"
    echo -e "${GREEN}🌐 Relatório HTML: ./test-reports/htmlcov/index.html${NC}"
    
    exit 0
else
    echo -e "\n${RED}❌ Alguns testes falharam!${NC}"
    exit 1
fi
