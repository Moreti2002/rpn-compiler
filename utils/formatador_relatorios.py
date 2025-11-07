# formatador de relatórios em markdown

import json
import os

def gerar_relatorio_gramatica_atributos(gramatica, arquivo="docs/GRAMATICA_ATRIBUTOS.md"):
    """
    gera documentação da gramática de atributos
    
    Args:
        gramatica (dict): gramática de atributos
        arquivo (str): caminho do arquivo
    """
    # criar diretório docs se não existir
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    
    conteudo = "# Gramática de Atributos\n\n"
    conteudo += "## Atributos Sintetizados\n\n"
    
    for attr, desc in gramatica['atributos_sintetizados'].items():
        conteudo += f"- **{attr}**: {desc}\n"
    
    conteudo += "\n## Atributos Herdados\n\n"
    for attr, desc in gramatica['atributos_herdados'].items():
        conteudo += f"- **{attr}**: {desc}\n"
    
    conteudo += "\n## Regras de Produção com Atributos\n\n"
    
    # operações aritméticas
    conteudo += "### Operações Aritméticas\n\n"
    for op, regra in gramatica['regras_tipo']['OPERACAO_ARITMETICA'].items():
        conteudo += f"#### Operador `{op}`\n\n"
        conteudo += f"**Produção**: {regra['producao']}\n\n"
        conteudo += f"**Descrição**: {regra['descricao']}\n\n"
        conteudo += "**Condições**:\n"
        for cond in regra['condicoes']:
            conteudo += f"- {cond}\n"
        conteudo += f"\n**Tipo Resultado**: {regra['tipo_resultado']}\n\n"
        conteudo += "**Verificações**:\n"
        for verif in regra['verificacoes']:
            conteudo += f"- {verif}\n"
        conteudo += "\n"
    
    # operações relacionais
    conteudo += "### Operações Relacionais\n\n"
    regra = list(gramatica['regras_tipo']['OPERACAO_RELACIONAL'].values())[0]
    conteudo += f"**Produção**: {regra['producao']}\n\n"
    conteudo += f"**Descrição**: {regra['descricao']}\n\n"
    conteudo += "**Operadores**: >, <, >=, <=, ==, !=\n\n"
    conteudo += "**Condições**:\n"
    for cond in regra['condicoes']:
        conteudo += f"- {cond}\n"
    conteudo += f"\n**Tipo Resultado**: {regra['tipo_resultado']}\n\n"
    
    # comandos especiais
    conteudo += "### Comandos Especiais\n\n"
    for cmd, regra in gramatica['regras_tipo']['COMANDOS'].items():
        conteudo += f"#### {cmd}\n\n"
        conteudo += f"**Produção**: {regra['producao']}\n\n"
        conteudo += f"**Descrição**: {regra['descricao']}\n\n"
        conteudo += "**Condições**:\n"
        for cond in regra['condicoes']:
            conteudo += f"- {cond}\n"
        conteudo += f"\n**Tipo Resultado**: {regra['tipo_resultado']}\n\n"
        if 'efeito_colateral' in regra:
            conteudo += f"**Efeito Colateral**: {regra['efeito_colateral']}\n\n"
    
    # estruturas de controle
    conteudo += "### Estruturas de Controle\n\n"
    for ctrl, regra in gramatica['regras_tipo']['CONTROLE'].items():
        conteudo += f"#### {ctrl}\n\n"
        conteudo += f"**Produção**: {regra['producao']}\n\n"
        conteudo += f"**Descrição**: {regra['descricao']}\n\n"
        conteudo += "**Condições**:\n"
        for cond in regra['condicoes']:
            conteudo += f"- {cond}\n"
        conteudo += f"\n**Tipo Resultado**: {regra['tipo_resultado']}\n\n"
    
    # regra de promoção
    conteudo += "## Regra de Promoção de Tipos\n\n"
    conteudo += "```\n"
    conteudo += "int  ⊕ int  → int\n"
    conteudo += "int  ⊕ real → real\n"
    conteudo += "real ⊕ int  → real\n"
    conteudo += "real ⊕ real → real\n"
    conteudo += "```\n\n"
    conteudo += "Onde ⊕ representa qualquer operador aritmético (+, -, *, |)\n"
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)

def gerar_relatorio_arvore_atribuida(arvore, arquivo="docs/ARVORE_ATRIBUIDA.md"):
    """
    gera relatório da árvore atribuída
    
    Args:
        arvore (dict): árvore atribuída
        arquivo (str): caminho do arquivo
    """
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    
    conteudo = "# Árvore Sintática Abstrata Atribuída\n\n"
    conteudo += "## Estrutura da Árvore\n\n"
    conteudo += "```\n"
    conteudo += imprimir_arvore_formatada(arvore)
    conteudo += "```\n\n"
    
    conteudo += "## Representação JSON\n\n"
    conteudo += "```json\n"
    conteudo += json.dumps(arvore, indent=2, ensure_ascii=False)
    conteudo += "\n```\n"
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)

def imprimir_arvore_formatada(no, nivel=0, prefixo=""):
    """
    imprime árvore em formato hierárquico
    
    Args:
        no (dict): nó da árvore
        nivel (int): nível de indentação
        prefixo (str): prefixo para formatação
        
    Returns:
        str: representação formatada
    """
    if not no:
        return ""
    
    resultado = ""
    indent = "  " * nivel
    
    tipo = no.get('tipo', '?')
    tipo_inferido = no.get('tipo_inferido', '')
    linha = no.get('linha', '')
    
    info = f"{tipo}"
    if tipo_inferido:
        info += f" : {tipo_inferido}"
    if 'operador' in no:
        info += f" [{no['operador']}]"
    if 'valor' in no:
        info += f" = {no['valor']}"
    if linha:
        info += f" (linha {linha})"
    
    resultado += f"{indent}{prefixo}{info}\n"
    
    filhos = no.get('filhos', [])
    for i, filho in enumerate(filhos):
        eh_ultimo = (i == len(filhos) - 1)
        novo_prefixo = "└─ " if eh_ultimo else "├─ "
        resultado += imprimir_arvore_formatada(filho, nivel + 1, novo_prefixo)
    
    return resultado

def gerar_relatorio_erros(erros, arquivo="docs/ERROS_SEMANTICOS.md"):
    """
    gera relatório de erros semânticos
    
    Args:
        erros (list): lista de erros encontrados
        arquivo (str): caminho do arquivo
    """
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    
    conteudo = "# Erros Semânticos\n\n"
    
    if not erros:
        conteudo += "✓ **Nenhum erro semântico encontrado!**\n"
    else:
        conteudo += f"## Total de Erros: {len(erros)}\n\n"
        
        for i, erro in enumerate(erros, 1):
            conteudo += f"### Erro {i}\n\n"
            conteudo += f"- **Tipo**: {erro.get('tipo', 'ERRO_DESCONHECIDO')}\n"
            conteudo += f"- **Mensagem**: {erro.get('mensagem', 'Sem descrição')}\n"
            
            if erro.get('linha'):
                conteudo += f"- **Linha**: {erro['linha']}\n"
            
            if erro.get('contexto'):
                conteudo += f"- **Contexto**: `{erro['contexto']}`\n"
            
            conteudo += "\n"
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)

def gerar_relatorio_julgamento_tipos(regras_aplicadas, arquivo="docs/JULGAMENTO_TIPOS.md"):
    """
    gera relatório do julgamento de tipos
    
    Args:
        regras_aplicadas (list): regras de dedução aplicadas
        arquivo (str): caminho do arquivo
    """
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    
    conteudo = "# Julgamento de Tipos\n\n"
    conteudo += "## Regras de Dedução Aplicadas\n\n"
    
    if not regras_aplicadas:
        conteudo += "Nenhuma regra aplicada.\n"
    else:
        for i, regra in enumerate(regras_aplicadas, 1):
            conteudo += f"### Regra {i}\n\n"
            conteudo += f"- **Linha**: {regra.get('linha', '?')}\n"
            conteudo += f"- **Tipo de Nó**: {regra.get('tipo_no', '?')}\n"
            conteudo += f"- **Tipo Inferido**: {regra.get('tipo_inferido', '?')}\n"
            
            if 'operador' in regra:
                conteudo += f"- **Operador**: `{regra['operador']}`\n"
            
            if 'tipos_operandos' in regra:
                tipos = regra['tipos_operandos']
                conteudo += f"- **Tipos dos Operandos**: {tipos[0]}, {tipos[1]}\n"
                
                # explicar a regra aplicada
                op = regra.get('operador', '?')
                if op in ['+', '-', '*']:
                    conteudo += f"- **Regra Aplicada**: Γ ⊢ e₁ : {tipos[0]}, Γ ⊢ e₂ : {tipos[1]} → Γ ⊢ e₁ {op} e₂ : {regra['tipo_inferido']}\n"
                elif op == '|':
                    conteudo += f"- **Regra Aplicada**: Divisão real sempre retorna tipo `real`\n"
                elif op in ['/', '%']:
                    conteudo += f"- **Regra Aplicada**: Operador `{op}` requer operandos inteiros e retorna `int`\n"
                elif op == '^':
                    conteudo += f"- **Regra Aplicada**: Potenciação com expoente inteiro retorna tipo da base\n"
                elif op in ['>', '<', '>=', '<=', '==', '!=']:
                    conteudo += f"- **Regra Aplicada**: Operador relacional retorna tipo `booleano`\n"
            
            if 'caminho' in regra:
                conteudo += f"- **Caminho na Árvore**: `{regra['caminho']}`\n"
            
            conteudo += "\n"
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)

def gerar_todos_relatorios(gramatica, arvore, erros, regras):
    """
    gera todos os relatórios de uma vez
    
    Args:
        gramatica (dict): gramática de atributos
        arvore (dict): árvore atribuída
        erros (list): erros encontrados
        regras (list): regras aplicadas
    """
    gerar_relatorio_gramatica_atributos(gramatica)
    gerar_relatorio_arvore_atribuida(arvore)
    gerar_relatorio_erros(erros)
    gerar_relatorio_julgamento_tipos(regras)
    
    print("✓ Todos os relatórios foram gerados em docs/")

if __name__ == '__main__':
    print("=== TESTE DO FORMATADOR DE RELATÓRIOS ===\n")
    
    # teste simples
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
    
    erros_teste = []
    
    regras_teste = [
        {
            'linha': 1,
            'tipo_no': 'OPERACAO',
            'tipo_inferido': 'int',
            'operador': '+',
            'tipos_operandos': ['int', 'int']
        }
    ]
    
    # teste de formatação de árvore
    print("Árvore formatada:")
    print(imprimir_arvore_formatada(arvore_teste))
    
    print("\n✓ Formatador testado com sucesso")
