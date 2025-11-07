#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analisador Léxico, Sintático e Semântico
Fase 3 - Análise Semântica com Gramática de Atributos

Integrantes do grupo (ordem alfabética):
[Nome Completo 1] - [username1]
[Nome Completo 2] - [username2]
[Nome Completo 3] - [username3]
[Nome Completo 4] - [username4]

Nome do grupo no Canvas: [Nome do Grupo]
"""

import sys
import os
import json

# adicionar diretórios ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# imports da Fase 1 (Análise Léxica)
from src.lexer import parse_expressao

# imports da Fase 2 (Análise Sintática)
from src.parser import parsear
from src.grammar import construir_gramatica
from src.syntax_tree import gerar_arvore

# imports da Fase 3 (Análise Semântica)
from src.gramatica_atributos import definir_gramatica_atributos, gerar_documentacao_gramatica
from src.tabela_simbolos import inicializar_tabela_simbolos, imprimir_tabela
from src.analisador_tipos import analisar_semantica, gerar_relatorio_julgamento_tipos
from src.analisador_memoria import analisar_semantica_memoria
from src.analisador_controle import analisar_semantica_controle
from src.arvore_atribuida import gerar_arvore_atribuida, salvar_arvore_json
from utils.formatador_relatorios import gerar_todos_relatorios

def main():
    """
    Executa análise completa: léxica, sintática e semântica
    
    Uso: python main_semantico.py <arquivo_teste.txt>
    """
    print("=" * 70)
    print("COMPILADOR - Análise Léxica, Sintática e Semântica")
    print("=" * 70)
    print()
    
    # verificar argumentos
    if len(sys.argv) < 2:
        print("Uso: python main_semantico.py <arquivo_teste.txt>")
        print("\nExemplo: python main_semantico.py test_fase3_1.txt")
        sys.exit(1)
    
    arquivo_entrada = sys.argv[1]
    
    if not os.path.exists(arquivo_entrada):
        print(f"✗ Erro: Arquivo '{arquivo_entrada}' não encontrado")
        sys.exit(1)
    
    print(f"Arquivo de entrada: {arquivo_entrada}")
    print()
    
    try:
        # ==================================================================
        # FASE 1: ANÁLISE LÉXICA
        # ==================================================================
        print("─" * 70)
        print("FASE 1: Análise Léxica")
        print("─" * 70)
        
        # ler arquivo e tokenizar linha por linha
        all_tokens = []
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        
        for num_linha, linha in enumerate(linhas, 1):
            linha = linha.strip()
            if not linha or linha.startswith('#'):
                continue
            
            try:
                tokens_linha = parse_expressao(linha)
                all_tokens.extend(tokens_linha)
            except Exception as e:
                print(f"✗ Erro léxico na linha {num_linha}: {str(e)}")
                sys.exit(1)
        
        tokens = all_tokens
        print(f"✓ Análise léxica concluída: {len(tokens)} tokens gerados")
        print()
        
        # ==================================================================
        # FASE 2: ANÁLISE SINTÁTICA
        # ==================================================================
        print("─" * 70)
        print("FASE 2: Análise Sintática")
        print("─" * 70)
        
        # construir gramática
        gramatica_info = construir_gramatica()
        tabela_parsing = gramatica_info['tabela']
        
        # parsear arquivo (linha por linha)
        arvores_sintaxe = []
        erros_sintaticos = []
        
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        
        for num_linha, linha in enumerate(linhas, 1):
            linha = linha.strip()
            if not linha or linha.startswith('#'):
                continue
            
            try:
                # parsear
                tokens_linha = parse_expressao(linha)
                resultado_parser = parsear(tokens_linha, tabela_parsing)
                
                if not resultado_parser.get('valido'):
                    erros_sintaticos.append(f"Linha {num_linha}: {resultado_parser.get('erro', 'Erro desconhecido')}")
                    continue
                
                # gerar árvore sintática
                arvore = gerar_arvore(resultado_parser['derivacao'])
                arvore['linha'] = num_linha
                arvores_sintaxe.append(arvore)
                
            except Exception as e:
                erros_sintaticos.append(f"Linha {num_linha}: {str(e)}")
        
        if erros_sintaticos:
            print("✗ Erros sintáticos encontrados:")
            for erro in erros_sintaticos:
                print(f"  {erro}")
            sys.exit(1)
        
        print(f"✓ Análise sintática concluída: {len(arvores_sintaxe)} árvores geradas")
        print()
        
        # ==================================================================
        # FASE 3: ANÁLISE SEMÂNTICA
        # ==================================================================
        print("─" * 70)
        print("FASE 3: Análise Semântica")
        print("─" * 70)
        
        # 1. Definir Gramática de Atributos
        print("\n1. Definindo gramática de atributos...")
        gramatica_atributos = definir_gramatica_atributos()
        print(f"   ✓ {len(gramatica_atributos['regras_tipo'])} categorias de regras definidas")
        
        # 2. Inicializar Tabela de Símbolos
        print("\n2. Inicializando tabela de símbolos...")
        tabela_simbolos = inicializar_tabela_simbolos()
        todos_erros = []  # initialize error list
        print("   ✓ Tabela de símbolos inicializada")
        
        # 3. Análise Semântica - Memória (para cada árvore, para popular símbolos)
        print("\n3. Populando tabela de símbolos...")
        for i, arvore in enumerate(arvores_sintaxe, 1):
            tabela_simbolos, erros_memoria = analisar_semantica_memoria(
                arvore, 
                tabela_simbolos
            )
            if erros_memoria:
                todos_erros.extend(erros_memoria)
        print("   ✓ Tabela de símbolos populada")
        
        # 4. Análise Semântica - Tipos (para cada árvore)
        print("\n4. Analisando tipos...")
        arvores_anotadas = []
        todas_regras = []
        
        for i, arvore in enumerate(arvores_sintaxe, 1):
            print(f"   Processando expressão {i}...")
            
            # análise de tipos
            arvore_anotada, erros_tipos = analisar_semantica(
                arvore, 
                gramatica_atributos, 
                tabela_simbolos
            )
            
            if erros_tipos:
                todos_erros.extend(erros_tipos)
            
            # coletar regras aplicadas
            regras = gerar_relatorio_julgamento_tipos(arvore_anotada)
            todas_regras.extend(regras)
            
            arvores_anotadas.append(arvore_anotada)
        
        print(f"   ✓ Análise de tipos concluída")
        print("\n5. Analisando estruturas de controle...")
        for arvore in arvores_anotadas:
            erros_controle = analisar_semantica_controle(
                arvore, 
                tabela_simbolos
            )
            if erros_controle:
                todos_erros.extend(erros_controle)
        
        print("   ✓ Análise de controle concluída")
        
        # 6. Gerar Árvore Atribuída Final
        print("\n6. Gerando árvore sintática abstrata atribuída...")
        
        # combinar todas as árvores em uma estrutura de programa
        arvore_programa = {
            'tipo': 'PROGRAMA',
            'tipo_inferido': 'void',
            'linha': 1,
            'filhos': arvores_anotadas
        }
        
        arvore_final = gerar_arvore_atribuida(arvore_programa)
        print("   ✓ Árvore atribuída gerada")
        
        # 7. Salvar árvore em JSON
        salvar_arvore_json(arvore_final, "arvore_atribuida.json")
        print("   ✓ Árvore salva em arvore_atribuida.json")
        
        # 8. Gerar Relatórios
        print("\n7. Gerando relatórios em markdown...")
        gerar_todos_relatorios(
            gramatica_atributos,
            arvore_final,
            todos_erros,
            todas_regras
        )
        
        print()
        print("=" * 70)
        print("RESULTADOS DA ANÁLISE SEMÂNTICA")
        print("=" * 70)
        
        # Exibir erros no console
        if todos_erros:
            print(f"\n✗ {len(todos_erros)} erro(s) semântico(s) encontrado(s):\n")
            for erro in todos_erros:
                linha = f" [Linha {erro['linha']}]" if erro.get('linha') else ""
                print(f"ERRO SEMÂNTICO{linha}: {erro['mensagem']}")
                if erro.get('contexto'):
                    print(f"  Contexto: {erro['contexto']}")
                print()
        else:
            print("\n✓ Nenhum erro semântico encontrado!")
        
        # Exibir tabela de símbolos
        print("\n" + imprimir_tabela(tabela_simbolos))
        
        # Resumo
        print("\n" + "=" * 70)
        print("RESUMO")
        print("=" * 70)
        print(f"✓ Tokens gerados: {len(tokens)}")
        print(f"✓ Expressões analisadas: {len(arvores_sintaxe)}")
        print(f"✓ Símbolos na tabela: {len(tabela_simbolos['simbolos'])}")
        print(f"✓ Regras de tipo aplicadas: {len(todas_regras)}")
        print(f"{'✗' if todos_erros else '✓'} Erros semânticos: {len(todos_erros)}")
        print()
        print("Arquivos gerados:")
        print("  - arvore_atribuida.json")
        print("  - docs/GRAMATICA_ATRIBUTOS.md")
        print("  - docs/ARVORE_ATRIBUIDA.md")
        print("  - docs/ERROS_SEMANTICOS.md")
        print("  - docs/JULGAMENTO_TIPOS.md")
        print()
        
        # código de saída
        if todos_erros:
            sys.exit(1)
        else:
            sys.exit(0)
        
    except Exception as e:
        print(f"\n✗ Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
