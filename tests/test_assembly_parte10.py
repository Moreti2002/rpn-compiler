#!/usr/bin/env python3
"""
Teste do Gerador de Assembly AVR - Parte 10
============================================

Testa o mapeamento de operações TAC para Assembly AVR.
Valida operações aritméticas básicas.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.gerador_assembly_avr import GeradorAssemblyAVR
from src.otimizador_tac import InstrucaoTAC


def teste_atribuicao_constante():
    """Teste 1: Atribuição de constante"""
    print("Teste 1: Atribuição de constante (t0 = 5)")
    print("-" * 60)
    
    gerador = GeradorAssemblyAVR()
    instrucoes = [
        InstrucaoTAC('ATRIBUICAO', 't0', '5')
    ]
    
    codigo = gerador.gerar(instrucoes)
    
    # Verificar se contém ldi
    assert 'ldi r16, 5' in codigo, "Instrução ldi não encontrada"
    assert 't0 = 5' in codigo, "Comentário não encontrado"
    
    print("✓ Código gerado contém: ldi r16, 5")
    print()


def teste_adicao_simples():
    """Teste 2: Adição simples"""
    print("Teste 2: Adição simples (t2 = t0 + t1)")
    print("-" * 60)
    
    gerador = GeradorAssemblyAVR()
    instrucoes = [
        InstrucaoTAC('ATRIBUICAO', 't0', '3'),
        InstrucaoTAC('ATRIBUICAO', 't1', '5'),
        InstrucaoTAC('OPERACAO', 't2', 't0', '+', 't1')
    ]
    
    codigo = gerador.gerar(instrucoes)
    
    # Verificar instruções
    assert 'ldi r16, 3' in codigo, "Primeira atribuição não encontrada"
    assert 'ldi r17, 5' in codigo, "Segunda atribuição não encontrada"
    assert 'add r18' in codigo, "Instrução add não encontrada"
    
    print("✓ Código contém:")
    print("  - ldi r16, 3")
    print("  - ldi r17, 5")
    print("  - add r18, ...")
    print()


def teste_subtracao():
    """Teste 3: Subtração"""
    print("Teste 3: Subtração (t1 = t0 - 2)")
    print("-" * 60)
    
    gerador = GeradorAssemblyAVR()
    instrucoes = [
        InstrucaoTAC('ATRIBUICAO', 't0', '10'),
        InstrucaoTAC('OPERACAO', 't1', 't0', '-', '2')
    ]
    
    codigo = gerador.gerar(instrucoes)
    
    assert 'ldi r16, 10' in codigo
    assert 'sub r17' in codigo
    
    print("✓ Código contém:")
    print("  - ldi r16, 10")
    print("  - sub r17, ...")
    print()


def teste_multiplicacao():
    """Teste 4: Multiplicação"""
    print("Teste 4: Multiplicação (t1 = t0 * 3)")
    print("-" * 60)
    
    gerador = GeradorAssemblyAVR()
    instrucoes = [
        InstrucaoTAC('ATRIBUICAO', 't0', '7'),
        InstrucaoTAC('OPERACAO', 't1', 't0', '*', '3')
    ]
    
    codigo = gerador.gerar(instrucoes)
    
    assert 'ldi r16, 7' in codigo
    assert 'mul r17' in codigo
    
    print("✓ Código contém:")
    print("  - ldi r16, 7")
    print("  - mul r17, ...")
    print()


def teste_copia():
    """Teste 5: Cópia de variável"""
    print("Teste 5: Cópia (X = t0)")
    print("-" * 60)
    
    gerador = GeradorAssemblyAVR()
    instrucoes = [
        InstrucaoTAC('ATRIBUICAO', 't0', '42'),
        InstrucaoTAC('COPIA', 'X', 't0')
    ]
    
    codigo = gerador.gerar(instrucoes)
    
    assert 'ldi r16, 42' in codigo
    assert 'mov r17, r16' in codigo
    
    print("✓ Código contém:")
    print("  - ldi r16, 42")
    print("  - mov r17, r16")
    print()


def teste_rotulo_e_goto():
    """Teste 6: Rótulo e goto"""
    print("Teste 6: Rótulo e salto (goto L0)")
    print("-" * 60)
    
    gerador = GeradorAssemblyAVR()
    instrucoes = [
        InstrucaoTAC('ATRIBUICAO', 't0', '1'),
        InstrucaoTAC('GOTO', 'L0'),
        InstrucaoTAC('ATRIBUICAO', 't1', '2'),
        InstrucaoTAC('ROTULO', 'L0'),
        InstrucaoTAC('ATRIBUICAO', 't2', '3')
    ]
    
    codigo = gerador.gerar(instrucoes)
    
    assert 'L0:' in codigo
    assert 'rjmp L0' in codigo
    
    print("✓ Código contém:")
    print("  - rjmp L0")
    print("  - L0:")
    print()


def teste_condicional():
    """Teste 7: Salto condicional"""
    print("Teste 7: Salto condicional (ifFalse t0 goto L1)")
    print("-" * 60)
    
    gerador = GeradorAssemblyAVR()
    instrucoes = [
        InstrucaoTAC('ATRIBUICAO', 't0', '0'),
        InstrucaoTAC('IF_FALSE', 'L1', 't0'),
        InstrucaoTAC('ATRIBUICAO', 't1', '100'),
        InstrucaoTAC('ROTULO', 'L1'),
        InstrucaoTAC('ATRIBUICAO', 't2', '200')
    ]
    
    codigo = gerador.gerar(instrucoes)
    
    assert 'tst r16' in codigo
    assert 'breq L1' in codigo
    assert 'L1:' in codigo
    
    print("✓ Código contém:")
    print("  - tst r16")
    print("  - breq L1")
    print("  - L1:")
    print()


def teste_expressao_complexa():
    """Teste 8: Expressão complexa"""
    print("Teste 8: Expressão complexa ((2+3)*4)")
    print("-" * 60)
    
    gerador = GeradorAssemblyAVR()
    instrucoes = [
        InstrucaoTAC('ATRIBUICAO', 't0', '2'),
        InstrucaoTAC('ATRIBUICAO', 't1', '3'),
        InstrucaoTAC('OPERACAO', 't2', 't0', '+', 't1'),  # t2 = 2+3
        InstrucaoTAC('ATRIBUICAO', 't3', '4'),
        InstrucaoTAC('OPERACAO', 't4', 't2', '*', 't3'),  # t4 = t2*4
    ]
    
    codigo = gerador.gerar(instrucoes)
    linhas = codigo.split('\n')
    
    # Contar instruções relevantes
    num_ldi = sum(1 for l in linhas if 'ldi' in l)
    num_add = sum(1 for l in linhas if 'add' in l)
    num_mul = sum(1 for l in linhas if 'mul' in l)
    
    assert num_ldi >= 3, f"Esperado >= 3 ldi, encontrado {num_ldi}"
    assert num_add >= 1, f"Esperado >= 1 add, encontrado {num_add}"
    assert num_mul >= 1, f"Esperado >= 1 mul, encontrado {num_mul}"
    
    print(f"✓ Código contém:")
    print(f"  - {num_ldi} instruções ldi")
    print(f"  - {num_add} instruções add")
    print(f"  - {num_mul} instruções mul")
    print()


def teste_gerenciamento_registradores():
    """Teste 9: Gerenciamento de registradores"""
    print("Teste 9: Gerenciamento de registradores")
    print("-" * 60)
    
    gerador = GeradorAssemblyAVR()
    
    # Alocar alguns registradores
    r0 = gerador.alocar_registrador('t0')
    r1 = gerador.alocar_registrador('t1')
    r2 = gerador.alocar_registrador('t2')
    
    assert r0 == 16, f"Primeiro registrador deve ser r16, obtido r{r0}"
    assert r1 == 17, f"Segundo registrador deve ser r17, obtido r{r1}"
    assert r2 == 18, f"Terceiro registrador deve ser r18, obtido r{r2}"
    
    # Verificar mapa
    assert gerador.obter_registrador('t0') == 16
    assert gerador.obter_registrador('t1') == 17
    assert gerador.obter_registrador('t2') == 18
    
    # Liberar e realocar
    gerador.liberar_registrador('t1')
    r1_novo = gerador.alocar_registrador('t3')
    assert r1_novo == 17, "Registrador liberado deve ser reutilizado"
    
    print("✓ Gerenciamento de registradores funcional:")
    print("  - Alocação sequencial: r16, r17, r18")
    print("  - Liberação e reutilização funcionando")
    print()


def teste_salvamento_arquivo():
    """Teste 10: Salvamento com TAC"""
    print("Teste 10: Salvamento de programa completo com TAC")
    print("-" * 60)
    
    gerador = GeradorAssemblyAVR()
    instrucoes = [
        InstrucaoTAC('ATRIBUICAO', 't0', '10'),
        InstrucaoTAC('ATRIBUICAO', 't1', '20'),
        InstrucaoTAC('OPERACAO', 't2', 't0', '+', 't1'),
        InstrucaoTAC('COPIA', 'RESULTADO', 't2')
    ]
    
    codigo = gerador.gerar(instrucoes)
    
    output_path = "output/teste_parte10.s"
    gerador.salvar(output_path)
    
    # Verificar arquivo
    path = Path(output_path)
    assert path.exists(), "Arquivo não foi criado"
    
    tamanho = path.stat().st_size
    assert tamanho > 2000, f"Arquivo muito pequeno: {tamanho} bytes"
    
    stats = gerador.obter_estatisticas()
    
    print(f"✓ Arquivo salvo: {output_path}")
    print(f"  - Tamanho: {tamanho} bytes")
    print(f"  - Linhas: {stats['linhas_codigo']}")
    print()


def main():
    """Executa todos os testes"""
    print("=" * 70)
    print("TESTES DO GERADOR DE ASSEMBLY AVR - PARTE 10")
    print("Operações Aritméticas e Mapeamento TAC → Assembly")
    print("=" * 70)
    print()
    
    testes = [
        teste_atribuicao_constante,
        teste_adicao_simples,
        teste_subtracao,
        teste_multiplicacao,
        teste_copia,
        teste_rotulo_e_goto,
        teste_condicional,
        teste_expressao_complexa,
        teste_gerenciamento_registradores,
        teste_salvamento_arquivo
    ]
    
    sucessos = 0
    falhas = 0
    
    for teste in testes:
        try:
            teste()
            sucessos += 1
        except Exception as e:
            falhas += 1
            print(f"✗ FALHA: {e}")
            import traceback
            traceback.print_exc()
            print()
    
    # Resumo
    print("=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    print(f"✓ Sucessos: {sucessos}/{len(testes)}")
    if falhas > 0:
        print(f"✗ Falhas: {falhas}/{len(testes)}")
    print()
    
    if falhas == 0:
        print(" Todos os testes passaram!")
        print()
        print("Operações implementadas:")
        print("  ✓ Atribuição de constantes (ldi)")
        print("  ✓ Adição (add)")
        print("  ✓ Subtração (sub)")
        print("  ✓ Multiplicação (mul)")
        print("  ✓ Cópia entre registradores (mov)")
        print("  ✓ Rótulos e saltos (rjmp)")
        print("  ✓ Saltos condicionais (tst + breq)")
        print()
        print("Próximos passos:")
        print("  - Parte 11: Acesso à memória SRAM")
        print("  - Parte 12: Estruturas de controle completas")
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
