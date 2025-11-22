#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Caminho: tests/test_gerador_tac.py

"""
Teste do Gerador TAC - Parte 1
Integração com Fases 1, 2 e 3

Este script testa o gerador de TAC processando arquivos de teste
através de todas as fases do compilador.
"""

import sys
import os

# ============================================================================
# CONFIGURAÇÃO DE PATHS
# ============================================================================

# Obter diretório do script e raiz do projeto
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# Adicionar raiz do projeto ao Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Também adicionar src/ e utils/ explicitamente (fallback)
src_dir = os.path.join(project_root, 'src')
utils_dir = os.path.join(project_root, 'utils')

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
if utils_dir not in sys.path:
    sys.path.insert(0, utils_dir)

# ============================================================================
# IMPORTS
# ============================================================================

try:
    # Imports das fases anteriores
    from src.lexer import parse_expressao
    from src.parser import parsear
    from src.grammar import construir_gramatica
    from src.syntax_tree import gerar_arvore
    from src.analisador_tipos import analisar_semantica
    from src.tabela_simbolos import inicializar_tabela_simbolos

    # Imports da Fase 4
    from src.gerador_tac import GeradorTAC
    from utils.formatador_tac import (
        exibir_tac_colorido, 
        gerar_estatisticas_detalhadas, 
        imprimir_estatisticas_detalhadas
    )
    
except ImportError as e:
    print("=" * 70)
    print("❌ ERRO DE IMPORTAÇÃO")
    print("=" * 70)
    print(f"\nErro: {e}\n")
    print("Verifique se todos os arquivos foram instalados corretamente.")
    print("\nPara debug, execute:")
    print("   python3 tests/debug_imports.py")
    print("\nOu reinstale os arquivos:")
    print("   bash /mnt/user-data/outputs/instalar_parte1.sh")
    print()
    sys.exit(1)


def processar_arquivo_teste(nome_arquivo: str):
    """
    Processa arquivo de teste através de todas as fases até geração de TAC
    
    Args:
        nome_arquivo: Caminho do arquivo de teste
    """
    print("\n" + "=" * 70)
    print("TESTE DO GERADOR TAC - PARTE 1")
    print("=" * 70)
    print(f"\nArquivo: {nome_arquivo}\n")
    
    if not os.path.exists(nome_arquivo):
        print(f"✗ Erro: Arquivo '{nome_arquivo}' não encontrado")
        return
    
    try:
        # ==================================================================
        # FASE 1: ANÁLISE LÉXICA
        # ==================================================================
        print("─" * 70)
        print("FASE 1: Análise Léxica")
        print("─" * 70)
        
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        
        expressoes_validas = []
        
        for num_linha, linha in enumerate(linhas, 1):
            linha = linha.strip()
            if not linha or linha.startswith('#'):
                continue
            
            try:
                tokens = parse_expressao(linha)
                expressoes_validas.append({
                    'linha': num_linha,
                    'texto': linha,
                    'tokens': tokens
                })
                print(f"✓ Linha {num_linha:2d}: {linha}")
            except Exception as e:
                print(f"✗ Linha {num_linha:2d}: {linha}")
                print(f"   Erro: {e}")
        
        print(f"\n✓ Total: {len(expressoes_validas)} expressões válidas\n")
        
        if not expressoes_validas:
            print("⚠️  Nenhuma expressão válida para processar")
            return
        
        # ==================================================================
        # FASE 2 e 3: SINTÁTICA E SEMÂNTICA
        # ==================================================================
        print("─" * 70)
        print("FASES 2 e 3: Análise Sintática e Semântica")
        print("─" * 70)
        
        gramatica_info = construir_gramatica()
        tabela = gramatica_info['tabela']
        tabela_simbolos = inicializar_tabela_simbolos()
        
        arvores_atribuidas = []
        
        for expr_info in expressoes_validas:
            try:
                # Análise sintática
                derivacao = parsear(expr_info['tokens'], tabela)
                arvore = gerar_arvore(derivacao['derivacao'])
                
                # Análise semântica
                erros_semanticos = []
                arvore_atribuida = analisar_semantica(arvore, tabela_simbolos, erros_semanticos)
                
                if erros_semanticos:
                    print(f"✗ Linha {expr_info['linha']}: Erros semânticos encontrados")
                    for erro in erros_semanticos:
                        print(f"   {erro}")
                else:
                    arvores_atribuidas.append({
                        'linha': expr_info['linha'],
                        'texto': expr_info['texto'],
                        'arvore': arvore_atribuida
                    })
                    print(f"✓ Linha {expr_info['linha']:2d}: {expr_info['texto']}")
                
            except Exception as e:
                print(f"✗ Linha {expr_info['linha']}: Erro na análise - {e}")
        
        print(f"\n✓ Total: {len(arvores_atribuidas)} árvores prontas para TAC\n")
        
        if not arvores_atribuidas:
            print("⚠️  Nenhuma árvore válida para gerar TAC")
            return
        
        # ==================================================================
        # FASE 4: GERAÇÃO DE TAC
        # ==================================================================
        print("─" * 70)
        print("FASE 4: Geração de TAC")
        print("─" * 70)
        
        # Criar um único gerador para manter contexto entre expressões
        gerador = GeradorTAC()
        todas_instrucoes = []
        instrucoes_por_expressao = []
        
        for arv_info in arvores_atribuidas:
            print(f"\nProcessando linha {arv_info['linha']}: {arv_info['texto']}")
            
            try:
                # Processar a árvore e obter o resultado
                # (usa o mesmo gerador para manter histórico e tabela de símbolos)
                resultado_var = gerador.processar_no(arv_info['arvore'])
                
                # Adicionar resultado ao histórico para RES
                if resultado_var and resultado_var != 'UNKNOWN':
                    gerador.historico_resultados.append(resultado_var)
                
                # Contar quantas instruções foram adicionadas
                num_instrucoes_atuais = len(gerador.instrucoes)
                num_instrucoes_anteriores = len(todas_instrucoes)
                novas_instrucoes = gerador.instrucoes[num_instrucoes_anteriores:]
                
                todas_instrucoes = gerador.instrucoes.copy()
                
                print(f"✓ {len(novas_instrucoes)} instruções TAC geradas")
                
                # Exibir TAC desta expressão
                if novas_instrucoes:
                    print("\nTAC gerado:")
                    for i, instrucao in enumerate(novas_instrucoes, 1):
                        print(f"  {i}. {instrucao}")
                    
                    instrucoes_por_expressao.append({
                        'linha': arv_info['linha'],
                        'texto': arv_info['texto'],
                        'instrucoes': novas_instrucoes
                    })
                
            except Exception as e:
                print(f"✗ Erro ao gerar TAC: {e}")
                import traceback
                traceback.print_exc()
        
        # ==================================================================
        # RESULTADOS FINAIS
        # ==================================================================
        print("\n" + "=" * 70)
        print("RESULTADOS FINAIS")
        print("=" * 70)
        
        if todas_instrucoes:
            # Exibir todo o TAC gerado
            exibir_tac_colorido(todas_instrucoes)
            
            # Estatísticas
            stats = gerar_estatisticas_detalhadas(todas_instrucoes)
            imprimir_estatisticas_detalhadas(stats)
            
            # Salvar em arquivo
            output_dir = os.path.join(project_root, "output")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            arquivo_saida = os.path.join(output_dir, "tac_original.txt")
            gerador.salvar_tac(arquivo_saida)
            
            print(f"\n✓ Teste concluído com sucesso!")
            print(f"✓ TAC salvo em: {arquivo_saida}")
        else:
            print("⚠️  Nenhuma instrução TAC foi gerada")
        
    except Exception as e:
        print(f"\n✗ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Função principal"""
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
    else:
        # Usar arquivo de teste padrão
        arquivo = os.path.join(project_root, "programas_teste", "test_tac_simples.txt")
        
        if not os.path.exists(arquivo):
            # Tentar caminho alternativo
            arquivo = "test_tac_simples.txt"
            
        if not os.path.exists(arquivo):
            print("=" * 70)
            print("❌ ERRO: Arquivo de teste não encontrado")
            print("=" * 70)
            print("\nUso: python3 test_gerador_tac.py <arquivo_teste.txt>")
            print("\nExemplo:")
            print("   python3 tests/test_gerador_tac.py programas_teste/test_tac_simples.txt")
            print()
            return
    
    processar_arquivo_teste(arquivo)


if __name__ == '__main__':
    main()