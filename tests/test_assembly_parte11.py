#!/usr/bin/env python3
"""
Teste da Parte 11: Acesso à SRAM para variáveis nomeadas (A-Z)

Objetivo:
- Verificar que variáveis A-Z são salvas na SRAM com sts
- Verificar que variáveis A-Z são carregadas da SRAM com lds
- Verificar endereços corretos (0x0120 para A, 0x0121 para B, etc.)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gerador_assembly_avr import GeradorAssemblyAVR
from src.otimizador_tac import InstrucaoTAC

def test_atribuicao_variavel_nomeada():
    """Teste 1: X = 10 deve gerar sts para salvar X na SRAM"""
    print("\n=== Teste 1: Atribuição de constante a variável nomeada ===")
    
    gerador = GeradorAssemblyAVR()
    instr = InstrucaoTAC(tipo='ATRIBUICAO', resultado='X', operando1='10')
    
    asm = gerador.gerar_atribuicao(instr)
    asm_str = '\n'.join(asm)
    
    print(asm_str)
    
    # Verificar que contém sts
    assert 'sts' in asm_str, "Deve conter instrução sts"
    # Verificar endereço de X (0x0137 = 0x0120 + 23)
    assert '0x0137' in asm_str, "Deve salvar X no endereço 0x0137"
    # Verificar que carrega constante 10
    assert 'ldi' in asm_str and '10' in asm_str, "Deve carregar constante 10"
    
    print(" PASSOU: Variável X salva corretamente na SRAM\n")

def test_copia_entre_variaveis():
    """Teste 2: Y = X deve carregar X da SRAM e salvar Y na SRAM"""
    print("\n=== Teste 2: Cópia entre variáveis nomeadas ===")
    
    gerador = GeradorAssemblyAVR()
    # Alocar X primeiro
    gerador.alocar_registrador('X')
    
    instr = InstrucaoTAC(tipo='COPIA', resultado='Y', operando1='X')
    
    asm = gerador.gerar_copia(instr)
    asm_str = '\n'.join(asm)
    
    print(asm_str)
    
    # Verificar que contém sts para Y
    assert 'sts' in asm_str, "Deve conter instrução sts para Y"
    # Verificar endereço de Y (0x0138 = 0x0120 + 24)
    assert '0x0138' in asm_str, "Deve salvar Y no endereço 0x0138"
    
    print(" PASSOU: Y = X com acesso à SRAM\n")

def test_operacao_com_variaveis():
    """Teste 3: Z = X + Y deve carregar X e Y da SRAM"""
    print("\n=== Teste 3: Operação com variáveis nomeadas ===")
    
    gerador = GeradorAssemblyAVR()
    instr = InstrucaoTAC(tipo='OPERACAO', resultado='Z', 
                        operando1='X', operando2='Y', operador='+')
    
    asm = gerador.gerar_operacao(instr)
    asm_str = '\n'.join(asm)
    
    print(asm_str)
    
    # Verificar que carrega X (0x0137)
    assert 'lds' in asm_str, "Deve conter instrução lds para carregar variáveis"
    assert '0x0137' in asm_str, "Deve carregar X de 0x0137"
    # Verificar que carrega Y (0x0138)
    assert '0x0138' in asm_str, "Deve carregar Y de 0x0138"
    # Verificar que salva Z (0x0139)
    assert 'sts' in asm_str, "Deve salvar Z com sts"
    assert '0x0139' in asm_str, "Deve salvar Z em 0x0139"
    # Verificar operação add
    assert 'add' in asm_str, "Deve conter instrução add"
    
    print(" PASSOU: Z = X + Y com acesso à SRAM\n")

def test_enderecos_corretos():
    """Teste 4: Verificar cálculo de endereços para múltiplas variáveis"""
    print("\n=== Teste 4: Endereços SRAM corretos ===")
    
    gerador = GeradorAssemblyAVR()
    
    # Testar endereços de A a Z
    casos = [
        ('A', 0x0120),
        ('B', 0x0121),
        ('X', 0x0137),  # X = 23ª letra
        ('Y', 0x0138),  # Y = 24ª letra
        ('Z', 0x0139),  # Z = 25ª letra
    ]
    
    for var, end_esperado in casos:
        end_calculado = gerador.calcular_endereco_variavel(var)
        print(f"{var}: 0x{end_calculado:04X} (esperado: 0x{end_esperado:04X})")
        assert end_calculado == end_esperado, f"Endereço incorreto para {var}"
    
    print(" PASSOU: Todos os endereços corretos\n")

def test_temporarios_vs_nomeadas():
    """Teste 5: Temporários (t0-t31) não devem usar SRAM"""
    print("\n=== Teste 5: Temporários vs Variáveis Nomeadas ===")
    
    gerador = GeradorAssemblyAVR()
    
    # Teste com temporário
    instr_temp = InstrucaoTAC(tipo='ATRIBUICAO', resultado='t0', operando1='42')
    asm_temp = gerador.gerar_atribuicao(instr_temp)
    asm_temp_str = '\n'.join(asm_temp)
    
    print("Temporário t0 = 42:")
    print(asm_temp_str)
    
    # Temporário NÃO deve usar sts
    assert 'sts' not in asm_temp_str, "Temporário não deve usar sts"
    assert 'ldi' in asm_temp_str, "Temporário deve usar ldi para registrador"
    
    # Teste com variável nomeada
    gerador2 = GeradorAssemblyAVR()
    instr_named = InstrucaoTAC(tipo='ATRIBUICAO', resultado='W', operando1='42')
    asm_named = gerador2.gerar_atribuicao(instr_named)
    asm_named_str = '\n'.join(asm_named)
    
    print("\nVariável nomeada W = 42:")
    print(asm_named_str)
    
    # Variável nomeada DEVE usar sts
    assert 'sts' in asm_named_str, "Variável nomeada deve usar sts"
    
    print(" PASSOU: Temporários em registradores, variáveis nomeadas na SRAM\n")

def test_operacao_mista():
    """Teste 6: Operação com variável nomeada + constante"""
    print("\n=== Teste 6: Operação mista (variável + constante) ===")
    
    gerador = GeradorAssemblyAVR()
    instr = InstrucaoTAC(tipo='OPERACAO', resultado='W', 
                        operando1='Z', operando2='5', operador='+')
    
    asm = gerador.gerar_operacao(instr)
    asm_str = '\n'.join(asm)
    
    print(asm_str)
    
    # Verificar que carrega Z da SRAM
    assert 'lds' in asm_str and '0x0139' in asm_str, "Deve carregar Z da SRAM"
    # Verificar que carrega constante 5
    assert 'ldi' in asm_str and '5' in asm_str, "Deve carregar constante 5"
    # Verificar que salva W na SRAM
    assert 'sts' in asm_str and '0x0136' in asm_str, "Deve salvar W na SRAM"
    
    print(" PASSOU: Operação mista funcionando\n")

def main():
    """Executar todos os testes da Parte 11"""
    print("=" * 70)
    print("TESTES DA PARTE 11: ACESSO À SRAM")
    print("=" * 70)
    
    testes = [
        ("Atribuição constante → variável", test_atribuicao_variavel_nomeada),
        ("Cópia entre variáveis", test_copia_entre_variaveis),
        ("Operação com variáveis", test_operacao_com_variaveis),
        ("Endereços SRAM corretos", test_enderecos_corretos),
        ("Temporários vs Nomeadas", test_temporarios_vs_nomeadas),
        ("Operação mista", test_operacao_mista),
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
