# Analisador Léxico e Executador RPN - Fase 1

## Descrição

Projeto implementa um **analisador léxico** baseado em **autômato finito determinístico (AFD)** e um **executador** que processa expressões matemáticas em **notação polonesa reversa (RPN)**. O sistema reconhece tokens válidos, detecta erros léxicos e executa operações matemáticas com comandos especiais de memória.

### Características:

- **AFD implementado com funções**: cada estado do autômato é representado por uma função
- **Executador RPN**: avalia expressões usando pilha com precisão IEEE 754
- **Tokens suportados**: números reais, operadores aritméticos, parênteses, palavras reservadas e identificadores
- **Comandos especiais**: gerenciamento de memória e histórico de resultados
- **Detecção de erros**: números malformados, parênteses desbalanceados, divisão por zero

## Estrutura do Projeto

```
├── src/
│   ├── lexer.py          # Analisador léxico principal (AFD)
│   ├── executor.py       # Executador de expressões RPN
│   └── token_types.py    # Definições de tipos de tokens
├── tests/
│   ├── test_lexer.py     # Testes unitários do analisador léxico
│   └── test_executor.py  # Testes unitários do executador
├── utils/
│   └── util.py           # Utilitários auxiliares
├── main.py               # Programa principal
├── expressoes.txt        # Arquivo de teste com expressões RPN
├── texto1.txt            # Arquivos de teste adicionais
├── texto2.txt
├── texto3.txt
├── tokens.txt            # Tokens gerados na última execução
└── README.md
```

## Operadores e Comandos Suportados

### Operadores aritméticos
- **Adição**: `+` → `(A B +)`
- **Subtração**: `-` → `(A B -)`
- **Multiplicação**: `*` → `(A B *)`
- **Divisão**: `/` → `(A B /)`
- **Resto da divisão**: `%` → `(A B %)`
- **Potenciação**: `^` → `(A B ^)`

### Comandos especiais
- **`(N RES)`**: Retorna resultado N linhas anteriores
- **`(V MEM)`**: Armazena valor V na memória MEM
- **`(MEM)`**: Recupera valor da memória MEM (retorna 0.0 se não inicializada)

### Formatos numéricos
- **Inteiros**: `5`, `10`, `42`
- **Decimais**: `3.14`, `2.0`, `15.75` (duas casas decimais)
- **Identificadores**: `MEM`, `VAR`, `CONTADOR` (letras maiúsculas)

## Como executar

### Execução principal
```bash
# Processar arquivo de expressões
python main.py expressoes.txt
```

### Execução de testes
```bash
# Testar analisador léxico
python tests/test_lexer.py

# Testar executador
python tests/test_executor.py
```

## Exemplos de uso

### Operações básicas
```
(3 7 +)         # Resultado: 10.0
(7 7 *)         # Resultado: 49.0
(18 9 /)        # Resultado: 2.0
```

### Expressões aninhadas
```
((2 3 *) (4 2 /) /)     # (6 / 2) = 3.0
((1.5 2.0 *) (6.0 3.0 /) +)  # 3.0 + 2.0 = 5.0
```

### Comandos especiais
```
(42.5 MEM)      # Armazena 42.5 na memória MEM
(MEM)           # Recupera valor: 42.5
(2 RES)         # Resultado 2 linhas anteriores
(3 VAR)         # Armazena 3.0 na variável VAR
(VAR 2 +)       # Soma VAR + 2 = 5.0
```

## Funcionalidades do Executador

### Gerenciamento de memória
- **Múltiplas variáveis**: MEM, VAR, CONTADOR, etc.
- **Persistência**: Valores mantidos durante execução do arquivo
- **Inicialização automática**: Variáveis não inicializadas retornam 0.0

### Histórico de resultados
- **Comando RES**: Acesso a resultados anteriores
- **Indexação relativa**: N linhas para trás no histórico
- **Validação**: Verifica se o resultado solicitado existe

### Precisão numérica
- **IEEE 754**: Operações em ponto flutuante
- **Formatação**: Resultados com duas casas decimais
- **Tratamento de erros**: Divisão por zero, overflow

## Tratamento de erros

### Erros léxicos
```
(3.14 2.0 &)      # Operador inválido
(3.14.5 2.0 +)    # Número malformado
((3.14 2.0 +)     # Parênteses desbalanceados
```

### Erros de execução
```
(5 0 /)           # Divisão por zero
(10 RES)          # RES inválido (histórico insuficiente)
(5 +)             # Operandos insuficientes
```

## Arquivos gerados

### tokens.txt
Arquivo com tokens da última execução do analisador léxico:
```
Tokens gerados pelo analisador léxico:
==================================================

Token 1:
  Tipo: PARENTESE_ABRE
  Valor: (
  Posição: 1
...
```

## Implementação técnica

### Analisador léxico (AFD)
- **Estados**: inicial, numero, numero_decimal, identificador  
- **Validação em tempo real**: erros detectados durante tokenização
- **Balanceamento**: parênteses validados automaticamente

### Executador RPN
- **Algoritmo de pilha**: avaliação eficiente de expressões
- **Contexto de execução**: histórico e memória compartilhados
- **Recursividade**: suporte a expressões aninhadas

# Analisador Sintático LL(1) - Fase 2

Implementação de um analisador sintático descendente recursivo LL(1) para linguagem de programação em notação polonesa reversa (RPN). Este projeto complementa a Fase 1 (Analisador Léxico) adicionando análise sintática, construção de árvore sintática abstrata e validação estrutural das expressões.

## Características da Linguagem

### Notação RPN

Expressões no formato `(operando1 operando2 operador)`.

**Operadores Aritméticos:**
- Adição: `+`
- Subtração: `-`
- Multiplicação: `*`
- Divisão: `/`
- Resto: `%`
- Potenciação: `^`

**Operadores Relacionais:**
- `>`, `<`, `==`, `!=`, `>=`, `<=`

**Comandos Especiais:**
- `(N RES)` - recupera resultado N linhas anteriores
- `(V MEM)` - armazena valor V na memória MEM
- `(MEM)` - recupera valor da memória MEM

**Expressões Aninhadas:**
```
((2 3 +) (4 5 *) -)
(((1 2 +) (3 4 *) +) 2 /)
```

## Uso

### Executar Analisador Sintático
```bash
python3 main_parser.py 
```

**Exemplo:**
```bash
python3 main_parser.py test1.txt
```

### Executar Testes

**Suite completa:**
```bash
python3 run_test.py
```

**Testes unitários:**
```bash
python3 -m pytest tests/test_parser.py -v
python3 -m pytest tests/test_grammar.py -v
```

**Testes standalone:**
```bash
python3 tests/test_parser.py --standalone
python3 tests/test_grammar.py --standalone
```

### Testar Módulos Individuais
```bash
python3 src/grammar.py     # Visualizar gramática e tabela LL(1)
python3 src/lexer.py       # Testar analisador léxico
python3 src/parser.py      # Testar parser
python3 src/syntax_tree.py # Testar geração de árvore
```

## Saídas Geradas

### GRAMATICA.md
Documentação automática contendo:
- Regras de produção da gramática
- Conjuntos FIRST e FOLLOW
- Tabela de análise LL(1)
- Exemplo de árvore sintática

### arvore_sintatica.json
Árvore sintática em formato JSON da última expressão processada.

## Arquivos de Teste

### test1.txt
- Operações aritméticas básicas
- Números inteiros e decimais
- Comandos de memória (MEM, VAR)
- Comando RES
- Expressões aninhadas

### test2.txt
- Armazenamento e recuperação de variáveis
- Operações com identificadores
- Combinações de comandos

### test3.txt
- Aninhamento profundo de expressões
- Uso de RES com operações
- Casos complexos

## Divisão de Tarefas

### Gramática e Análise LL(1)
**Arquivo:** `src/grammar.py`

Funções:
- `construir_gramatica()` - Define regras de produção
- `calcular_first()` - Calcula conjuntos FIRST
- `calcular_follow()` - Calcula conjuntos FOLLOW
- `construir_tabela_ll1()` - Constrói tabela de análise
- `validar_gramatica_ll1()` - Valida ausência de conflitos

### Parser Descendente Recursivo
**Arquivo:** `src/parser.py`

Funções:
- `parsear()` - Análise sintática principal
- `parse_expressao()` - Analisa expressões
- `parse_operacao()` - Analisa operações
- `parse_comando_memoria()` - Analisa comandos MEM
- `parse_comando_res()` - Analisa comando RES

### Leitura de Tokens
**Arquivo:** `src/token_reader.py`

Funções:
- `ler_tokens()` - Lê tokens de arquivo
- `validar_tokens()` - Valida estrutura de tokens

### Árvore Sintática e Integração
**Arquivos:** `src/syntax_tree.py`, `main_parser.py`

Funções:
- `gerar_arvore()` - Constrói AST
- `imprimir_arvore()` - Visualiza árvore
- `salvar_arvore()` - Salva em JSON
- `main()` - Integração de módulos
- `salvar_documentacao()` - Gera GRAMATICA.md

## Exemplos

### Expressão Simples
**Entrada:** `(3 5 +)`

**Saída:**
```
EXPRESSAO
  └─ OPERACAO: +
    ├─ NUMERO: 3
    └─ NUMERO: 5
```

### Expressão Aninhada
**Entrada:** `((2 3 *) (4 2 /) /)`

**Saída:**
```
EXPRESSAO
  └─ OPERACAO: /
    ├─ EXPRESSAO
      └─ OPERACAO: *
        ├─ NUMERO: 2
        └─ NUMERO: 3
    └─ EXPRESSAO
      └─ OPERACAO: /
        ├─ NUMERO: 4
        └─ NUMERO: 2
```

### Comando de Memória
**Entrada:** `(42 MEM)`

**Saída:**
```
EXPRESSAO
  └─ COMANDO_ARMAZENAR
    ├─ NUMERO: 42
    └─ IDENTIFICADOR: MEM
```

## Tratamento de Erros

O analisador detecta:
- Caracteres inválidos (léxico)
- Números malformados (léxico)
- Parênteses não balanceados (léxico)
- Tokens inesperados (sintático)
- Operandos insuficientes (sintático)
- Estrutura de expressão inválida (sintático)

**Exemplo:**
```
Entrada: (3 5)
Erro: Erro sintático [pos 3]: Esperado OPERADOR, encontrado PARENTESE_FECHA
```

## Limitações

- Estruturas de controle (IF/WHILE) estão definidas na gramática mas não totalmente implementadas no parser
- Não há análise semântica (será implementada na Fase 3)
- Não há geração de código para estruturas de controle
- Não há verificação de tipos

## Documentação Adicional

Consulte `GRAMATICA.md` para detalhes completos sobre:
- Gramática formal em EBNF
- Conjuntos FIRST e FOLLOW calculados
- Tabela LL(1) completa
- Exemplos de derivações

## Depuração

**Modo debug:**
```bash
python3 -m pdb main_parser.py test1.txt
```

**Visualizar gramática:**
```bash
python3 src/grammar.py
```

**Verificar árvore JSON:**
```bash
python3 -m json.tool arvore_sintatica.json
```

## Contribuições
@Moreti2002