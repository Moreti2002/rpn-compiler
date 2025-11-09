#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analisador Completo - Fases 1, 2 e 3
Análise Léxica + Sintática + Semântica

Uso: python3 main_semantico.py <arquivo.txt>
"""

import sys
import os
import json

# adicionar diretórios ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.lexer import parse_expressao
from src.parser import parsear
from src.grammar import construir_gramatica
from src.syntax_tree import gerar_arvore
from src.gramatica_atributos import definir_gramatica_atributos
from src.tabela_simbolos import inicializar_tabela_simbolos, imprimir_tabela, adicionar_resultado_historico
from src.analisador_tipos import analisar_semantica, gerar_relatorio_julgamento_tipos
from src.analisador_memoria import analisar_semantica_memoria
from src.analisador_controle import analisar_semantica_controle
from src.arvore_atribuida import (
    gerar_arvore_atribuida, 
    salvar_arvore_json, 
    extrair_informacoes_arvore,
    validar_arvore_atribuida
)
from utils.formatador_relatorios import gerar_todos_relatorios

def processar_arquivo(nome_arquivo):
    """
    processa arquivo de teste completo
    
    Args:
        nome_arquivo (str): caminho do arquivo
        
    Returns:
        tuple: (sucesso, mensagem)
    """
    print("=" * 80)
    print(f"ANALISADOR COMPLETO - FASE 3")
    print("=" * 80)
    print(f"\n📂 Arquivo: {nome_arquivo}\n")
    
    # verificar se arquivo existe
    if not os.path.exists(nome_arquivo):
        return False, f"Erro: Arquivo '{nome_arquivo}' não encontrado"
    
    # ler arquivo
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
    except Exception as e:
        return False, f"Erro ao ler arquivo: {str(e)}"
    
    print(f"📄 Total de linhas: {len(linhas)}\n")
    
    # inicializar estruturas
    print("🔧 Inicializando estruturas...")
    
    try:
        gramatica_sintatica = construir_gramatica()
        tabela_ll1 = gramatica_sintatica['tabela']
        print("  ✓ Gramática sintática LL(1)")
        
        gramatica_atributos = definir_gramatica_atributos()
        print("  ✓ Gramática de atributos")
        
        tabela_simbolos = inicializar_tabela_simbolos()
        print("  ✓ Tabela de símbolos")
        
    except Exception as e:
        return False, f"Erro na inicialização: {str(e)}"
    
    # processar cada linha
    print(f"\n{'─' * 80}")
    print("PROCESSANDO EXPRESSÕES")
    print(f"{'─' * 80}\n")
    
    erros_lexicos = []
    erros_sintaticos = []
    erros_semanticos = []
    arvores_atribuidas = []
    todas_regras_aplicadas = []
    
    for num_linha, linha in enumerate(linhas, 1):
        linha = linha.strip()
        
        # pular linhas vazias e comentários
        if not linha or linha.startswith('#'):
            continue
        
        print(f"Linha {num_linha}: {linha}")
        
        # ===== FASE 1: ANÁLISE LÉXICA =====
        try:
            tokens = parse_expressao(linha)
            print(f"  ✓ Análise léxica: {len(tokens)} tokens")
        except Exception as e:
            erro_msg = str(e)
            erros_lexicos.append({
                'linha': num_linha,
                'expressao': linha,
                'erro': erro_msg
            })
            print(f"  ✗ Erro léxico: {erro_msg}")
            continue
        
        # ===== FASE 2: ANÁLISE SINTÁTICA =====
        try:
            resultado_parser = parsear(tokens, tabela_ll1)
            
            if not resultado_parser.get('valido', False):
                erro_msg = resultado_parser.get('erro', 'Erro desconhecido')
                erros_sintaticos.append({
                    'linha': num_linha,
                    'expressao': linha,
                    'erro': erro_msg
                })
                print(f"  ✗ Erro sintático: {erro_msg}")
                continue
            
            arvore_sintatica = gerar_arvore(resultado_parser['derivacao'])
            print(f"  ✓ Análise sintática: árvore gerada")
            
        except Exception as e:
            erro_msg = str(e)
            erros_sintaticos.append({
                'linha': num_linha,
                'expressao': linha,
                'erro': erro_msg
            })
            print(f"  ✗ Erro sintático: {erro_msg}")
            continue
        
        # ===== FASE 3: ANÁLISE SEMÂNTICA =====
        
        # 3.1: Análise de tipos
        try:
            arvore_anotada, erros_tipo = analisar_semantica(
                arvore_sintatica, 
                gramatica_atributos, 
                tabela_simbolos
            )
            
            if erros_tipo:
                for erro in erros_tipo:
                    erro['linha'] = num_linha
                    erro['expressao'] = linha
                    erros_semanticos.append(erro)
                print(f"  ✗ Erros de tipo: {len(erros_tipo)}")
                for erro in erros_tipo:
                    print(f"    - {erro['mensagem']}")
                continue
            
            print(f"  ✓ Análise de tipos: OK")
            
        except Exception as e:
            erro_msg = f"Erro na análise de tipos: {str(e)}"
            erros_semanticos.append({
                'tipo': 'ERRO_INTERNO',
                'linha': num_linha,
                'expressao': linha,
                'mensagem': erro_msg
            })
            print(f"  ✗ {erro_msg}")
            continue
        
        # 3.2: Análise de memória
        try:
            tabela_simbolos, erros_memoria = analisar_semantica_memoria(
                arvore_anotada, 
                tabela_simbolos
            )
            
            if erros_memoria:
                for erro in erros_memoria:
                    erro['linha'] = num_linha
                    erro['expressao'] = linha
                    erros_semanticos.append(erro)
                print(f"  ✗ Erros de memória: {len(erros_memoria)}")
                for erro in erros_memoria:
                    print(f"    - {erro['mensagem']}")
                continue
            
            print(f"  ✓ Análise de memória: OK")
            
        except Exception as e:
            erro_msg = f"Erro na análise de memória: {str(e)}"
            erros_semanticos.append({
                'tipo': 'ERRO_INTERNO',
                'linha': num_linha,
                'expressao': linha,
                'mensagem': erro_msg
            })
            print(f"  ✗ {erro_msg}")
            continue
        
        # 3.3: Análise de controle
        try:
            erros_controle = analisar_semantica_controle(
                arvore_anotada, 
                tabela_simbolos
            )
            
            if erros_controle:
                for erro in erros_controle:
                    erro['linha'] = num_linha
                    erro['expressao'] = linha
                    erros_semanticos.append(erro)
                print(f"  ✗ Erros de controle: {len(erros_controle)}")
                for erro in erros_controle:
                    print(f"    - {erro['mensagem']}")
                continue
            
            print(f"  ✓ Análise de controle: OK")
            
        except Exception as e:
            erro_msg = f"Erro na análise de controle: {str(e)}"
            erros_semanticos.append({
                'tipo': 'ERRO_INTERNO',
                'linha': num_linha,
                'expressao': linha,
                'mensagem': erro_msg
            })
            print(f"  ✗ {erro_msg}")
            continue
        
        # 3.4: Gerar árvore atribuída
        try:
            arvore_final = gerar_arvore_atribuida(arvore_anotada)
            arvores_atribuidas.append({
                'linha': num_linha,
                'expressao': linha,
                'arvore': arvore_final
            })
            
            print(f"  ✓ Árvore atribuída: gerada")
            
            # adicionar resultado ao histórico
            tipo_resultado = arvore_final.get('tipo_inferido')
            if tipo_resultado:
                adicionar_resultado_historico(tabela_simbolos, tipo_resultado)
            
        except Exception as e:
            erro_msg = f"Erro ao gerar árvore atribuída: {str(e)}"
            erros_semanticos.append({
                'tipo': 'ERRO_INTERNO',
                'linha': num_linha,
                'expressao': linha,
                'mensagem': erro_msg
            })
            print(f"  ✗ {erro_msg}")
            continue
        
        # coletar regras de julgamento de tipos
        try:
            regras = gerar_relatorio_julgamento_tipos(arvore_anotada)
            for regra in regras:
                regra['linha_codigo'] = num_linha
            todas_regras_aplicadas.extend(regras)
        except:
            pass
        
        print(f"  ✅ Linha {num_linha} processada com sucesso\n")
    
    # ===== RESULTADOS FINAIS =====
    print(f"{'─' * 80}")
    print("RESULTADOS DA ANÁLISE")
    print(f"{'─' * 80}\n")
    
    total_linhas = len([l for l in linhas if l.strip() and not l.strip().startswith('#')])
    linhas_sucesso = len(arvores_atribuidas)
    
    print(f"📊 Estatísticas:")
    print(f"  - Total de linhas processadas: {total_linhas}")
    print(f"  - Linhas com sucesso: {linhas_sucesso}")
    print(f"  - Erros léxicos: {len(erros_lexicos)}")
    print(f"  - Erros sintáticos: {len(erros_sintaticos)}")
    print(f"  - Erros semânticos: {len(erros_semanticos)}")
    
    # exibir tabela de símbolos
    if tabela_simbolos['simbolos']:
        print(f"\n{'─' * 80}")
        print("TABELA DE SÍMBOLOS")
        print(f"{'─' * 80}\n")
        print(imprimir_tabela(tabela_simbolos))
    
    # consolidar todos os erros
    todos_erros = []
    
    for erro in erros_lexicos:
        todos_erros.append({
            'tipo': 'ERRO_LEXICO',
            'linha': erro['linha'],
            'mensagem': erro['erro'],
            'contexto': erro['expressao']
        })
    
    for erro in erros_sintaticos:
        todos_erros.append({
            'tipo': 'ERRO_SINTATICO',
            'linha': erro['linha'],
            'mensagem': erro['erro'],
            'contexto': erro['expressao']
        })
    
    todos_erros.extend(erros_semanticos)
    
    # exibir erros se houver
    if todos_erros:
        print(f"{'─' * 80}")
        print("⚠️  ERROS ENCONTRADOS")
        print(f"{'─' * 80}\n")
        
        for i, erro in enumerate(todos_erros, 1):
            print(f"{i}. [{erro.get('tipo', 'ERRO')}] Linha {erro.get('linha', '?')}")
            print(f"   {erro.get('mensagem', 'Mensagem não disponível')}")
            if erro.get('contexto'):
                print(f"   Contexto: {erro['contexto']}")
            print()
    
    # ===== GERAR RELATÓRIOS =====
    print(f"{'─' * 80}")
    print("GERANDO RELATÓRIOS")
    print(f"{'─' * 80}\n")
    
    try:
        # usar última árvore atribuída para o relatório (ou criar vazia)
        if arvores_atribuidas:
            ultima_arvore = arvores_atribuidas[-1]['arvore']
            info_arvore = extrair_informacoes_arvore(ultima_arvore)
        else:
            ultima_arvore = {'tipo': 'VAZIO', 'tipo_inferido': None, 'linha': 0, 'filhos': []}
            info_arvore = {
                'total_nos': 0,
                'profundidade': 0,
                'total_linhas': 0,
                'operadores_usados': [],
                'tipos_encontrados': {}
            }
        
        # salvar árvore em JSON
        salvar_arvore_json(ultima_arvore, "arvore_atribuida.json")
        print("  ✓ arvore_atribuida.json")
        
        # gerar todos os relatórios markdown
        gerar_todos_relatorios(
            gramatica_atributos,
            ultima_arvore,
            info_arvore,
            todos_erros,
            todas_regras_aplicadas
        )
        
    except Exception as e:
        print(f"  ✗ Erro ao gerar relatórios: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # ===== RESUMO FINAL =====
    print(f"{'=' * 80}")
    
    if todos_erros:
        print(f"❌ ANÁLISE CONCLUÍDA COM ERROS ({len(todos_erros)} erro(s))")
        return False, f"Foram encontrados {len(todos_erros)} erro(s)"
    else:
        print("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
        print("\n📁 Arquivos gerados:")
        print("  - arvore_atribuida.json")
        print("  - docs/GRAMATICA_ATRIBUTOS.md")
        print("  - docs/ARVORE_ATRIBUIDA.md")
        print("  - docs/ERROS_SEMANTICOS.md")
        print("  - docs/JULGAMENTO_TIPOS.md")
        return True, "Análise concluída sem erros"
    
    print(f"{'=' * 80}\n")

def main():
    """função principal"""
    if len(sys.argv) != 2:
        print("Uso: python3 main_semantico.py <arquivo.txt>")
        print("\nExemplo:")
        print("  python3 main_semantico.py test_fase3_1.txt")
        sys.exit(1)
    
    nome_arquivo = sys.argv[1]
    sucesso, mensagem = processar_arquivo(nome_arquivo)
    
    if not sucesso:
        print(f"\n❌ {mensagem}")
        sys.exit(1)

if __name__ == '__main__':
    main()
