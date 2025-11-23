# analisador sintático descendente recursivo LL(1)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.token_types import *

class ParserError(Exception):
    """exceção para erros sintáticos"""
    def __init__(self, mensagem, linha=None, posicao=None):
        self.mensagem = mensagem
        self.linha = linha
        self.posicao = posicao
        contexto = f" [linha {linha}]" if linha else ""
        contexto += f" [pos {posicao}]" if posicao else ""
        super().__init__(f"Erro sintático{contexto}: {mensagem}")

def criar_contexto_parser(tokens):
    """
    inicializa contexto do parser
    
    Args:
        tokens (list): lista de tokens
        
    Returns:
        dict: contexto com buffer, posição e pilha
    """
    return {
        'tokens': tokens,
        'posicao': 0,
        'pilha': [],
        'derivacao': []
    }

def token_atual(contexto):
    """
    retorna token atual sem avançar
    
    Args:
        contexto (dict): contexto do parser
        
    Returns:
        dict: token atual ou None se fim
    """
    pos = contexto['posicao']
    if pos < len(contexto['tokens']):
        return contexto['tokens'][pos]
    return None

def avancar_token(contexto):
    """
    avança para próximo token
    
    Args:
        contexto (dict): contexto do parser
    """
    contexto['posicao'] += 1

def match(tipo_esperado, contexto):
    """
    verifica se token atual é do tipo esperado e avança
    
    Args:
        tipo_esperado (str): tipo esperado do token
        contexto (dict): contexto do parser
        
    Returns:
        dict: token consumido
        
    Raises:
        ParserError: se token não corresponde
    """
    token = token_atual(contexto)
    
    if token is None:
        raise ParserError(f"Esperado {tipo_esperado}, encontrado fim de arquivo")
    
    if token['tipo'] != tipo_esperado:
        raise ParserError(
            f"Esperado {tipo_esperado}, encontrado {token['tipo']} ('{token['valor']}')",
            posicao=token.get('posicao')
        )
    
    avancar_token(contexto)
    return token

def match_valor(valor_esperado, contexto):
    """
    verifica se valor do token atual corresponde e avança
    
    Args:
        valor_esperado (str): valor esperado
        contexto (dict): contexto do parser
        
    Returns:
        dict: token consumido
        
    Raises:
        ParserError: se valor não corresponde
    """
    token = token_atual(contexto)
    
    if token is None:
        raise ParserError(f"Esperado '{valor_esperado}', encontrado fim de arquivo")
    
    if token['valor'] != valor_esperado:
        raise ParserError(
            f"Esperado '{valor_esperado}', encontrado '{token['valor']}'",
            posicao=token.get('posicao')
        )
    
    avancar_token(contexto)
    return token

def parsear(tokens, tabela_ll1):
    """
    função principal do parser LL(1)
    
    Args:
        tokens (list): lista de tokens
        tabela_ll1 (dict): tabela de análise LL(1)
        
    Returns:
        dict: estrutura de derivação
        
    Raises:
        ParserError: em caso de erro sintático
    """
    if not tokens:
        raise ParserError("Lista de tokens vazia")
    
    contexto = criar_contexto_parser(tokens)
    
    try:
        # inicia análise pelo símbolo inicial
        derivacao = parse_programa(contexto, tabela_ll1)
        
        # verifica se consumiu todos os tokens
        if token_atual(contexto) is not None:
            token = token_atual(contexto)
            raise ParserError(
                f"Tokens excedentes após expressão válida: '{token['valor']}'",
                posicao=token.get('posicao')
            )
        
        return {
            'derivacao': derivacao,
            'valido': True
        }
        
    except ParserError:
        raise
    except Exception as e:
        raise ParserError(f"Erro interno do parser: {str(e)}")

def parse_programa(contexto, tabela):
    """
    analisa PROGRAMA -> EXPRESSAO
    
    Args:
        contexto (dict): contexto do parser
        tabela (dict): tabela LL(1)
        
    Returns:
        dict: nó da derivação
    """
    return parse_expressao(contexto, tabela)

def parse_expressao(contexto, tabela):
    """
    analisa EXPRESSAO -> ( CONTEUDO )
    
    Args:
        contexto (dict): contexto do parser
        tabela (dict): tabela LL(1)
        
    Returns:
        dict: nó da derivação
    """
    match(PARENTESE_ABRE, contexto)
    
    conteudo = parse_conteudo(contexto, tabela)
    
    match(PARENTESE_FECHA, contexto)
    
    return {
        'tipo': 'EXPRESSAO',
        'conteudo': conteudo
    }

def parse_conteudo(contexto, tabela):
    """
    analisa CONTEUDO -> OPERACAO | COMANDO_MEM | COMANDO_RES | ESTRUTURA_CONTROLE
    
    Args:
        contexto (dict): contexto do parser
        tabela (dict): tabela LL(1)
        
    Returns:
        dict: nó da derivação
    """
    token = token_atual(contexto)
    
    if token is None:
        raise ParserError("Token esperado, encontrado fim de arquivo")
    
    # verificar tipo de conteúdo pelo lookahead
    
    # comando RES: (N RES)
    if token['tipo'] == NUMERO:
        # olhar próximo token e o token seguinte para decidir
        pos_backup = contexto['posicao']
        avancar_token(contexto)
        proximo = token_atual(contexto)
        
        if proximo and proximo['tipo'] == PALAVRA_RESERVADA and proximo['valor'] == 'RES':
            contexto['posicao'] = pos_backup
            return parse_comando_res(contexto, tabela)
        elif proximo and proximo['tipo'] == IDENTIFICADOR:
            # pode ser (V MEM) ou (A B op_rel)
            avancar_token(contexto)
            terceiro = token_atual(contexto)
            contexto['posicao'] = pos_backup  # voltar
            
            if terceiro and terceiro['tipo'] == PARENTESE_FECHA:
                # é comando memória: (V MEM)
                return parse_comando_memoria(contexto, tabela)
            else:
                # continuar verificando operador
                contexto['posicao'] = pos_backup
                return parse_operacao_ou_comparacao(contexto, tabela)
        else:
            # voltar e tentar como operação ou comparação
            contexto['posicao'] = pos_backup
            return parse_operacao_ou_comparacao(contexto, tabela)
    
    # comando memória: (MEM)
    elif token['tipo'] == IDENTIFICADOR:
        # verificar se é só identificador ou operação
        pos_backup = contexto['posicao']
        avancar_token(contexto)
        proximo = token_atual(contexto)
        contexto['posicao'] = pos_backup
        
        if proximo and proximo['tipo'] == PARENTESE_FECHA:
            # apenas (MEM)
            return parse_comando_memoria(contexto, tabela)
        else:
            # operação ou comparação
            return parse_operacao_ou_comparacao(contexto, tabela)
    
    # expressão aninhada ou estrutura de controle ou comando de armazenamento
    elif token['tipo'] == PARENTESE_ABRE:
        # lookahead mais profundo para identificar o tipo
        # pode ser: ((expr) ID) = comando armazenar
        #          ((expr1) (expr2) op) = operação
        #          ((op1) (op2) op_rel ...) = estrutura de controle
        pos_backup = contexto['posicao']
        
        try:
            # ler primeira sub-expressão
            parse_expressao(contexto, tabela)
            proximo = token_atual(contexto)
            
            # se é identificador seguido de ), é comando armazenar
            if proximo and proximo['tipo'] == IDENTIFICADOR:
                avancar_token(contexto)
                apos_id = token_atual(contexto)
                contexto['posicao'] = pos_backup
                
                if apos_id and apos_id['tipo'] == PARENTESE_FECHA:
                    return parse_comando_memoria(contexto, tabela)
            
            # caso contrário, é operação ou estrutura
            contexto['posicao'] = pos_backup
            return parse_operacao_ou_estrutura(contexto, tabela)
        except:
            contexto['posicao'] = pos_backup
            return parse_operacao_ou_estrutura(contexto, tabela)
    
    else:
        raise ParserError(
            f"Token inesperado no início de conteúdo: {token['tipo']} ('{token['valor']}')",
            posicao=token.get('posicao')
        )

def parse_operacao_ou_comparacao(contexto, tabela):
    """
    decide entre operação aritmética ou comparação através de lookahead
    verifica qual tipo de operador vem após os dois operandos
    """
    pos_backup = contexto['posicao']
    
    try:
        # pular primeiro operando
        parse_operando(contexto, tabela)
        # pular segundo operando
        parse_operando(contexto, tabela)
        # verificar qual tipo de operador
        token = token_atual(contexto)
        
        if token and token['tipo'] == OPERADOR_RELACIONAL:
            # é comparação ou estrutura de controle
            contexto['posicao'] = pos_backup
            return parse_comparacao_ou_estrutura(contexto, tabela)
        elif token and token['tipo'] == OPERADOR:
            # é operação aritmética
            contexto['posicao'] = pos_backup
            return parse_operacao(contexto, tabela)
        else:
            contexto['posicao'] = pos_backup
            raise ParserError(f"Esperado operador, encontrado {token['tipo'] if token else 'EOF'}")
    except ParserError:
        raise
    except:
        # em caso de erro, tentar como operação
        contexto['posicao'] = pos_backup
        return parse_operacao(contexto, tabela)

def parse_operacao_ou_estrutura(contexto, tabela):
    """
    decide entre operação com expressão aninhada ou estrutura de controle
    verifica através de lookahead se há operador relacional seguido de IF/WHILE
    """
    # lookahead para detectar estrutura de controle
    # estrutura: (operando operando op_rel (bloco) IF/WHILE) ou (operando operando op_rel (bloco) (bloco) IF)
    pos_backup = contexto['posicao']
    
    try:
        # pular primeiro operando (expressão)
        parse_operando(contexto, tabela)
        # pular segundo operando
        parse_operando(contexto, tabela)
        # verificar se há operador relacional
        token = token_atual(contexto)
        
        if token and token['tipo'] == OPERADOR_RELACIONAL:
            # é comparação ou estrutura de controle
            contexto['posicao'] = pos_backup
            return parse_comparacao_ou_estrutura(contexto, tabela)
        else:
            # é operação aritmética
            contexto['posicao'] = pos_backup
            return parse_operacao(contexto, tabela)
    except:
        # em caso de erro, tentar como operação
        contexto['posicao'] = pos_backup
        return parse_operacao(contexto, tabela)

def parse_bloco_composto(contexto, tabela):
    """
    parseia um bloco que pode conter múltiplas expressões
    sintaxe: (expr) ou ((expr1) (expr2) ...)
    
    Returns:
        dict: expressão única ou bloco composto com lista de expressões
    """
    # ler o bloco
    match(PARENTESE_ABRE, contexto)
    
    # verificar se o primeiro token é parêntese abre (bloco composto)
    token_inicio = token_atual(contexto)
    
    if token_inicio and token_inicio['tipo'] == PARENTESE_ABRE:
        # bloco composto com múltiplas expressões: ((expr1) (expr2) ...)
        expressoes = []
        
        while True:
            token = token_atual(contexto)
            
            # se encontrar fecha parêntese, terminou o bloco composto
            if token and token['tipo'] == PARENTESE_FECHA:
                match(PARENTESE_FECHA, contexto)
                break
            
            # se encontrar abre parêntese, é uma expressão
            elif token and token['tipo'] == PARENTESE_ABRE:
                expr = parse_expressao(contexto, tabela)
                expressoes.append(expr)
            
            else:
                raise ParserError(
                    f"Esperado '(' ou ')' em bloco composto, encontrado {token}",
                    posicao=token.get('posicao') if token else None
                )
        
        # retornar bloco composto
        return {
            'tipo': 'BLOCO_COMPOSTO',
            'expressoes': expressoes
        }
    
    else:
        # bloco simples com uma única expressão: (expr)
        # parsear o conteúdo da expressão
        conteudo = parse_conteudo(contexto, tabela)
        match(PARENTESE_FECHA, contexto)
        
        return {
            'tipo': 'EXPRESSAO',
            'conteudo': conteudo
        }

def parse_comparacao_ou_estrutura(contexto, tabela):
    """
    decide entre comparação simples ou estrutura de controle (IF/WHILE)
    comparação simples: (A B op_rel)
    estrutura IF: (A B op_rel (bloco_true) (bloco_false) IF)
    estrutura WHILE: (A B op_rel (bloco) WHILE)
    bloco pode ser: (expr) ou ((expr1) (expr2) ...)
    """
    # parsear operandos e operador relacional
    operando1 = parse_operando(contexto, tabela)
    operando2 = parse_operando(contexto, tabela)
    
    token = token_atual(contexto)
    if token is None or token['tipo'] != OPERADOR_RELACIONAL:
        raise ParserError("Esperado operador relacional")
    
    operador = match(OPERADOR_RELACIONAL, contexto)
    
    # verificar o que vem depois
    token_seguinte = token_atual(contexto)
    
    # se é parêntese fecha, é comparação simples
    if token_seguinte and token_seguinte['tipo'] == PARENTESE_FECHA:
        return {
            'tipo': 'COMPARACAO',
            'operador': operador['valor'],
            'operando1': operando1,
            'operando2': operando2
        }
    
    # se é parêntese abre, pode ser estrutura de controle
    elif token_seguinte and token_seguinte['tipo'] == PARENTESE_ABRE:
        # ler primeiro bloco (pode ser composto)
        bloco1 = parse_bloco_composto(contexto, tabela)
        
        # verificar o próximo token após bloco1
        token_pos_bloco1 = token_atual(contexto)
        
        # se é outro parêntese abre, pode ser IF (dois blocos)
        if token_pos_bloco1 and token_pos_bloco1['tipo'] == PARENTESE_ABRE:
            # ler segundo bloco (pode ser composto)
            bloco2 = parse_bloco_composto(contexto, tabela)
            
            # agora deve ter IF
            token_palavra = token_atual(contexto)
            if token_palavra and token_palavra['tipo'] == PALAVRA_RESERVADA and token_palavra['valor'] == 'IF':
                match_valor('IF', contexto)
                return {
                    'tipo': 'DECISAO',
                    'condicao': {
                        'tipo': 'CONDICAO',
                        'operando1': operando1,
                        'operando2': operando2,
                        'operador': operador['valor']
                    },
                    'bloco_verdadeiro': bloco1,
                    'bloco_falso': bloco2
                }
            else:
                raise ParserError(
                    f"Esperado IF após dois blocos, encontrado {token_palavra}",
                    posicao=token_palavra.get('posicao') if token_palavra else None
                )
        
        # se é palavra reservada WHILE, é loop (um bloco)
        elif token_pos_bloco1 and token_pos_bloco1['tipo'] == PALAVRA_RESERVADA and token_pos_bloco1['valor'] == 'WHILE':
            match_valor('WHILE', contexto)
            return {
                'tipo': 'LACO',
                'condicao': {
                    'tipo': 'CONDICAO',
                    'operando1': operando1,
                    'operando2': operando2,
                    'operador': operador['valor']
                },
                'bloco': bloco1
            }
        
        else:
            raise ParserError(
                f"Esperado IF ou WHILE após bloco, encontrado {token_pos_bloco1}",
                posicao=token_pos_bloco1.get('posicao') if token_pos_bloco1 else None
            )
    
    else:
        raise ParserError(
            f"Token inesperado após operador relacional: {token_seguinte}",
            posicao=token_seguinte.get('posicao') if token_seguinte else None
        )

def parse_operacao(contexto, tabela):
    """
    analisa OPERACAO -> OPERANDO OPERANDO OPERADOR_ARIT
    
    Args:
        contexto (dict): contexto do parser
        tabela (dict): tabela LL(1)
        
    Returns:
        dict: nó da derivação
    """
    operando1 = parse_operando(contexto, tabela)
    operando2 = parse_operando(contexto, tabela)
    
    # verificar operador aritmético
    token = token_atual(contexto)
    if token is None:
        raise ParserError("Esperado operador, encontrado fim de arquivo")
    
    if token['tipo'] == OPERADOR:
        operador = match(OPERADOR, contexto)
        return {
            'tipo': 'OPERACAO',
            'operador': operador['valor'],
            'operando1': operando1,
            'operando2': operando2
        }
    else:
        raise ParserError(
            f"Esperado operador aritmético, encontrado {token['tipo']}",
            posicao=token.get('posicao')
        )

def parse_operando(contexto, tabela):
    """
    analisa OPERANDO -> numero | identificador | EXPRESSAO
    
    Args:
        contexto (dict): contexto do parser
        tabela (dict): tabela LL(1)
        
    Returns:
        dict: nó da derivação
    """
    token = token_atual(contexto)
    
    if token is None:
        raise ParserError("Esperado operando, encontrado fim de arquivo")
    
    if token['tipo'] == NUMERO:
        numero = match(NUMERO, contexto)
        return {
            'tipo': 'NUMERO',
            'valor': numero['valor']
        }
    
    elif token['tipo'] == IDENTIFICADOR:
        identificador = match(IDENTIFICADOR, contexto)
        return {
            'tipo': 'IDENTIFICADOR',
            'valor': identificador['valor']
        }
    
    elif token['tipo'] == PARENTESE_ABRE:
        # expressão aninhada
        return parse_expressao(contexto, tabela)
    
    else:
        raise ParserError(
            f"Esperado operando, encontrado {token['tipo']} ('{token['valor']}')",
            posicao=token.get('posicao')
        )

def parse_comando_memoria(contexto, tabela):
    """
    analisa COMANDO_MEM -> (numero|expressao) identificador | identificador
    
    Args:
        contexto (dict): contexto do parser
        tabela (dict): tabela LL(1)
        
    Returns:
        dict: nó da derivação
    """
    token = token_atual(contexto)
    
    if token['tipo'] == NUMERO:
        # armazenar com número: (V MEM)
        numero = match(NUMERO, contexto)
        identificador = match(IDENTIFICADOR, contexto)
        
        return {
            'tipo': 'COMANDO_ARMAZENAR',
            'valor': numero['valor'],
            'identificador': identificador['valor']
        }
    
    elif token['tipo'] == PARENTESE_ABRE:
        # armazenar com expressão: ((expr) MEM)
        expressao = parse_expressao(contexto, tabela)
        identificador = match(IDENTIFICADOR, contexto)
        
        return {
            'tipo': 'COMANDO_ARMAZENAR_EXPRESSAO',
            'expressao': expressao,
            'identificador': identificador['valor']
        }
    
    elif token['tipo'] == IDENTIFICADOR:
        # recuperar: (MEM)
        identificador = match(IDENTIFICADOR, contexto)
        
        return {
            'tipo': 'COMANDO_RECUPERAR',
            'identificador': identificador['valor']
        }
    
    else:
        raise ParserError(
            f"Esperado número, expressão ou identificador no comando de memória",
            posicao=token.get('posicao')
        )

def parse_comando_res(contexto, tabela):
    """
    analisa COMANDO_RES -> numero RES
    
    Args:
        contexto (dict): contexto do parser
        tabela (dict): tabela LL(1)
        
    Returns:
        dict: nó da derivação
    """
    numero = match(NUMERO, contexto)
    match_valor('RES', contexto)
    
    return {
        'tipo': 'COMANDO_RES',
        'n': numero['valor']
    }

def parse_estrutura_controle(contexto, tabela):
    """
    analisa estruturas de controle IF ou WHILE
    formato: (operando1 operando2 op_rel (bloco) IF/WHILE) ou
             (operando1 operando2 op_rel (bloco_true) (bloco_false) IF)
    
    Args:
        contexto (dict): contexto do parser
        tabela (dict): tabela LL(1)
        
    Returns:
        dict: nó da derivação DECISAO ou LACO
    """
    # parsear condição
    condicao = parse_condicao(contexto, tabela)
    
    # parsear primeiro bloco
    bloco1 = parse_expressao(contexto, tabela)
    
    # verificar qual estrutura (IF ou WHILE)
    token = token_atual(contexto)
    if token is None:
        raise ParserError("Esperado IF ou WHILE, encontrado fim de arquivo")
    
    if token['tipo'] == PALAVRA_RESERVADA:
        if token['valor'] == 'WHILE':
            match_valor('WHILE', contexto)
            return {
                'tipo': 'LACO',
                'condicao': condicao,
                'bloco': bloco1
            }
        elif token['valor'] == 'IF':
            # IF tem dois blocos
            bloco2 = parse_expressao(contexto, tabela)
            match_valor('IF', contexto)
            return {
                'tipo': 'DECISAO',
                'condicao': condicao,
                'bloco_verdadeiro': bloco1,
                'bloco_falso': bloco2
            }
        else:
            raise ParserError(
                f"Esperado IF ou WHILE, encontrado {token['valor']}",
                posicao=token.get('posicao')
            )
    else:
        raise ParserError(
            f"Esperado palavra reservada (IF/WHILE), encontrado {token['tipo']}",
            posicao=token.get('posicao')
        )

def parse_condicao(contexto, tabela):
    """
    analisa CONDICAO -> OPERANDO OPERANDO OPERADOR_REL
    
    Args:
        contexto (dict): contexto do parser
        tabela (dict): tabela LL(1)
        
    Returns:
        dict: nó da condição com operandos e operador
    """
    operando1 = parse_operando(contexto, tabela)
    operando2 = parse_operando(contexto, tabela)
    
    token = token_atual(contexto)
    if token is None:
        raise ParserError("Esperado operador relacional, encontrado fim de arquivo")
    
    if token['tipo'] == OPERADOR_RELACIONAL:
        operador = match(OPERADOR_RELACIONAL, contexto)
        return {
            'tipo': 'CONDICAO',
            'operando1': operando1,
            'operando2': operando2,
            'operador': operador['valor']
        }
    else:
        raise ParserError(
            f"Esperado operador relacional, encontrado {token['tipo']}",
            posicao=token.get('posicao')
        )

if __name__ == '__main__':
    # teste do parser
    from src.lexer import parse_expressao as tokenizar
    from src.grammar import construir_gramatica
    
    try:
        # construir gramática
        gramatica_info = construir_gramatica()
        tabela = gramatica_info['tabela']
        
        # testar expressões
        expressoes_teste = [
            "(3 5 +)",
            "((2 3 *) (4 2 /) /)",
            "(42 MEM)",
            "(MEM)",
            "(1 RES)",
        ]
        
        print("=== TESTE DO PARSER ===\n")
        
        for expr in expressoes_teste:
            print(f"Expressão: {expr}")
            try:
                tokens = tokenizar(expr)
                resultado = parsear(tokens, tabela)
                print(f"  ✓ Válida")
                print(f"  Derivação: {resultado['derivacao']}")
            except ParserError as e:
                print(f"  ✗ Erro: {e}")
            print()
        
    except Exception as e:
        print(f"Erro: {e}")