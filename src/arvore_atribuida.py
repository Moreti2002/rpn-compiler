# gerador de árvore sintática abstrata atribuída

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ArvoreAtribuidaError(Exception):
    """exceção para erros na árvore atribuída"""
    def __init__(self, mensagem):
        self.mensagem = mensagem
        super().__init__(f"Erro na árvore atribuída: {mensagem}")

def gerar_arvore_atribuida(arvore_anotada):
    """
    constrói árvore sintática abstrata atribuída final
    
    Args:
        arvore_anotada (dict): árvore com anotações de tipo
        
    Returns:
        dict: árvore atribuída completa
    """
    if not arvore_anotada:
        raise ArvoreAtribuidaError("Árvore anotada vazia")
    
    # copiar e limpar árvore
    arvore_final = limpar_arvore(arvore_anotada)
    
    return arvore_final

def limpar_arvore(no):
    """
    remove informações desnecessárias e organiza estrutura
    
    Args:
        no (dict): nó da árvore
        
    Returns:
        dict: nó limpo
    """
    if not no:
        return None
    
    # criar novo nó com campos ordenados
    no_limpo = {
        'tipo': no.get('tipo'),
        'tipo_inferido': no.get('tipo_inferido'),
        'linha': no.get('linha', 1)
    }
    
    # adicionar campos específicos por tipo
    if no.get('valor') is not None:
        no_limpo['valor'] = no['valor']
    
    if no.get('operador') is not None:
        no_limpo['operador'] = no['operador']
    
    # processar filhos recursivamente
    if no.get('filhos'):
        no_limpo['filhos'] = []
        for filho in no['filhos']:
            filho_limpo = limpar_arvore(filho)
            if filho_limpo:
                no_limpo['filhos'].append(filho_limpo)
    else:
        no_limpo['filhos'] = []
    
    return no_limpo

def salvar_arvore_json(arvore, nome_arquivo="arvore_atribuida.json"):
    """
    salva árvore em formato JSON
    
    Args:
        arvore (dict): árvore atribuída
        nome_arquivo (str): nome do arquivo
    """
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(arvore, arquivo, indent=2, ensure_ascii=False)
    except Exception as e:
        raise ArvoreAtribuidaError(f"Erro ao salvar árvore: {str(e)}")

def carregar_arvore_json(nome_arquivo):
    """
    carrega árvore de arquivo JSON
    
    Args:
        nome_arquivo (str): nome do arquivo
        
    Returns:
        dict: árvore atribuída
    """
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except Exception as e:
        raise ArvoreAtribuidaError(f"Erro ao carregar árvore: {str(e)}")

def imprimir_arvore_atribuida(arvore, nivel=0, prefixo=""):
    """
    imprime árvore formatada com tipos
    
    Args:
        arvore (dict): árvore atribuída
        nivel (int): nível de indentação
        prefixo (str): prefixo para o nó
        
    Returns:
        str: representação textual
    """
    if not arvore:
        return ""
    
    resultado = ""
    indentacao = "  " * nivel
    
    # informações do nó
    tipo = arvore.get('tipo', 'DESCONHECIDO')
    tipo_inferido = arvore.get('tipo_inferido')
    valor = arvore.get('valor')
    operador = arvore.get('operador')
    linha = arvore.get('linha', '?')
    
    # montar linha de saída
    info = f"{tipo}"
    
    if tipo_inferido:
        info += f" : {tipo_inferido}"
    
    if valor is not None:
        info += f" = {valor}"
    
    if operador is not None:
        info += f" [{operador}]"
    
    info += f" (linha {linha})"
    
    resultado += f"{indentacao}{prefixo}{info}\n"
    
    # imprimir filhos
    filhos = arvore.get('filhos', [])
    for i, filho in enumerate(filhos):
        if i == len(filhos) - 1:
            resultado += imprimir_arvore_atribuida(filho, nivel + 1, "└─ ")
        else:
            resultado += imprimir_arvore_atribuida(filho, nivel + 1, "├─ ")
    
    return resultado

def extrair_informacoes_arvore(arvore):
    """
    extrai informações estatísticas da árvore
    
    Args:
        arvore (dict): árvore atribuída
        
    Returns:
        dict: estatísticas da árvore
    """
    info = {
        'total_nos': 0,
        'profundidade': 0,
        'tipos_encontrados': {},
        'operadores_usados': set(),
        'linhas': set()
    }
    
    def analisar_no(no, profundidade=0):
        if not no:
            return
        
        info['total_nos'] += 1
        info['profundidade'] = max(info['profundidade'], profundidade)
        
        # contar tipos
        tipo = no.get('tipo')
        if tipo:
            info['tipos_encontrados'][tipo] = info['tipos_encontrados'].get(tipo, 0) + 1
        
        # coletar operadores
        operador = no.get('operador')
        if operador:
            info['operadores_usados'].add(operador)
        
        # coletar linhas
        linha = no.get('linha')
        if linha:
            info['linhas'].add(linha)
        
        # recursão
        for filho in no.get('filhos', []):
            analisar_no(filho, profundidade + 1)
    
    analisar_no(arvore)
    
    # converter set para lista
    info['operadores_usados'] = sorted(list(info['operadores_usados']))
    info['linhas'] = sorted(list(info['linhas']))
    info['total_linhas'] = len(info['linhas'])
    
    return info

def validar_arvore_atribuida(arvore):
    """
    valida consistência da árvore atribuída
    
    Args:
        arvore (dict): árvore atribuída
        
    Returns:
        tuple: (bool_valida, lista_problemas)
    """
    problemas = []
    
    def validar_no(no, caminho="raiz"):
        if not no:
            return
        
        # verificar campos obrigatórios
        if 'tipo' not in no:
            problemas.append(f"{caminho}: nó sem campo 'tipo'")
        
        if 'tipo_inferido' not in no:
            problemas.append(f"{caminho}: nó sem campo 'tipo_inferido'")
        
        if 'linha' not in no:
            problemas.append(f"{caminho}: nó sem campo 'linha'")
        
        if 'filhos' not in no:
            problemas.append(f"{caminho}: nó sem campo 'filhos'")
        
        # validar tipo inferido
        tipo_inferido = no.get('tipo_inferido')
        if tipo_inferido and tipo_inferido not in ['int', 'real', 'booleano', 'erro', None]:
            problemas.append(f"{caminho}: tipo_inferido inválido '{tipo_inferido}'")
        
        # recursão
        for i, filho in enumerate(no.get('filhos', [])):
            validar_no(filho, f"{caminho}/filho[{i}]")
    
    validar_no(arvore)
    
    return len(problemas) == 0, problemas

def gerar_representacao_markdown(arvore):
    """
    gera representação da árvore em markdown
    
    Args:
        arvore (dict): árvore atribuída
        
    Returns:
        str: representação em markdown
    """
    md = "# Árvore Sintática Abstrata Atribuída\n\n"
    
    # estatísticas
    info = extrair_informacoes_arvore(arvore)
    
    md += "## Estatísticas\n\n"
    md += f"- Total de nós: {info['total_nos']}\n"
    md += f"- Profundidade: {info['profundidade']}\n"
    md += f"- Total de linhas: {info['total_linhas']}\n"
    md += f"- Operadores usados: {', '.join(info['operadores_usados']) if info['operadores_usados'] else 'nenhum'}\n\n"
    
    md += "## Distribuição de Tipos de Nós\n\n"
    md += "| Tipo | Quantidade |\n"
    md += "|------|------------|\n"
    for tipo, qtd in sorted(info['tipos_encontrados'].items()):
        md += f"| {tipo} | {qtd} |\n"
    md += "\n"
    
    # árvore formatada
    md += "## Estrutura da Árvore\n\n"
    md += "```\n"
    md += imprimir_arvore_atribuida(arvore)
    md += "```\n\n"
    
    # validação
    valida, problemas = validar_arvore_atribuida(arvore)
    if valida:
        md += "## ✓ Árvore válida\n\n"
    else:
        md += "## ✗ Problemas encontrados\n\n"
        for problema in problemas:
            md += f"- {problema}\n"
        md += "\n"
    
    return md

if __name__ == '__main__':
    # teste da árvore atribuída
    print("=== TESTE DA ÁRVORE ATRIBUÍDA ===\n")
    
    try:
        # criar árvore de teste
        arvore_teste = {
            'tipo': 'EXPRESSAO',
            'tipo_inferido': 'int',
            'linha': 1,
            'filhos': [
                {
                    'tipo': 'OPERACAO',
                    'operador': '+',
                    'tipo_inferido': 'int',
                    'linha': 1,
                    'filhos': [
                        {
                            'tipo': 'NUMERO',
                            'valor': '3',
                            'tipo_inferido': 'int',
                            'linha': 1,
                            'filhos': []
                        },
                        {
                            'tipo': 'NUMERO',
                            'valor': '5',
                            'tipo_inferido': 'int',
                            'linha': 1,
                            'filhos': []
                        }
                    ]
                }
            ]
        }
        
        # gerar árvore atribuída
        arvore_final = gerar_arvore_atribuida(arvore_teste)
        print("✓ Árvore atribuída gerada")
        
        # imprimir
        print("\nÁrvore formatada:")
        print(imprimir_arvore_atribuida(arvore_final))
        
        # extrair informações
        info = extrair_informacoes_arvore(arvore_final)
        print("Estatísticas:")
        print(f"  - Total de nós: {info['total_nos']}")
        print(f"  - Profundidade: {info['profundidade']}")
        print(f"  - Operadores: {info['operadores_usados']}")
        
        # validar
        valida, problemas = validar_arvore_atribuida(arvore_final)
        if valida:
            print("\n✓ Árvore válida")
        else:
            print(f"\n✗ Problemas: {problemas}")
        
        # salvar JSON
        salvar_arvore_json(arvore_final, "teste_arvore_atribuida.json")
        print("\n✓ Árvore salva em JSON")
        
        # carregar JSON
        arvore_carregada = carregar_arvore_json("teste_arvore_atribuida.json")
        print("✓ Árvore carregada de JSON")
        
        # limpar arquivo de teste
        if os.path.exists("teste_arvore_atribuida.json"):
            os.remove("teste_arvore_atribuida.json")
        
    except ArvoreAtribuidaError as e:
        print(f"Erro: {e}")