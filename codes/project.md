# Proposta de Estrutura para Fase 3 - Analisador Semântico

Analisando os arquivos da base de conhecimento e a documentação da Fase 3, proponho a seguinte estrutura:

## 📁 Estrutura de Arquivos Proposta

```
.
├── src/
│   ├── __init__.py
│   ├── token_types.py              # [EXISTENTE - ATUALIZAR]
│   ├── lexer.py                    # [EXISTENTE - ATUALIZAR]
│   ├── grammar.py                  # [EXISTENTE - MANTER]
│   ├── parser.py                   # [EXISTENTE - MANTER]
│   ├── syntax_tree.py              # [EXISTENTE - MANTER]
│   ├── executor.py                 # [EXISTENTE - MANTER]
│   ├── token_reader.py             # [EXISTENTE - MANTER]
│   ├── control_structures.py       # [EXISTENTE - MANTER]
│   ├── assembly_generator.py       # [EXISTENTE - MANTER]
│   │
│   ├── gramatica_atributos.py      # [NOVO - ALUNO 1]
│   ├── tabela_simbolos.py          # [NOVO - ALUNO 1]
│   ├── analisador_tipos.py         # [NOVO - ALUNO 2]
│   ├── analisador_memoria.py       # [NOVO - ALUNO 3]
│   ├── analisador_controle.py      # [NOVO - ALUNO 3]
│   └── arvore_atribuida.py         # [NOVO - ALUNO 4]
│
├── tests/
│   ├── test_lexer.py               # [EXISTENTE - MANTER]
│   ├── test_grammar.py             # [EXISTENTE - MANTER]
│   ├── test_parser.py              # [EXISTENTE - MANTER]
│   ├── test_executor.py            # [EXISTENTE - MANTER]
│   ├── test_semantico.py           # [NOVO]
│   └── test_tabela_simbolos.py     # [NOVO]
│
├── utils/
│   ├── util.py                     # [EXISTENTE - MANTER]
│   └── formatador_relatorios.py   # [NOVO - ALUNO 4]
│
├── docs/                            # [NOVO - DOCUMENTAÇÃO MARKDOWN]
│   ├── GRAMATICA_ATRIBUTOS.md      # Gramática de atributos
│   ├── ARVORE_ATRIBUIDA.md         # Árvore da última execução
│   ├── ERROS_SEMANTICOS.md         # Erros detectados
│   └── JULGAMENTO_TIPOS.md         # Regras de dedução aplicadas
│
├── test_fase3_1.txt                # [NOVO - 3 arquivos mínimo]
├── test_fase3_2.txt                # [NOVO - com erros semânticos]
├── test_fase3_3.txt                # [NOVO - casos complexos]
│
├── main_semantico.py               # [NOVO - ALUNO 4]
├── main_parser.py                  # [EXISTENTE - MANTER]
├── run_test.py                     # [EXISTENTE - ATUALIZAR]
└── README.md                       # [EXISTENTE - ATUALIZAR]
```

---

## 🔧 Detalhamento dos Novos Módulos

### **1. `src/gramatica_atributos.py` - ALUNO 1**

**Responsabilidade:** Definir gramática de atributos e estrutura semântica

**Funções principais:**
```python
def definir_gramatica_atributos()
    """
    Define regras semânticas da linguagem
    
    Returns:
        dict: Estrutura com:
            - 'regras': regras de produção com atributos
            - 'atributos_sintetizados': definições
            - 'atributos_herdados': definições
            - 'regras_tipo': regras de inferência de tipos
    """

def obter_regra_semantica(tipo_no, operador=None)
    """
    Retorna regra semântica para um tipo de nó
    
    Args:
        tipo_no (str): tipo do nó (OPERACAO, NUMERO, etc)
        operador (str): operador quando aplicável
        
    Returns:
        dict: regra semântica com verificações de tipo
    """

def promover_tipo(tipo1, tipo2)
    """
    Define tipo resultante de operação entre tipos diferentes
    
    Args:
        tipo1 (str): primeiro tipo ('int' ou 'real')
        tipo2 (str): segundo tipo ('int' ou 'real')
        
    Returns:
        str: tipo resultante ('int' ou 'real')
    """
```

**Estrutura de dados:**
```python
# Exemplo de regra na gramática de atributos
{
    'producao': 'OPERACAO → OPERANDO OPERANDO OPERADOR_ARIT',
    'operador': '+',
    'regra_tipo': {
        'se': ['operando1.tipo == int', 'operando2.tipo == int'],
        'entao': 'resultado.tipo = int',
        'senao_se': ['operando1.tipo in [int, real]', 'operando2.tipo in [int, real]'],
        'entao': 'resultado.tipo = real'
    },
    'verificacoes': ['tipos_compativeis(operando1, operando2)']
}
```

---

### **2. `src/tabela_simbolos.py` - ALUNO 1**

**Responsabilidade:** Gerenciar símbolos (memórias/variáveis)

**Funções principais:**
```python
def inicializar_tabela_simbolos()
    """
    Cria estrutura inicial da tabela de símbolos
    
    Returns:
        dict: Tabela de símbolos vazia
    """

def adicionar_simbolo(tabela, nome, tipo, valor=None, linha=None)
    """
    Adiciona símbolo à tabela
    
    Args:
        tabela (dict): tabela de símbolos
        nome (str): nome da memória (ex: MEM, VAR)
        tipo (str): tipo do símbolo ('int' ou 'real')
        valor: valor inicial (opcional)
        linha (int): linha de declaração
        
    Returns:
        bool: True se adicionado com sucesso
    """

def buscar_simbolo(tabela, nome)
    """
    Busca símbolo na tabela
    
    Args:
        tabela (dict): tabela de símbolos
        nome (str): nome do símbolo
        
    Returns:
        dict: informações do símbolo ou None
    """

def simbolo_inicializado(tabela, nome)
    """
    Verifica se símbolo foi inicializado
    
    Args:
        tabela (dict): tabela de símbolos
        nome (str): nome do símbolo
        
    Returns:
        bool: True se inicializado
    """

def atualizar_simbolo(tabela, nome, **kwargs)
    """
    Atualiza informações de um símbolo
    
    Args:
        tabela (dict): tabela de símbolos
        nome (str): nome do símbolo
        **kwargs: atributos a atualizar
    """
```

**Estrutura da tabela:**
```python
{
    'MEM': {
        'tipo': 'real',
        'inicializada': True,
        'valor': 42.5,
        'linha_declaracao': 3,
        'escopo': 0
    },
    'CONTADOR': {
        'tipo': 'int',
        'inicializada': True,
        'valor': 0,
        'linha_declaracao': 5,
        'escopo': 0
    }
}
```

---

### **3. `src/analisador_tipos.py` - ALUNO 2**

**Responsabilidade:** Verificação de tipos e inferência

**Funções principais:**
```python
def analisar_semantica(arvore_sintatica, gramatica_atributos, tabela_simbolos)
    """
    Análise semântica principal - verificação de tipos
    
    Args:
        arvore_sintatica (dict): AST da Fase 2
        gramatica_atributos (dict): regras semânticas
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        tuple: (arvore_anotada, lista_erros)
    """

def inferir_tipo(no, tabela_simbolos)
    """
    Infere tipo de um nó da árvore
    
    Args:
        no (dict): nó da árvore
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        str: tipo inferido ('int', 'real', 'booleano')
    """

def verificar_compatibilidade_tipos(tipo1, tipo2, operador)
    """
    Verifica se tipos são compatíveis para operação
    
    Args:
        tipo1 (str): tipo do primeiro operando
        tipo2 (str): tipo do segundo operando
        operador (str): operador da operação
        
    Returns:
        tuple: (bool_compativel, tipo_resultado)
    """

def anotar_tipo_no(no, tipo)
    """
    Adiciona anotação de tipo ao nó
    
    Args:
        no (dict): nó da árvore
        tipo (str): tipo a ser anotado
    """

def validar_operacao_aritmetica(no, tabela_simbolos)
    """
    Valida operação aritmética específica
    
    Args:
        no (dict): nó OPERACAO
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        tuple: (tipo_resultado, erro_ou_None)
    """
```

**Classes de erro:**
```python
class ErroSemantico(Exception):
    """Exceção para erros semânticos"""
    def __init__(self, mensagem, linha=None, contexto=None)
```

---

### **4. `src/analisador_memoria.py` - ALUNO 3**

**Responsabilidade:** Validação de memórias e comandos especiais

**Funções principais:**
```python
def analisar_semantica_memoria(arvore_sintatica, tabela_simbolos)
    """
    Valida uso de memórias (MEM)
    
    Args:
        arvore_sintatica (dict): árvore já anotada com tipos
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        tuple: (tabela_atualizada, lista_erros)
    """

def validar_comando_armazenar(no, tabela_simbolos)
    """
    Valida comando (V MEM)
    
    Args:
        no (dict): nó COMANDO_ARMAZENAR
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        erro_ou_None
    """

def validar_comando_recuperar(no, tabela_simbolos)
    """
    Valida comando (MEM) - AGORA ERRO SE NÃO INICIALIZADA
    
    Args:
        no (dict): nó COMANDO_RECUPERAR
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        erro_ou_None
    """

def validar_comando_res(no, historico_resultados)
    """
    Valida comando (N RES)
    
    Args:
        no (dict): nó COMANDO_RES
        historico_resultados (list): lista de resultados anteriores
        
    Returns:
        erro_ou_None
    """
```

---

### **5. `src/analisador_controle.py` - ALUNO 3**

**Responsabilidade:** Validação de estruturas de controle

**Funções principais:**
```python
def analisar_semantica_controle(arvore_sintatica, tabela_simbolos)
    """
    Valida estruturas de controle (IF, WHILE)
    
    Args:
        arvore_sintatica (dict): árvore anotada
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        lista_erros
    """

def validar_estrutura_decisao(no, tabela_simbolos)
    """
    Valida estrutura IF
    
    Args:
        no (dict): nó DECISAO
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        erro_ou_None
    """

def validar_estrutura_laco(no, tabela_simbolos)
    """
    Valida estrutura WHILE
    
    Args:
        no (dict): nó LACO
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        erro_ou_None
    """

def validar_condicao(condicao_no, tabela_simbolos)
    """
    Valida que condição retorna booleano
    
    Args:
        condicao_no (dict): nó de condição
        tabela_simbolos (dict): tabela de símbolos
        
    Returns:
        tuple: (bool_valido, erro_ou_None)
    """
```

---

### **6. `src/arvore_atribuida.py` - ALUNO 4**

**Responsabilidade:** Gerar árvore atribuída final e salvar

**Funções principais:**
```python
def gerar_arvore_atribuida(arvore_anotada)
    """
    Constrói árvore sintática abstrata atribuída final
    
    Args:
        arvore_anotada (dict): árvore com anotações de tipo
        
    Returns:
        dict: árvore atribuída completa
    """

def salvar_arvore_json(arvore, nome_arquivo="arvore_atribuida.json")
    """
    Salva árvore em formato JSON
    
    Args:
        arvore (dict): árvore atribuída
        nome_arquivo (str): nome do arquivo
    """

def imprimir_arvore_atribuida(arvore, nivel=0)
    """
    Imprime árvore formatada com tipos
    
    Args:
        arvore (dict): árvore atribuída
        nivel (int): nível de indentação
        
    Returns:
        str: representação textual
    """
```

**Formato da árvore atribuída JSON:**
```python
{
    "tipo": "EXPRESSAO",
    "tipo_inferido": "int",
    "linha": 1,
    "filhos": [
        {
            "tipo": "OPERACAO",
            "operador": "+",
            "tipo_inferido": "int",
            "linha": 1,
            "filhos": [
                {
                    "tipo": "NUMERO",
                    "valor": "3",
                    "tipo_inferido": "int",
                    "linha": 1,
                    "filhos": []
                },
                {
                    "tipo": "NUMERO",
                    "valor": "5",
                    "tipo_inferido": "int",
                    "linha": 1,
                    "filhos": []
                }
            ]
        }
    ]
}
```

---

### **7. `utils/formatador_relatorios.py` - ALUNO 4**

**Responsabilidade:** Gerar relatórios markdown

**Funções principais:**
```python
def gerar_relatorio_gramatica_atributos(gramatica, arquivo="docs/GRAMATICA_ATRIBUTOS.md")
    """
    Gera documentação da gramática de atributos
    
    Args:
        gramatica (dict): gramática de atributos
        arquivo (str): caminho do arquivo
    """

def gerar_relatorio_arvore_atribuida(arvore, arquivo="docs/ARVORE_ATRIBUIDA.md")
    """
    Gera relatório da árvore atribuída
    
    Args:
        arvore (dict): árvore atribuída
        arquivo (str): caminho do arquivo
    """

def gerar_relatorio_erros(erros, arquivo="docs/ERROS_SEMANTICOS.md")
    """
    Gera relatório de erros semânticos
    
    Args:
        erros (list): lista de erros encontrados
        arquivo (str): caminho do arquivo
    """

def gerar_relatorio_julgamento_tipos(regras_aplicadas, arquivo="docs/JULGAMENTO_TIPOS.md")
    """
    Gera relatório do julgamento de tipos
    
    Args:
        regras_aplicadas (list): regras de dedução aplicadas
        arquivo (str): caminho do arquivo
    """
```

---

### **8. `main_semantico.py` - ALUNO 4**

**Responsabilidade:** Programa principal integrado

```python
def main():
    """
    Executa análise completa: léxica, sintática e semântica
    
    Uso: python main_semantico.py test_fase3_1.txt
    """
    # 1. Ler arquivo de entrada
    # 2. Análise Léxica (Fase 1)
    # 3. Análise Sintática (Fase 2) -> AST
    # 4. Definir Gramática de Atributos (Aluno 1)
    # 5. Inicializar Tabela de Símbolos (Aluno 1)
    # 6. Análise Semântica - Tipos (Aluno 2)
    # 7. Análise Semântica - Memória (Aluno 3)
    # 8. Análise Semântica - Controle (Aluno 3)
    # 9. Gerar Árvore Atribuída (Aluno 4)
    # 10. Gerar Relatórios (Aluno 4)
    # 11. Exibir erros no console
```

---

## 📝 Atualizações Necessárias

### **`src/token_types.py` - ATUALIZAR**

Adicionar operadores relacionais e novo operador de divisão:

```python
# Operadores relacionais (NOVOS)
OPERADORES_RELACIONAIS = {'>', '<', '>=', '<=', '==', '!='}

# Atualizar operadores válidos
OPERADORES_VALIDOS = {'+', '-', '*', '|', '/', '%', '^'}  # '|' é novo
```

### **`src/lexer.py` - ATUALIZAR**

Reconhecer `|` como operador de divisão real e operadores relacionais de dois caracteres (`>=`, `<=`, `==`, `!=`)

---

## 🧪 Arquivos de Teste

### **test_fase3_1.txt** - Casos válidos
```
(5 3 +)
(10 2 /)
(10.0 2.0 |)
(42 MEM)
(MEM)
(2 3 ^)
((MEM 10 >) ((MEM 5 -) MEM) ((MEM 5 +) MEM) IF)
((5 10 <) ((5 1 +) CONTADOR) WHILE)
```

### **test_fase3_2.txt** - Erros semânticos
```
(VAR_NAO_INICIALIZADA)
(5.5 2 /)
(2 3.5 %)
(2.0 3.5 ^)
```

### **test_fase3_3.txt** - Casos complexos
```
(100 INICIAL)
((INICIAL 50 >) ((INICIAL 10 -) INICIAL) ((INICIAL 10 +) INICIAL) IF)
(INICIAL 2 ^)
```

---

## 📋 Checklist de Implementação

### Aluno 1:
- [ ] `src/gramatica_atributos.py`
- [ ] `src/tabela_simbolos.py`
- [ ] `docs/GRAMATICA_ATRIBUTOS.md` (documentação)
- [ ] Testes unitários da tabela de símbolos

### Aluno 2:
- [ ] `src/analisador_tipos.py`
- [ ] Integração com gramática de atributos
- [ ] Testes de verificação de tipos

### Aluno 3:
- [ ] `src/analisador_memoria.py`
- [ ] `src/analisador_controle.py`
- [ ] Testes de memória e controle

### Aluno 4:
- [ ] `src/arvore_atribuida.py`
- [ ] `utils/formatador_relatorios.py`
- [ ] `main_semantico.py`
- [ ] Atualizar `README.md`
- [ ] Criar 3 arquivos de teste
- [ ] Gerar todos os relatórios markdown

---

## 🔗 Interfaces entre Módulos

```
lexer.py → parser.py → analisador_tipos.py → analisador_memoria.py → analisador_controle.py → arvore_atribuida.py → relatórios
                ↓                ↓                      ↓
         gramatica_atributos   tabela_simbolos    tabela_simbolos
```

---

Esta estrutura:
- ✅ Segue o padrão das Fases 1 e 2
- ✅ Respeita a divisão de tarefas especificada
- ✅ Não adiciona funcionalidades além do pedido
- ✅ Mantém organização clara e modular
- ✅ Facilita integração e testes