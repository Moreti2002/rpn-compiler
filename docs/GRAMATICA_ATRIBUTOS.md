# Gramática de Atributos

## Atributos Sintetizados

- **tipo**: ['int', 'real', 'booleano']
- **valor**: calculado durante execução
- **inicializada**: para memórias

## Atributos Herdados

- **escopo**: nível de escopo
- **tabela_simbolos**: referência à tabela

## Regras de Produção com Atributos

### Operações Aritméticas

#### Operador `+`

**Produção**: EXPRESSAO → OPERANDO₁ OPERANDO₂ +

**Descrição**: Adição de números inteiros ou reais

**Condições**:
- tipo(operando1) in [int, real]
- tipo(operando2) in [int, real]

**Tipo Resultado**: promover_tipo(tipo(operando1), tipo(operando2))

**Verificações**:
- tipos_numericos

#### Operador `-`

**Produção**: EXPRESSAO → OPERANDO₁ OPERANDO₂ -

**Descrição**: Subtração de números inteiros ou reais

**Condições**:
- tipo(operando1) in [int, real]
- tipo(operando2) in [int, real]

**Tipo Resultado**: promover_tipo(tipo(operando1), tipo(operando2))

**Verificações**:
- tipos_numericos

#### Operador `*`

**Produção**: EXPRESSAO → OPERANDO₁ OPERANDO₂ *

**Descrição**: Multiplicação de números inteiros ou reais

**Condições**:
- tipo(operando1) in [int, real]
- tipo(operando2) in [int, real]

**Tipo Resultado**: promover_tipo(tipo(operando1), tipo(operando2))

**Verificações**:
- tipos_numericos

#### Operador `|`

**Produção**: EXPRESSAO → OPERANDO₁ OPERANDO₂ |

**Descrição**: Divisão real (resultado sempre real)

**Condições**:
- tipo(operando1) in [int, real]
- tipo(operando2) in [int, real]
- operando2 != 0

**Tipo Resultado**: real

**Verificações**:
- tipos_numericos
- divisao_por_zero

#### Operador `/`

**Produção**: EXPRESSAO → OPERANDO₁ OPERANDO₂ /

**Descrição**: Divisão inteira (ambos operandos devem ser inteiros)

**Condições**:
- tipo(operando1) == int
- tipo(operando2) == int
- operando2 != 0

**Tipo Resultado**: int

**Verificações**:
- tipos_inteiros
- divisao_por_zero

#### Operador `%`

**Produção**: EXPRESSAO → OPERANDO₁ OPERANDO₂ %

**Descrição**: Resto da divisão inteira (ambos operandos devem ser inteiros)

**Condições**:
- tipo(operando1) == int
- tipo(operando2) == int
- operando2 != 0

**Tipo Resultado**: int

**Verificações**:
- tipos_inteiros
- divisao_por_zero

#### Operador `^`

**Produção**: EXPRESSAO → OPERANDO₁ OPERANDO₂ ^

**Descrição**: Potenciação (expoente deve ser inteiro)

**Condições**:
- tipo(operando1) in [int, real]
- tipo(operando2) == int

**Tipo Resultado**: tipo(operando1)

**Verificações**:
- base_numerica
- expoente_inteiro

### Operações Relacionais

**Produção**: EXPRESSAO → OPERANDO₁ OPERANDO₂ OP_REL

**Descrição**: Comparação relacional (retorna booleano)

**Operadores**: >, <, >=, <=, ==, !=

**Condições**:
- tipo(operando1) in [int, real]
- tipo(operando2) in [int, real]

**Tipo Resultado**: booleano

### Comandos Especiais

#### ARMAZENAR

**Produção**: COMANDO → VALOR IDENTIFICADOR

**Descrição**: Armazena valor em memória

**Condições**:
- tipo(valor) in [int, real]
- identificador valido

**Tipo Resultado**: tipo(valor)

**Efeito Colateral**: adiciona simbolo na tabela

#### RECUPERAR

**Produção**: COMANDO → IDENTIFICADOR

**Descrição**: Recupera valor de memória (erro se não inicializada)

**Condições**:
- identificador in tabela_simbolos
- simbolo.inicializada == True

**Tipo Resultado**: tipo(simbolo)

#### RES

**Produção**: COMANDO → NUMERO RES

**Descrição**: Recupera resultado N linhas anteriores

**Condições**:
- tipo(N) == int
- N >= 0
- N <= tamanho(historico)

**Tipo Resultado**: tipo(historico[N])

### Estruturas de Controle

#### IF

**Produção**: DECISAO → CONDICAO BLOCO_V BLOCO_F IF

**Descrição**: Estrutura condicional (condição deve ser booleana)

**Condições**:
- tipo(condicao) == booleano
- tipo(bloco_verdadeiro) == tipo(bloco_falso)

**Tipo Resultado**: tipo(bloco_verdadeiro)

#### WHILE

**Produção**: LACO → CONDICAO BLOCO WHILE

**Descrição**: Laço de repetição (condição deve ser booleana)

**Condições**:
- tipo(condicao) == booleano

**Tipo Resultado**: tipo(bloco)

## Regra de Promoção de Tipos

```
int  ⊕ int  → int
int  ⊕ real → real
real ⊕ int  → real
real ⊕ real → real
```

Onde ⊕ representa qualquer operador aritmético (+, -, *, |)
