# formatador de relatórios em markdown para análise semântica

import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def gerar_relatorio_gramatica_atributos(gramatica, arquivo="docs/GRAMATICA_ATRIBUTOS.md"):
    """
    gera documentação da gramática de atributos
    
    Args:
        gramatica (dict): gramática de atributos
        arquivo (str): caminho do arquivo
    """
    md = "# Gramática de Atributos - Fase 3\n\n"
    md += f"*Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    md += "---\n\n"
    
    # introdução
    md += "## Introdução\n\n"
    md += "Esta gramática de atributos define as regras semânticas para a linguagem de programação "
    md += "simplificada em notação polonesa reversa (RPN). Cada regra especifica como os tipos são "
    md += "inferidos e propagados através da árvore sintática abstrata.\n\n"
    
    # atributos sintetizados
    md += "## Atributos Sintetizados\n\n"
    md += "Atributos calculados a partir dos filhos (propagação bottom-up):\n\n"
    for attr, descricao in gramatica['atributos_sintetizados'].items():
        if isinstance(descricao, list):
            md += f"- **{attr}**: valores possíveis = `{', '.join(descricao)}`\n"
        else:
            md += f"- **{attr}**: {descricao}\n"
    md += "\n"
    
    # atributos herdados
    md += "## Atributos Herdados\n\n"
    md += "Atributos calculados a partir do pai ou irmãos (propagação top-down):\n\n"
    for attr, descricao in gramatica['atributos_herdados'].items():
        md += f"- **{attr}**: {descricao}\n"
    md += "\n"
    
    # regra de promoção de tipos
    md += "## Regra de Promoção de Tipos\n\n"
    md += "A função `promover_tipo(τ₁, τ₂)` define o tipo resultante de operações entre tipos diferentes:\n\n"
    md += "```\n"
    md += "promover_tipo : Tipo × Tipo → Tipo\n\n"
    md += "promover_tipo(int, int)   = int\n"
    md += "promover_tipo(int, real)  = real\n"
    md += "promover_tipo(real, int)  = real\n"
    md += "promover_tipo(real, real) = real\n"
    md += "```\n\n"
    md += "Esta regra é aplicada em operações aritméticas (+, -, *, |) quando os operandos têm tipos diferentes.\n\n"
    
    # operações aritméticas
    md += "## Regras para Operações Aritméticas\n\n"
    
    for op, regra in gramatica['regras_tipo']['OPERACAO_ARITMETICA'].items():
        md += f"### Operador `{op}` - {regra['descricao']}\n\n"
        md += f"**Produção:** `{regra['producao']}`\n\n"
        
        md += "**Regra de Inferência:**\n\n"
        md += "```\n"
        condicoes_str = "    ".join(regra['condicoes'])
        md += f"Γ ⊢ operando₁ : τ₁    Γ ⊢ operando₂ : τ₂    {condicoes_str}\n"
        md += "─" * 70 + "\n"
        md += f"Γ ⊢ operando₁ {op} operando₂ : {regra['tipo_resultado']}\n"
        md += "```\n\n"
        
        md += "**Condições:**\n"
        for cond in regra['condicoes']:
            md += f"- {cond}\n"
        md += "\n"
        
        md += "**Verificações:**\n"
        for verif in regra['verificacoes']:
            md += f"- `{verif}`\n"
        md += "\n"
    
    # operações relacionais
    md += "## Regras para Operações Relacionais\n\n"
    md += "Todos os operadores relacionais (`>`, `<`, `>=`, `<=`, `==`, `!=`) seguem a mesma regra:\n\n"
    
    regra_rel = list(gramatica['regras_tipo']['OPERACAO_RELACIONAL'].values())[0]
    md += f"**Produção:** `{regra_rel['producao']}`\n\n"
    
    md += "**Regra de Inferência:**\n\n"
    md += "```\n"
    md += "Γ ⊢ operando₁ : τ₁    Γ ⊢ operando₂ : τ₂    τ₁, τ₂ ∈ {int, real}\n"
    md += "─" * 70 + "\n"
    md += "Γ ⊢ operando₁ op_rel operando₂ : booleano\n"
    md += "```\n\n"
    
    md += "**Descrição:** " + regra_rel['descricao'] + "\n\n"
    
    # comandos especiais
    md += "## Regras para Comandos Especiais\n\n"
    
    for cmd, regra in gramatica['regras_tipo']['COMANDOS'].items():
        md += f"### {cmd}\n\n"
        md += f"**Descrição:** {regra['descricao']}\n\n"
        md += f"**Produção:** `{regra['producao']}`\n\n"
        
        md += "**Condições:**\n"
        for cond in regra['condicoes']:
            md += f"- {cond}\n"
        md += "\n"
        
        md += f"**Tipo Resultado:** `{regra['tipo_resultado']}`\n\n"
        
        if 'efeito_colateral' in regra:
            md += f"**Efeito Colateral:** {regra['efeito_colateral']}\n\n"
    
    # estruturas de controle
    md += "## Regras para Estruturas de Controle\n\n"
    
    for ctrl, regra in gramatica['regras_tipo']['CONTROLE'].items():
        md += f"### {ctrl}\n\n"
        md += f"**Descrição:** {regra['descricao']}\n\n"
        md += f"**Produção:** `{regra['producao']}`\n\n"
        
        md += "**Condições:**\n"
        for cond in regra['condicoes']:
            md += f"- {cond}\n"
        md += "\n"
        
        md += f"**Tipo Resultado:** `{regra['tipo_resultado']}`\n\n"
    
    # salvar arquivo
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(md)

def gerar_relatorio_arvore_atribuida(arvore, info_estatisticas, arquivo="docs/ARVORE_ATRIBUIDA.md"):
    """
    gera relatório da árvore atribuída
    
    Args:
        arvore (dict): árvore atribuída
        info_estatisticas (dict): estatísticas da árvore
        arquivo (str): caminho do arquivo
    """
    from src.arvore_atribuida import imprimir_arvore_atribuida
    
    md = "# Árvore Sintática Abstrata Atribuída\n\n"
    md += f"*Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    md += "---\n\n"
    
    # estatísticas
    md += "## Estatísticas da Árvore\n\n"
    md += f"- **Total de nós:** {info_estatisticas['total_nos']}\n"
    md += f"- **Profundidade máxima:** {info_estatisticas['profundidade']}\n"
    md += f"- **Total de linhas processadas:** {info_estatisticas['total_linhas']}\n"
    
    if info_estatisticas['operadores_usados']:
        md += f"- **Operadores utilizados:** {', '.join(f'`{op}`' for op in info_estatisticas['operadores_usados'])}\n"
    else:
        md += "- **Operadores utilizados:** nenhum\n"
    
    md += "\n"
    
    # distribuição de tipos de nós
    md += "## Distribuição de Tipos de Nós\n\n"
    md += "| Tipo de Nó | Quantidade |\n"
    md += "|------------|------------|\n"
    
    for tipo, qtd in sorted(info_estatisticas['tipos_encontrados'].items()):
        md += f"| {tipo} | {qtd} |\n"
    
    md += "\n"
    
    # árvore formatada
    md += "## Estrutura da Árvore\n\n"
    md += "Representação hierárquica com tipos inferidos:\n\n"
    md += "```\n"
    md += imprimir_arvore_atribuida(arvore)
    md += "```\n\n"
    
    # legenda
    md += "## Legenda\n\n"
    md += "- **TIPO** : tipo_inferido = valor [operador] (linha)\n"
    md += "- Tipos possíveis: `int`, `real`, `booleano`\n"
    md += "- `├─` indica filho não-terminal\n"
    md += "- `└─` indica último filho\n\n"
    
    # salvar arquivo
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(md)

def gerar_relatorio_erros(erros, arquivo="docs/ERROS_SEMANTICOS.md"):
    """
    gera relatório de erros semânticos
    
    Args:
        erros (list): lista de erros encontrados
        arquivo (str): caminho do arquivo
    """
    md = "# Relatório de Erros Semânticos\n\n"
    md += f"*Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    md += "---\n\n"
    
    # resumo
    md += "## Resumo\n\n"
    
    if not erros:
        md += "✅ **Nenhum erro semântico encontrado!**\n\n"
        md += "A análise semântica foi concluída com sucesso. Todos os tipos são compatíveis, "
        md += "todas as memórias foram corretamente inicializadas e todas as estruturas de controle "
        md += "estão bem formadas.\n\n"
    else:
        md += f"⚠️ **Total de erros encontrados:** {len(erros)}\n\n"
        
        # classificar erros por tipo
        erros_tipo = {}
        for erro in erros:
            tipo = erro.get('tipo', 'ERRO_DESCONHECIDO')
            erros_tipo[tipo] = erros_tipo.get(tipo, 0) + 1
        
        md += "### Distribuição por Categoria\n\n"
        md += "| Categoria | Quantidade |\n"
        md += "|-----------|------------|\n"
        
        for tipo, qtd in sorted(erros_tipo.items()):
            md += f"| {tipo} | {qtd} |\n"
        
        md += "\n"
        
        # erros detalhados
        md += "## Erros Detalhados\n\n"
        
        for i, erro in enumerate(erros, 1):
            tipo = erro.get('tipo', 'ERRO_DESCONHECIDO')
            mensagem = erro.get('mensagem', 'Mensagem não especificada')
            linha = erro.get('linha')
            contexto = erro.get('contexto')
            
            linha_str = f"Linha {linha}" if linha else "Linha desconhecida"
            
            md += f"### Erro {i}: {tipo}\n\n"
            md += f"**Localização:** {linha_str}\n\n"
            md += f"**Mensagem:** {mensagem}\n\n"
            
            if contexto:
                md += f"**Contexto:**\n```\n{contexto}\n```\n\n"
            
            md += "---\n\n"
    
    # salvar arquivo
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(md)

def gerar_relatorio_julgamento_tipos(regras_aplicadas, arquivo="docs/JULGAMENTO_TIPOS.md"):
    """
    gera relatório do julgamento de tipos
    
    Args:
        regras_aplicadas (list): regras de dedução aplicadas
        arquivo (str): caminho do arquivo
    """
    md = "# Relatório de Julgamento de Tipos\n\n"
    md += f"*Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    md += "---\n\n"
    
    # introdução
    md += "## Introdução\n\n"
    md += "Este relatório documenta todas as regras de dedução de tipos aplicadas durante a "
    md += "análise semântica. Cada entrada mostra como o tipo de uma expressão foi inferido "
    md += "a partir dos tipos de seus componentes.\n\n"
    
    # estatísticas
    md += "## Estatísticas\n\n"
    md += f"- **Total de regras aplicadas:** {len(regras_aplicadas)}\n"
    
    if regras_aplicadas:
        # contar tipos inferidos
        tipos_contagem = {}
        for regra in regras_aplicadas:
            tipo = regra.get('tipo_inferido')
            if tipo:
                tipos_contagem[tipo] = tipos_contagem.get(tipo, 0) + 1
        
        md += "\n### Distribuição de Tipos Inferidos\n\n"
        md += "| Tipo | Quantidade |\n"
        md += "|------|------------|\n"
        
        for tipo, qtd in sorted(tipos_contagem.items()):
            md += f"| `{tipo}` | {qtd} |\n"
        
        md += "\n"
    
    # regras aplicadas
    md += "## Regras de Dedução Aplicadas\n\n"
    
    if not regras_aplicadas:
        md += "*Nenhuma regra de dedução foi aplicada.*\n\n"
    else:
        for i, regra in enumerate(regras_aplicadas, 1):
            linha = regra.get('linha', '?')
            tipo_no = regra.get('tipo_no', 'DESCONHECIDO')
            tipo_inferido = regra.get('tipo_inferido', '?')
            
            md += f"### Regra {i} - Linha {linha}\n\n"
            md += f"**Tipo do Nó:** `{tipo_no}`\n\n"
            md += f"**Tipo Inferido:** `{tipo_inferido}`\n\n"
            
            # informações adicionais para operações
            if tipo_no == 'OPERACAO':
                operador = regra.get('operador')
                tipos_operandos = regra.get('tipos_operandos', [])
                
                md += f"**Operador:** `{operador}`\n\n"
                
                if len(tipos_operandos) >= 2:
                    md += "**Dedução:**\n\n"
                    md += "```\n"
                    md += f"Γ ⊢ operando₁ : {tipos_operandos[0]}\n"
                    md += f"Γ ⊢ operando₂ : {tipos_operandos[1]}\n"
                    md += "─" * 50 + "\n"
                    md += f"Γ ⊢ operando₁ {operador} operando₂ : {tipo_inferido}\n"
                    md += "```\n\n"
                    
                    # explicação da promoção de tipos
                    if tipos_operandos[0] != tipos_operandos[1]:
                        md += f"*Promoção de tipos aplicada: `{tipos_operandos[0]}` + `{tipos_operandos[1]}` → `{tipo_inferido}`*\n\n"
            
            elif tipo_no == 'NUMERO':
                valor = regra.get('valor')
                if valor:
                    md += f"**Valor:** `{valor}`\n\n"
            
            md += "---\n\n"
    
    # salvar arquivo
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(md)

def gerar_todos_relatorios(gramatica, arvore, info_arvore, erros_todos, regras_aplicadas):
    """
    gera todos os 4 relatórios de uma vez
    
    Args:
        gramatica (dict): gramática de atributos
        arvore (dict): árvore atribuída
        info_arvore (dict): estatísticas da árvore
        erros_todos (list): todos os erros encontrados
        regras_aplicadas (list): regras de dedução aplicadas
    """
    print("\n📝 Gerando relatórios markdown...")
    
    try:
        gerar_relatorio_gramatica_atributos(gramatica)
        print("  ✓ GRAMATICA_ATRIBUTOS.md")
        
        gerar_relatorio_arvore_atribuida(arvore, info_arvore)
        print("  ✓ ARVORE_ATRIBUIDA.md")
        
        gerar_relatorio_erros(erros_todos)
        print("  ✓ ERROS_SEMANTICOS.md")
        
        gerar_relatorio_julgamento_tipos(regras_aplicadas)
        print("  ✓ JULGAMENTO_TIPOS.md")
        
        print("\n✅ Todos os relatórios foram gerados com sucesso na pasta docs/\n")
        
    except Exception as e:
        print(f"\n❌ Erro ao gerar relatórios: {str(e)}\n")
        raise

if __name__ == '__main__':
    print("=== TESTE DO FORMATADOR DE RELATÓRIOS ===\n")
    
    # teste básico
    from src.gramatica_atributos import definir_gramatica_atributos
    
    try:
        # criar dados de teste
        gramatica = definir_gramatica_atributos()
        
        arvore_teste = {
            'tipo': 'EXPRESSAO',
            'tipo_inferido': 'int',
            'linha': 1,
            'filhos': []
        }
        
        info_teste = {
            'total_nos': 3,
            'profundidade': 2,
            'total_linhas': 1,
            'operadores_usados': ['+'],
            'tipos_encontrados': {'EXPRESSAO': 1, 'OPERACAO': 1, 'NUMERO': 2}
        }
        
        erros_teste = []
        
        regras_teste = [
            {
                'linha': 1,
                'tipo_no': 'NUMERO',
                'tipo_inferido': 'int'
            }
        ]
        
        # gerar relatórios
        gerar_todos_relatorios(gramatica, arvore_teste, info_teste, erros_teste, regras_teste)
        
        print("✓ Teste concluído com sucesso!")
        
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
