#!/usr/bin/env python3
"""
Teste do Otimizador TAC
=======================

Testa as otimizações implementadas:
- Constant Folding
- Constant Propagation
- Dead Code Elimination

Usage:
    python3 test_otimizador.py
"""

import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).parent))

from src.otimizador_tac import OtimizadorTAC, InstrucaoTAC, imprimir_comparacao


def criar_teste_constant_folding():
    """Teste de Constant Folding"""
    instrucoes = [
        InstrucaoTAC('ATRIBUICAO', 't0', '2'),
        InstrucaoTAC('ATRIBUICAO', 't1', '3'),
        InstrucaoTAC('OPERACAO', 't2', 't0', '+', 't1'),  # Deve virar: t2 = 5
        InstrucaoTAC('ATRIBUICAO', 't3', '10'),
        InstrucaoTAC('ATRIBUICAO', 't4', '4'),
        InstrucaoTAC('OPERACAO', 't5', 't3', '-', 't4'),  # Deve virar: t5 = 6
        InstrucaoTAC('OPERACAO', 't6', '7', '*', '8'),    # Deve virar: t6 = 56
    ]
    return instrucoes


def criar_teste_constant_propagation():
    """Teste de Constant Propagation"""
    instrucoes = [
        InstrucaoTAC('ATRIBUICAO', 't0', '5'),
        InstrucaoTAC('OPERACAO', 't1', 't0', '+', '3'),   # Propaga t0=5 → t1 = 8
        InstrucaoTAC('ATRIBUICAO', 't2', '10'),
        InstrucaoTAC('OPERACAO', 't3', 't2', '*', '2'),   # Propaga t2=10 → t3 = 20
        InstrucaoTAC('OPERACAO', 't4', 't0', '+', 't2'),  # Propaga ambos → t4 = 15
    ]
    return instrucoes


def criar_teste_dead_code():
    """Teste de Dead Code Elimination"""
    instrucoes = [
        InstrucaoTAC('ATRIBUICAO', 't0', '5'),
        InstrucaoTAC('ATRIBUICAO', 't1', '3'),            # Nunca usado - deve ser removido
        InstrucaoTAC('OPERACAO', 't2', 't0', '+', '2'),
        InstrucaoTAC('ATRIBUICAO', 't3', '10'),           # Nunca usado - deve ser removido
        InstrucaoTAC('COPIA', 'X', 't2'),                 # Usa t2, resultado final
    ]
    return instrucoes


def criar_teste_completo():
    """Teste com todas as otimizações"""
    instrucoes = [
        # Operações com constantes
        InstrucaoTAC('ATRIBUICAO', 't0', '2'),
        InstrucaoTAC('ATRIBUICAO', 't1', '3'),
        InstrucaoTAC('OPERACAO', 't2', 't0', '+', 't1'),  # Folding: t2 = 5
        
        # Propagação
        InstrucaoTAC('OPERACAO', 't3', 't2', '*', '2'),   # Propagação: t3 = 10
        
        # Dead code
        InstrucaoTAC('ATRIBUICAO', 't4', '100'),          # Nunca usado
        InstrucaoTAC('ATRIBUICAO', 't5', '200'),          # Nunca usado
        
        # Resultado final
        InstrucaoTAC('COPIA', 'RESULTADO', 't3'),
    ]
    return instrucoes


def criar_teste_estruturas_controle():
    """Teste com IF e WHILE"""
    instrucoes = [
        # Comparação com constantes
        InstrucaoTAC('ATRIBUICAO', 't0', '10'),
        InstrucaoTAC('ATRIBUICAO', 't1', '5'),
        InstrucaoTAC('OPERACAO', 't2', 't0', '>', 't1'),  # Folding: t2 = 1
        
        # IF structure
        InstrucaoTAC('IF_FALSE', 'L0', 't2'),
        InstrucaoTAC('ATRIBUICAO', 't3', '100'),
        InstrucaoTAC('COPIA', 'X', 't3'),
        InstrucaoTAC('GOTO', 'L1'),
        
        InstrucaoTAC('ROTULO', 'L0'),
        InstrucaoTAC('ATRIBUICAO', 't4', '0'),
        InstrucaoTAC('COPIA', 'X', 't4'),
        
        InstrucaoTAC('ROTULO', 'L1'),
    ]
    return instrucoes


def executar_teste(nome: str, instrucoes: List[InstrucaoTAC], nivel: str = 'completo'):
    """Executa um teste de otimização"""
    print("\n" + "=" * 80)
    print(f"TESTE: {nome}")
    print("=" * 80)
    
    otimizador = OtimizadorTAC()
    otimizado = otimizador.otimizar(instrucoes, nivel)
    
    imprimir_comparacao(instrucoes, otimizado)
    
    # Estatísticas
    stats = otimizador.obter_estatisticas()
    print("ESTATÍSTICAS DE OTIMIZAÇÃO:")
    print(f"  • Constant Folding: {stats['constant_folding']} otimizações")
    print(f"  • Constant Propagation: {stats['constant_propagation']} substituições")
    print(f"  • Dead Code Elimination: {stats['dead_code_elimination']} instruções removidas")
    print()


def main():
    """Função principal"""
    print("=" * 80)
    print("TESTE DO OTIMIZADOR TAC")
    print("=" * 80)
    
    # Teste 1: Constant Folding
    executar_teste(
        "Constant Folding (Parte 5)",
        criar_teste_constant_folding(),
        nivel='folding'
    )
    
    # Teste 2: Constant Propagation
    executar_teste(
        "Constant Propagation (Parte 6)",
        criar_teste_constant_propagation(),
        nivel='propagation'
    )
    
    # Teste 3: Dead Code Elimination
    executar_teste(
        "Dead Code Elimination (Parte 7)",
        criar_teste_dead_code(),
        nivel='dead_code'
    )
    
    # Teste 4: Otimização Completa
    executar_teste(
        "Otimização Completa (Partes 5+6+7)",
        criar_teste_completo(),
        nivel='completo'
    )
    
    # Teste 5: Estruturas de Controle
    executar_teste(
        "Estruturas de Controle com Otimização",
        criar_teste_estruturas_controle(),
        nivel='completo'
    )
    
    print("=" * 80)
    print(" Todos os testes concluídos!")
    print("=" * 80)


if __name__ == '__main__':
    main()
