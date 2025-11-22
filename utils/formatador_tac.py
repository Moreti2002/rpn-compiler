#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Caminho: utils/formatador_tac.py

"""
Formatador de Three Address Code (TAC)
Fase 4 - Utilitários para visualização e documentação

Este módulo fornece funções para formatar e visualizar código TAC de forma legível.
"""

from typing import List, Dict, Any

def formatar_instrucao_tac(instrucao: Any, numero: int = 0) -> str:
    """
    Formata uma instrução TAC para exibição
    
    Args:
        instrucao: Objeto InstrucaoTAC
        numero: Número da instrução (opcional)
        
    Returns:
        String formatada da instrução
    """
    if numero > 0:
        return f"{numero:3d}. {str(instrucao)}"
    return str(instrucao)


def formatar_lista_tac(instrucoes: List[Any], titulo: str = "TAC") -> str:
    """
    Formata uma lista de instruções TAC
    
    Args:
        instrucoes: Lista de objetos InstrucaoTAC
        titulo: Título para o bloco de código
        
    Returns:
        String formatada com todas as instruções
    """
    linhas = []
    linhas.append("=" * 60)
    linhas.append(titulo)
    linhas.append("=" * 60)
    linhas.append("")
    
    if not instrucoes:
        linhas.append("# Nenhuma instrução")
    else:
        for i, instrucao in enumerate(instrucoes, 1):
            linhas.append(formatar_instrucao_tac(instrucao, i))
    
    linhas.append("")
    linhas.append("=" * 60)
    linhas.append(f"Total: {len(instrucoes)} instruções")
    linhas.append("=" * 60)
    
    return "\n".join(linhas)


def gerar_tabela_comparacao(tac_original: List[Any], tac_otimizado: List[Any]) -> str:
    """
    Gera tabela comparativa entre TAC original e otimizado
    
    Args:
        tac_original: Lista de instruções TAC originais
        tac_otimizado: Lista de instruções TAC otimizadas
        
    Returns:
        String com tabela comparativa em formato Markdown
    """
    linhas = []
    linhas.append("# Comparação: TAC Original vs TAC Otimizado")
    linhas.append("")
    linhas.append("## Estatísticas")
    linhas.append("")
    linhas.append("| Métrica | Original | Otimizado | Redução |")
    linhas.append("|---------|----------|-----------|---------|")
    
    total_original = len(tac_original)
    total_otimizado = len(tac_otimizado)
    reducao = total_original - total_otimizado
    percentual = (reducao / total_original * 100) if total_original > 0 else 0
    
    linhas.append(f"| Instruções | {total_original} | {total_otimizado} | {reducao} ({percentual:.1f}%) |")
    linhas.append("")
    
    linhas.append("## TAC Original")
    linhas.append("")
    linhas.append("```")
    for i, instrucao in enumerate(tac_original, 1):
        linhas.append(f"{i:3d}. {instrucao}")
    linhas.append("```")
    linhas.append("")
    
    linhas.append("## TAC Otimizado")
    linhas.append("")
    linhas.append("```")
    for i, instrucao in enumerate(tac_otimizado, 1):
        linhas.append(f"{i:3d}. {instrucao}")
    linhas.append("```")
    linhas.append("")
    
    return "\n".join(linhas)


def exibir_tac_colorido(instrucoes: List[Any]) -> None:
    """
    Exibe instruções TAC no terminal com destaque visual
    
    Args:
        instrucoes: Lista de objetos InstrucaoTAC
    """
    print("\n" + "=" * 60)
    print("📝 THREE ADDRESS CODE (TAC)")
    print("=" * 60 + "\n")
    
    if not instrucoes:
        print("⚠️  Nenhuma instrução gerada")
    else:
        for i, instrucao in enumerate(instrucoes, 1):
            # Adicionar indicador visual por tipo
            if hasattr(instrucao, 'tipo'):
                if instrucao.tipo == 'ATRIBUICAO':
                    prefixo = "📌"
                elif instrucao.tipo == 'OPERACAO':
                    prefixo = "🔢"
                elif instrucao.tipo == 'ROTULO':
                    prefixo = "🏷️ "
                elif instrucao.tipo in ['GOTO', 'IF', 'IF_FALSE']:
                    prefixo = "➡️ "
                else:
                    prefixo = "  "
            else:
                prefixo = "  "
            
            print(f"{prefixo} {i:3d}. {instrucao}")
    
    print("\n" + "=" * 60)
    print(f"Total: {len(instrucoes)} instruções")
    print("=" * 60 + "\n")


def salvar_documentacao_tac(instrucoes: List[Any], nome_arquivo: str, 
                            titulo: str = "Código TAC") -> None:
    """
    Salva documentação do TAC em formato Markdown
    
    Args:
        instrucoes: Lista de objetos InstrucaoTAC
        nome_arquivo: Caminho do arquivo de saída
        titulo: Título do documento
    """
    linhas = []
    linhas.append(f"# {titulo}")
    linhas.append("")
    linhas.append("## Código Three Address Code (TAC)")
    linhas.append("")
    linhas.append("```")
    
    if not instrucoes:
        linhas.append("# Nenhuma instrução gerada")
    else:
        for i, instrucao in enumerate(instrucoes, 1):
            linhas.append(f"{i:3d}. {instrucao}")
    
    linhas.append("```")
    linhas.append("")
    linhas.append("## Estatísticas")
    linhas.append("")
    linhas.append(f"- **Total de instruções:** {len(instrucoes)}")
    
    # Contar tipos de instrução
    tipos_count: Dict[str, int] = {}
    for instrucao in instrucoes:
        if hasattr(instrucao, 'tipo'):
            tipo = instrucao.tipo
            tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
    
    if tipos_count:
        linhas.append("- **Instruções por tipo:**")
        for tipo, count in sorted(tipos_count.items()):
            linhas.append(f"  - {tipo}: {count}")
    
    linhas.append("")
    
    # Salvar arquivo
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write("\n".join(linhas))
        print(f"✓ Documentação TAC salva em: {nome_arquivo}")
    except Exception as e:
        print(f"✗ Erro ao salvar documentação: {e}")


def gerar_estatisticas_detalhadas(instrucoes: List[Any]) -> Dict[str, Any]:
    """
    Gera estatísticas detalhadas sobre o código TAC
    
    Args:
        instrucoes: Lista de objetos InstrucaoTAC
        
    Returns:
        Dicionário com estatísticas
    """
    stats = {
        'total_instrucoes': len(instrucoes),
        'tipos': {},
        'temporarios': set(),
        'rotulos': set(),
        'variaveis': set()
    }
    
    for instrucao in instrucoes:
        if not hasattr(instrucao, 'tipo'):
            continue
        
        # Contar tipos
        tipo = instrucao.tipo
        stats['tipos'][tipo] = stats['tipos'].get(tipo, 0) + 1
        
        # Coletar temporários, rótulos e variáveis
        if hasattr(instrucao, 'resultado') and instrucao.resultado:
            if instrucao.resultado.startswith('t'):
                stats['temporarios'].add(instrucao.resultado)
            elif instrucao.resultado.startswith('L'):
                stats['rotulos'].add(instrucao.resultado)
            else:
                stats['variaveis'].add(instrucao.resultado)
        
        if hasattr(instrucao, 'operando1') and instrucao.operando1:
            if instrucao.operando1.startswith('t'):
                stats['temporarios'].add(instrucao.operando1)
            elif not instrucao.operando1[0].isdigit():
                stats['variaveis'].add(instrucao.operando1)
        
        if hasattr(instrucao, 'operando2') and instrucao.operando2:
            if instrucao.operando2.startswith('t'):
                stats['temporarios'].add(instrucao.operando2)
            elif not instrucao.operando2[0].isdigit():
                stats['variaveis'].add(instrucao.operando2)
    
    # Converter sets para contagem
    stats['total_temporarios'] = len(stats['temporarios'])
    stats['total_rotulos'] = len(stats['rotulos'])
    stats['total_variaveis'] = len(stats['variaveis'])
    
    return stats


def imprimir_estatisticas_detalhadas(stats: Dict[str, Any]) -> None:
    """
    Imprime estatísticas detalhadas de forma formatada
    
    Args:
        stats: Dicionário com estatísticas (retornado por gerar_estatisticas_detalhadas)
    """
    print("\n" + "=" * 60)
    print("📊 ESTATÍSTICAS DETALHADAS DO TAC")
    print("=" * 60)
    
    print(f"\nTotal de instruções:  {stats['total_instrucoes']}")
    print(f"Temporários únicos:   {stats['total_temporarios']}")
    print(f"Rótulos únicos:       {stats['total_rotulos']}")
    print(f"Variáveis únicas:     {stats['total_variaveis']}")
    
    if stats['tipos']:
        print("\nInstruções por tipo:")
        for tipo, count in sorted(stats['tipos'].items()):
            percentual = (count / stats['total_instrucoes'] * 100) if stats['total_instrucoes'] > 0 else 0
            print(f"  • {tipo:20s}: {count:3d} ({percentual:5.1f}%)")
    
    print("=" * 60 + "\n")


# Teste do módulo
if __name__ == '__main__':
    print("Módulo formatador_tac.py carregado com sucesso!")
    print("\nFunções disponíveis:")
    print("  • formatar_instrucao_tac()")
    print("  • formatar_lista_tac()")
    print("  • gerar_tabela_comparacao()")
    print("  • exibir_tac_colorido()")
    print("  • salvar_documentacao_tac()")
    print("  • gerar_estatisticas_detalhadas()")
    print("  • imprimir_estatisticas_detalhadas()")