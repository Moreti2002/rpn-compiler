#!/usr/bin/env python3
"""
Teste das Funções de Debug Print
Valida a geração correta das funções print_number, print_newline, print_space
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gerador_assembly_avr import GeradorAssemblyAVR

def test_funcoes_print_existem():
    """Teste 1: Verificar que funções de print são geradas"""
    print("\n=== Teste 1: Funções de print existem ===")
    
    gerador = GeradorAssemblyAVR(debug_print=True)
    assembly = gerador.gerar([])
    
    assert 'print_number:' in assembly, "Função print_number deve existir"
    assert 'print_newline:' in assembly, "Função print_newline deve existir"
    assert 'print_space:' in assembly, "Função print_space deve existir"
    
    print("✅ PASSOU: Todas as funções de print estão presentes\n")

def test_print_number_implementacao():
    """Teste 2: Verificar implementação de print_number"""
    print("\n=== Teste 2: Implementação print_number ===")
    
    gerador = GeradorAssemblyAVR()
    assembly = gerador.gerar([])
    
    # Verificar divisões por 100 e 10
    assert 'div_100:' in assembly, "Deve ter loop para divisão por 100"
    assert 'div_10:' in assembly, "Deve ter loop para divisão por 10"
    
    # Verificar conversão para ASCII
    assert 'subi r16, -48' in assembly, "Deve converter para ASCII (adicionar 48)"
    
    print("✅ PASSOU: print_number implementado corretamente\n")

def test_debug_print_ativo():
    """Teste 3: Verificar que debug_print gera calls"""
    print("\n=== Teste 3: Debug print ativo ===")
    
    from src.otimizador_tac import InstrucaoTAC
    
    gerador = GeradorAssemblyAVR(debug_print=True)
    instr = InstrucaoTAC(tipo='OPERACAO', resultado='t0', 
                        operando1='10', operando2='20', operador='+')
    
    asm = gerador.gerar_operacao(instr)
    asm_str = '\n'.join(asm)
    
    assert 'call print_number' in asm_str, "Deve chamar print_number"
    assert 'call print_space' in asm_str, "Deve chamar print_space"
    
    print(asm_str)
    print("\n✅ PASSOU: Debug print gera calls corretamente\n")

def test_debug_print_inativo():
    """Teste 4: Verificar que sem debug_print não gera calls"""
    print("\n=== Teste 4: Debug print inativo ===")
    
    from src.otimizador_tac import InstrucaoTAC
    
    gerador = GeradorAssemblyAVR(debug_print=False)
    instr = InstrucaoTAC(tipo='OPERACAO', resultado='t0', 
                        operando1='10', operando2='20', operador='+')
    
    asm = gerador.gerar_operacao(instr)
    asm_str = '\n'.join(asm)
    
    assert 'call print_number' not in asm_str, "Não deve chamar print_number"
    assert 'DEBUG' not in asm_str, "Não deve ter comentários DEBUG"
    
    print("✅ PASSOU: Sem debug print, não gera calls\n")

def test_print_newline():
    """Teste 5: Verificar implementação de print_newline"""
    print("\n=== Teste 5: Implementação print_newline ===")
    
    gerador = GeradorAssemblyAVR()
    assembly = gerador.gerar([])
    
    # Verificar CR e LF
    assert 'ldi r16, 13' in assembly, "Deve carregar CR (13)"
    assert 'ldi r16, 10' in assembly, "Deve carregar LF (10)"
    
    print("✅ PASSOU: print_newline implementado (CR+LF)\n")

def main():
    """Executar todos os testes"""
    print("=" * 70)
    print("TESTES DAS FUNÇÕES DE DEBUG PRINT")
    print("=" * 70)
    
    testes = [
        ("Funções de print existem", test_funcoes_print_existem),
        ("Implementação print_number", test_print_number_implementacao),
        ("Debug print ativo", test_debug_print_ativo),
        ("Debug print inativo", test_debug_print_inativo),
        ("Implementação print_newline", test_print_newline),
    ]
    
    passou = 0
    falhou = 0
    
    for nome, teste in testes:
        try:
            teste()
            passou += 1
        except AssertionError as e:
            print(f"❌ FALHOU: {nome}")
            print(f"   Erro: {e}\n")
            falhou += 1
        except Exception as e:
            print(f"❌ ERRO: {nome}")
            print(f"   Exceção: {e}\n")
            falhou += 1
    
    print("=" * 70)
    print(f"RESULTADO: {passou}/{len(testes)} testes passaram")
    if falhou == 0:
        print("✅ TODOS OS TESTES PASSARAM!")
    else:
        print(f"❌ {falhou} teste(s) falharam")
    print("=" * 70)
    
    return falhou == 0

if __name__ == '__main__':
    sucesso = main()
    sys.exit(0 if sucesso else 1)
