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

---

# Analisador Semântico - Fase 3

Implementação de um analisador semântico completo com verificação de tipos, validação de memória e estruturas de controle. Esta fase complementa as Fases 1 (Análise Léxica) e 2 (Análise Sintática), adicionando análise semântica, gramática de atributos e geração de árvore atribuída.

## Características da Fase 3

### Análise Semântica

O analisador semântico realiza três tipos principais de verificações:

**1. Verificação de Tipos:**
- Compatibilidade de tipos em operações aritméticas
- Promoção automática de tipos (int → real)
- Validação de expoente inteiro em potenciação
- Operandos inteiros para divisão inteira (`/`) e resto (`%`)
- Operadores relacionais retornam tipo `booleano`

**2. Verificação de Memória:**
- Memórias devem ser inicializadas antes do uso
- Validação de comandos especiais (`MEM`, `RES`)
- Tabela de símbolos com escopo

**3. Verificação de Controle:**
- Condições de IF/WHILE devem retornar booleano
- Validação de estrutura de blocos
- Verificação de aninhamento

### Gramática de Atributos

A gramática de atributos define regras de inferência de tipos:

**Tipos de Dados:**
- `int`: números inteiros
- `real`: números de ponto flutuante
- `booleano`: resultado de operações relacionais (não pode ser armazenado em memória)

**Regra de Promoção:**
```
promover_tipo(int, int)   = int
promover_tipo(int, real)  = real
promover_tipo(real, int)  = real
promover_tipo(real, real) = real
```

**Novos Operadores:**
- `|` : divisão real (resultado sempre `real`)
- `>`, `<`, `>=`, `<=`, `==`, `!=` : operadores relacionais (retornam `booleano`)

## Uso da Fase 3

### Executar Analisador Completo

```bash
python3 main_semantico.py <arquivo.txt>
```

**Exemplo:**
```bash
python3 main_semantico.py test_fase3_1.txt
```

### Arquivos de Teste

**test_fase3_1.txt** - Casos válidos:
- Operações aritméticas básicas
- Expressões aninhadas
- Promoção de tipos
- Operadores relacionais

**test_fase3_2.txt** - Erros semânticos:
- Memórias não inicializadas
- Divisão inteira com operando real
- Expoente não inteiro
- RES sem histórico suficiente

**test_fase3_3.txt** - Casos complexos:
- Expressões profundamente aninhadas
- Múltiplos comandos RES
- Comparações relacionais
- Mistura de tipos

## Saídas Geradas pela Fase 3

### arvore_atribuida.json
Árvore sintática abstrata atribuída em formato JSON com tipos inferidos.

### docs/GRAMATICA_ATRIBUTOS.md
Documentação completa da gramática de atributos contendo:
- Atributos sintetizados e herdados
- Regras de produção com tipos
- Regras de inferência de tipos
- Exemplos de aplicação

### docs/ARVORE_ATRIBUIDA.md
Representação da árvore atribuída da última execução com:
- Estatísticas (total de nós, profundidade)
- Distribuição de tipos de nós
- Estrutura hierárquica formatada
- Tipos inferidos para cada nó

### docs/ERROS_SEMANTICOS.md
Relatório de todos os erros encontrados:
- Resumo com contagem por categoria
- Erros detalhados com linha e contexto
- Classificação (léxico, sintático, semântico)

### docs/JULGAMENTO_TIPOS.md
Documentação das regras de dedução aplicadas:
- Todas as regras de inferência utilizadas
- Tipos inferidos para cada expressão
- Explicação de promoções de tipos
- Aplicação de regras semânticas

## Estrutura do Projeto - Fase 3

```
├── src/
│   ├── lexer.py                    # Analisador léxico (Fase 1)
│   ├── parser.py                   # Analisador sintático (Fase 2)
│   ├── grammar.py                  # Gramática LL(1) (Fase 2)
│   ├── syntax_tree.py              # Árvore sintática (Fase 2)
│   │
│   ├── gramatica_atributos.py      # Gramática de atributos (Fase 3)
│   ├── tabela_simbolos.py          # Tabela de símbolos (Fase 3)
│   ├── analisador_tipos.py         # Verificação de tipos (Fase 3)
│   ├── analisador_memoria.py       # Validação de memória (Fase 3)
│   ├── analisador_controle.py      # Validação de controle (Fase 3)
│   └── arvore_atribuida.py         # Árvore atribuída (Fase 3)
│
├── utils/
│   ├── util.py                     # Utilitários gerais
│   └── formatador_relatorios.py    # Geração de relatórios MD (Fase 3)
│
├── docs/                            # Relatórios markdown (Fase 3)
│   ├── GRAMATICA_ATRIBUTOS.md
│   ├── ARVORE_ATRIBUIDA.md
│   ├── ERROS_SEMANTICOS.md
│   └── JULGAMENTO_TIPOS.md
│
├── tests/                           # Testes unitários
│   ├── test_lexer.py
│   ├── test_parser.py
│   └── test_grammar.py
│
├── main.py                          # Executor RPN (Fase 1)
├── main_parser.py                   # Analisador sintático (Fase 2)
├── main_semantico.py                # Analisador completo (Fase 3)
│
├── test_fase3_1.txt                 # Teste - casos válidos
├── test_fase3_2.txt                 # Teste - erros semânticos
├── test_fase3_3.txt                 # Teste - casos complexos
│
└── README.md
```

## Divisão de Tarefas - Fase 3

### Aluno 1: Gramática de Atributos e Tabela de Símbolos
**Arquivos:** `src/gramatica_atributos.py`, `src/tabela_simbolos.py`

Funções principais:
- `definir_gramatica_atributos()` - Define regras semânticas
- `promover_tipo()` - Promoção de tipos
- `inicializar_tabela_simbolos()` - Cria tabela
- `adicionar_simbolo()` - Adiciona à tabela
- `buscar_simbolo()` - Busca símbolo
- `simbolo_inicializado()` - Verifica inicialização

### Aluno 2: Verificação de Tipos
**Arquivo:** `src/analisador_tipos.py`

Funções principais:
- `analisar_semantica()` - Análise semântica principal
- `inferir_tipo_no()` - Infere tipo de um nó
- `validar_operacao_aritmetica()` - Valida operação
- `verificar_compatibilidade_tipos()` - Verifica compatibilidade
- `gerar_relatorio_julgamento_tipos()` - Gera relatório de tipos

### Aluno 3: Memória e Controle
**Arquivos:** `src/analisador_memoria.py`, `src/analisador_controle.py`

Funções principais:
- `analisar_semantica_memoria()` - Valida memórias
- `validar_comando_armazenar()` - Valida (V MEM)
- `validar_comando_recuperar()` - Valida (MEM)
- `analisar_semantica_controle()` - Valida IF/WHILE
- `validar_condicao()` - Valida condição booleana

### Aluno 4: Árvore Atribuída e Integração
**Arquivos:** `src/arvore_atribuida.py`, `utils/formatador_relatorios.py`, `main_semantico.py`

Funções principais:
- `gerar_arvore_atribuida()` - Gera AST atribuída
- `salvar_arvore_json()` - Salva em JSON
- `gerar_todos_relatorios()` - Gera 4 relatórios MD
- `main()` - Integração completa

## Exemplos de Verificações Semânticas

### Verificação de Tipos

```python
# Válido: int + int = int
(5 3 +)

# Válido: real + int = real (promoção)
(3.14 2 +)

# Válido: divisão real sempre retorna real
(10.0 2.0 |)

# ERRO: divisão inteira requer operandos int
(5.5 2 /)

# ERRO: expoente deve ser inteiro
(2.0 3.5 ^)
```

### Verificação de Memória

```python
# ERRO: memória não inicializada
(VAR)

# Válido: armazenar primeiro
(42 VAR)
(VAR)  # Agora válido
```

### Operadores Relacionais

```python
# Válido: retorna booleano
(5 3 >)
(10 20 <=)
(3.14 2.71 ==)
```

## Fluxo de Execução - Fase 3

1. **Análise Léxica** (Fase 1) → tokens
2. **Análise Sintática** (Fase 2) → AST
3. **Definir Gramática de Atributos**
4. **Análise Semântica - Tipos** → AST anotada com tipos
5. **Análise Semântica - Memória** → validação de símbolos
6. **Análise Semântica - Controle** → validação de IF/WHILE
7. **Gerar Árvore Atribuída** → AST final
8. **Gerar Relatórios Markdown** (4 arquivos)
9. **Exibir erros** (se houver)

## Mensagens de Erro

### Erro de Tipo
```
ERRO SEMÂNTICO [Linha 5]: Operador '/' requer operandos inteiros
Contexto: tipos: real, int
```

### Erro de Memória
```
ERRO SEMÂNTICO [Linha 3]: Memória 'VAR' utilizada sem inicialização
Contexto: (VAR)
```

### Erro de Controle
```
ERRO SEMÂNTICO [Linha 7]: Condição deve retornar booleano, encontrado 'int'
Contexto: tipo do nó: OPERACAO
```

## Testes

### Executar análise completa
```bash
python3 main_semantico.py test_fase3_1.txt
python3 main_semantico.py test_fase3_2.txt
python3 main_semantico.py test_fase3_3.txt
```

### Verificar relatórios gerados
```bash
cat docs/GRAMATICA_ATRIBUTOS.md
cat docs/ERROS_SEMANTICOS.md
cat docs/JULGAMENTO_TIPOS.md
python3 -m json.tool arvore_atribuida.json
```

### Testes individuais dos módulos
```bash
python3 src/gramatica_atributos.py
python3 src/tabela_simbolos.py
python3 src/analisador_tipos.py
python3 utils/formatador_relatorios.py
```

## Contribuições
@Moreti2002