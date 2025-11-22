#!/usr/bin/env python3
"""
Compilador RPN Completo - Fase 6: Assembly AVR
===============================================

Integra todas as fases do compilador e gera código Assembly AVR:
1. Análise Léxica
2. Análise Sintática
3. Análise Semântica
4. Geração TAC
5. Otimização TAC
6. Geração Assembly AVR

Usage:
    python3 main_assembly.py <arquivo_entrada> [--nivel <nivel>] [--output <arquivo.s>]
    
Exemplo:
    python3 main_assembly.py test_completo.txt --output output/programa.s
"""

import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).parent))

from src.lexer import parse_expressao as tokenizar
from src.parser import parsear
from src.grammar import construir_gramatica
from src.syntax_tree import converter_derivacao_para_arvore
from src.arvore_atribuida import gerar_arvore_atribuida
from src.gerador_tac import GeradorTAC
from src.otimizador_tac import OtimizadorTAC
from src.gerador_assembly_avr import GeradorAssemblyAVR


def compilar_para_assembly(expressoes: List[str], nivel_otimizacao: str = 'completo',
                          baud_rate: int = 9600) -> tuple:
    """
    Compila expressões RPN para Assembly AVR
    
    Args:
        expressoes: Lista de expressões RPN
        nivel_otimizacao: Nível de otimização TAC
        baud_rate: Taxa UART
        
    Returns:
        (codigo_assembly, estatisticas)
    """
    print("=" * 80)
    print("COMPILADOR RPN → ASSEMBLY AVR")
    print("=" * 80)
    print()
    
    # Fase 1-2: Preparação
    gramatica = construir_gramatica()
    gerador_tac = GeradorTAC()
    otimizador = OtimizadorTAC()
    
    print(f"📝 Compilando {len(expressoes)} expressões...")
    print()
    
    # Processar cada expressão
    sucessos = 0
    falhas = 0
    
    for i, expressao in enumerate(expressoes, 1):
        try:
            # Fase 1: Léxica
            tokens = tokenizar(expressao)
            if not tokens:
                print(f"  {i}. ✗ {expressao} - Erro léxico")
                falhas += 1
                continue
            
            # Fase 2: Sintática
            resultado_parser = parsear(tokens, gramatica['tabela'])
            derivacao = resultado_parser['derivacao']
            
            # Fase 3: Semântica
            arvore = converter_derivacao_para_arvore(derivacao)
            arvore_atribuida = gerar_arvore_atribuida(arvore)
            
            # Fase 4: TAC
            num_antes = len(gerador_tac.instrucoes)
            resultado = gerador_tac.processar_no(arvore_atribuida)
            gerador_tac.historico_resultados.append(resultado)
            num_geradas = len(gerador_tac.instrucoes) - num_antes
            
            print(f"  {i}. ✓ {expressao} ({num_geradas} instruções TAC)")
            sucessos += 1
            
        except Exception as e:
            print(f"  {i}. ✗ {expressao} - {e}")
            falhas += 1
    
    print()
    print(f"Resultado: {sucessos} sucessos, {falhas} falhas")
    print()
    
    # Fase 5: Otimização TAC
    print("🔧 Otimizando código TAC...")
    tac_original = gerador_tac.instrucoes
    tac_otimizado = otimizador.otimizar(tac_original, nivel_otimizacao)
    
    reducao = len(tac_original) - len(tac_otimizado)
    percentual = (reducao / len(tac_original) * 100) if tac_original else 0
    
    print(f"  TAC Original: {len(tac_original)} instruções")
    print(f"  TAC Otimizado: {len(tac_otimizado)} instruções")
    print(f"  Redução: {reducao} instruções ({percentual:.1f}%)")
    print()
    
    # Fase 6: Geração Assembly
    print("⚙️  Gerando Assembly AVR...")
    gerador_asm = GeradorAssemblyAVR(baud_rate=baud_rate)
    codigo_assembly = gerador_asm.gerar(tac_otimizado)
    
    stats_asm = gerador_asm.obter_estatisticas()
    print(f"  Assembly: {stats_asm['linhas_codigo']} linhas")
    print(f"  Baud rate: {stats_asm['baud_rate']}")
    print()
    
    # Estatísticas finais
    estatisticas = {
        'expressoes_total': len(expressoes),
        'expressoes_sucesso': sucessos,
        'expressoes_falhas': falhas,
        'tac_original': len(tac_original),
        'tac_otimizado': len(tac_otimizado),
        'reducao_tac': reducao,
        'percentual_reducao': percentual,
        'linhas_assembly': stats_asm['linhas_codigo'],
        'baud_rate': baud_rate,
        'nivel_otimizacao': nivel_otimizacao
    }
    
    return codigo_assembly, estatisticas


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("Uso: python3 main_assembly.py <arquivo_entrada> [opções]")
        print()
        print("Opções:")
        print("  --nivel <nivel>     Nível de otimização (folding|propagation|dead_code|completo)")
        print("  --output <arquivo>  Arquivo de saída Assembly (.s)")
        print("  --baud <rate>       Taxa UART (9600 ou 115200)")
        print()
        print("Exemplo:")
        print("  python3 main_assembly.py test_completo.txt --output programa.s")
        sys.exit(1)
    
    arquivo_entrada = sys.argv[1]
    
    # Opções
    nivel = 'completo'
    output = 'output/programa.s'
    baud = 9600
    
    if '--nivel' in sys.argv:
        idx = sys.argv.index('--nivel')
        if idx + 1 < len(sys.argv):
            nivel = sys.argv[idx + 1]
    
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output = sys.argv[idx + 1]
    
    if '--baud' in sys.argv:
        idx = sys.argv.index('--baud')
        if idx + 1 < len(sys.argv):
            baud = int(sys.argv[idx + 1])
    
    # Ler arquivo
    caminho = Path(arquivo_entrada)
    if not caminho.exists():
        print(f"❌ Arquivo não encontrado: {arquivo_entrada}")
        sys.exit(1)
    
    with open(caminho, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    expressoes = [
        linha.strip()
        for linha in linhas
        if linha.strip() and not linha.strip().startswith('#')
    ]
    
    # Compilar
    assembly, stats = compilar_para_assembly(expressoes, nivel, baud)
    
    # Salvar
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(assembly)
    
    # Relatório final
    print("=" * 80)
    print("RELATÓRIO FINAL")
    print("=" * 80)
    print(f"Arquivo de entrada: {arquivo_entrada}")
    print(f"Arquivo de saída: {output}")
    print()
    print(f"Expressões: {stats['expressoes_total']}")
    print(f"  ✓ Compiladas: {stats['expressoes_sucesso']}")
    print(f"  ✗ Com erro: {stats['expressoes_falhas']}")
    print()
    print(f"Código TAC:")
    print(f"  Original: {stats['tac_original']} instruções")
    print(f"  Otimizado: {stats['tac_otimizado']} instruções")
    print(f"  Redução: {stats['reducao_tac']} ({stats['percentual_reducao']:.1f}%)")
    print()
    print(f"Assembly AVR:")
    print(f"  Linhas: {stats['linhas_assembly']}")
    print(f"  Baud rate: {stats['baud_rate']}")
    print(f"  Nível de otimização: {stats['nivel_otimizacao']}")
    print()
    print("=" * 80)
    print()
    print("Para compilar e gravar no Arduino:")
    print(f"  avr-gcc -mmcu=atmega328p {output} -o {output_path.stem}.elf")
    print(f"  avr-objcopy -O ihex -j .text -j .data {output_path.stem}.elf {output_path.stem}.hex")
    print(f"  avrdude -p atmega328p -c arduino -P /dev/ttyUSB0 -b 115200 -U flash:w:{output_path.stem}.hex")
    print()
    print("✅ Compilação concluída!")


if __name__ == '__main__':
    main()
