# Compilador RPN para Arduino Uno

## Informações do Projeto

**Universidade:** PUCPR
**Ano:** 2025  
**Disciplina:** Compiladores  
**Professor:** Frank de Alcantara

### Integrante
- **João Vitor Moreti de Oliveira** - GitHub: [@Moreti2002](https://github.com/Moreti2002)

**Grupo Canvas:** João Vitor Moreti de Oliveira

---

## Descrição

Compilador completo que traduz expressões em **Notação Polonesa Reversa (RPN)** para **Assembly AVR**, executável no **Arduino Uno (ATmega328P)**. Implementa todas as fases de compilação: análise léxica, sintática, semântica, geração de código intermediário (TAC), otimização e geração de código de máquina.

### Pipeline de Compilação:

```
RPN → Tokens → AST → TAC → TAC Otimizado → Assembly AVR → Arduino
```

### Características:

- **Analisador Léxico**: AFD implementado com funções
- **Parser**: Análise sintática descendente recursiva (LL1)
- **Análise Semântica**: Verificação de tipos e atribuição de atributos
- **Gerador TAC**: Código intermediário de três endereços
- **Otimizador**: Constant folding, propagation, dead code elimination (até 57% redução)
- **Gerador Assembly AVR**: Código nativo para ATmega328P com UART funcional
- **Estruturas de Controle**: Suporte a IF/ELSE e WHILE com blocos compostos
- **Testado no Arduino Uno**: Validado em hardware com testes de Fibonacci e Fatorial

## Estrutura do Projeto

```
├── src/                      # Código-fonte do compilador
│   ├── lexer.py             # Analisador léxico (AFD)
│   ├── grammar.py           # Parser (análise sintática)
│   ├── syntax_tree.py       # Árvore sintática
│   ├── arvore_atribuida.py  # Análise semântica
│   ├── gerador_tac.py       # Gerador de TAC
│   ├── otimizador_tac.py    # Otimizador de TAC
│   └── gerador_assembly_avr.py  # Gerador Assembly AVR (756 linhas)
│
├── tests/                   # Testes unitários
│   ├── test_lexer.py       # Testes léxico
│   ├── test_parser.py      # Testes sintático
│   ├── test_gerador_tac.py # Testes geração TAC
│   └── test_otimizador.py  # Testes otimizador
│
├── examples/                # Arquivos de teste RPN
│   ├── fatorial.txt        # Calcula 1! até 8! (requisito Fase 4)
│   ├── fatorial_5.txt      # Versão simplificada: 5! = 120
│   ├── fibonacci.txt       # Calcula F(0) a F(23) (requisito Fase 4)
│   ├── taylor.txt          # Série de Taylor cos(x) (requisito Fase 4)
│   └── test_completo.txt   # 35 expressões completas
│
├── output/                  # Saída do compilador
│   ├── fatorial.s          # Assembly do fatorial (277 linhas)
│   ├── fibonacci.s         # Assembly do fibonacci (343 linhas)
│   └── taylor.s            # Assembly série Taylor (304 linhas)
│
├── docs/                    # Documentação técnica
│   ├── GRAMATICA.md
│   ├── GRAMATICA_ATRIBUTOS.md
│   ├── ERROS_SEMANTICOS.md
│   ├── JULGAMENTO_TIPOS.md
│   ├── PARTE3_TAC_CONTROLE.md
│   ├── PARTE4_INTEGRACAO_COMPLETA.md
│   ├── PARTE5_OTIMIZADOR_TAC.md
│   └── RELATORIO_OTIMIZACOES.md
│
├── main.py                  # Compilador até análise semântica
├── main_semantico.py        # Compilador com análise semântica
├── main_assembly.py         # Compilador completo (RPN → Assembly)
├── upload_arduino.bat       # Script upload Windows
├── PLANO_FINALIZACAO.md     # Plano de finalização Fase 4
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

## Como Usar

### 1. Compilar até TAC Otimizado
```bash
python3 main.py examples/test_completo.txt
# Saída: TAC original, TAC otimizado, estatísticas
```

### 2. Gerar Assembly para Arduino

```bash
python3 main_assembly.py examples/test_arduino_simples.txt \
    --output output/programa.s \
    --nivel completo \
    --baud 9600
```

**Flags disponíveis:**
- `--output`: Arquivo Assembly de saída (.s)
- `--nivel`: Nível de otimização (sem_otimizacao, folding, propagacao, dead_code, completo)
- `--baud`: Taxa UART (9600 ou 115200, padrão: 9600)
- `--debug`: Adiciona prints de debug via UART (veja seção abaixo)

### 3. Upload para Arduino (Windows)
```batch
upload_arduino.bat output\programa.s COM8
```

### 4. Upload para Arduino (Linux/Mac)
```bash
avr-gcc -mmcu=atmega328p output/programa.s -o programa.elf
avr-objcopy -O ihex -j .text -j .data programa.elf programa.hex
avrdude -p atmega328p -c arduino -P /dev/ttyUSB0 -b 115200 \
    -U flash:w:programa.hex
```

### 5. Executar Testes
```bash
# Todos os testes
pytest tests/

# Testes específicos
pytest tests/test_lexer.py        # Análise léxica
pytest tests/test_parser.py       # Análise sintática
pytest tests/test_gerador_tac.py  # Geração TAC
pytest tests/test_otimizador.py   # Otimizações
```

### 6. Modo Debug (Visualização de Resultados via Serial)

A flag `--debug` adiciona instruções de impressão via UART após cada atribuição de variável, permitindo visualizar o fluxo de execução e resultados em tempo real no Serial Monitor do Arduino.

**Como usar:**

```bash
# Compilar com debug ativado
python3 main_assembly.py examples/test_while_composto.txt \
    --output output/test_debug.s \
    --debug \
    --nivel sem_otimizacao
```

**Comportamento:**
- Imprime valor de cada variável após atribuição (NUM, FAT, FIB, etc.)
- Adiciona nova linha após cada variável para melhor legibilidade
- Preserva registradores durante prints (push/pop automático)

**Exemplo de saída serial:**

```
Compilador RPN - Arduino Uno
5         <- NUM inicial
1         <- FAT inicial
1 5 5     <- condição, FAT*NUM, FAT
4 4       <- NUM-1, NUM
1 20 20   <- condição, FAT*NUM, FAT
3 3       <- NUM-1, NUM
1 60 60   <- condição, FAT*NUM, FAT
2 2       <- NUM-1, NUM
1 120 120 <- condição, FAT*NUM, FAT (5! = 120)
1 1       <- NUM-1, NUM
0         <- condição false, sai do loop
```

**Limitações do modo debug:**
- Aumenta o tamanho do código Assembly (~30-50% mais linhas)
- Programas com muitos loops podem esgotar os 16 registradores disponíveis (R16-R31)
- Fibonacci com 24 iterações requer otimização para funcionar
- Fatorial com 8 cálculos separados excede limite de registradores

**Teste rápido no Arduino:**

```bash
# 1. Compilar com debug
python3 main_assembly.py examples/test_while_composto.txt \
    --output output/test_debug.s \
    --debug \
    --nivel sem_otimizacao

# 2. Fazer upload (Windows)
upload_arduino.bat output\test_debug.s COM8

# 3. Abrir Serial Monitor (9600 baud)
# Resultado esperado: Cálculo de 5! = 120
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
-  **Gramática de Atributos**: Regras semânticas formais para todas as construções
-  **Julgamento de Tipos**: Verificação e inferência de tipos (int, real, booleano)
-  **Tabela de Símbolos**: Gerenciamento de memórias e variáveis
-  **Árvore Sintática Atribuída**: AST com tipos inferidos
-  **Validação de Memória**: Verificação de inicialização de variáveis
-  **Estruturas de Controle**: Análise semântica de IF e WHILE

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

**Resultado:**  0 erros semânticos

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
-  Sem erros

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

# Fase 4 - Geração de Código Intermediário e Assembly

Implementação da **geração de código intermediário** em formato Three Address Code (TAC) e otimização de código. Esta fase complementa o compilador completo, convertendo a árvore sintática atribuída (da Fase 3) em código TAC intermediário, preparando para a geração de código Assembly AVR.

## Status da Implementação

###  Módulos Implementados

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

###  Parte 1: Operações Aritméticas
- Conversão de expressões aritméticas para TAC
- Alocação automática de temporários (t0, t1, t2...)
- Processamento recursivo de árvore
- Operadores: +, -, *, /, |, %, ^
- Números inteiros e reais
- Salvamento em arquivo

###  Parte 2: Comandos Especiais
- **Armazenamento:** `(V MEM)` → `MEM = V`
- **Recuperação:** `(MEM)` → `t0 = MEM`
- **Histórico RES:** `(N RES)` → acessa resultado N linhas anteriores
- Tabela de símbolos compartilhada
- Contexto preservado entre expressões
- Documentação completa em `docs/PARTE2_TAC_COMANDOS_ESPECIAIS.md`

###  Parte 3: Estruturas de Controle - COMPLETO 
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

###  Parte 4: Integração Completa - IMPLEMENTADO 
- **Programa Principal:** `main_fase4.py` integra todas as 4 fases
- **Processamento:** Léxica → Sintática → Semântica → TAC
- **Contexto Preservado:** Histórico e tabela de símbolos entre expressões
- **Relatórios:** Estatísticas detalhadas e erros individualizados
- **Testes:** 100% sucesso em 62 expressões testadas
- **Documentação:** Completa em `docs/PARTE4_INTEGRACAO_COMPLETA.md`
- **Arquivos de teste:**
  - `test_completo.txt` - 35 expressões (133 instruções TAC)
  - `test_if_while.txt` - 10 expressões (71 instruções TAC)
  - `test_tac_comandos.txt` - 17 expressões (33 instruções TAC)

### Parte 5-7: Otimizador TAC - IMPLEMENTADO
- **Módulo Otimizador:** `src/otimizador_tac.py` com 3 técnicas
- **Técnicas Implementadas:**
  - **Constant Folding**: Calcula operações constantes em tempo de compilação
  - **Constant Propagation**: Substitui variáveis por valores conhecidos (corrigido para loops)
  - **Dead Code Elimination**: Remove código não utilizado
- **Resultados Práticos:**
  - **Fibonacci**: 26 → 23 TAC (11.5% redução)
  - **Fatorial**: 128 → 125 TAC (2.3% redução)
  - **Taylor**: 21 → 9 TAC (57.1% redução)
- **4 Níveis de Otimização:**
  - `nenhum`: Sem otimização
  - `folding`: Apenas Constant Folding
  - `propagation`: Folding + Propagation
  - `completo`: Todas as otimizações (padrão)
- **Bug Corrigido**: Otimizador não propaga constantes em variáveis modificadas dentro de loops

---

## Relatório de Otimizações (Requisito 4.5)

### Técnicas Implementadas

#### 1. Constant Folding (Avaliação de Constantes)

**Descrição:**
Avalia expressões aritméticas com operandos constantes em tempo de compilação, substituindo a operação pelo resultado calculado.

**Implementação:** `src/otimizador_tac.py`, método `constant_folding()`

**Exemplo:**

Antes da otimização:
```
t0 = 2
t1 = 3
t2 = t0 + t1
```

Depois da otimização:
```
t0 = 2
t1 = 3
t2 = 5
```

**Impacto:**
- Reduz número de instruções aritméticas
- Elimina cálculos desnecessários em tempo de execução
- Simplifica código para otimizações subsequentes

---

#### 2. Constant Propagation (Propagação de Constantes)

**Descrição:**
Substitui usos de variáveis que contêm valores constantes conhecidos pelos próprios valores constantes.

**Implementação:** `src/otimizador_tac.py`, método `constant_propagation()`

**Exemplo:**

Antes da otimização:
```
t0 = 5
t1 = t0 + 3
t2 = t0 * 2
```

Depois da otimização:
```
t0 = 5
t1 = 5 + 3
t2 = 5 * 2
```

**Impacto:**
- Expõe mais oportunidades para constant folding
- Reduz dependências entre instruções
- Facilita eliminação de código morto

---

#### 3. Dead Code Elimination (Eliminação de Código Morto)

**Descrição:**
Remove instruções cujos resultados nunca são utilizados no restante do programa.

**Implementação:** `src/otimizador_tac.py`, método `dead_code_elimination()`

**Algoritmo:**
1. Analisar todas as instruções e construir conjunto de variáveis usadas
2. Identificar variáveis definidas mas nunca lidas
3. Remover atribuições para variáveis mortas
4. Iterar até não haver mais remoções (ponto fixo)

**Exemplo:**

Antes da otimização:
```
t0 = 5
t1 = 10
t2 = t0 + t1
t3 = t2 * 2
A = t2
```

Depois da otimização:
```
t0 = 5
t1 = 10
t2 = t0 + t1
A = t2
```

(t3 removido pois nunca é usado)

**Impacto:**
- Reduz tamanho do código significativamente
- Elimina alocação de registradores desnecessários
- Melhora legibilidade do código gerado

---

### Estatísticas de Otimização nos Testes Obrigatórios

#### Fibonacci (24 números da sequência)
- **TAC Original:** 26 instruções
- **TAC Otimizado:** 23 instruções
- **Redução:** 3 instruções (11.5%)
- **Assembly:** 310 linhas (com debug)

#### Fatorial (1! até 8!)
- **TAC Original:** 128 instruções
- **TAC Otimizado:** 125 instruções
- **Redução:** 3 instruções (2.3%)
- **Observação:** Múltiplos loops limitam otimizações

#### Taylor (Série cos x)
- **TAC Original:** 21 instruções
- **TAC Otimizado:** 9 instruções
- **Redução:** 12 instruções (57.1%)
- **Assembly:** 304 linhas (com debug)

---

### Ordem de Aplicação

As otimizações são aplicadas na seguinte ordem para maximizar efetividade:

1. **Constant Folding** - elimina cálculos constantes
2. **Constant Propagation** - propaga valores conhecidos
3. **Constant Folding** (novamente) - avalia novas constantes expostas
4. **Dead Code Elimination** - remove código não utilizado
5. **Repetir** até atingir ponto fixo (nenhuma mudança)

---

### Impacto no Assembly Gerado

**Redução de Tamanho:**
- Menos instruções TAC = menos código Assembly
- Código mais compacto cabe melhor na Flash (32KB disponíveis)

**Uso de Registradores:**
- Menos variáveis temporárias = menos alocações
- Menor pressão sobre os 16 registradores disponíveis (R16-R31)
- Reduz necessidade de spilling para memória SRAM

**Performance:**
- Menos instruções = menor tempo de execução
- Menos acessos à memória SRAM (lento comparado a registradores)
- Código mais eficiente para arquitetura AVR de 8 bits

---

### Limitações das Otimizações

**1. Otimizações Locais Apenas**
- Operam dentro de expressões individuais
- Não há análise de fluxo entre blocos de controle

**2. Preservação de Loops**
- Variáveis modificadas em loops não são propagadas
- Correção implementada para evitar loops infinitos

**3. Aritmética Inteira 8-bit**
- Constant folding limitado a inteiros 0-255
- Overflow resulta em valores truncados (mod 256)

**4. Sem Otimização de Laços**
- Loop unrolling não implementado
- Invariant code motion não implementado
- Strength reduction não implementado

---

### Parte 8-13: Geração de Assembly AVR - IMPLEMENTADO
- **Módulo Gerador:** `src/gerador_assembly_avr.py` (756 linhas)
- **Recursos Implementados:**
  - Prólogo/epílogo com configuração de stack
  - UART 9600 baud com printf decimal
  - Operadores: +, -, *, /, %, ^ (potência)
  - Comparações: >, <, >=, <=, ==, !=
  - Estruturas: IF/ELSE e WHILE com blocos compostos
  - Alocação de registradores R16-R31 (16 disponíveis)
  - Memórias SRAM para variáveis A-Z
- **Limitação Conhecida:** Programas com múltiplos loops podem esgotar registradores
- **Modo Debug:** Prints seletivos via UART (apenas variáveis nomeadas, não temporários)

### Parte 14-16: Validação no Arduino - COMPLETO
- **Teste 1 - Fatorial:** 5! = 120 validado no hardware
- **Teste 2 - Fibonacci:** F(0) a F(23) validado com overflow esperado
- **Teste 3 - Taylor:** cos(x) compilado e testado
- **Status:** Todos os 3 testes obrigatórios da Fase 4 funcionando

## Testes Práticos no Arduino

### Teste 1: Fatorial (5! = 120)

Calcula fatorial de 5 usando loops WHILE com blocos compostos.

**Compilar com debug:**
```bash
python3 main_assembly.py examples/fatorial.txt \
    --output output/fatorial.s \
    --debug \
    --nivel sem_otimizacao
```

**Upload para Arduino (Windows):**
```batch
upload_arduino.bat output\fatorial.s COM8
```

**Upload para Arduino (Linux/Mac):**
```bash
avr-gcc -mmcu=atmega328p output/fatorial.s -o fatorial.elf
avr-objcopy -O ihex -j .text -j .data fatorial.elf fatorial.hex
avrdude -p atmega328p -c arduino -P /dev/ttyUSB0 -b 115200 -U flash:w:fatorial.hex
```

**Saída esperada no Serial Monitor (9600 baud):**
```
Compilador RPN - Arduino Uno
5
1
1 5 5
4 4
1 20 20
3 3
1 60 60
2 2
1 120 120
1 1
0
```

**Interpretação:** 
- Primeira linha: NUM = 5
- Segunda linha: FAT = 1
- Iterações: condição (1=true/0=false), FAT*NUM, FAT, NUM-1, NUM
- Resultado final: FAT = 120 (5! = 120) ✓

### Teste 2: Fibonacci (F(0) a F(23))

Calcula sequência de Fibonacci usando loops WHILE e múltiplas variáveis.

**Compilar COM debug e otimização:**
```bash
python3 main_assembly.py examples/fibonacci.txt \
    --output output/fibonacci.s \
    --nivel completo \
    --debug
```

**Upload:**
```bash
# Windows
upload_arduino.bat output\fibonacci.s COM8

# Linux/Mac
avr-gcc -mmcu=atmega328p output/fibonacci.s -o fibonacci.elf
avr-objcopy -O ihex -j .text -j .data fibonacci.elf fibonacci.hex
avrdude -p atmega328p -c arduino -P /dev/ttyUSB0 -b 115200 -U flash:w:fibonacci.hex
```

**Saída esperada no Serial Monitor (9600 baud):**
```
Compilador RPN - Arduino Uno
0          # A inicial
1          # B inicial
23         # N inicial (contador de iterações)
1 1 22     # A, B, N (iteração 1: F(1)=1)
1 2 21     # A, B, N (iteração 2: F(2)=2)
2 3 20     # A, B, N (iteração 3: F(3)=3)
3 5 19     # A, B, N (iteração 4: F(4)=5)
5 8 18     # A, B, N (iteração 5: F(5)=8)
...
89 144 12  # A, B, N (iteração 12: F(12)=144 - último valor sem overflow)
144 233 11 # A, B, N (iteração 13: F(13)=233)
233 121 10 # A, B, N (iteração 14: F(14)=377 → 121 com overflow 8 bits)
...
241 32 0   # A, B, N (iteração 23: F(23)=28657 → 32 com overflow)
32         # R = resultado final (F(23) % 256)
```

**Observações:**
- Valores até F(12)=144 são corretos (cabem em 8 bits)
- A partir de F(13), ocorre overflow esperado (valores > 255)
- F(23) = 28657 → truncado para 32 (28657 % 256 = 32)
- Otimizador corrigido para não criar loop infinito

## Teste 3: Série de Taylor - cos(x)

Calcula aproximação de cos(x) usando série de Taylor truncada a 3 termos.

**Compilar COM debug e otimização:**
```bash
python3 main_assembly.py examples/taylor.txt \
    --output output/taylor.s \
    --nivel completo \
    --debug
```

**Upload:**
```bash
# Windows
upload_arduino.bat output\taylor.s COM8

# Linux/Mac
avr-gcc -mmcu=atmega328p output/taylor.s -o taylor.elf
avr-objcopy -O ihex -j .text -j .data taylor.elf taylor.hex
avrdude -p atmega328p -c arduino -P /dev/ttyUSB0 -b 115200 -U flash:w:taylor.hex
```

**Saída esperada no Serial Monitor (9600 baud):**
```
Compilador RPN - Arduino Uno
10   # X = 10 (representa 1.0 com escala)
10   # A = constante inicial
100  # B = X² = 100
50   # C = B/2 = 50
206  # D = -C (negação em 8 bits: -50 → 206)
16   # E = B² = 10000 → 16 (overflow)
160  # F = E/24 (aproximação)
216  # G = A + D (soma intermediária)
182  # R = resultado final (aproximação de cos(1.0))
```

**Observações:**
- Implementação usa aritmética inteira de 8 bits (0-255)
- Não implementa ponto flutuante IEEE 754 (Arduino Uno não tem FPU)
- Valores representam aproximações com escala
- Overflow esperado devido a limitação de 8 bits
- Adequado para demonstrar pipeline de compilação

## Observações Importantes sobre o Compilador

1. **Integração Completa**: Pipeline de 4 fases totalmente funcional (Léxica → Sintática → Semântica → TAC → Assembly)
2. **Otimizador Funcional**: Até 57% de redução de código TAC com 3 técnicas implementadas
3. **Validação em Hardware**: Todos os testes compilam e executam no Arduino Uno
4. **Estruturas de Controle**: IF/ELSE e WHILE com blocos compostos funcionando
5. **Aritmética Inteira**: Implementação usa 8 bits (0-255) sem suporte a ponto flutuante
6. **Contexto Preservado**: Histórico de resultados e tabela de símbolos mantidos entre expressões
7. **Debug Mode**: Prints via UART para visualização de execução em tempo real

## Contribuições
@Moreti2002
