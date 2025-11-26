#!/usr/bin/env python3
"""
Teste do Gerador de Assembly AVR - Parte 9
==========================================

Testa a geração do prólogo e epílogo do código Assembly.
Valida estrutura básica sem necessidade de compilador AVR.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.gerador_assembly_avr import GeradorAssemblyAVR


def validar_assembly(codigo: str) -> tuple:
    """
    Valida estrutura básica do código Assembly
    
    Returns:
        (sucesso: bool, erros: list)
    """
    erros = []
    linhas = codigo.split('\n')
    
    # Verificar elementos essenciais
    tem_include = any('#include <avr/io.h>' in linha for linha in linhas)
    tem_main = any('.global main' in linha for linha in linhas)
    tem_section_text = any('.section .text' in linha for linha in linhas)
    tem_section_data = any('.section .data' in linha for linha in linhas)
    tem_section_bss = any('.section .bss' in linha for linha in linhas)
    tem_loop_forever = any('loop_forever:' in linha for linha in linhas)
    tem_setup_uart = any('setup_uart:' in linha for linha in linhas)
    tem_programa_principal = any('programa_principal:' in linha for linha in linhas)
    
    # Stack pointer
    tem_stack_low = any('STACK_LOW' in linha for linha in linhas)
    tem_stack_high = any('STACK_HIGH' in linha for linha in linhas)
    
    # UART
    tem_baud_rate = any('BAUD_RATE' in linha for linha in linhas)
    tem_uart_transmit = any('uart_transmit:' in linha for linha in linhas)
    
    # Validações
    if not tem_include:
        erros.append("Falta #include <avr/io.h>")
    
    if not tem_main:
        erros.append("Falta .global main")
    
    if not tem_section_text:
        erros.append("Falta seção .text")
    
    if not tem_section_data:
        erros.append("Falta seção .data")
    
    if not tem_section_bss:
        erros.append("Falta seção .bss")
    
    if not tem_loop_forever:
        erros.append("Falta loop_forever")
    
    if not tem_setup_uart:
        erros.append("Falta função setup_uart")
    
    if not tem_programa_principal:
        erros.append("Falta função programa_principal")
    
    if not tem_stack_low or not tem_stack_high:
        erros.append("Falta configuração de stack")
    
    if not tem_baud_rate:
        erros.append("Falta configuração de baud rate")
    
    if not tem_uart_transmit:
        erros.append("Falta função uart_transmit")
    
    return len(erros) == 0, erros


def teste_geracao_basica():
    """Teste 1: Geração básica do código"""
    print("Teste 1: Geração básica do código Assembly")
    print("-" * 60)
    
    gerador = GeradorAssemblyAVR()
    codigo = gerador.gerar()
    
    assert len(codigo) > 0, "Código Assembly vazio"
    assert len(gerador.codigo) > 100, f"Código muito curto: {len(gerador.codigo)} linhas"
    
    print(f"✓ Código gerado: {len(gerador.codigo)} linhas")
    print()


def teste_validacao_estrutura():
    """Teste 2: Validação da estrutura"""
    print("Teste 2: Validação da estrutura do Assembly")
    print("-" * 60)
    
    gerador = GeradorAssemblyAVR(baud_rate=9600)
    codigo = gerador.gerar()
    
    sucesso, erros = validar_assembly(codigo)
    
    if sucesso:
        print("✓ Estrutura válida")
    else:
        print("✗ Erros encontrados:")
        for erro in erros:
            print(f"  - {erro}")
        raise AssertionError("Estrutura inválida")
    
    print()


def teste_baud_rates():
    """Teste 3: Diferentes baud rates"""
    print("Teste 3: Diferentes configurações de baud rate")
    print("-" * 60)
    
    for baud in [9600, 115200]:
        gerador = GeradorAssemblyAVR(baud_rate=baud)
        codigo = gerador.gerar()
        
        assert f"; {baud} baud" in codigo, f"Baud rate {baud} não configurado"
        print(f"✓ Baud rate {baud} configurado corretamente")
    
    print()


def teste_salvamento_arquivo():
    """Teste 4: Salvamento em arquivo"""
    print("Teste 4: Salvamento em arquivo")
    print("-" * 60)
    
    gerador = GeradorAssemblyAVR()
    gerador.gerar()
    
    output_path = "output/teste_parte9.s"
    gerador.salvar(output_path)
    
    # Verificar se arquivo foi criado
    path = Path(output_path)
    assert path.exists(), f"Arquivo não foi criado: {output_path}"
    
    # Verificar tamanho
    tamanho = path.stat().st_size
    assert tamanho > 1000, f"Arquivo muito pequeno: {tamanho} bytes"
    
    print(f"✓ Arquivo salvo: {output_path} ({tamanho} bytes)")
    print()


def teste_estatisticas():
    """Teste 5: Estatísticas"""
    print("Teste 5: Estatísticas da geração")
    print("-" * 60)
    
    gerador = GeradorAssemblyAVR(baud_rate=115200)
    gerador.gerar()
    
    stats = gerador.obter_estatisticas()
    
    assert 'linhas_codigo' in stats
    assert 'baud_rate' in stats
    assert stats['linhas_codigo'] > 100
    assert stats['baud_rate'] == 115200
    
    print(f"✓ Linhas de código: {stats['linhas_codigo']}")
    print(f"✓ Baud rate: {stats['baud_rate']}")
    print()


def teste_secoes():
    """Teste 6: Verificar seções do Assembly"""
    print("Teste 6: Verificação das seções Assembly")
    print("-" * 60)
    
    gerador = GeradorAssemblyAVR()
    codigo = gerador.gerar()
    
    # Contar seções
    secoes_encontradas = {
        '.text': codigo.count('.section .text'),
        '.data': codigo.count('.section .data'),
        '.bss': codigo.count('.section .bss')
    }
    
    for secao, count in secoes_encontradas.items():
        assert count >= 1, f"Seção {secao} não encontrada"
        print(f"✓ Seção {secao}: {count} ocorrência(s)")
    
    print()


def main():
    """Executa todos os testes"""
    print("=" * 70)
    print("TESTES DO GERADOR DE ASSEMBLY AVR - PARTE 9")
    print("=" * 70)
    print()
    
    testes = [
        teste_geracao_basica,
        teste_validacao_estrutura,
        teste_baud_rates,
        teste_salvamento_arquivo,
        teste_estatisticas,
        teste_secoes
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
        print("Próximos passos:")
        print("  - Parte 10: Implementar operações aritméticas")
        print("  - Parte 11: Implementar acesso à memória")
        print("  - Parte 12: Implementar estruturas de controle")
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
