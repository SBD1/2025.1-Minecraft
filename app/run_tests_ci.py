#!/usr/bin/env python3
"""
Script para executar testes no ambiente CI/CD
Garante que todos os artefatos necessários sejam gerados
"""
import subprocess
import sys
import os
from pathlib import Path

def ensure_directories():
    """Garante que os diretórios necessários existem"""
    directories = [
        ".pytest_cache",
        "htmlcov"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Diretório {directory} garantido")

def run_tests_with_coverage():
    """Executa os testes com cobertura completa para CI/CD"""
    print("Executando testes para CI/CD")
    print("=" * 60)
    
    # Garantir que os diretórios existem
    ensure_directories()
    
    # Comando para executar os testes com todos os relatórios
    cmd = [
        sys.executable, "-m", "pytest",
        "--tb=short",
        "--verbose",
        "--strict-markers",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "--cov-report=xml:coverage.xml",
        "--cov-fail-under=30",
        "--junitxml=test-results.xml",
        "tests/"
    ]
    
    print(f"Executando comando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
        
        # Verificar se os arquivos foram gerados
        artifacts = [
            "coverage.xml",
            "test-results.xml",
            "htmlcov/index.html",
            ".pytest_cache"
        ]
        
        print("\nVerificando artefatos gerados:")
        all_artifacts_exist = True
        
        for artifact in artifacts:
            if os.path.exists(artifact):
                print(f"{artifact}")
            else:
                print(f"{artifact}")
                all_artifacts_exist = False
        
        if result.returncode == 0:
            print("\nTodos os testes passaram!")
            if all_artifacts_exist:
                print("Todos os artefatos foram gerados com sucesso!")
            else:
                print("Alguns artefatos não foram gerados")
        else:
            print("\nAlguns testes falharam!")
            
        return result.returncode
        
    except Exception as e:
        print(f"Erro ao executar testes: {e}")
        return 1

def generate_coverage_summary():
    """Gera um resumo da cobertura"""
    try:
        # Executar apenas o relatório de cobertura
        cmd = [
            sys.executable, "-m", "pytest",
            "--cov=src",
            "--cov-report=term",
            "--quiet",
            "--collect-only"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        print("Resumo de Cobertura:")
        print(result.stdout)
        
    except Exception as e:
        print(f"Não foi possível gerar resumo de cobertura: {e}")

if __name__ == "__main__":
    print("🎯 Script de testes para CI/CD - Minecraft Project")
    print("=" * 60)
    
    exit_code = run_tests_with_coverage()
    
    if exit_code == 0:
        generate_coverage_summary()
    
    print(f"\nProcesso finalizado com código: {exit_code}")
    sys.exit(exit_code)
