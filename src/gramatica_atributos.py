# gramática de atributos para análise semântica
# define regras de tipos e verificações semânticas

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.token_types import *

class GramaticaAtributosError(Exception):
    """exceção para erros na gramática de atributos"""
    def __init__(self, mensagem):
        self.mensagem = mensagem
        super().__init__(f"Erro na gramática de atributos: {mensagem}")

def definir_gramatica_atributos():
    """
    define regras semânticas da linguagem
    
    Returns:
        dict: estrutura com regras, atributos e verificações
    """
    gramatica = {
        'atributos_sintetizados': {
            'tipo': ['int', 'real', 'booleano'],
            'valor': 'calculado durante execução',
            'inicializada': 'para memórias'
        },
        'atributos_herdados': {
            'escopo': 'nível de escopo',
            'tabela_simbolos': 'referência à tabela'
        },
        'regras_tipo': {},
        'verificacoes': {}
    }
    
    # regras para operações aritméticas
    gramatica['regras_tipo']['OPERACAO_ARITMETICA'] = {
        '+': definir_regra_adicao(),
        '-': definir_regra_subtracao(),
        '*': definir_regra_multiplicacao(),
        '|': definir_regra_divisao_real(),
        '/': definir_regra_divisao_inteira(),
        '%': definir_regra_resto(),
        '^': definir_regra_potencia()
    }
    
    # regras para operações relacionais
    gramatica['regras_tipo']['OPERACAO_RELACIONAL'] = {
        '>': definir_regra_relacional(),
        '<': definir_regra_relacional(),
        '>=': definir_regra_relacional(),
        '<=': definir_regra_relacional(),
        '==': definir_regra_relacional(),
        '!=': definir_regra_relacional()
    }
    
    # regras para comandos especiais
    gramatica['regras_tipo']['COMANDOS'] = {
        'ARMAZENAR': definir_regra_armazenar(),
        'RECUPERAR': definir_regra_recuperar(),
        'RES': definir_regra_res()
    }
    
    # regras para estruturas de controle
    gramatica['regras_tipo']['CONTROLE'] = {
        'IF': definir_regra_if(),
        'WHILE': definir_regra_while()
    }
    
    return gramatica

def definir_regra_adicao():
    """
    define regra para operador +
    
    Regra: Γ ⊢ e₁ : τ₁    Γ ⊢ e₂ : τ₂    τ₁, τ₂ ∈ {int, real}
           ------------------------------------------------
                    Γ ⊢ e₁ + e₂ : promover(τ₁, τ₂)
    """
    return {
        'producao': 'EXPRESSAO → OPERANDO₁ OPERANDO₂ +',
        'condicoes': [
            'tipo(operando1) in [int, real]',
            'tipo(operando2) in [int, real]'
        ],
        'tipo_resultado': 'promover_tipo(tipo(operando1), tipo(operando2))',
        'verificacoes': ['tipos_numericos'],
        'descricao': 'Adição de números inteiros ou reais'
    }

def definir_regra_subtracao():
    """
    define regra para operador -
    
    Regra: Γ ⊢ e₁ : τ₁    Γ ⊢ e₂ : τ₂    τ₁, τ₂ ∈ {int, real}
           ------------------------------------------------
                    Γ ⊢ e₁ - e₂ : promover(τ₁, τ₂)
    """
    return {
        'producao': 'EXPRESSAO → OPERANDO₁ OPERANDO₂ -',
        'condicoes': [
            'tipo(operando1) in [int, real]',
            'tipo(operando2) in [int, real]'
        ],
        'tipo_resultado': 'promover_tipo(tipo(operando1), tipo(operando2))',
        'verificacoes': ['tipos_numericos'],
        'descricao': 'Subtração de números inteiros ou reais'
    }

def definir_regra_multiplicacao():
    """
    define regra para operador *
    
    Regra: Γ ⊢ e₁ : τ₁    Γ ⊢ e₂ : τ₂    τ₁, τ₂ ∈ {int, real}
           ------------------------------------------------
                    Γ ⊢ e₁ * e₂ : promover(τ₁, τ₂)
    """
    return {
        'producao': 'EXPRESSAO → OPERANDO₁ OPERANDO₂ *',
        'condicoes': [
            'tipo(operando1) in [int, real]',
            'tipo(operando2) in [int, real]'
        ],
        'tipo_resultado': 'promover_tipo(tipo(operando1), tipo(operando2))',
        'verificacoes': ['tipos_numericos'],
        'descricao': 'Multiplicação de números inteiros ou reais'
    }

def definir_regra_divisao_real():
    """
    define regra para operador | (divisão real)
    
    Regra: Γ ⊢ e₁ : τ₁    Γ ⊢ e₂ : τ₂    τ₁, τ₂ ∈ {int, real}
           ------------------------------------------------
                        Γ ⊢ e₁ | e₂ : real
    """
    return {
        'producao': 'EXPRESSAO → OPERANDO₁ OPERANDO₂ |',
        'condicoes': [
            'tipo(operando1) in [int, real]',
            'tipo(operando2) in [int, real]',
            'operando2 != 0'
        ],
        'tipo_resultado': 'real',
        'verificacoes': ['tipos_numericos', 'divisao_por_zero'],
        'descricao': 'Divisão real (resultado sempre real)'
    }

def definir_regra_divisao_inteira():
    """
    define regra para operador / (divisão inteira)
    
    Regra: Γ ⊢ e₁ : int    Γ ⊢ e₂ : int    e₂ ≠ 0
           ----------------------------------------
                    Γ ⊢ e₁ / e₂ : int
    """
    return {
        'producao': 'EXPRESSAO → OPERANDO₁ OPERANDO₂ /',
        'condicoes': [
            'tipo(operando1) == int',
            'tipo(operando2) == int',
            'operando2 != 0'
        ],
        'tipo_resultado': 'int',
        'verificacoes': ['tipos_inteiros', 'divisao_por_zero'],
        'descricao': 'Divisão inteira (ambos operandos devem ser inteiros)'
    }

def definir_regra_resto():
    """
    define regra para operador % (resto)
    
    Regra: Γ ⊢ e₁ : int    Γ ⊢ e₂ : int    e₂ ≠ 0
           ----------------------------------------
                    Γ ⊢ e₁ % e₂ : int
    """
    return {
        'producao': 'EXPRESSAO → OPERANDO₁ OPERANDO₂ %',
        'condicoes': [
            'tipo(operando1) == int',
            'tipo(operando2) == int',
            'operando2 != 0'
        ],
        'tipo_resultado': 'int',
        'verificacoes': ['tipos_inteiros', 'divisao_por_zero'],
        'descricao': 'Resto da divisão inteira (ambos operandos devem ser inteiros)'
    }

def definir_regra_potencia():
    """
    define regra para operador ^ (potência)
    
    Regra: Γ ⊢ e₁ : τ    Γ ⊢ e₂ : int    τ ∈ {int, real}
           ----------------------------------------------
                    Γ ⊢ e₁ ^ e₂ : τ
    """
    return {
        'producao': 'EXPRESSAO → OPERANDO₁ OPERANDO₂ ^',
        'condicoes': [
            'tipo(operando1) in [int, real]',
            'tipo(operando2) == int'
        ],
        'tipo_resultado': 'tipo(operando1)',
        'verificacoes': ['base_numerica', 'expoente_inteiro'],
        'descricao': 'Potenciação (expoente deve ser inteiro)'
    }

def definir_regra_relacional():
    """
    define regra para operadores relacionais (>, <, >=, <=, ==, !=)
    
    Regra: Γ ⊢ e₁ : τ₁    Γ ⊢ e₂ : τ₂    τ₁, τ₂ ∈ {int, real}
           ------------------------------------------------
                    Γ ⊢ e₁ op e₂ : booleano
    """
    return {
        'producao': 'EXPRESSAO → OPERANDO₁ OPERANDO₂ OP_REL',
        'condicoes': [
            'tipo(operando1) in [int, real]',
            'tipo(operando2) in [int, real]'
        ],
        'tipo_resultado': 'booleano',
        'verificacoes': ['tipos_numericos'],
        'descricao': 'Comparação relacional (retorna booleano)'
    }

def definir_regra_armazenar():
    """
    define regra para comando (V MEM)
    
    Regra: Γ ⊢ e : τ    τ ∈ {int, real}
           ---------------------------
           Γ[MEM ↦ (τ, inicializada)] ⊢ (e MEM) : τ
    """
    return {
        'producao': 'COMANDO → VALOR IDENTIFICADOR',
        'condicoes': [
            'tipo(valor) in [int, real]',
            'identificador valido'
        ],
        'tipo_resultado': 'tipo(valor)',
        'efeito_colateral': 'adiciona simbolo na tabela',
        'verificacoes': ['tipo_valor_valido'],
        'descricao': 'Armazena valor em memória'
    }

def definir_regra_recuperar():
    """
    define regra para comando (MEM)
    
    Regra: MEM ∈ Γ    Γ(MEM) = (τ, inicializada)
           -------------------------------------
                    Γ ⊢ MEM : τ
    """
    return {
        'producao': 'COMANDO → IDENTIFICADOR',
        'condicoes': [
            'identificador in tabela_simbolos',
            'simbolo.inicializada == True'
        ],
        'tipo_resultado': 'tipo(simbolo)',
        'verificacoes': ['memoria_inicializada'],
        'descricao': 'Recupera valor de memória (erro se não inicializada)'
    }

def definir_regra_res():
    """
    define regra para comando (N RES)
    
    Regra: N ∈ ℕ    N ≤ |historico|    historico[N] : τ
           --------------------------------------------
                    Γ ⊢ (N RES) : τ
    """
    return {
        'producao': 'COMANDO → NUMERO RES',
        'condicoes': [
            'tipo(N) == int',
            'N >= 0',
            'N <= tamanho(historico)'
        ],
        'tipo_resultado': 'tipo(historico[N])',
        'verificacoes': ['N_valido', 'historico_suficiente'],
        'descricao': 'Recupera resultado N linhas anteriores'
    }

def definir_regra_if():
    """
    define regra para estrutura IF
    
    Regra: Γ ⊢ e₁ : booleano    Γ ⊢ e₂ : τ    Γ ⊢ e₃ : τ
           ----------------------------------------------
                Γ ⊢ if e₁ then e₂ else e₃ : τ
    """
    return {
        'producao': 'DECISAO → CONDICAO BLOCO_V BLOCO_F IF',
        'condicoes': [
            'tipo(condicao) == booleano',
            'tipo(bloco_verdadeiro) == tipo(bloco_falso)'
        ],
        'tipo_resultado': 'tipo(bloco_verdadeiro)',
        'verificacoes': ['condicao_booleana', 'tipos_blocos_compativeis'],
        'descricao': 'Estrutura condicional (condição deve ser booleana)'
    }

def definir_regra_while():
    """
    define regra para estrutura WHILE
    
    Regra: Γ ⊢ e₁ : booleano    Γ ⊢ e₂ : τ
           -------------------------------
                Γ ⊢ while e₁ do e₂ : τ
    """
    return {
        'producao': 'LACO → CONDICAO BLOCO WHILE',
        'condicoes': [
            'tipo(condicao) == booleano'
        ],
        'tipo_resultado': 'tipo(bloco)',
        'verificacoes': ['condicao_booleana'],
        'descricao': 'Laço de repetição (condição deve ser booleana)'
    }

def promover_tipo(tipo1, tipo2):
    """
    define tipo resultante de operação entre tipos diferentes
    
    Regra de promoção:
    - int  ⊕ int  → int
    - int  ⊕ real → real
    - real ⊕ int  → real
    - real ⊕ real → real
    
    Args:
        tipo1 (str): primeiro tipo ('int' ou 'real')
        tipo2 (str): segundo tipo ('int' ou 'real')
        
    Returns:
        str: tipo resultante ('int' ou 'real')
    """
    if tipo1 == 'real' or tipo2 == 'real':
        return 'real'
    return 'int'

def obter_regra_semantica(tipo_no, operador=None):
    """
    retorna regra semântica para um tipo de nó
    
    Args:
        tipo_no (str): tipo do nó (OPERACAO, NUMERO, etc)
        operador (str): operador quando aplicável
        
    Returns:
        dict: regra semântica com verificações de tipo
    """
    gramatica = definir_gramatica_atributos()
    
    if tipo_no == 'OPERACAO':
        if operador in gramatica['regras_tipo']['OPERACAO_ARITMETICA']:
            return gramatica['regras_tipo']['OPERACAO_ARITMETICA'][operador]
        elif operador in gramatica['regras_tipo']['OPERACAO_RELACIONAL']:
            return gramatica['regras_tipo']['OPERACAO_RELACIONAL'][operador]
    
    elif tipo_no in ['COMANDO_ARMAZENAR', 'COMANDO_RECUPERAR', 'COMANDO_RES']:
        comando_map = {
            'COMANDO_ARMAZENAR': 'ARMAZENAR',
            'COMANDO_RECUPERAR': 'RECUPERAR',
            'COMANDO_RES': 'RES'
        }
        return gramatica['regras_tipo']['COMANDOS'].get(comando_map[tipo_no])
    
    elif tipo_no in ['DECISAO', 'LACO']:
        controle_map = {
            'DECISAO': 'IF',
            'LACO': 'WHILE'
        }
        return gramatica['regras_tipo']['CONTROLE'].get(controle_map[tipo_no])
    
    return None

def gerar_documentacao_gramatica():
    """
    gera documentação completa da gramática de atributos
    
    Returns:
        str: documentação em formato markdown
    """
    gramatica = definir_gramatica_atributos()
    
    doc = "# Gramática de Atributos\n\n"
    doc += "## Atributos Sintetizados\n\n"
    for attr, descricao in gramatica['atributos_sintetizados'].items():
        doc += f"- **{attr}**: {descricao}\n"
    
    doc += "\n## Atributos Herdados\n\n"
    for attr, descricao in gramatica['atributos_herdados'].items():
        doc += f"- **{attr}**: {descricao}\n"
    
    doc += "\n## Regras de Produção com Atributos\n\n"
    
    doc += "### Operações Aritméticas\n\n"
    for op, regra in gramatica['regras_tipo']['OPERACAO_ARITMETICA'].items():
        doc += f"#### Operador `{op}`\n\n"
        doc += f"**Produção**: {regra['producao']}\n\n"
        doc += f"**Descrição**: {regra['descricao']}\n\n"
        doc += "**Condições**:\n"
        for cond in regra['condicoes']:
            doc += f"- {cond}\n"
        doc += f"\n**Tipo Resultado**: {regra['tipo_resultado']}\n\n"
        doc += "**Verificações**:\n"
        for verif in regra['verificacoes']:
            doc += f"- {verif}\n"
        doc += "\n"
    
    doc += "### Operações Relacionais\n\n"
    regra = list(gramatica['regras_tipo']['OPERACAO_RELACIONAL'].values())[0]
    doc += f"**Produção**: {regra['producao']}\n\n"
    doc += f"**Descrição**: {regra['descricao']}\n\n"
    doc += "**Operadores**: >, <, >=, <=, ==, !=\n\n"
    doc += "**Condições**:\n"
    for cond in regra['condicoes']:
        doc += f"- {cond}\n"
    doc += f"\n**Tipo Resultado**: {regra['tipo_resultado']}\n\n"
    
    doc += "\n### Comandos Especiais\n\n"
    for cmd, regra in gramatica['regras_tipo']['COMANDOS'].items():
        doc += f"#### {cmd}\n\n"
        doc += f"**Produção**: {regra['producao']}\n\n"
        doc += f"**Descrição**: {regra['descricao']}\n\n"
        doc += "**Condições**:\n"
        for cond in regra['condicoes']:
            doc += f"- {cond}\n"
        doc += f"\n**Tipo Resultado**: {regra['tipo_resultado']}\n\n"
        if 'efeito_colateral' in regra:
            doc += f"**Efeito Colateral**: {regra['efeito_colateral']}\n\n"
    
    doc += "\n### Estruturas de Controle\n\n"
    for ctrl, regra in gramatica['regras_tipo']['CONTROLE'].items():
        doc += f"#### {ctrl}\n\n"
        doc += f"**Produção**: {regra['producao']}\n\n"
        doc += f"**Descrição**: {regra['descricao']}\n\n"
        doc += "**Condições**:\n"
        for cond in regra['condicoes']:
            doc += f"- {cond}\n"
        doc += f"\n**Tipo Resultado**: {regra['tipo_resultado']}\n\n"
    
    doc += "\n## Regra de Promoção de Tipos\n\n"
    doc += "```\n"
    doc += "int  ⊕ int  → int\n"
    doc += "int  ⊕ real → real\n"
    doc += "real ⊕ int  → real\n"
    doc += "real ⊕ real → real\n"
    doc += "```\n\n"
    doc += "Onde ⊕ representa qualquer operador aritmético (+, -, *, |)\n"
    
    return doc

if __name__ == '__main__':
    # teste da gramática de atributos
    print("=== GRAMÁTICA DE ATRIBUTOS ===\n")
    
    try:
        gramatica = definir_gramatica_atributos()
        
        print("Regras definidas:")
        print(f"  - Operações aritméticas: {len(gramatica['regras_tipo']['OPERACAO_ARITMETICA'])}")
        print(f"  - Operações relacionais: {len(gramatica['regras_tipo']['OPERACAO_RELACIONAL'])}")
        print(f"  - Comandos especiais: {len(gramatica['regras_tipo']['COMANDOS'])}")
        print(f"  - Estruturas de controle: {len(gramatica['regras_tipo']['CONTROLE'])}")
        
        print("\n✓ Gramática de atributos definida com sucesso!")
        
        # testar promoção de tipos
        print("\nTeste de promoção de tipos:")
        print(f"  int + int = {promover_tipo('int', 'int')}")
        print(f"  int + real = {promover_tipo('int', 'real')}")
        print(f"  real + int = {promover_tipo('real', 'int')}")
        print(f"  real + real = {promover_tipo('real', 'real')}")
        
        # gerar documentação
        print("\nGerando documentação...")
        doc = gerar_documentacao_gramatica()
        print("✓ Documentação gerada")
        
    except GramaticaAtributosError as e:
        print(f"Erro: {e}")