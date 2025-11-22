#!/usr/bin/env python3
"""
Compilador RPN - Fase 4: Integração Completa
============================================

Integra todas as 4 fases do compilador:
- Fase 1: Análise Léxica (tokenização)
- Fase 2: Análise Sintática (parsing)
- Fase 3: Análise Semântica (atribuição de tipos)
- Fase 4: Geração de Código Intermediário (TAC)

Uso:
    python3 main_fase4.py <arquivo_entrada> [arquivo_saida_tac]

Exemplo:
    python3 main_fase4.py test_if_while.txt output/programa.tac
"""

import sys
import os
from pathlib import Path

# Adicionar diretório do projeto ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.lexer import parse_expressao as tokenizar
from src.parser import parsear
from src.grammar import construir_gramatica
from src.syntax_tree import converter_derivacao_para_arvore
from src.arvore_atribuida import gerar_arvore_atribuida
from src.gerador_tac import GeradorTAC
from utils.formatador_tac import formatar_lista_tac


def ler_arquivo_entrada(caminho: str) -> list:
    """
    Lê arquivo de entrada e retorna lista de expressões válidas
    
    Args:
        caminho: Caminho do arquivo de entrada
        
    Returns:
        Lista de tuplas (numero_linha, expressao)
    """
    expressoes = []
    
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            for num_linha, linha in enumerate(f, start=1):
                # Remover espaços e verificar se não é comentário
                linha = linha.strip()
                
                if linha and not linha.startswith('#'):
                    expressoes.append((num_linha, linha))
        
        return expressoes
    
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{caminho}' não encontrado")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        sys.exit(1)


def compilar_expressao(expressao: str, numero_linha: int, gramatica: dict, gerador: GeradorTAC) -> tuple:
    """
    Compila uma expressão através das 4 fases
    
    Args:
        expressao: String da expressão RPN
        numero_linha: Número da linha no arquivo
        gramatica: Gramática do compilador
        gerador: Instância do gerador TAC (mantém estado entre expressões)
        
    Returns:
        Tupla (sucesso: bool, mensagem: str, num_instrucoes: int)
    """
    try:
        # FASE 1: Análise Léxica
        tokens = tokenizar(expressao)
        
        if not tokens:
            return False, "Erro: Nenhum token gerado", 0
        
        # FASE 2: Análise Sintática
        resultado_parser = parsear(tokens, gramatica['tabela'])
        derivacao = resultado_parser['derivacao']
        
        # FASE 3: Análise Semântica (Árvore Sintática + Atribuição)
        arvore = converter_derivacao_para_arvore(derivacao)
        arvore_atribuida = gerar_arvore_atribuida(arvore)
        
        # FASE 4: Geração de TAC
        num_instrucoes_antes = len(gerador.instrucoes)
        resultado = gerador.processar_no(arvore_atribuida)
        
        # Adicionar resultado ao histórico (para comando RES)
        gerador.historico_resultados.append(resultado)
        
        num_instrucoes_geradas = len(gerador.instrucoes) - num_instrucoes_antes
        
        return True, f"✓ {num_instrucoes_geradas} instruções TAC geradas", num_instrucoes_geradas
    
    except Exception as e:
        return False, f"✗ Erro: {str(e)}", 0


def main():
    """Função principal"""
    
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("Uso: python3 main_fase4.py <arquivo_entrada> [arquivo_saida_tac]")
        print()
        print("Exemplos:")
        print("  python3 main_fase4.py expressoes.txt")
        print("  python3 main_fase4.py test_if_while.txt output/programa.tac")
        sys.exit(1)
    
    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[2] if len(sys.argv) > 2 else "output/tac_original.txt"
    
    # Banner
    print("=" * 70)
    print("COMPILADOR RPN - FASE 4: INTEGRAÇÃO COMPLETA")
    print("=" * 70)
    print()
    print(f"📁 Arquivo de entrada: {arquivo_entrada}")
    print(f"📝 Arquivo de saída TAC: {arquivo_saida}")
    print()
    
    # Ler arquivo de entrada
    expressoes = ler_arquivo_entrada(arquivo_entrada)
    print(f"📊 Total de expressões encontradas: {len(expressoes)}")
    print()
    
    # Construir gramática (Fase 2)
    print("⚙️  Construindo gramática...")
    gramatica = construir_gramatica()
    print("✓ Gramática construída")
    print()
    
    # Criar gerador TAC (Fase 4)
    # Usar uma única instância para manter contexto entre expressões
    gerador = GeradorTAC()
    
    # Estatísticas
    total_expressoes = len(expressoes)
    expressoes_sucesso = 0
    expressoes_erro = 0
    total_instrucoes = 0
    
    # Processar cada expressão
    print("─" * 70)
    print("PROCESSAMENTO DAS EXPRESSÕES")
    print("─" * 70)
    print()
    
    erros_detalhados = []
    
    for num_linha, expressao in expressoes:
        print(f"Linha {num_linha:3d}: {expressao}")
        
        sucesso, mensagem, num_instrucoes = compilar_expressao(
            expressao, num_linha, gramatica, gerador
        )
        
        if sucesso:
            expressoes_sucesso += 1
            total_instrucoes += num_instrucoes
            print(f"         {mensagem}")
        else:
            expressoes_erro += 1
            print(f"         {mensagem}")
            erros_detalhados.append((num_linha, expressao, mensagem))
        
        print()
    
    # Salvar TAC gerado
    print("─" * 70)
    print("SALVANDO TAC")
    print("─" * 70)
    print()
    
    # Criar diretório de saída se não existir
    os.makedirs(os.path.dirname(arquivo_saida), exist_ok=True)
    
    # Formatar e salvar TAC
    conteudo_tac = formatar_lista_tac(gerador.instrucoes, "THREE ADDRESS CODE (TAC)")
    
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(conteudo_tac)
    
    print(f"✓ TAC salvo em: {arquivo_saida}")
    print()
    
    # Resumo final
    print("=" * 70)
    print("RESUMO DA COMPILAÇÃO")
    print("=" * 70)
    print()
    print(f"📊 Expressões processadas:")
    print(f"   • Total: {total_expressoes}")
    print(f"   • Sucesso: {expressoes_sucesso} ({100*expressoes_sucesso/total_expressoes:.1f}%)")
    print(f"   • Erros: {expressoes_erro} ({100*expressoes_erro/total_expressoes:.1f}%)")
    print()
    print(f"📝 TAC gerado:")
    print(f"   • Total de instruções: {total_instrucoes}")
    print(f"   • Temporários criados: {gerador.contador_temporarios}")
    print(f"   • Rótulos criados: {gerador.contador_rotulos}")
    print(f"   • Variáveis na tabela: {len(gerador.tabela_simbolos)}")
    print()
    
    # Mostrar erros detalhados se houver
    if erros_detalhados:
        print("─" * 70)
        print("ERROS DETALHADOS")
        print("─" * 70)
        print()
        for num_linha, expressao, mensagem in erros_detalhados:
            print(f"Linha {num_linha}: {expressao}")
            print(f"  {mensagem}")
            print()
    
    # Status final
    if expressoes_erro == 0:
        print("✅ Compilação concluída com sucesso!")
    else:
        print(f"⚠️  Compilação concluída com {expressoes_erro} erro(s)")
    
    print()
    print("=" * 70)
    
    # Retornar código de saída apropriado
    sys.exit(0 if expressoes_erro == 0 else 1)


if __name__ == '__main__':
    main()
