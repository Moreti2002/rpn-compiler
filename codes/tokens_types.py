# definicoes de tipos de tokens e funcoes auxiliares para o analisador lexico

# constantes para tipos de tokens
NUMERO = "NUMERO"
OPERADOR = "OPERADOR"
OPERADOR_RELACIONAL = "OPERADOR_RELACIONAL"
PARENTESE_ABRE = "PARENTESE_ABRE"
PARENTESE_FECHA = "PARENTESE_FECHA"
PALAVRA_RESERVADA = "PALAVRA_RESERVADA"
IDENTIFICADOR = "IDENTIFICADOR"

# conjuntos de caracteres validos
OPERADORES_VALIDOS = {'+', '-', '*', '|', '/', '%', '^'}  # '|' e divisao real
OPERADORES_RELACIONAIS = {'>', '<', '=', '!'}  # ==, !=, >=, <= sao compostos
PALAVRAS_RESERVADAS = {'RES', 'IF', 'WHILE', 'THEN', 'ELSE', 'PRINT'}

def criar_token(tipo, valor, posicao=None):
    """
    cria um novo token
    
    Args:
        tipo (str): tipo do token
        valor (str): valor do token
        posicao (int, optional): posicao do token no texto
        
    Returns:
        dict: dicionario representando o token
    """
    token = {
        'tipo': tipo,
        'valor': valor
    }
    if posicao is not None:
        token['posicao'] = posicao
    return token

def eh_operador_valido(char):
    """verifica se o caractere e um operador valido"""
    return char in OPERADORES_VALIDOS

def eh_operador_relacional(char):
    """verifica se o caractere e parte de operador relacional"""
    return char in OPERADORES_RELACIONAIS

def eh_palavra_reservada(palavra):
    """verifica se a palavra e uma palavra reservada"""
    return palavra.upper() in PALAVRAS_RESERVADAS

def eh_letra_maiuscula(char):
    """verifica se o caractere e uma letra maiuscula"""
    return char.isupper() and char.isalpha()

def eh_digito(char):
    """verifica se o caractere e um digito"""
    return char.isdigit()

def eh_ponto_decimal(char):
    """verifica se o caractere e um ponto decimal"""
    return char == '.'

def eh_espaco(char):
    """verifica se o caractere e um espaco em branco"""
    return char.isspace()

def eh_parentese_abre(char):
    """verifica se o caractere e parentese de abertura"""
    return char == '('

def eh_parentese_fecha(char):
    """verifica se o caractere e parentese de fechamento"""
    return char == ')'