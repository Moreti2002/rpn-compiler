#!/usr/bin/env python3
"""Debug: mostrar tipos de instruções TAC"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.lexer import parse_expressao as tokenizar
from src.parser import parsear
from src.grammar import construir_gramatica
from src.syntax_tree import converter_derivacao_para_arvore
from src.arvore_atribuida import gerar_arvore_atribuida
from src.gerador_tac import GeradorTAC

arquivo = 'examples/test_while_composto.txt'

with open(arquivo, 'r') as f:
    linhas = f.readlines()

expressoes = [l.strip() for l in linhas if l.strip() and not l.strip().startswith('#')]

gramatica = construir_gramatica()
gerador_tac = GeradorTAC()

for expressao in expressoes:
    tokens = tokenizar(expressao)
    resultado_parser = parsear(tokens, gramatica['tabela'])
    derivacao = resultado_parser['derivacao']
    arvore = converter_derivacao_para_arvore(derivacao)
    arvore_atribuida = gerar_arvore_atribuida(arvore)
    resultado = gerador_tac.processar_no(arvore_atribuida)
    gerador_tac.historico_resultados.append(resultado)

print("=" * 80)
print("INSTRUÇÕES TAC COM TIPOS:")
print("=" * 80)
for i, instr in enumerate(gerador_tac.instrucoes, 1):
    print(f"{i:3d}. [{instr.tipo:15s}] {instr}")
