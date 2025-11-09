# analisador semantico - validacao de estruturas de controle (IF, WHILE)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.token_types import *
from src.tabela_simbolos import *
from src.analisador_tipos import ErroSemantico

def analisar_semantica_controle(arvore_sintatica, tabela_simbolos):
    """
    valida estruturas de controle (IF, WHILE)
    
    Args:
        arvore_sintatica (dict): arvore ja anotada com tipos
        tabela_simbolos (dict): tabela de simbolos
        
    Returns:
        list: lista de erros encontrados
    """
    erros = []
    
    try:
        # percorrer arvore validando estruturas de controle
        validar_estruturas_controle(arvore_sintatica, tabela_simbolos, erros)
        
        return erros
        
    except Exception as e:
        erros.append({
            'tipo': 'ERRO_INTERNO',
            'mensagem': f"Erro interno na análise de controle: {str(e)}",
            'linha': None
        })
        return erros

def validar_estruturas_controle(no, tabela_simbolos, erros):
    """
    percorre arvore validando estruturas de controle
    
    Args:
        no (dict): no da arvore
        tabela_simbolos (dict): tabela de simbolos
        erros (list): lista de erros encontrados
    """
    if not no:
        return
    
    tipo_no = no.get('tipo')
    
    # validar estrutura especifica
    if tipo_no == 'DECISAO':
        erro = validar_estrutura_decisao(no, tabela_simbolos)
        if erro:
            erros.append(erro)
    
    elif tipo_no == 'LACO':
        erro = validar_estrutura_laco(no, tabela_simbolos)
        if erro:
            erros.append(erro)
    
    # recursao nos filhos
    for filho in no.get('filhos', []):
        validar_estruturas_controle(filho, tabela_simbolos, erros)

def validar_estrutura_decisao(no, tabela_simbolos):
    """
    valida estrutura IF
    
    Sintaxe RPN: (operando1 operando2 op_rel (bloco_v) (bloco_f) IF)
    
    Args:
        no (dict): no DECISAO
        tabela_simbolos (dict): tabela de simbolos
        
    Returns:
        dict ou None: erro se invalido
    """
    filhos = no.get('filhos', [])
    linha = no.get('linha')
    
    # estrutura esperada: [condicao, bloco_verdadeiro, bloco_falso]
    if len(filhos) < 3:
        return {
            'tipo': 'ERRO_CONTROLE',
            'mensagem': 'Estrutura IF mal formada: faltam componentes',
            'linha': linha,
            'contexto': f'esperados 3 filhos (condição, bloco_v, bloco_f), encontrados {len(filhos)}'
        }
    
    condicao_no = filhos[0]
    bloco_v_no = filhos[1]
    bloco_f_no = filhos[2]
    
    # validar condicao
    erro_condicao = validar_condicao(condicao_no, tabela_simbolos)
    if erro_condicao:
        erro_condicao['contexto'] = 'IF: ' + erro_condicao.get('contexto', '')
        return erro_condicao
    
    # validar que blocos sao expressoes validas
    if bloco_v_no.get('tipo') != 'EXPRESSAO':
        return {
            'tipo': 'ERRO_CONTROLE',
            'mensagem': f"IF: bloco verdadeiro deve ser EXPRESSAO, encontrado '{bloco_v_no.get('tipo')}'",
            'linha': linha,
            'contexto': 'bloco verdadeiro'
        }
    
    if bloco_f_no.get('tipo') != 'EXPRESSAO':
        return {
            'tipo': 'ERRO_CONTROLE',
            'mensagem': f"IF: bloco falso deve ser EXPRESSAO, encontrado '{bloco_f_no.get('tipo')}'",
            'linha': linha,
            'contexto': 'bloco falso'
        }
    
    # verificar compatibilidade de tipos dos blocos (opcional, mas recomendado)
    tipo_v = bloco_v_no.get('tipo_inferido')
    tipo_f = bloco_f_no.get('tipo_inferido')
    
    if tipo_v and tipo_f and tipo_v != tipo_f and tipo_v != 'erro' and tipo_f != 'erro':
        # aviso: blocos com tipos diferentes (nao e erro fatal)
        return {
            'tipo': 'AVISO_CONTROLE',
            'mensagem': f"IF: blocos com tipos diferentes (verdadeiro: {tipo_v}, falso: {tipo_f})",
            'linha': linha,
            'contexto': 'compatibilidade de tipos'
        }
    
    return None  # sem erro

def validar_estrutura_laco(no, tabela_simbolos):
    """
    valida estrutura WHILE
    
    Sintaxe RPN: (operando1 operando2 op_rel (bloco) WHILE)
    
    Args:
        no (dict): no LACO
        tabela_simbolos (dict): tabela de simbolos
        
    Returns:
        dict ou None: erro se invalido
    """
    filhos = no.get('filhos', [])
    linha = no.get('linha')
    
    # estrutura esperada: [condicao, bloco]
    if len(filhos) < 2:
        return {
            'tipo': 'ERRO_CONTROLE',
            'mensagem': 'Estrutura WHILE mal formada: faltam componentes',
            'linha': linha,
            'contexto': f'esperados 2 filhos (condição, bloco), encontrados {len(filhos)}'
        }
    
    condicao_no = filhos[0]
    bloco_no = filhos[1]
    
    # validar condicao
    erro_condicao = validar_condicao(condicao_no, tabela_simbolos)
    if erro_condicao:
        erro_condicao['contexto'] = 'WHILE: ' + erro_condicao.get('contexto', '')
        return erro_condicao
    
    # validar que bloco e expressao valida
    if bloco_no.get('tipo') != 'EXPRESSAO':
        return {
            'tipo': 'ERRO_CONTROLE',
            'mensagem': f"WHILE: bloco deve ser EXPRESSAO, encontrado '{bloco_no.get('tipo')}'",
            'linha': linha,
            'contexto': 'bloco de repetição'
        }
    
    return None  # sem erro

def validar_condicao(condicao_no, tabela_simbolos):
    """
    valida que condicao retorna booleano
    
    Args:
        condicao_no (dict): no de condicao
        tabela_simbolos (dict): tabela de simbolos
        
    Returns:
        dict ou None: erro se invalido
    """
    linha = condicao_no.get('linha')
    tipo_condicao = condicao_no.get('tipo_inferido')
    
    # condicao deve ter tipo booleano
    if tipo_condicao != 'booleano':
        tipo_no = condicao_no.get('tipo')
        
        return {
            'tipo': 'ERRO_CONTROLE',
            'mensagem': f"Condição deve retornar booleano, encontrado '{tipo_condicao}'",
            'linha': linha,
            'contexto': f'tipo do no: {tipo_no}'
        }
    
    # verificar que e uma operacao relacional
    if condicao_no.get('tipo') != 'CONDICAO':
        return {
            'tipo': 'ERRO_CONTROLE',
            'mensagem': f"Esperada operação relacional, encontrado '{condicao_no.get('tipo')}'",
            'linha': linha,
            'contexto': 'condicao de controle'
        }
    
    # validar operador relacional
    operador = condicao_no.get('operador')
    operadores_validos = ['>', '<', '>=', '<=', '==', '!=']
    
    if operador not in operadores_validos:
        return {
            'tipo': 'ERRO_CONTROLE',
            'mensagem': f"Operador relacional inválido: '{operador}'",
            'linha': linha,
            'contexto': f'esperados: {operadores_validos}'
        }
    
    # validar operandos da condicao
    filhos = condicao_no.get('filhos', [])
    if len(filhos) < 2:
        return {
            'tipo': 'ERRO_CONTROLE',
            'mensagem': 'Condição mal formada: faltam operandos',
            'linha': linha,
            'contexto': f'esperados 2 operandos, encontrados {len(filhos)}'
        }
    
    tipo1 = filhos[0].get('tipo_inferido')
    tipo2 = filhos[1].get('tipo_inferido')
    
    # operandos devem ser numericos
    if tipo1 not in ['int', 'real'] or tipo2 not in ['int', 'real']:
        return {
            'tipo': 'ERRO_CONTROLE',
            'mensagem': f"Operandos de condição devem ser numéricos, encontrados '{tipo1}' e '{tipo2}'",
            'linha': linha,
            'contexto': f'operador: {operador}'
        }
    
    return None  # sem erro

def validar_aninhamento_controle(arvore):
    """
    valida aninhamento de estruturas de controle
    
    Args:
        arvore (dict): arvore sintatica
        
    Returns:
        list: lista de avisos sobre aninhamento profundo
    """
    avisos = []
    
    def contar_profundidade(no, nivel=0):
        if not no:
            return nivel
        
        tipo_no = no.get('tipo')
        novo_nivel = nivel
        
        if tipo_no in ['DECISAO', 'LACO']:
            novo_nivel = nivel + 1
            
            # avisar se aninhamento muito profundo
            if novo_nivel > 3:
                avisos.append({
                    'tipo': 'AVISO_CONTROLE',
                    'mensagem': f'Aninhamento profundo de estruturas de controle (nível {novo_nivel})',
                    'linha': no.get('linha'),
                    'contexto': f'tipo: {tipo_no}'
                })
        
        max_prof = novo_nivel
        for filho in no.get('filhos', []):
            prof_filho = contar_profundidade(filho, novo_nivel)
            max_prof = max(max_prof, prof_filho)
        
        return max_prof
    
    profundidade = contar_profundidade(arvore)
    return avisos

def gerar_relatorio_controle(erros, avisos=None):
    """
    gera relatorio de analise de estruturas de controle
    
    Args:
        erros (list): lista de erros encontrados
        avisos (list): lista de avisos (opcional)
        
    Returns:
        str: relatorio formatado
    """
    relatorio = "# Relatorio de Analise de Estruturas de Controle\n\n"
    
    # estatisticas
    erros_criticos = [e for e in erros if e['tipo'] == 'ERRO_CONTROLE']
    avisos_controle = [e for e in erros if e['tipo'] == 'AVISO_CONTROLE']
    
    relatorio += "## Estatisticas\n\n"
    relatorio += f"- Erros criticos: {len(erros_criticos)}\n"
    relatorio += f"- Avisos: {len(avisos_controle)}\n"
    relatorio += f"- Total de problemas: {len(erros)}\n\n"
    
    # erros criticos
    if erros_criticos:
        relatorio += "## Erros Criticos\n\n"
        for i, erro in enumerate(erros_criticos, 1):
            linha_str = f"Linha {erro['linha']}" if erro['linha'] else "Linha ?"
            relatorio += f"### Erro {i} [{linha_str}]\n\n"
            relatorio += f"**Mensagem**: {erro['mensagem']}\n\n"
            if erro.get('contexto'):
                relatorio += f"**Contexto**: {erro['contexto']}\n\n"
    
    # avisos
    if avisos_controle:
        relatorio += "## Avisos\n\n"
        for i, aviso in enumerate(avisos_controle, 1):
            linha_str = f"Linha {aviso['linha']}" if aviso['linha'] else "Linha ?"
            relatorio += f"### Aviso {i} [{linha_str}]\n\n"
            relatorio += f"**Mensagem**: {aviso['mensagem']}\n\n"
            if aviso.get('contexto'):
                relatorio += f"**Contexto**: {aviso['contexto']}\n\n"
    
    if not erros_criticos and not avisos_controle:
        relatorio += "## Nenhum problema encontrado nas estruturas de controle\n\n"
    
    return relatorio

if __name__ == '__main__':
    # teste do analisador de controle
    print("=== TESTE DO ANALISADOR DE ESTRUTURAS DE CONTROLE ===\n")
    
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
        
        # testar estruturas de controle
        testes = [
            ("((5 10 >) ((5)) ((10)) IF)", "IF com condicao valida"),
            ("((5 10 <) ((5 1 +) CONTADOR) WHILE)", "WHILE com condicao valida")
        ]
        
        for expr, descricao in testes:
            print(f"Testando: {descricao}")
            print(f"  Expressao: {expr}")
            
            # analise lexica e sintatica
            tokens = parse_expressao(expr)
            resultado_parser = parsear(tokens, tabela)
            arvore = gerar_arvore(resultado_parser['derivacao'])
            
            # analise de tipos
            arvore_anotada, erros_tipo = analisar_semantica(arvore, gramatica_atributos, tabela_simbolos)
            
            # analise de controle
            erros_controle = analisar_semantica_controle(arvore_anotada, tabela_simbolos)
            
            if erros_controle:
                print(f"  Erros: {len(erros_controle)}")
                for erro in erros_controle:
                    print(f"    - {erro['mensagem']}")
            else:
                print(f"  Estrutura valida")
            
            print()
        
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()