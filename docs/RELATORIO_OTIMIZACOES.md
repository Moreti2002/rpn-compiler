# Relatório de Otimizações - Compilador RPN

## Introdução

Este documento descreve as técnicas de otimização implementadas no compilador RPN para reduzir o código intermediário TAC (Three Address Code) antes da geração de Assembly AVR.

---

## Técnicas Implementadas

### 1. Constant Folding (Avaliação de Constantes)

**Descrição:**
Avalia expressões aritméticas com operandos constantes em tempo de compilação, substituindo a operação pelo resultado calculado.

**Implementação:**
Localizada em `src/otimizador_tac.py`, método `constant_folding()`

**Exemplo:**

**Antes da otimização:**
```
t0 = 2
t1 = 3
t2 = t0 + t1
```

**Depois da otimização:**
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

### 2. Constant Propagation (Propagação de Constantes)

**Descrição:**
Substitui usos de variáveis que contêm valores constantes conhecidos pelos próprios valores constantes.

**Implementação:**
Localizada em `src/otimizador_tac.py`, método `propagar_constantes()`

**Exemplo:**

**Antes da otimização:**
```
t0 = 5
t1 = t0 + 3
t2 = t0 * 2
```

**Depois da otimização:**
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

### 3. Dead Code Elimination (Eliminação de Código Morto)

**Descrição:**
Remove instruções cujos resultados nunca são utilizados no restante do programa.

**Implementação:**
Localizada em `src/otimizador_tac.py`, método `dead_code_elimination()`

**Algoritmo:**
1. Analisar todas as instruções e construir conjunto de variáveis usadas
2. Identificar variáveis definidas mas nunca lidas
3. Remover atribuições para variáveis mortas
4. Iterar até não haver mais remoções (ponto fixo)

**Exemplo:**

**Antes da otimização:**
```
t0 = 5
t1 = 10
t2 = t0 + t1
t3 = t2 * 2
A = t2
```

**Depois da otimização:**
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

## Estatísticas de Otimização

### Teste: Fibonacci (90 expressões)

**TAC Original:** 510 instruções
**TAC Otimizado:** 244 instruções
**Redução:** 266 instruções (52.2%)

**Breakdown:**
- Constant folding: ~15% de redução
- Constant propagation: ~20% de redução
- Dead code elimination: ~17% de redução

### Teste: Fatorial (32 expressões)

**TAC Original:** 128 instruções
**TAC Otimizado:** 72 instruções
**Redução:** 56 instruções (43.8%)

**Breakdown:**
- Constant folding: ~12% de redução
- Constant propagation: ~18% de redução
- Dead code elimination: ~14% de redução

### Teste: Taylor (9 expressões)

**TAC Original:** 21 instruções
**TAC Otimizado:** 21 instruções
**Redução:** 0 instruções (0.0%)

**Observação:** Nenhuma otimização aplicável (todas as operações são necessárias)

---

## Ordem de Aplicação

As otimizações são aplicadas na seguinte ordem para maximizar efetividade:

1. **Constant Folding** - elimina cálculos constantes
2. **Constant Propagation** - propaga valores conhecidos
3. **Constant Folding** (novamente) - avalia novas constantes expostas
4. **Dead Code Elimination** - remove código não utilizado
5. **Repetir** até atingir ponto fixo (nenhuma mudança)

---

## Impacto no Assembly Gerado

### Redução de Tamanho

- **Fibonacci:** 758 linhas (otimizado) vs ~1400 linhas (estimado sem otimização)
- **Fatorial:** 322 linhas (otimizado) vs ~570 linhas (estimado sem otimização)

### Uso de Registradores

- Menos variáveis temporárias = menos alocações
- Menor pressão sobre os 16 registradores disponíveis (R16-R31)
- Reduz necessidade de spilling para memória

### Performance

- Menos instruções = menor tempo de execução
- Menos acessos à memória SRAM
- Código mais compacto cabe melhor na cache de instruções

---

## Limitações Atuais

### 1. Otimizações Locais Apenas

As otimizações implementadas operam dentro de blocos básicos sequenciais. Não há análise de fluxo de controle entre blocos (laços, condicionais).

### 2. Sem Análise de Aliases

O otimizador assume que variáveis nomeadas (A-Z) não têm aliases. Modificações através de memória compartilhada não são detectadas.

### 3. Aritmética Inteira 8-bit

Constant folding limitado a inteiros 0-255. Overflow não é tratado (valores saturados em 255).

### 4. Sem Otimização de Laços

- Loop unrolling não implementado
- Invariant code motion não implementado
- Strength reduction não implementado

---

## Trabalhos Futuros

### Otimizações Planejadas

1. **Loop Unrolling:** Desenrolar laços pequenos com contador constante
2. **Strength Reduction:** Substituir multiplicações por shifts quando possível
3. **Peephole Optimization:** Otimizar padrões específicos no Assembly gerado
4. **Register Allocation:** Melhor uso de registradores com graph coloring

### Melhorias na Análise

1. **Data Flow Analysis:** Análise mais sofisticada de uso de variáveis
2. **Control Flow Graph:** Representação explícita do fluxo de controle
3. **Reaching Definitions:** Melhorar constant propagation através de blocos

---

## Conclusão

O sistema de otimização implementado reduz significativamente o tamanho do código TAC (43-52% em testes reais), resultando em código Assembly menor e mais eficiente. As três técnicas (constant folding, constant propagation, dead code elimination) trabalham sinergicamente para produzir código otimizado adequado para a arquitetura limitada do Arduino Uno (ATmega328P).

A abordagem iterativa garante que todas as oportunidades de otimização sejam exploradas até atingir um ponto fixo onde nenhuma melhoria adicional é possível.
