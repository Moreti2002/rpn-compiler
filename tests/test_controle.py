#!/usr/bin/env python3
"""
Testes da Parte 12: Estruturas de Controle
Valida IF/ELSE e WHILE
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gerador_assembly_avr import GeradorAssemblyAVR
from src.otimizador_tac import InstrucaoTAC

def test_comparacao_igual():
    """Teste 1: Comparação == gera breq"""
    print("\n=== Teste 1: Comparação == ===")
    
    gerador = GeradorAssemblyAVR()
    instr = InstrucaoTAC(tipo='OPERACAO', resultado='t0',
                        operando1='10', operando2='10', operador='==')
    
    asm = gerador.gerar_operacao(instr)
    asm_str = '\n'.join(asm)
    
    print(asm_str)
    
    assert 'cp r' in asm_str, "Deve usar instrução cp"
    assert 'breq' in asm_str, "Deve usar breq para =="
    assert 'ldi r' in asm_str and '1' in asm_str, "Deve carregar 1 (verdadeiro)"
    assert 'ldi r' in asm_str and '0' in asm_str, "Deve carregar 0 (falso)"
    
    print(" PASSOU: Comparação == implementada\n")

def test_comparacao_diferente():
    """Teste 2: Comparação != gera brne"""
    print("\n=== Teste 2: Comparação != ===")
    
    gerador = GeradorAssemblyAVR()
    instr = InstrucaoTAC(tipo='OPERACAO', resultado='t0',
                        operando1='5', operando2='10', operador='!=')
    
    asm = gerador.gerar_operacao(instr)
    asm_str = '\n'.join(asm)
    
    print(asm_str)
    
    assert 'brne' in asm_str, "Deve usar brne para !="
    assert 'cmp_true' in asm_str or 'cmp_end' in asm_str, "Deve ter labels"
    
    print(" PASSOU: Comparação != implementada\n")

def test_comparacao_menor():
    """Teste 3: Comparação < gera brlo"""
    print("\n=== Teste 3: Comparação < ===")
    
    gerador = GeradorAssemblyAVR()
    instr = InstrucaoTAC(tipo='OPERACAO', resultado='t0',
                        operando1='5', operando2='10', operador='<')
    
    asm = gerador.gerar_operacao(instr)
    asm_str = '\n'.join(asm)
    
    print(asm_str)
    
    assert 'brlo' in asm_str, "Deve usar brlo para <"
    
    print(" PASSOU: Comparação < implementada\n")

def test_comparacao_maior():
    """Teste 4: Comparação > """
    print("\n=== Teste 4: Comparação > ===")
    
    gerador = GeradorAssemblyAVR()
    instr = InstrucaoTAC(tipo='OPERACAO', resultado='t0',
                        operando1='15', operando2='10', operador='>')
    
    asm = gerador.gerar_operacao(instr)
    asm_str = '\n'.join(asm)
    
    print(asm_str)
    
    assert 'cp r' in asm_str, "Deve usar cp"
    # > é implementado como NOT(<= ), então pode usar brlo e breq
    assert 'brlo' in asm_str or 'breq' in asm_str, "Deve ter branches"
    
    print(" PASSOU: Comparação > implementada\n")

def test_rotulo():
    """Teste 5: Geração de rótulos"""
    print("\n=== Teste 5: Rótulos ===")
    
    gerador = GeradorAssemblyAVR()
    instr = InstrucaoTAC(tipo='ROTULO', resultado='L0')
    
    asm = gerador.gerar_rotulo(instr)
    asm_str = '\n'.join(asm)
    
    print(asm_str)
    
    assert 'L0:' in asm_str, "Deve gerar label L0:"
    
    print(" PASSOU: Rótulos funcionando\n")

def test_goto():
    """Teste 6: Salto incondicional"""
    print("\n=== Teste 6: Goto ===")
    
    gerador = GeradorAssemblyAVR()
    instr = InstrucaoTAC(tipo='GOTO', resultado='L1')
    
    asm = gerador.gerar_goto(instr)
    asm_str = '\n'.join(asm)
    
    print(asm_str)
    
    assert 'rjmp L1' in asm_str, "Deve gerar rjmp L1"
    
    print(" PASSOU: Goto funcionando\n")

def test_if_false():
    """Teste 7: Salto condicional (ifFalse)"""
    print("\n=== Teste 7: ifFalse ===")
    
    gerador = GeradorAssemblyAVR()
    # Alocar registrador para t0
    gerador.alocar_registrador('t0')
    
    instr = InstrucaoTAC(tipo='IF_FALSE', operando1='t0', resultado='L2')
    
    asm = gerador.gerar_if_false(instr)
    asm_str = '\n'.join(asm)
    
    print(asm_str)
    
    assert 'tst r' in asm_str, "Deve testar registrador"
    assert 'breq L2' in asm_str, "Deve saltar se zero (falso)"
    
    print(" PASSOU: ifFalse funcionando\n")

def main():
    """Executar todos os testes"""
    print("=" * 70)
    print("TESTES DA PARTE 12: ESTRUTURAS DE CONTROLE")
    print("=" * 70)
    
    testes = [
        ("Comparação ==", test_comparacao_igual),
        ("Comparação !=", test_comparacao_diferente),
        ("Comparação <", test_comparacao_menor),
        ("Comparação >", test_comparacao_maior),
        ("Rótulos", test_rotulo),
        ("Goto", test_goto),
        ("ifFalse", test_if_false),
    ]
    
    passou = 0
    falhou = 0
    
    for nome, teste in testes:
        try:
            teste()
            passou += 1
        except AssertionError as e:
            print(f" FALHOU: {nome}")
            print(f"   Erro: {e}\n")
            falhou += 1
        except Exception as e:
            print(f" ERRO: {nome}")
            print(f"   Exceção: {e}\n")
            falhou += 1
    
    print("=" * 70)
    print(f"RESULTADO: {passou}/{len(testes)} testes passaram")
    if falhou == 0:
        print(" TODOS OS TESTES PASSARAM!")
    else:
        print(f" {falhou} teste(s) falharam")
    print("=" * 70)
    
    return falhou == 0

if __name__ == '__main__':
    sucesso = main()
    sys.exit(0 if sucesso else 1)
