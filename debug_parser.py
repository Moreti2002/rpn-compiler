#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/darkdogg762/documents/codes/rpn-compiler')

from src.lexer import parse_expressao as tokenizar
from src.parser import parsear
from src.grammar import construir_gramatica
import json

expr = '(A B == (100 RESULT) (200 RESULT) IF)'
tokens = tokenizar(expr)
gram = construir_gramatica()
resultado = parsear(tokens, gram['tabela'])

print("=== DERIVAÇÃO ===")
print(json.dumps(resultado['derivacao'], indent=2))
