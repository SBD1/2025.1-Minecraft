#!/usr/bin/env python3
"""
Script para executar os testes do projeto
"""
import subprocess
import sys
import os

def run_tests():
    """Executa os testes com pytest"""
    print("🧪 Executando testes do Minecraft")
    print("=" * 50)
    
    # Comando para executar os testes
    cmd = [
        sys.executable, "-m", "pytest",
        "--tb=short",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "-v"
    ]
    
    try:
        result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print("\n✅ Todos os testes passaram!")
            print("📊 Relatório de cobertura gerado em: htmlcov/index.html")
        else:
            print("\n❌ Alguns testes falharam!")
            
        return result.returncode
        
    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")
        return 1

def run_specific_test(test_file=None, test_class=None, test_method=None):
    """Executa um teste específico"""
    cmd = [sys.executable, "-m", "pytest", "-v"]
    
    if test_file:
        cmd.append(f"tests/{test_file}")
    if test_class:
        cmd.append(f"-k {test_class}")
    if test_method:
        cmd.append(f"-k {test_method}")
    
    try:
        result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
        return result.returncode
    except Exception as e:
        print(f"❌ Erro ao executar teste específico: {e}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Executa teste específico
        if sys.argv[1] == "--file" and len(sys.argv) > 2:
            exit_code = run_specific_test(test_file=sys.argv[2])
        elif sys.argv[1] == "--class" and len(sys.argv) > 2:
            exit_code = run_specific_test(test_class=sys.argv[2])
        elif sys.argv[1] == "--method" and len(sys.argv) > 2:
            exit_code = run_specific_test(test_method=sys.argv[2])
        else:
            print("Uso: python run_tests.py [--file <arquivo> | --class <classe> | --method <metodo>]")
            exit_code = 1
    else:
        # Executa todos os testes
        exit_code = run_tests()
    
    sys.exit(exit_code) 