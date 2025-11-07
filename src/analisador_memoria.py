# analisador semântico - validação de memórias e comandos especiais

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.token_types import *
from src.tabela_simbolos import *
from src.analisador_tipos import ErroSemantico

def analisar_semantica_memoria(arvore_sintatica, tabela_simbolos):
    """
    valida uso de memórias (MEM, VAR, etc)
    
    Args:
        arvore_sintatica (dict): árvore já anotada com tipos
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        tuple: (tabela_atualizada, lista_erros)
    """
    erros = []
    
    try:
        # percorrer árvore validando comandos de memória
        validar_comandos_memoria(arvore_sintatica, tabela_simbolos, erros)
        
        return tabela_simbolos, erros
        
    except Exception as e:
        erros.append({
            'tipo': 'ERRO_INTERNO',
            'mensagem': f"Erro interno na análise de memória: {str(e)}",
            'linha': None
        })
        return tabela_simbolos, erros

def validar_comandos_memoria(no, tabela_simbolos, erros):
    """
    percorre árvore validando comandos de memória
    
    Args:
        no (dict): nó da árvore
        tabela_simbolos (dict): tabela de símbolos
        erros (list): lista de erros encontrados
    """
    if not no:
        return
    
    tipo_no = no.get('tipo')
    
    # validar comando específico
    if tipo_no == 'COMANDO_ARMAZENAR':
        erro = validar_comando_armazenar(no, tabela_simbolos)
        if erro:
            erros.append(erro)
    
    elif tipo_no == 'COMANDO_RECUPERAR':
        erro = validar_comando_recuperar(no, tabela_simbolos)
        if erro:
            erros.append(erro)
    
    elif tipo_no == 'COMANDO_RES':
        erro = validar_comando_res(no, tabela_simbolos)
        if erro:
            erros.append(erro)
    
    # recursão nos filhos
    for filho in no.get('filhos', []):
        validar_comandos_memoria(filho, tabela_simbolos, erros)

def validar_comando_armazenar(no, tabela_simbolos):
    """
    valida comando (V MEM)
    
    Args:
        no (dict): nó COMANDO_ARMAZENAR
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        dict ou None: erro se inválido
    """
    filhos = no.get('filhos', [])
    linha = no.get('linha')
    
    if len(filhos) < 2:
        return {
            'tipo': 'ERRO_MEMORIA',
            'mensagem': 'Comando de armazenamento mal formado',
            'linha': linha,
            'contexto': 'faltam operandos'
        }
    
    valor_no = filhos[0]
    identificador_no = filhos[1]
    
    nome = identificador_no.get('valor')
    tipo_valor = valor_no.get('tipo_inferido')
    
    # validar tipo do valor
    if tipo_valor not in ['int', 'real']:
        return {
            'tipo': 'ERRO_MEMORIA',
            'mensagem': f"Valor inválido para armazenamento: tipo '{tipo_valor}'",
            'linha': linha,
            'contexto': f"({nome})"
        }
    
    # adicionar ou atualizar na tabela de símbolos
    try:
        if simbolo_existe(tabela_simbolos, nome):
            # atualizar símbolo existente
            atualizar_simbolo(tabela_simbolos, nome, 
                            tipo=tipo_valor, 
                            inicializada=True,
                            linha_declaracao=linha)
        else:
            # adicionar novo símbolo
            adicionar_simbolo(tabela_simbolos, nome, tipo_valor, 
                            valor=None, linha=linha)
            atualizar_simbolo(tabela_simbolos, nome, inicializada=True)
        
        return None  # sem erro
        
    except TabelaSimbolosError as e:
        return {
            'tipo': 'ERRO_MEMORIA',
            'mensagem': str(e),
            'linha': linha,
            'contexto': f"({nome})"
        }

def validar_comando_recuperar(no, tabela_simbolos):
    """
    valida comando (MEM) - AGORA ERRO SE NÃO INICIALIZADA
    
    Args:
        no (dict): nó COMANDO_RECUPERAR
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        dict ou None: erro se inválido
    """
    filhos = no.get('filhos', [])
    linha = no.get('linha')
    
    if len(filhos) < 1:
        return {
            'tipo': 'ERRO_MEMORIA',
            'mensagem': 'Comando de recuperação mal formado',
            'linha': linha,
            'contexto': 'falta identificador'
        }
    
    identificador_no = filhos[0]
    nome = identificador_no.get('valor')
    
    # verificar se símbolo existe
    if not simbolo_existe(tabela_simbolos, nome):
        return {
            'tipo': 'ERRO_MEMORIA',
            'mensagem': f"Memória '{nome}' não declarada",
            'linha': linha,
            'contexto': f"({nome})"
        }
    
    # verificar se foi inicializada (MUDANÇA DA FASE 2)
    try:
        if not simbolo_inicializado(tabela_simbolos, nome):
            return {
                'tipo': 'ERRO_MEMORIA',
                'mensagem': f"Memória '{nome}' utilizada sem inicialização",
                'linha': linha,
                'contexto': f"({nome})"
            }
    except TabelaSimbolosError as e:
        return {
            'tipo': 'ERRO_MEMORIA',
            'mensagem': str(e),
            'linha': linha,
            'contexto': f"({nome})"
        }
    
    return None  # sem erro

def validar_comando_res(no, tabela_simbolos):
    """
    valida comando (N RES)
    
    Args:
        no (dict): nó COMANDO_RES
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        dict ou None: erro se inválido
    """
    filhos = no.get('filhos', [])
    linha = no.get('linha')
    
    if len(filhos) < 1:
        return {
            'tipo': 'ERRO_MEMORIA',
            'mensagem': 'Comando RES mal formado',
            'linha': linha,
            'contexto': 'falta valor N'
        }
    
    n_no = filhos[0]
    tipo_n = n_no.get('tipo_inferido')
    
    # N deve ser inteiro
    if tipo_n != 'int':
        return {
            'tipo': 'ERRO_MEMORIA',
            'mensagem': f"Comando RES requer N inteiro, encontrado '{tipo_n}'",
            'linha': linha,
            'contexto': f"(N RES)"
        }
    
    try:
        n = int(float(n_no.get('valor', 0)))
        
        # N deve ser positivo
        if n < 1:
            return {
                'tipo': 'ERRO_MEMORIA',
                'mensagem': f"Comando RES requer N >= 1, encontrado {n}",
                'linha': linha,
                'contexto': f"({n} RES)"
            }
        
        # verificar se há resultados suficientes no histórico
        tamanho_historico = len(tabela_simbolos['historico_resultados'])
        if n > tamanho_historico:
            return {
                'tipo': 'ERRO_MEMORIA',
                'mensagem': f"RES: não há resultado {n} linhas atrás (histórico: {tamanho_historico})",
                'linha': linha,
                'contexto': f"({n} RES)"
            }
        
    except (ValueError, TypeError) as e:
        return {
            'tipo': 'ERRO_MEMORIA',
            'mensagem': f"Valor inválido para N em RES: {str(e)}",
            'linha': linha,
            'contexto': f"({n_no.get('valor')} RES)"
        }
    
    return None  # sem erro

def validar_uso_identificadores(arvore, tabela_simbolos):
    """
    valida que todos identificadores usados estão declarados
    
    Args:
        arvore (dict): árvore sintática
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        list: lista de erros encontrados
    """
    erros = []
    
    def verificar_no(no):
        if not no:
            return
        
        tipo_no = no.get('tipo')
        
        # identificador em operação ou expressão
        if tipo_no == 'IDENTIFICADOR':
            nome = no.get('valor')
            linha = no.get('linha')
            
            # verificar se não é parte de comando de armazenamento
            # (nesses casos, o identificador será declarado)
            pai = no.get('pai')  # assumindo que adicionamos referência ao pai
            
            if not simbolo_existe(tabela_simbolos, nome):
                erros.append({
                    'tipo': 'ERRO_MEMORIA',
                    'mensagem': f"Identificador '{nome}' não declarado",
                    'linha': linha,
                    'contexto': f"({nome})"
                })
        
        # recursão
        for filho in no.get('filhos', []):
            verificar_no(filho)
    
    verificar_no(arvore)
    return erros

def gerar_relatorio_memoria(tabela_simbolos, erros):
    """
    gera relatório de análise de memória
    
    Args:
        tabela_simbolos (dict): tabela de símbolos
        erros (list): lista de erros encontrados
        
    Returns:
        str: relatório formatado
    """
    relatorio = "# Relatório de Análise de Memória\n\n"
    
    # estatísticas
    total_simbolos = len(tabela_simbolos['simbolos'])
    simbolos_inicializados = sum(1 for s in tabela_simbolos['simbolos'].values() if s['inicializada'])
    
    relatorio += "## Estatísticas\n\n"
    relatorio += f"- Total de símbolos: {total_simbolos}\n"
    relatorio += f"- Símbolos inicializados: {simbolos_inicializados}\n"
    relatorio += f"- Símbolos não inicializados: {total_simbolos - simbolos_inicializados}\n"
    relatorio += f"- Tamanho do histórico: {len(tabela_simbolos['historico_resultados'])}\n"
    relatorio += f"- Erros encontrados: {len(erros)}\n\n"
    
    # tabela de símbolos
    if total_simbolos > 0:
        relatorio += "## Tabela de Símbolos\n\n"
        relatorio += "| Nome | Tipo | Inicializada | Linha | Escopo |\n"
        relatorio += "|------|------|--------------|-------|--------|\n"
        
        for nome, info in sorted(tabela_simbolos['simbolos'].items()):
            inicializada = '✓' if info['inicializada'] else '✗'
            linha = info['linha_declaracao'] if info['linha_declaracao'] else '-'
            relatorio += f"| {nome} | {info['tipo']} | {inicializada} | {linha} | {info['escopo']} |\n"
        
        relatorio += "\n"
    
    # erros
    if erros:
        relatorio += "## Erros Semânticos - Memória\n\n"
        for i, erro in enumerate(erros, 1):
            linha_str = f"Linha {erro['linha']}" if erro['linha'] else "Linha ?"
            relatorio += f"### Erro {i} [{linha_str}]\n\n"
            relatorio += f"**Tipo**: {erro['tipo']}\n\n"
            relatorio += f"**Mensagem**: {erro['mensagem']}\n\n"
            if erro.get('contexto'):
                relatorio += f"**Contexto**: `{erro['contexto']}`\n\n"
    else:
        relatorio += "## ✓ Nenhum erro de memória encontrado\n\n"
    
    return relatorio

if __name__ == '__main__':
    # teste do analisador de memória
    print("=== TESTE DO ANALISADOR DE MEMÓRIA ===\n")
    
    from src.lexer import parse_expressao
    from src.parser import parsear
    from src.grammar import construir_gramatica
    from src.syntax_tree import gerar_arvore
    from src.gramatica_atributos import definir_gramatica_atributos
    from src.analisador_tipos import analisar_semantica
    
    try:
        # construir infraestrutura
        gramatica_info = construir_gramatica()
        tabela = gramatica_info['tabela']
        gramatica_atributos = definir_gramatica_atributos()
        tabela_simbolos = inicializar_tabela_simbolos()
        
        # testar comandos de memória
        testes = [
            ("(42 MEM)", "armazenar valor"),
            ("(MEM)", "recuperar valor (deve dar erro - não inicializado)"),
            ("(1 RES)", "RES sem histórico (deve dar erro)")
        ]
        
        for expr, descricao in testes:
            print(f"Testando: {expr} - {descricao}")
            
            # análise léxica e sintática
            tokens = parse_expressao(expr)
            resultado_parser = parsear(tokens, tabela)
            arvore = gerar_arvore(resultado_parser['derivacao'])
            
            # análise de tipos
            arvore_anotada, erros_tipo = analisar_semantica(arvore, gramatica_atributos, tabela_simbolos)
            
            # análise de memória
            tabela_simbolos, erros_memoria = analisar_semantica_memoria(arvore_anotada, tabela_simbolos)
            
            if erros_memoria:
                print(f"  ✗ Erros de memória: {len(erros_memoria)}")
                for erro in erros_memoria:
                    print(f"    - {erro['mensagem']}")
            else:
                print(f"  ✓ Sem erros de memória")
            
            print()
        
        # imprimir relatório
        print(imprimir_tabela(tabela_simbolos))
        
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()