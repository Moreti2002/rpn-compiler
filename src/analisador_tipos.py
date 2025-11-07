# analisador semântico - verificação de tipos

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.token_types import *
from src.gramatica_atributos import definir_gramatica_atributos, promover_tipo, obter_regra_semantica
from src.tabela_simbolos import *

class ErroSemantico(Exception):
    """exceção para erros semânticos"""
    def __init__(self, mensagem, linha=None, contexto=None):
        self.mensagem = mensagem
        self.linha = linha
        self.contexto = contexto
        contexto_str = f"\nContexto: {contexto}" if contexto else ""
        linha_str = f" [Linha {linha}]" if linha else ""
        super().__init__(f"ERRO SEMÂNTICO{linha_str}: {mensagem}{contexto_str}")

def analisar_semantica(arvore_sintatica, gramatica_atributos, tabela_simbolos):
    """
    análise semântica principal - verificação de tipos
    
    Args:
        arvore_sintatica (dict): AST da Fase 2
        gramatica_atributos (dict): regras semânticas
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        tuple: (arvore_anotada, lista_erros)
    """
    erros = []
    
    try:
        # percorrer árvore em pós-ordem para inferir tipos
        arvore_anotada = anotar_tipos_arvore(arvore_sintatica, tabela_simbolos, erros)
        
        return arvore_anotada, erros
        
    except Exception as e:
        erros.append({
            'tipo': 'ERRO_INTERNO',
            'mensagem': str(e),
            'linha': None
        })
        return arvore_sintatica, erros

def anotar_tipos_arvore(no, tabela_simbolos, erros, linha_atual=1):
    """
    percorre árvore anotando tipos (pós-ordem)
    
    Args:
        no (dict): nó da árvore
        tabela_simbolos (dict): tabela de símbolos
        erros (list): lista de erros encontrados
        linha_atual (int): linha atual do código
        
    Returns:
        dict: nó anotado com tipo
    """
    if not no:
        return no
    
    # adicionar linha ao nó se não tiver
    if 'linha' not in no:
        no['linha'] = linha_atual
    
    # processar filhos primeiro (pós-ordem)
    if 'filhos' in no and no['filhos']:
        for i, filho in enumerate(no['filhos']):
            no['filhos'][i] = anotar_tipos_arvore(filho, tabela_simbolos, erros, no.get('linha', linha_atual))
    
    # inferir tipo do nó atual
    try:
        tipo = inferir_tipo_no(no, tabela_simbolos, erros)
        no['tipo_inferido'] = tipo
    except ErroSemantico as e:
        erros.append({
            'tipo': 'ERRO_TIPO',
            'mensagem': e.mensagem,
            'linha': e.linha or no.get('linha'),
            'contexto': e.contexto
        })
        no['tipo_inferido'] = 'erro'
    
    return no

def inferir_tipo_no(no, tabela_simbolos, erros):
    """
    infere tipo de um nó da árvore
    
    Args:
        no (dict): nó da árvore
        tabela_simbolos (dict): tabela de símbolos
        erros (list): lista de erros
        
    Returns:
        str: tipo inferido ('int', 'real', 'booleano')
        
    Raises:
        ErroSemantico: se erro de tipo detectado
    """
    tipo_no = no.get('tipo')
    
    if tipo_no == 'NUMERO':
        return inferir_tipo_numero(no)
    
    elif tipo_no == 'IDENTIFICADOR':
        return inferir_tipo_identificador(no, tabela_simbolos)
    
    elif tipo_no == 'OPERACAO':
        return inferir_tipo_operacao(no, tabela_simbolos)
    
    elif tipo_no == 'CONDICAO':
        return inferir_tipo_condicao(no, tabela_simbolos)
    
    elif tipo_no == 'EXPRESSAO':
        # expressão herda tipo do filho
        if no.get('filhos') and len(no['filhos']) > 0:
            return no['filhos'][0].get('tipo_inferido', 'erro')
        return 'erro'
    
    elif tipo_no in ['COMANDO_ARMAZENAR', 'COMANDO_RECUPERAR', 'COMANDO_RES']:
        return inferir_tipo_comando(no, tabela_simbolos)
    
    elif tipo_no in ['DECISAO', 'LACO']:
        # estruturas de controle retornam tipo do bloco
        return inferir_tipo_estrutura_controle(no, tabela_simbolos)
    
    else:
        # tipo desconhecido - não anotar
        return None

def inferir_tipo_numero(no):
    """
    infere tipo de um número literal
    
    Args:
        no (dict): nó NUMERO
        
    Returns:
        str: 'int' ou 'real'
    """
    valor = no.get('valor', '')
    
    # verificar se tem ponto decimal
    if '.' in valor:
        return 'real'
    else:
        return 'int'

def inferir_tipo_identificador(no, tabela_simbolos):
    """
    infere tipo de um identificador (memória)
    
    Args:
        no (dict): nó IDENTIFICADOR
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        str: tipo do símbolo
        
    Raises:
        ErroSemantico: se identificador não declarado
    """
    nome = no.get('valor')
    
    if not simbolo_existe(tabela_simbolos, nome):
        raise ErroSemantico(
            f"Identificador '{nome}' não declarado",
            linha=no.get('linha'),
            contexto=f"({nome})"
        )
    
    return obter_tipo_simbolo(tabela_simbolos, nome)

def inferir_tipo_operacao(no, tabela_simbolos):
    """
    infere tipo de uma operação aritmética
    
    Args:
        no (dict): nó OPERACAO
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        str: tipo resultante da operação
        
    Raises:
        ErroSemantico: se tipos incompatíveis
    """
    operador = no.get('operador')
    filhos = no.get('filhos', [])
    
    if len(filhos) < 2:
        raise ErroSemantico(
            f"Operação '{operador}' requer 2 operandos",
            linha=no.get('linha')
        )
    
    tipo1 = filhos[0].get('tipo_inferido')
    tipo2 = filhos[1].get('tipo_inferido')
    
    # validar operação específica
    return validar_operacao_aritmetica(operador, tipo1, tipo2, no.get('linha'))

def validar_operacao_aritmetica(operador, tipo1, tipo2, linha):
    """
    valida operação aritmética e retorna tipo resultado
    
    Args:
        operador (str): operador (+, -, *, |, /, %, ^)
        tipo1 (str): tipo do primeiro operando
        tipo2 (str): tipo do segundo operando
        linha (int): linha do código
        
    Returns:
        str: tipo resultante
        
    Raises:
        ErroSemantico: se operação inválida
    """
    # verificar se tipos são numéricos
    if tipo1 not in ['int', 'real'] or tipo2 not in ['int', 'real']:
        raise ErroSemantico(
            f"Operação '{operador}' requer operandos numéricos",
            linha=linha,
            contexto=f"tipos: {tipo1}, {tipo2}"
        )
    
    # regras específicas por operador
    if operador == '|':
        # divisão real sempre retorna real
        return 'real'
    
    elif operador in ['/', '%']:
        # divisão inteira e resto requerem ambos inteiros
        if tipo1 != 'int' or tipo2 != 'int':
            raise ErroSemantico(
                f"Operador '{operador}' requer operandos inteiros",
                linha=linha,
                contexto=f"tipos: {tipo1}, {tipo2}"
            )
        return 'int'
    
    elif operador == '^':
        # potência: expoente deve ser inteiro
        if tipo2 != 'int':
            raise ErroSemantico(
                "Expoente de potenciação deve ser inteiro",
                linha=linha,
                contexto=f"tipo do expoente: {tipo2}"
            )
        # resultado tem tipo da base
        return tipo1
    
    else:
        # +, -, * : promover tipo
        return promover_tipo(tipo1, tipo2)

def inferir_tipo_condicao(no, tabela_simbolos):
    """
    infere tipo de uma condição (operação relacional)
    
    Args:
        no (dict): nó CONDICAO
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        str: 'booleano'
        
    Raises:
        ErroSemantico: se tipos incompatíveis
    """
    operador = no.get('operador')
    filhos = no.get('filhos', [])
    
    if len(filhos) < 2:
        raise ErroSemantico(
            f"Operador relacional '{operador}' requer 2 operandos",
            linha=no.get('linha')
        )
    
    tipo1 = filhos[0].get('tipo_inferido')
    tipo2 = filhos[1].get('tipo_inferido')
    
    # operadores relacionais requerem operandos numéricos
    if tipo1 not in ['int', 'real'] or tipo2 not in ['int', 'real']:
        raise ErroSemantico(
            f"Operador relacional '{operador}' requer operandos numéricos",
            linha=no.get('linha'),
            contexto=f"tipos: {tipo1}, {tipo2}"
        )
    
    # resultado sempre é booleano
    return 'booleano'

def inferir_tipo_comando(no, tabela_simbolos):
    """
    infere tipo de comandos especiais
    
    Args:
        no (dict): nó de comando
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        str: tipo do comando
    """
    tipo_no = no.get('tipo')
    
    if tipo_no == 'COMANDO_ARMAZENAR':
        # tipo do valor sendo armazenado
        filhos = no.get('filhos', [])
        if filhos:
            return filhos[0].get('tipo_inferido', 'erro')
        return 'erro'
    
    elif tipo_no == 'COMANDO_RECUPERAR':
        # tipo vem da tabela de símbolos
        filhos = no.get('filhos', [])
        if filhos:
            nome = filhos[0].get('valor')
            if simbolo_existe(tabela_simbolos, nome):
                return obter_tipo_simbolo(tabela_simbolos, nome)
        return 'erro'
    
    elif tipo_no == 'COMANDO_RES':
        # tipo vem do histórico
        filhos = no.get('filhos', [])
        if filhos:
            n = int(float(filhos[0].get('valor', 0)))
            try:
                res = obter_resultado_historico(tabela_simbolos, n)
                return res['tipo']
            except:
                return 'erro'
        return 'erro'
    
    return 'erro'

def inferir_tipo_estrutura_controle(no, tabela_simbolos):
    """
    infere tipo de estruturas de controle (IF/WHILE)
    
    Args:
        no (dict): nó DECISAO ou LACO
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        str: tipo do bloco
    """
    tipo_no = no.get('tipo')
    filhos = no.get('filhos', [])
    
    if tipo_no == 'DECISAO' and len(filhos) >= 2:
        # IF: retorna tipo do bloco verdadeiro
        return filhos[1].get('tipo_inferido', 'erro')
    
    elif tipo_no == 'LACO' and len(filhos) >= 2:
        # WHILE: retorna tipo do bloco
        return filhos[1].get('tipo_inferido', 'erro')
    
    return 'erro'

def verificar_compatibilidade_tipos(tipo1, tipo2, operador):
    """
    verifica se tipos são compatíveis para operação
    
    Args:
        tipo1 (str): tipo do primeiro operando
        tipo2 (str): tipo do segundo operando
        operador (str): operador da operação
        
    Returns:
        tuple: (bool_compativel, tipo_resultado)
    """
    # operadores que aceitam int e real
    operadores_numericos = ['+', '-', '*', '|', '>', '<', '>=', '<=', '==', '!=']
    
    # operadores que requerem int
    operadores_inteiros = ['/', '%']
    
    if operador in operadores_numericos:
        if tipo1 in ['int', 'real'] and tipo2 in ['int', 'real']:
            if operador == '|':
                return True, 'real'
            elif operador in ['>', '<', '>=', '<=', '==', '!=']:
                return True, 'booleano'
            else:
                return True, promover_tipo(tipo1, tipo2)
    
    elif operador in operadores_inteiros:
        if tipo1 == 'int' and tipo2 == 'int':
            return True, 'int'
    
    elif operador == '^':
        if tipo1 in ['int', 'real'] and tipo2 == 'int':
            return True, tipo1
    
    return False, None

def gerar_relatorio_julgamento_tipos(arvore_anotada):
    """
    gera relatório das regras de dedução aplicadas
    
    Args:
        arvore_anotada (dict): árvore com tipos anotados
        
    Returns:
        list: lista de regras aplicadas
    """
    regras = []
    
    def coletar_regras(no, caminho=""):
        if not no:
            return
        
        tipo_no = no.get('tipo')
        tipo_inferido = no.get('tipo_inferido')
        linha = no.get('linha', '?')
        
        if tipo_inferido and tipo_inferido != 'erro':
            regra = {
                'linha': linha,
                'tipo_no': tipo_no,
                'tipo_inferido': tipo_inferido,
                'caminho': caminho
            }
            
            if tipo_no == 'OPERACAO':
                regra['operador'] = no.get('operador')
                filhos = no.get('filhos', [])
                if len(filhos) >= 2:
                    regra['tipos_operandos'] = [
                        filhos[0].get('tipo_inferido'),
                        filhos[1].get('tipo_inferido')
                    ]
            
            regras.append(regra)
        
        # recursão nos filhos
        for i, filho in enumerate(no.get('filhos', [])):
            coletar_regras(filho, f"{caminho}/{tipo_no}[{i}]")
    
    coletar_regras(arvore_anotada)
    return regras

if __name__ == '__main__':
    # teste do analisador de tipos
    print("=== TESTE DO ANALISADOR DE TIPOS ===\n")
    
    from src.lexer import parse_expressao
    from src.parser import parsear
    from src.grammar import construir_gramatica
    from src.syntax_tree import gerar_arvore
    
    try:
        # construir infraestrutura
        gramatica_info = construir_gramatica()
        tabela = gramatica_info['tabela']
        gramatica_atributos = definir_gramatica_atributos()
        tabela_simbolos = inicializar_tabela_simbolos()
        
        # testar expressões
        testes = [
            "(3 5 +)",           # int + int = int
            "(3.5 2 +)",         # real + int = real
            "(10 2 /)",          # int / int = int (divisão inteira)
            "(10.0 2.0 |)",      # real | real = real (divisão real)
            "(2 3 ^)",           # int ^ int = int
            "(5 3 >)"            # int > int = booleano
        ]
        
        for expr in testes:
            print(f"Testando: {expr}")
            
            # análise léxica e sintática
            tokens = parse_expressao(expr)
            resultado_parser = parsear(tokens, tabela)
            arvore = gerar_arvore(resultado_parser['derivacao'])
            
            # análise semântica
            arvore_anotada, erros = analisar_semantica(arvore, gramatica_atributos, tabela_simbolos)
            
            if erros:
                print(f"  ✗ Erros: {len(erros)}")
                for erro in erros:
                    print(f"    - {erro['mensagem']}")
            else:
                tipo = arvore_anotada.get('tipo_inferido', '?')
                print(f"  ✓ Tipo inferido: {tipo}")
            
            print()
        
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()