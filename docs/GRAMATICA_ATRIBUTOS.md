# Gramática de Atributos - Fase 3

*Gerado em: 2025-11-05 07:18:08*

---

## Introdução

Esta gramática de atributos define as regras semânticas para a linguagem de programação simplificada em notação polonesa reversa (RPN). Cada regra especifica como os tipos são inferidos e propagados através da árvore sintática abstrata.

## Atributos Sintetizados

Atributos calculados a partir dos filhos (propagação bottom-up):

- **tipo**: valores possíveis = `int, real, booleano`
- **valor**: calculado durante execução
- **inicializada**: para memórias

## Atributos Herdados

Atributos calculados a partir do pai ou irmãos (propagação top-down):

- **escopo**: nível de escopo
- **tabela_simbolos**: referência à tabela

## Regra de Promoção de Tipos

A função `promover_tipo(τ₁, τ₂)` define o tipo resultante de operações entre tipos diferentes:

```
promover_tipo : Tipo × Tipo → Tipo

promover_tipo(int, int)   = int
promover_tipo(int, real)  = real
promover_tipo(real, int)  = real
promover_tipo(real, real) = real
```

Esta regra é aplicada em operações aritméticas (+, -, *, |) quando os operandos têm tipos diferentes.

## Regras para Operações Aritméticas

### Operador `+` - Adição de números inteiros ou reais

**Produção:** `EXPRESSAO → OPERANDO₁ OPERANDO₂ +`

**Regra de Inferência:**

```
Γ ⊢ operando₁ : τ₁    Γ ⊢ operando₂ : τ₂    tipo(operando1) in [int, real]    tipo(operando2) in [int, real]
──────────────────────────────────────────────────────────────────────
Γ ⊢ operando₁ + operando₂ : promover_tipo(tipo(operando1), tipo(operando2))
```

**Condições:**
- tipo(operando1) in [int, real]
- tipo(operando2) in [int, real]

**Verificações:**
- `tipos_numericos`

### Operador `-` - Subtração de números inteiros ou reais

**Produção:** `EXPRESSAO → OPERANDO₁ OPERANDO₂ -`

**Regra de Inferência:**

```
Γ ⊢ operando₁ : τ₁    Γ ⊢ operando₂ : τ₂    tipo(operando1) in [int, real]    tipo(operando2) in [int, real]
──────────────────────────────────────────────────────────────────────
Γ ⊢ operando₁ - operando₂ : promover_tipo(tipo(operando1), tipo(operando2))
```

**Condições:**
- tipo(operando1) in [int, real]
- tipo(operando2) in [int, real]

**Verificações:**
- `tipos_numericos`

### Operador `*` - Multiplicação de números inteiros ou reais

**Produção:** `EXPRESSAO → OPERANDO₁ OPERANDO₂ *`

**Regra de Inferência:**

```
Γ ⊢ operando₁ : τ₁    Γ ⊢ operando₂ : τ₂    tipo(operando1) in [int, real]    tipo(operando2) in [int, real]
──────────────────────────────────────────────────────────────────────
Γ ⊢ operando₁ * operando₂ : promover_tipo(tipo(operando1), tipo(operando2))
```

**Condições:**
- tipo(operando1) in [int, real]
- tipo(operando2) in [int, real]

**Verificações:**
- `tipos_numericos`

### Operador `|` - Divisão real (resultado sempre real)

**Produção:** `EXPRESSAO → OPERANDO₁ OPERANDO₂ |`

**Regra de Inferência:**

```
Γ ⊢ operando₁ : τ₁    Γ ⊢ operando₂ : τ₂    tipo(operando1) in [int, real]    tipo(operando2) in [int, real]    operando2 != 0
──────────────────────────────────────────────────────────────────────
Γ ⊢ operando₁ | operando₂ : real
```

**Condições:**
- tipo(operando1) in [int, real]
- tipo(operando2) in [int, real]
- operando2 != 0

**Verificações:**
- `tipos_numericos`
- `divisao_por_zero`

### Operador `/` - Divisão inteira (ambos operandos devem ser inteiros)

**Produção:** `EXPRESSAO → OPERANDO₁ OPERANDO₂ /`

**Regra de Inferência:**

```
Γ ⊢ operando₁ : τ₁    Γ ⊢ operando₂ : τ₂    tipo(operando1) == int    tipo(operando2) == int    operando2 != 0
──────────────────────────────────────────────────────────────────────
Γ ⊢ operando₁ / operando₂ : int
```

**Condições:**
- tipo(operando1) == int
- tipo(operando2) == int
- operando2 != 0

**Verificações:**
- `tipos_inteiros`
- `divisao_por_zero`

### Operador `%` - Resto da divisão inteira (ambos operandos devem ser inteiros)

**Produção:** `EXPRESSAO → OPERANDO₁ OPERANDO₂ %`

**Regra de Inferência:**

```
Γ ⊢ operando₁ : τ₁    Γ ⊢ operando₂ : τ₂    tipo(operando1) == int    tipo(operando2) == int    operando2 != 0
──────────────────────────────────────────────────────────────────────
Γ ⊢ operando₁ % operando₂ : int
```

**Condições:**
- tipo(operando1) == int
- tipo(operando2) == int
- operando2 != 0

**Verificações:**
- `tipos_inteiros`
- `divisao_por_zero`

### Operador `^` - Potenciação (expoente deve ser inteiro)

**Produção:** `EXPRESSAO → OPERANDO₁ OPERANDO₂ ^`

**Regra de Inferência:**

```
Γ ⊢ operando₁ : τ₁    Γ ⊢ operando₂ : τ₂    tipo(operando1) in [int, real]    tipo(operando2) == int
──────────────────────────────────────────────────────────────────────
Γ ⊢ operando₁ ^ operando₂ : tipo(operando1)
```

**Condições:**
- tipo(operando1) in [int, real]
- tipo(operando2) == int

**Verificações:**
- `base_numerica`
- `expoente_inteiro`

## Regras para Operações Relacionais

Todos os operadores relacionais (`>`, `<`, `>=`, `<=`, `==`, `!=`) seguem a mesma regra:

**Produção:** `EXPRESSAO → OPERANDO₁ OPERANDO₂ OP_REL`

**Regra de Inferência:**

```
Γ ⊢ operando₁ : τ₁    Γ ⊢ operando₂ : τ₂    τ₁, τ₂ ∈ {int, real}
──────────────────────────────────────────────────────────────────────
Γ ⊢ operando₁ op_rel operando₂ : booleano
```

**Descrição:** Comparação relacional (retorna booleano)

## Regras para Comandos Especiais

### ARMAZENAR

**Descrição:** Armazena valor em memória

**Produção:** `COMANDO → VALOR IDENTIFICADOR`

**Condições:**
- tipo(valor) in [int, real]
- identificador valido

**Tipo Resultado:** `tipo(valor)`

**Efeito Colateral:** adiciona simbolo na tabela

### RECUPERAR

**Descrição:** Recupera valor de memória (erro se não inicializada)

**Produção:** `COMANDO → IDENTIFICADOR`

**Condições:**
- identificador in tabela_simbolos
- simbolo.inicializada == True

**Tipo Resultado:** `tipo(simbolo)`

### RES

**Descrição:** Recupera resultado N linhas anteriores

**Produção:** `COMANDO → NUMERO RES`

**Condições:**
- tipo(N) == int
- N >= 0
- N <= tamanho(historico)

**Tipo Resultado:** `tipo(historico[N])`

## Regras para Estruturas de Controle

### IF

**Descrição:** Estrutura condicional (condição deve ser booleana)

**Produção:** `DECISAO → CONDICAO BLOCO_V BLOCO_F IF`

**Condições:**
- tipo(condicao) == booleano
- tipo(bloco_verdadeiro) == tipo(bloco_falso)

**Tipo Resultado:** `tipo(bloco_verdadeiro)`

### WHILE

**Descrição:** Laço de repetição (condição deve ser booleana)

**Produção:** `LACO → CONDICAO BLOCO WHILE`

**Condições:**
- tipo(condicao) == booleano

**Tipo Resultado:** `tipo(bloco)`

