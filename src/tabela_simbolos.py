# tabela de símbolos para gerenciamento de memórias e variáveis

class TabelaSimbolosError(Exception):
    """exceção para erros na tabela de símbolos"""
    def __init__(self, mensagem):
        self.mensagem = mensagem
        super().__init__(f"Erro na tabela de símbolos: {mensagem}")

def inicializar_tabela_simbolos():
    """
    cria estrutura inicial da tabela de símbolos
    
    Returns:
        dict: tabela de símbolos vazia com metadados
    """
    return {
        'simbolos': {},
        'escopo_atual': 0,
        'contador_escopos': 0,
        'historico_resultados': []
    }

def adicionar_simbolo(tabela, nome, tipo, valor=None, linha=None):
    """
    adiciona símbolo à tabela
    
    Args:
        tabela (dict): tabela de símbolos
        nome (str): nome da memória (ex: MEM, VAR, CONTADOR)
        tipo (str): tipo do símbolo ('int' ou 'real')
        valor: valor inicial (opcional)
        linha (int): linha de declaração
        
    Returns:
        bool: True se adicionado com sucesso
        
    Raises:
        TabelaSimbolosError: se símbolo inválido
    """
    if not nome:
        raise TabelaSimbolosError("Nome de símbolo vazio")
    
    if tipo not in ['int', 'real']:
        raise TabelaSimbolosError(f"Tipo inválido: {tipo}")
    
    # verificar se nome é válido (letras maiúsculas)
    if not nome.isupper() or not nome.isalpha():
        raise TabelaSimbolosError(f"Nome de símbolo inválido: {nome}")
    
    simbolo = {
        'nome': nome,
        'tipo': tipo,
        'inicializada': valor is not None,
        'valor': valor,
        'linha_declaracao': linha,
        'escopo': tabela['escopo_atual']
    }
    
    tabela['simbolos'][nome] = simbolo
    return True

def buscar_simbolo(tabela, nome):
    """
    busca símbolo na tabela
    
    Args:
        tabela (dict): tabela de símbolos
        nome (str): nome do símbolo
        
    Returns:
        dict: informações do símbolo ou None se não encontrado
    """
    return tabela['simbolos'].get(nome)

def simbolo_existe(tabela, nome):
    """
    verifica se símbolo existe na tabela
    
    Args:
        tabela (dict): tabela de símbolos
        nome (str): nome do símbolo
        
    Returns:
        bool: True se existe
    """
    return nome in tabela['simbolos']

def simbolo_inicializado(tabela, nome):
    """
    verifica se símbolo foi inicializado
    
    Args:
        tabela (dict): tabela de símbolos
        nome (str): nome do símbolo
        
    Returns:
        bool: True se inicializado
        
    Raises:
        TabelaSimbolosError: se símbolo não existe
    """
    if not simbolo_existe(tabela, nome):
        raise TabelaSimbolosError(f"Símbolo '{nome}' não existe na tabela")
    
    simbolo = tabela['simbolos'][nome]
    return simbolo['inicializada']

def atualizar_simbolo(tabela, nome, **kwargs):
    """
    atualiza informações de um símbolo
    
    Args:
        tabela (dict): tabela de símbolos
        nome (str): nome do símbolo
        **kwargs: atributos a atualizar (tipo, valor, inicializada, etc)
        
    Raises:
        TabelaSimbolosError: se símbolo não existe
    """
    if not simbolo_existe(tabela, nome):
        raise TabelaSimbolosError(f"Símbolo '{nome}' não existe na tabela")
    
    simbolo = tabela['simbolos'][nome]
    
    for chave, valor in kwargs.items():
        if chave in simbolo:
            simbolo[chave] = valor
        else:
            raise TabelaSimbolosError(f"Atributo inválido: {chave}")

def obter_tipo_simbolo(tabela, nome):
    """
    obtém tipo de um símbolo
    
    Args:
        tabela (dict): tabela de símbolos
        nome (str): nome do símbolo
        
    Returns:
        str: tipo do símbolo ('int' ou 'real')
        
    Raises:
        TabelaSimbolosError: se símbolo não existe
    """
    if not simbolo_existe(tabela, nome):
        raise TabelaSimbolosError(f"Símbolo '{nome}' não existe na tabela")
    
    return tabela['simbolos'][nome]['tipo']

def adicionar_resultado_historico(tabela, tipo, valor=None):
    """
    adiciona resultado ao histórico
    
    Args:
        tabela (dict): tabela de símbolos
        tipo (str): tipo do resultado
        valor: valor (opcional)
    """
    resultado = {
        'tipo': tipo,
        'valor': valor
    }
    tabela['historico_resultados'].append(resultado)

def obter_resultado_historico(tabela, n):
    """
    obtém resultado N linhas anteriores
    
    Args:
        tabela (dict): tabela de símbolos
        n (int): número de linhas para trás
        
    Returns:
        dict: resultado com tipo e valor
        
    Raises:
        TabelaSimbolosError: se N inválido
    """
    if n < 1:
        raise TabelaSimbolosError(f"N deve ser positivo: {n}")
    
    if n > len(tabela['historico_resultados']):
        raise TabelaSimbolosError(
            f"Histórico insuficiente: solicitado {n}, disponível {len(tabela['historico_resultados'])}"
        )
    
    # N=1 é o resultado imediatamente anterior (índice -1)
    indice = -n
    return tabela['historico_resultados'][indice]

def entrar_escopo(tabela):
    """
    entra em novo escopo (para estruturas de controle aninhadas)
    
    Args:
        tabela (dict): tabela de símbolos
    """
    tabela['contador_escopos'] += 1
    tabela['escopo_atual'] = tabela['contador_escopos']

def sair_escopo(tabela):
    """
    sai do escopo atual
    
    Args:
        tabela (dict): tabela de símbolos
    """
    if tabela['escopo_atual'] > 0:
        # remove símbolos do escopo atual
        simbolos_remover = [
            nome for nome, info in tabela['simbolos'].items()
            if info['escopo'] == tabela['escopo_atual']
        ]
        
        for nome in simbolos_remover:
            del tabela['simbolos'][nome]
        
        tabela['escopo_atual'] -= 1

def listar_simbolos(tabela):
    """
    lista todos os símbolos da tabela
    
    Args:
        tabela (dict): tabela de símbolos
        
    Returns:
        list: lista de tuplas (nome, info)
    """
    return [(nome, info) for nome, info in tabela['simbolos'].items()]

def listar_simbolos_escopo(tabela, escopo=None):
    """
    lista símbolos de um escopo específico
    
    Args:
        tabela (dict): tabela de símbolos
        escopo (int): nível de escopo (None para escopo atual)
        
    Returns:
        list: lista de tuplas (nome, info)
    """
    if escopo is None:
        escopo = tabela['escopo_atual']
    
    return [
        (nome, info) for nome, info in tabela['simbolos'].items()
        if info['escopo'] == escopo
    ]

def imprimir_tabela(tabela):
    """
    imprime tabela de símbolos formatada
    
    Args:
        tabela (dict): tabela de símbolos
        
    Returns:
        str: representação textual da tabela
    """
    resultado = "=== TABELA DE SÍMBOLOS ===\n\n"
    
    if not tabela['simbolos']:
        resultado += "Tabela vazia\n"
        return resultado
    
    resultado += f"Escopo atual: {tabela['escopo_atual']}\n\n"
    
    # cabeçalho
    resultado += f"{'Nome':<15} {'Tipo':<8} {'Inicializada':<12} {'Valor':<10} {'Linha':<6} {'Escopo':<6}\n"
    resultado += "-" * 70 + "\n"
    
    # símbolos
    for nome, info in sorted(tabela['simbolos'].items()):
        inicializada = 'Sim' if info['inicializada'] else 'Não'
        valor = str(info['valor']) if info['valor'] is not None else '-'
        linha = str(info['linha_declaracao']) if info['linha_declaracao'] else '-'
        
        resultado += f"{nome:<15} {info['tipo']:<8} {inicializada:<12} {valor:<10} {linha:<6} {info['escopo']:<6}\n"
    
    # histórico
    if tabela['historico_resultados']:
        resultado += f"\n=== HISTÓRICO DE RESULTADOS ({len(tabela['historico_resultados'])}) ===\n\n"
        for i, res in enumerate(tabela['historico_resultados'], 1):
            valor = str(res['valor']) if res['valor'] is not None else '-'
            resultado += f"  {i}. Tipo: {res['tipo']}, Valor: {valor}\n"
    
    return resultado

def validar_tabela(tabela):
    """
    valida consistência da tabela de símbolos
    
    Args:
        tabela (dict): tabela de símbolos
        
    Returns:
        tuple: (bool_valida, lista_erros)
    """
    erros = []
    
    # verificar estrutura básica
    if 'simbolos' not in tabela:
        erros.append("Tabela sem campo 'simbolos'")
    
    if 'escopo_atual' not in tabela:
        erros.append("Tabela sem campo 'escopo_atual'")
    
    if 'historico_resultados' not in tabela:
        erros.append("Tabela sem campo 'historico_resultados'")
    
    if erros:
        return False, erros
    
    # verificar símbolos
    for nome, info in tabela['simbolos'].items():
        if 'tipo' not in info:
            erros.append(f"Símbolo '{nome}' sem tipo")
        elif info['tipo'] not in ['int', 'real']:
            erros.append(f"Símbolo '{nome}' com tipo inválido: {info['tipo']}")
        
        if 'inicializada' not in info:
            erros.append(f"Símbolo '{nome}' sem flag de inicialização")
        
        if 'escopo' not in info:
            erros.append(f"Símbolo '{nome}' sem escopo")
    
    return len(erros) == 0, erros

if __name__ == '__main__':
    # teste da tabela de símbolos
    print("=== TESTE DA TABELA DE SÍMBOLOS ===\n")
    
    try:
        # inicializar tabela
        tabela = inicializar_tabela_simbolos()
        print("✓ Tabela inicializada")
        
        # adicionar símbolos
        adicionar_simbolo(tabela, 'MEM', 'real', 42.5, linha=1)
        print("✓ Símbolo MEM adicionado")
        
        adicionar_simbolo(tabela, 'CONTADOR', 'int', 0, linha=2)
        print("✓ Símbolo CONTADOR adicionado")
        
        adicionar_simbolo(tabela, 'VAR', 'int', linha=3)
        print("✓ Símbolo VAR adicionado (não inicializado)")
        
        # buscar símbolos
        mem = buscar_simbolo(tabela, 'MEM')
        print(f"\n✓ Busca MEM: tipo={mem['tipo']}, valor={mem['valor']}")
        
        # verificar inicialização
        print(f"✓ MEM inicializada: {simbolo_inicializado(tabela, 'MEM')}")
        print(f"✓ VAR inicializada: {simbolo_inicializado(tabela, 'VAR')}")
        
        # atualizar símbolo
        atualizar_simbolo(tabela, 'VAR', valor=10, inicializada=True)
        print("✓ VAR atualizada")
        
        # adicionar ao histórico
        adicionar_resultado_historico(tabela, 'int', 100)
        adicionar_resultado_historico(tabela, 'real', 3.14)
        print("✓ Resultados adicionados ao histórico")
        
        # obter do histórico
        res = obter_resultado_historico(tabela, 1)
        print(f"✓ Resultado anterior: tipo={res['tipo']}, valor={res['valor']}")
        
        # imprimir tabela
        print("\n" + imprimir_tabela(tabela))
        
        # validar
        valida, erros = validar_tabela(tabela)
        if valida:
            print("✓ Tabela válida")
        else:
            print(f"✗ Erros: {erros}")
        
    except TabelaSimbolosError as e:
        print(f"Erro: {e}")
