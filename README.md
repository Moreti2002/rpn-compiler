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

---

# Analisador Semântico - Fase 3

Implementação completa de um **analisador semântico** com gramática de atributos, verificação de tipos, validação de memórias e análise de estruturas de controle. Este projeto integra as três fases do compilador: análise léxica, sintática e semântica.

## Características da Fase 3

### Análise Semântica Completa
- ✅ **Gramática de Atributos**: Regras semânticas formais para todas as construções
- ✅ **Julgamento de Tipos**: Verificação e inferência de tipos (int, real, booleano)
- ✅ **Tabela de Símbolos**: Gerenciamento de memórias e variáveis
- ✅ **Árvore Sintática Atribuída**: AST com tipos inferidos
- ✅ **Validação de Memória**: Verificação de inicialização de variáveis
- ✅ **Estruturas de Controle**: Análise semântica de IF e WHILE

### Tipos de Dados Suportados
- **int**: Números inteiros
- **real** (float): Números de ponto flutuante (IEEE 754)
- **booleano**: Resultado de operações relacionais (interno)

### Operadores

#### Operadores Aritméticos
- `+` (adição): int/real → promove tipo
- `-` (subtração): int/real → promove tipo
- `*` (multiplicação): int/real → promove tipo
- `|` (divisão real): int/real → sempre real
- `/` (divisão inteira): **apenas int** → int
- `%` (resto): **apenas int** → int
- `^` (potência): base int/real, **expoente int** → tipo da base

#### Operadores Relacionais
- `>` (maior que): int/real → booleano
- `<` (menor que): int/real → booleano
- `>=` (maior ou igual): int/real → booleano
- `<=` (menor ou igual): int/real → booleano
- `==` (igual): int/real → booleano
- `!=` (diferente): int/real → booleano

### Regras de Promoção de Tipos
```
int  ⊕ int  → int
int  ⊕ real → real
real ⊕ int  → real
real ⊕ real → real
```
Onde ⊕ representa operadores: `+`, `-`, `*`, `|`

## Uso da Fase 3

### Executar Análise Completa (3 Fases)
```bash
python3 main_semantico.py <arquivo_teste.txt>
```

**Exemplo:**
```bash
python3 main_semantico.py test_simples.txt
```

### Saída do Programa
O programa executa as 3 fases em sequência e exibe:
1. **Fase 1**: Análise Léxica (tokens gerados)
2. **Fase 2**: Análise Sintática (árvores geradas)
3. **Fase 3**: Análise Semântica
   - Gramática de atributos definida
   - Tabela de símbolos populada
   - Tipos inferidos e validados
   - Erros semânticos (se houver)

### Arquivos Gerados

#### Árvore Atribuída (JSON)
`arvore_atribuida.json` - Árvore sintática com tipos inferidos
```json
{
  "tipo": "OPERACAO",
  "tipo_inferido": "int",
  "linha": 1,
  "valor": "+",
  "filhos": [...]
}
```

#### Documentação em Markdown (docs/)
1. **GRAMATICA_ATRIBUTOS.md**
   - Atributos sintetizados e herdados
   - Regras de produção com atributos
   - Regras para cada operador
   - Comandos especiais
   - Estruturas de controle

2. **ARVORE_ATRIBUIDA.md**
   - Visualização hierárquica da árvore
   - Representação JSON completa
   - Tipos inferidos em cada nó

3. **ERROS_SEMANTICOS.md**
   - Lista de erros encontrados
   - Linha e contexto de cada erro
   - Descrição detalhada

4. **JULGAMENTO_TIPOS.md**
   - Regras de dedução aplicadas
   - Tipos inferidos por expressão
   - Justificativa de cada inferência

## Estrutura do Projeto - Fase 3

```
├── src/
│   ├── gramatica_atributos.py    # Gramática de atributos e regras semânticas
│   ├── tabela_simbolos.py        # Gerenciamento de símbolos e memórias
│   ├── analisador_tipos.py       # Verificação e inferência de tipos
│   ├── analisador_memoria.py     # Validação de uso de memórias
│   ├── analisador_controle.py    # Validação de estruturas de controle
│   └── arvore_atribuida.py       # Geração da árvore atribuída
├── utils/
│   └── formatador_relatorios.py  # Geração de relatórios em Markdown
├── docs/                          # Documentação gerada automaticamente
│   ├── GRAMATICA_ATRIBUTOS.md
│   ├── ARVORE_ATRIBUIDA.md
│   ├── ERROS_SEMANTICOS.md
│   └── JULGAMENTO_TIPOS.md
├── main_semantico.py              # Programa principal integrado (3 fases)
├── test_simples.txt               # Arquivo de teste válido
├── test_fase3_1.txt               # Teste com casos válidos
├── test_fase3_2.txt               # Teste com erros semânticos
└── test_fase3_3.txt               # Teste com casos complexos
```

## Arquivos de Teste - Fase 3

### test_simples.txt
Arquivo de teste com **sintaxe totalmente válida** e sem erros semânticos:
```
# Operações com inteiros
(3 5 +)         # int + int = int
(10 3 -)        # Subtração
(4 7 *)         # Multiplicação
(15 3 /)        # Divisão inteira (ambos int)
(10 3 %)        # Resto (ambos int)
(2 8 ^)         # Potência (expoente int)

# Operações com reais
(10.0 3.0 |)    # Divisão real (sempre retorna real)
(15.5 2.5 +)    # Adição de reais

# Promoção de tipos
(5 2.5 +)       # int + real = real
(10.0 3 -)      # real - int = real
```

**Resultado:** ✅ 0 erros semânticos

### test_fase3_2.txt
Exemplos de **erros semânticos** detectados:
```
(5.5 2 /)       # Erro: divisão inteira requer operandos int
(2 3.5 %)       # Erro: resto requer operandos int
(2.0 3.5 ^)     # Erro: expoente deve ser int
```

## Exemplos de Análise Semântica

### Exemplo 1: Operação Válida
**Entrada:** `(3 5 +)`

**Análise:**
- Léxica: 5 tokens
- Sintática: Árvore gerada
- Semântica:
  - Tipo(3) = int
  - Tipo(5) = int
  - Tipo(3 + 5) = promover(int, int) = **int**
  - Sem erros

### Exemplo 2: Promoção de Tipo
**Entrada:** `(5 2.5 +)`

**Análise:**
- Tipo(5) = int
- Tipo(2.5) = real
- Tipo(5 + 2.5) = promover(int, real) = **real**
- Promoção automática

### Exemplo 3: Erro de Tipo
**Entrada:** `(5.5 2 /)`

**Análise:**
- Tipo(5.5) = real
- Tipo(2) = int
- Operador `/` requer: int, int
- **ERRO SEMÂNTICO**: Operador `/` requer operandos inteiros

### Exemplo 4: Divisão Real
**Entrada:** `(10.0 3.0 |)`

**Análise:**
- Tipo(10.0) = real
- Tipo(3.0) = real
- Operador `|` sempre retorna: **real**
- ✅ Sem erros

## Erros Semânticos Detectados

### Erros de Tipo
- Operação com tipos incompatíveis
- Expoente não inteiro em potência
- Operandos não inteiros em divisão inteira (`/`) ou resto (`%`)
- Operandos não numéricos em operações aritméticas

### Erros de Memória
- Uso de memória não inicializada
- Identificador não declarado
- Tipo inválido para armazenamento

### Erros de Controle
- Condição não booleana em IF/WHILE
- Tipos incompatíveis nos blocos de IF

## Validação e Testes

### Rotinas de Teste Utilizadas

1. **Teste de Operações Aritméticas**
   ```bash
   python3 main_semantico.py test_simples.txt
   ```
   - Valida todas as operações aritméticas
   - Verifica promoção de tipos
   - Confirma inferência correta

2. **Teste de Erros Semânticos**
   ```bash
   python3 main_semantico.py test_fase3_2.txt
   ```
   - Valida detecção de erros de tipo
   - Confirma mensagens de erro claras
   - Verifica linha e contexto dos erros

3. **Teste de Casos Complexos**
   ```bash
   python3 main_semantico.py test_fase3_3.txt
   ```
   - Expressões aninhadas
   - Múltiplas variáveis
   - Combinações de operadores

### Verificação dos Arquivos Gerados
```bash
# Verificar árvore atribuída
cat arvore_atribuida.json | python3 -m json.tool

# Visualizar relatórios
cat docs/GRAMATICA_ATRIBUTOS.md
cat docs/JULGAMENTO_TIPOS.md
cat docs/ERROS_SEMANTICOS.md
cat docs/ARVORE_ATRIBUIDA.md
```


## Depuração

### Visualizar Gramática de Atributos
```bash
python3 src/gramatica_atributos.py
```

### Testar Tabela de Símbolos
```bash
python3 src/tabela_simbolos.py
```

### Testar Analisador de Tipos
```bash
python3 src/analisador_tipos.py
```

## Contribuições
@Moreti2002

---

# 25  Fase 4 - Geração de Código Intermediário e Assembly

Implementação da **geração de código intermediário** em formato Three Address Code (TAC) e otimização de código. Esta fase complementa o compilador completo, convertendo a árvore sintática atribuída (da Fase 3) em código TAC intermediário, preparando para a geração de código Assembly AVR.

## Status da Implementação

### ✅ Módulos Implementados

#### 1. Gerador de TAC (`src/gerador_tac.py`)
- **Classe `InstrucaoTAC`**: Representa instruções TAC
  - Suporta tipos: ATRIBUICAO, OPERACAO, COPIA, ROTULO, GOTO, IF, IF_FALSE
  - Formato de string legível para debug e saída
  
- **Classe `GeradorTAC`**: Gerador principal de código TAC
  - Conversão de árvore sintática atribuída para TAC
  - Alocação automática de variáveis temporárias (t0, t1, t2, ...)
  - Geração de rótulos para estruturas de controle (L0, L1, L2, ...)
  - Suporte a operações aritméticas: +, -, *, /, |, %, ^
  - Suporte a operadores relacionais: >, <, >=, <=, ==, !=
  - Processamento recursivo de expressões aninhadas
  - Salvamento de TAC em arquivo texto

#### 2. Teste do Gerador TAC (`tests/test_gerador_tac.py`)
- Integração completa das 4 fases:
  - Fase 1: Análise Léxica
  - Fase 2: Análise Sintática
  - Fase 3: Análise Semântica
  - Fase 4: Geração de TAC
- Processamento de arquivos de teste
- Exibição colorida do TAC gerado
- Geração de estatísticas detalhadas
- Salvamento automático em `output/tac_original.txt`

#### 3. Formatador de TAC (`utils/formatador_tac.py`)
- Exibição colorida de instruções TAC
- Geração de estatísticas detalhadas:
  - Total de instruções
  - Temporários utilizados
  - Rótulos criados
  - Distribuição por tipo de instrução
- Formatação profissional dos relatórios

## Formato do TAC Gerado

### Tipos de Instruções

#### Atribuição Simples
```
t1 = 5
```

#### Operação Binária
```
t2 = t0 + t1
t3 = t1 * 2
t4 = a / b
```

#### Operação Unária
```
t1 = - a
```

#### Cópia
```
a = b
```

#### Salto Incondicional
```
goto L1
```

#### Salto Condicional
```
if a goto L1
ifFalse a goto L2
```

#### Rótulo
```
L0:
L1:
```

## Como Executar

### Teste do Gerador TAC
```bash
python3 tests/test_gerador_tac.py test_tac_simples.txt
```

Este comando executa todas as 4 fases em sequência:
1. Análise léxica dos tokens
2. Construção da árvore sintática
3. Análise semântica e inferência de tipos
4. Geração do código TAC

### Arquivos de Teste

#### `test_tac_simples.txt`
Arquivo de teste com expressões válidas para geração de TAC:
```
# Operações aritméticas básicas
(3 5 +)         # Adição
(10 3 -)        # Subtração
(4 7 *)         # Multiplicação
(15 3 /)        # Divisão inteira

# Operações com reais
(10.0 3.0 |)    # Divisão real
(2.5 1.5 +)     # Adição de reais

# Expressões aninhadas
((2 3 *) (4 2 /) +)    # (2*3) + (4/2)
```

#### Arquivo de Saída
`output/tac_original.txt` contém:
```
============================================================
THREE ADDRESS CODE (TAC)
============================================================

  1. t0 = 3
  2. t1 = 5
  3. t2 = t0 + t1
  4. t3 = 10
  5. t4 = 3
  6. t5 = t3 - t4
  ...

============================================================
Total de instruções: 15
Temporários utilizados: 10
Rótulos criados: 0
============================================================
```

## Exemplo de Conversão

### Expressão de Entrada
```
(3 5 +)
```

### Árvore Sintática Atribuída
```json
{
  "tipo": "OPERACAO",
  "tipo_inferido": "int",
  "valor": "+",
  "filhos": [
    {
      "tipo": "NUMERO",
      "valor": "3",
      "tipo_inferido": "int"
    },
    {
      "tipo": "NUMERO",
      "valor": "5",
      "tipo_inferido": "int"
    }
  ]
}
```

### TAC Gerado
```
1. t0 = 3
2. t1 = 5
3. t2 = t0 + t1
```

## Estrutura de Dados

### Classe InstrucaoTAC
```python
class InstrucaoTAC:
    def __init__(self, tipo, resultado=None, operando1=None, 
                 operador=None, operando2=None, linha=None):
        self.tipo = tipo           # ATRIBUICAO, OPERACAO, etc.
        self.resultado = resultado # Variável destino
        self.operando1 = operando1 # Primeiro operando
        self.operador = operador   # Operador (+, -, *, etc.)
        self.operando2 = operando2 # Segundo operando
        self.linha = linha         # Linha original
```

### Classe GeradorTAC
```python
class GeradorTAC:
    def __init__(self):
        self.instrucoes = []           # Lista de instruções
        self.contador_temporarios = 0  # Contador de temporários
        self.contador_rotulos = 0      # Contador de rótulos
        self.tabela_simbolos = {}      # Tabela de símbolos
```


## Documentação Técnica

### Geração de TAC

O processo de geração segue o algoritmo:

1. **Percorrer árvore em pós-ordem**
   - Processar filhos antes do nó pai
   - Garantir que operandos sejam calculados antes da operação

2. **Para cada nó numérico**
   - Criar temporário novo
   - Gerar instrução de atribuição

3. **Para cada operação**
   - Processar recursivamente operandos
   - Criar temporário para resultado
   - Gerar instrução de operação

4. **Retornar variável resultado**
   - Propagar resultado para nível superior

### Exemplo Detalhado

**Entrada:** `((2 3 *) (4 2 /) +)`

**Processamento:**
```
1. Processar (2 3 *)
   t0 = 2
   t1 = 3
   t2 = t0 * t1
   
2. Processar (4 2 /)
   t3 = 4
   t4 = 2
   t5 = t3 / t4
   
3. Processar adição final
   t6 = t2 + t5
```

## Validação e Testes

### Teste Básico - Parte 1 (Operações Aritméticas)
```bash
# Executar teste simples
python3 tests/test_gerador_tac.py test_tac_simples.txt
```

### Teste Parte 2 (Comandos Especiais)
```bash
# Executar teste de comandos MEM, VAR e RES
python3 tests/test_gerador_tac.py test_tac_comandos.txt
```

**Comandos testados:**
- `(10 VAR)` - Armazenamento em memória
- `(MEM)` - Recuperação de memória
- `(2 RES)` - Acesso ao histórico de resultados

### Resultado Esperado
```
✓ Total: 15-16 expressões válidas
✓ Total: 15 árvores prontas para TAC
✓ ~29 instruções TAC geradas
✓ TAC salvo em: output/tac_original.txt
```

### Verificar Saída
```bash
# Visualizar TAC gerado
cat output/tac_original.txt
```

## Recursos Implementados - Fase 4

### ✅ Parte 1: Operações Aritméticas
- Conversão de expressões aritméticas para TAC
- Alocação automática de temporários (t0, t1, t2...)
- Processamento recursivo de árvore
- Operadores: +, -, *, /, |, %, ^
- Números inteiros e reais
- Salvamento em arquivo

### ✅ Parte 2: Comandos Especiais
- **Armazenamento:** `(V MEM)` → `MEM = V`
- **Recuperação:** `(MEM)` → `t0 = MEM`
- **Histórico RES:** `(N RES)` → acessa resultado N linhas anteriores
- Tabela de símbolos compartilhada
- Contexto preservado entre expressões
- Documentação completa em `docs/PARTE2_TAC_COMANDOS_ESPECIAIS.md`

### ✅ Parte 3: Estruturas de Controle - COMPLETO ✅
- **Parser Atualizado:** Suporte completo a operadores relacionais (>, <, ==, !=, >=, <=)
- **Parser Atualizado:** Reconhecimento de estruturas IF e WHILE
- **Parser Atualizado:** Suporte a expressões aninhadas em blocos
- **IF (DECISAO):** Geração completa de TAC com `ifFalse` e `goto`
- **WHILE (LACO):** Geração completa de TAC com loops e rótulos
- **Rótulos:** Geração automática (L0, L1, L2, ...)
- **Instruções novas:** IF_FALSE, GOTO, ROTULO
- **Comparações:** Operações relacionais simples (sem IF/WHILE)
- **Documentação:** Completa em `docs/PARTE3_TAC_CONTROLE.md`
- **Testes:** 10 expressões de teste em `test_if_while.txt` (100% sucesso)
- **TAC Gerado:** 71 instruções com 12 rótulos e 33 temporários

### ⏳ Próximas Implementações
- [ ] Parte 4: Integração completa
- [ ] Parte 5-8: Otimizações (Folding, Propagation, Dead Code)
- [ ] Parte 9-13: Geração de Assembly AVR
- [ ] Parte 14-16: Programas de teste e validação no Arduino

## Observações Importantes

1. **Integração Completa**: O gerador TAC está integrado com todas as fases anteriores
2. **Compatibilidade**: Mantém compatibilidade com estruturas das Fases 1, 2 e 3
3. **Extensibilidade**: Estrutura preparada para otimizações e geração de Assembly
4. **Documentação**: Código totalmente documentado e comentado
5. **Contexto Preservado**: Histórico de resultados e tabela de símbolos mantidos entre expressões

## Contribuições
@Moreti2002