# Relatório de Julgamento de Tipos

*Gerado em: 2025-11-05 07:18:08*

---

## Introdução

Este relatório documenta todas as regras de dedução de tipos aplicadas durante a análise semântica. Cada entrada mostra como o tipo de uma expressão foi inferido a partir dos tipos de seus componentes.

## Estatísticas

- **Total de regras aplicadas:** 81

### Distribuição de Tipos Inferidos

| Tipo | Quantidade |
|------|------------|
| `int` | 64 |
| `real` | 17 |

## Regras de Dedução Aplicadas

### Regra 1 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 2 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 3 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 4 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 5 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 6 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 7 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 8 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 9 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `real`

---

### Regra 10 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `real`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : real
Γ ⊢ operando₂ : real
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : real
```

---

### Regra 11 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `real`

---

### Regra 12 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `real`

---

### Regra 13 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 14 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 15 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 16 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 17 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `real`

---

### Regra 18 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `real`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : real
Γ ⊢ operando₂ : real
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : real
```

---

### Regra 19 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `real`

---

### Regra 20 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `real`

---

### Regra 21 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 22 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 23 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 24 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 25 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 26 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 27 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 28 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 29 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 30 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 31 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 32 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 33 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 34 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 35 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 36 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 37 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 38 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 39 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 40 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 41 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 42 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 43 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 44 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 45 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 46 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 47 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 48 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 49 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `real`

---

### Regra 50 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `real`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : real
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : real
```

*Promoção de tipos aplicada: `real` + `int` → `real`*

---

### Regra 51 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `real`

---

### Regra 52 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 53 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 54 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 55 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 56 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 57 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 58 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 59 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 60 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 61 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `real`

---

### Regra 62 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `real`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : real
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : real
```

*Promoção de tipos aplicada: `real` + `int` → `real`*

---

### Regra 63 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `real`

---

### Regra 64 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `real`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : real
Γ ⊢ operando₂ : real
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : real
```

---

### Regra 65 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `real`

---

### Regra 66 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `real`

---

### Regra 67 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 68 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 69 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 70 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 71 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 72 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 73 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 74 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 75 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 76 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 77 - Linha 1

**Tipo do Nó:** `EXPRESSAO`

**Tipo Inferido:** `int`

---

### Regra 78 - Linha 1

**Tipo do Nó:** `OPERACAO`

**Tipo Inferido:** `int`

**Operador:** `None`

**Dedução:**

```
Γ ⊢ operando₁ : int
Γ ⊢ operando₂ : int
──────────────────────────────────────────────────
Γ ⊢ operando₁ None operando₂ : int
```

---

### Regra 79 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 80 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

### Regra 81 - Linha 1

**Tipo do Nó:** `NUMERO`

**Tipo Inferido:** `int`

---

