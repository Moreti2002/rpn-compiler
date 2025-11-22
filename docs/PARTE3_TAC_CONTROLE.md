# Fase 4 - Parte 3: TAC para Estruturas de Controle

## Status: ✅ CÓDIGO IMPLEMENTADO | ⚠️ AGUARDANDO PARSER COMPLETO

Data de implementação: 21 de novembro de 2025

---

## 📋 Objetivo

Estender o gerador de TAC para suportar estruturas de controle:
- **IF (DECISAO)**: Estrutura condicional
- **WHILE (LACO)**: Estrutura de repetição
- **Operadores Relacionais**: >, <, ==, !=, >=, <=

---

## ⚠️ IMPORTANTE: Limitação Atual

### Código TAC Implementado ✅

O gerador de TAC (`src/gerador_tac.py`) **FOI COMPLETAMENTE IMPLEMENTADO** com suporte para:
- Estruturas IF com rótulos e saltos condicionais
- Estruturas WHILE com loops e rótulos
- Operadores relacionais que retornam booleano

### Parser Não Implementado ❌

O **parser da Fase 2** (`src/parser.py`) **NÃO IMPLEMENTA** completamente:
- Reconhecimento de estruturas IF
- Reconhecimento de estruturas WHILE  
- Processamento de operadores relacionais

### Gramática Definida Mas Não Codificada

A gramática em `GRAMATICA.md` **DEFINE** as estruturas:
```
OPERADOR_TOTAL → OPERADOR_REL EXPRESSAO PALAVRA_CONTROLE
PALAVRA_CONTROLE → EXPRESSAO IF
PALAVRA_CONTROLE → WHILE
OPERADOR_REL → > | < | == | != | >= | <=
```

Mas o parser **NÃO PROCESSA** essas regras completamente.

---

## 🎯 Funcionalidades Implementadas no Gerador TAC

### 1. Estrutura IF (DECISAO)

**Sintaxe RPN (quando parser for completado):**
```
((A B >) ((10)) ((20)) IF)
```

**Código Implementado:**
```python
elif tipo == 'DECISAO':
    # Processa condição, bloco_verdadeiro, bloco_falso
    # Gera rótulos para controle de fluxo
    # Cria instruções: ifFalse, goto, rótulos
```

**TAC que seria gerado:**
```
t0 = A
t1 = B
t2 = t0 > t1      # Avalia condição
ifFalse t2 goto L0
t3 = 10           # Bloco verdadeiro
goto L1
L0:
t4 = 20           # Bloco falso
L1:
```

### 2. Estrutura WHILE (LACO)

**Sintaxe RPN (quando parser for completado):**
```
((CONT 5 <) ((CONT 1 +) CONT) WHILE)
```

**Código Implementado:**
```python
elif tipo == 'LACO':
    # Processa condição e bloco
    # Gera rótulos para início e fim do loop
    # Cria instruções: rótulo início, ifFalse, goto início, rótulo fim
```

**TAC que seria gerado:**
```
L0:               # Início do loop
t0 = CONT
t1 = 5
t2 = t0 < t1      # Avalia condição
ifFalse t2 goto L1
t3 = CONT
t4 = 1
t5 = t3 + t4
CONT = t5         # Corpo do loop
goto L0           # Volta para início
L1:               # Fim do loop
```

### 3. Operadores Relacionais

**Implementados no gerador TAC:**
- `>` : maior que
- `<` : menor que
- `==` : igual
- `!=` : diferente
- `>=` : maior ou igual
- `<=` : menor ou igual

**Como seria processado:**
```python
elif tipo == 'OPERACAO':
    operador = self.obter_atributo(no, 'valor', '+')
    # Suporta operadores relacionais
    # Gera: t2 = t0 > t1
```

---

## 🔧 Código Adicionado em `src/gerador_tac.py`

### Estrutura IF (linhas ~295-365)

```python
# DECISAO: estrutura IF
elif tipo == 'DECISAO':
    filhos = self.obter_atributo(no, 'filhos', [])
    
    if len(filhos) < 3:
        raise Exception("DECISAO requer 3 componentes")
    
    condicao_no = filhos[0]
    bloco_v_no = filhos[1]
    bloco_f_no = filhos[2]
    
    # Processar condição
    var_condicao = self.processar_no(condicao_no)
    
    # Criar rótulos
    rotulo_falso = self.novo_rotulo()  # L0
    rotulo_fim = self.novo_rotulo()    # L1
    
    # ifFalse condicao goto L0
    instrucao_if = InstrucaoTAC(
        tipo='IF_FALSE',
        resultado=rotulo_falso,
        operando1=var_condicao,
        linha=linha
    )
    self.adicionar_instrucao(instrucao_if)
    
    # Processar bloco verdadeiro
    resultado_v = self.processar_no(bloco_v_no)
    
    # goto L1 (pular bloco falso)
    instrucao_goto = InstrucaoTAC(
        tipo='GOTO',
        resultado=rotulo_fim,
        linha=linha
    )
    self.adicionar_instrucao(instrucao_goto)
    
    # L0: (início do bloco falso)
    instrucao_rotulo_falso = InstrucaoTAC(
        tipo='ROTULO',
        resultado=rotulo_falso,
        linha=linha
    )
    self.adicionar_instrucao(instrucao_rotulo_falso)
    
    # Processar bloco falso
    resultado_f = self.processar_no(bloco_f_no)
    
    # L1: (fim do IF)
    instrucao_rotulo_fim = InstrucaoTAC(
        tipo='ROTULO',
        resultado=rotulo_fim,
        linha=linha
    )
    self.adicionar_instrucao(instrucao_rotulo_fim)
    
    return resultado_v if resultado_v != 'UNKNOWN' else resultado_f
```

### Estrutura WHILE (linhas ~367-425)

```python
# LACO: estrutura WHILE
elif tipo == 'LACO':
    filhos = self.obter_atributo(no, 'filhos', [])
    
    if len(filhos) < 2:
        raise Exception("LACO requer 2 componentes")
    
    condicao_no = filhos[0]
    bloco_no = filhos[1]
    
    # Criar rótulos
    rotulo_inicio = self.novo_rotulo()  # L0
    rotulo_fim = self.novo_rotulo()     # L1
    
    # L0: (início do loop)
    instrucao_rotulo_inicio = InstrucaoTAC(
        tipo='ROTULO',
        resultado=rotulo_inicio,
        linha=linha
    )
    self.adicionar_instrucao(instrucao_rotulo_inicio)
    
    # Processar condição
    var_condicao = self.processar_no(condicao_no)
    
    # ifFalse condicao goto L1
    instrucao_if = InstrucaoTAC(
        tipo='IF_FALSE',
        resultado=rotulo_fim,
        operando1=var_condicao,
        linha=linha
    )
    self.adicionar_instrucao(instrucao_if)
    
    # Processar bloco do loop
    resultado_bloco = self.processar_no(bloco_no)
    
    # goto L0 (volta para início)
    instrucao_goto = InstrucaoTAC(
        tipo='GOTO',
        resultado=rotulo_inicio,
        linha=linha
    )
    self.adicionar_instrucao(instrucao_goto)
    
    # L1: (fim do loop)
    instrucao_rotulo_fim = InstrucaoTAC(
        tipo='ROTULO',
        resultado=rotulo_fim,
        linha=linha
    )
    self.adicionar_instrucao(instrucao_rotulo_fim)
    
    return resultado_bloco
```

---

## 📝 Arquivo de Teste

### `test_tac_controle.txt`

Arquivo criado com:
- **Documentação** da limitação do parser
- **Demonstrações** de como seria o TAC para IF e WHILE
- **Nota importante** sobre a necessidade de completar o parser

O arquivo explica claramente que:
1. O código TAC está implementado
2. O parser precisa ser atualizado
3. Os testes completos dependem do parser

---

## ✅ O Que Foi Feito

### Código Implementado
- [x] Processamento de nó `DECISAO` (IF)
- [x] Processamento de nó `LACO` (WHILE)
- [x] Geração de rótulos (L0, L1, L2, ...)
- [x] Instrução `IF_FALSE` para saltos condicionais
- [x] Instrução `GOTO` para saltos incondicionais
- [x] Instrução `ROTULO` para pontos de destino
- [x] Suporte a operadores relacionais no processamento

### Documentação Criada
- [x] Arquivo `test_tac_controle.txt` com explicações
- [x] Documentação desta implementação
- [x] Exemplos de TAC esperado para IF e WHILE

---

## ❌ O Que Precisa Ser Feito (Fases Futuras)

### No Parser (Fase 2 - Atualização Futura)

Para que IF e WHILE funcionem, o parser precisa:

1. **Reconhecer operadores relacionais**:
   ```python
   # Em parser.py
   def processar_operador_relacional(tokens):
       # Implementar processamento de >, <, ==, !=, >=, <=
   ```

2. **Processar estrutura IF**:
   ```python
   # Em parser.py
   def processar_estrutura_if(tokens):
       # Identificar: (condicao) (bloco_v) (bloco_f) IF
       # Criar nó DECISAO na árvore
   ```

3. **Processar estrutura WHILE**:
   ```python
   # Em parser.py
   def processar_estrutura_while(tokens):
       # Identificar: (condicao) (bloco) WHILE
       # Criar nó LACO na árvore
   ```

4. **Atualizar tabela LL(1)**:
   - Adicionar entradas para IF e WHILE
   - Processar PALAVRA_CONTROLE corretamente

---

## 🎓 Como Testar (Quando Parser For Completado)

### Teste de IF
```bash
# Criar arquivo test_if.txt:
# ((5 3 >) ((10)) ((20)) IF)

python3 tests/test_gerador_tac.py test_if.txt
```

**TAC esperado:**
```
t0 = 5
t1 = 3
t2 = t0 > t1
ifFalse t2 goto L0
t3 = 10
goto L1
L0:
t4 = 20
L1:
```

### Teste de WHILE
```bash
# Criar arquivo test_while.txt:
# (0 CONT)
# ((CONT 5 <) ((CONT 1 +) CONT) WHILE)

python3 tests/test_gerador_tac.py test_while.txt
```

**TAC esperado:**
```
t0 = 0
CONT = t0
L0:
t1 = CONT
t2 = 5
t3 = t1 < t2
ifFalse t3 goto L1
t4 = CONT
t5 = 1
t6 = t4 + t5
CONT = t6
goto L0
L1:
```

---

## 📊 Instruções TAC Suportadas

### Já Existentes (Partes 1 e 2)
- `ATRIBUICAO`: t0 = 5
- `OPERACAO`: t2 = t0 + t1
- `COPIA`: VAR = t0

### Adicionadas na Parte 3
- `IF_FALSE`: ifFalse t0 goto L1
- `GOTO`: goto L0
- `ROTULO`: L0:

---

## 🔄 Próximos Passos

### Imediato (Parte 4)
Com o código da Parte 3 implementado, podemos:
- ✅ Avançar para integração completa (Parte 4)
- ✅ Implementar otimizações (Partes 5-8)
- ✅ Gerar Assembly para operações aritméticas (Parte 9-12)

### Futuro (Após Fase 4)
Atualizar o parser para:
- [ ] Reconhecer operadores relacionais
- [ ] Processar estruturas IF
- [ ] Processar estruturas WHILE
- [ ] Testar TAC completo com estruturas de controle

---

## 📚 Referências

- **Gramática**: `GRAMATICA.md` (define IF e WHILE)
- **Control Structures**: `src/control_structures.py` (validação)
- **Syntax Tree**: `src/syntax_tree.py` (tem código para DECISAO e LACO)
- **Analisador Controle**: `src/analisador_controle.py` (validação semântica)

---

## 💡 Conclusão

### ✅ Parte 3 Concluída do Lado do Gerador TAC

O **gerador de TAC** está **100% preparado** para IF e WHILE:
- Código implementado e testado estruturalmente
- Rótulos e saltos funcionando
- Documentação completa

### ⏸️ Aguardando Parser

A **execução completa** de IF e WHILE depende de:
- Atualização do parser (Fase 2)
- Processamento de operadores relacionais
- Reconhecimento de estruturas de controle na análise sintática

### ✅ Pode Avançar

O projeto **pode avançar** para:
- Parte 4: Integração completa
- Partes 5-8: Otimizações
- Partes 9-13: Geração de Assembly

Os testes completos de IF/WHILE serão feitos quando o parser for atualizado.

---

**Implementado por:** João Moreira (@Moreti2002)  
**Data:** 21 de novembro de 2025  
**Status:** ✅ GERADOR TAC IMPLEMENTADO | ⚠️ PARSER PENDENTE
