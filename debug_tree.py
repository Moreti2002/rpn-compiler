#!/usr/bin/env python3
"""Script para debug - mostra árvore completa"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.lexer import parse_expressao as tokenizar
from src.parser import parsear
from src.grammar import construir_gramatica
from src.syntax_tree import converter_derivacao_para_arvore
from src.arvore_atribuida import gerar_arvore_atribuida

def mostrar_arvore(no, nivel=0):
    """Mostra árvore de forma hierárquica"""
    indent = "  " * nivel
    tipo = no.get('tipo', '?')
    valor = no.get('valor', '')
    
    if valor:
        print(f"{indent}{tipo}: {valor}")
    else:
        print(f"{indent}{tipo}")
    
    # Mostrar atributos especiais
    if 'expressoes' in no:
        print(f"{indent}  [expressoes: {len(no['expressoes'])} itens]")
        for i, expr in enumerate(no['expressoes']):
            print(f"{indent}  [{i}]:")
            mostrar_arvore(expr, nivel + 2)
    
    # Mostrar filhos
    filhos = no.get('filhos', [])
    for filho in filhos:
        mostrar_arvore(filho, nivel + 1)

def main():
    arquivo = sys.argv[1] if len(sys.argv) > 1 else 'examples/test_while_composto.txt'
    
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    
    expressoes = [l.strip() for l in linhas if l.strip() and not l.strip().startswith('#')]
    
    gramatica = construir_gramatica()
    
    print(f"Analisando expressão 3: {expressoes[2]}\n")
    
    expressao = expressoes[2]
    tokens = tokenizar(expressao)
    resultado_parser = parsear(tokens, gramatica['tabela'])
    derivacao = resultado_parser['derivacao']
    
    print("ÁRVORE SINTÁTICA:")
    print("=" * 80)
    arvore = converter_derivacao_para_arvore(derivacao)
    mostrar_arvore(arvore)
    
    print("\n" + "=" * 80)
    print("ÁRVORE ATRIBUÍDA:")
    print("=" * 80)
    arvore_atribuida = gerar_arvore_atribuida(arvore)
    mostrar_arvore(arvore_atribuida)

if __name__ == '__main__':
    main()
