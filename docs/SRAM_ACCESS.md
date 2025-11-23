# Parte 11: Acesso à Memória SRAM

## Objetivo

Implementar acesso à memória SRAM do ATmega328P para persistência de variáveis nomeadas (A-Z), permitindo que seus valores sejam mantidos entre operações.

## Estratégia de Memória

### Layout SRAM (ATmega328P: 0x0100 - 0x08FF, 2KB)

```
0x0100 - 0x011F: Temporários t0-t31 (32 bytes) - RESERVADO
0x0120 - 0x0139: Variáveis A-Z (26 bytes) - IMPLEMENTADO
0x013A - 0x08FF: Espaço livre (1974 bytes)
```

### Estratégia de Alocação

1. **Variáveis Nomeadas (A-Z)**: Persistem na SRAM
   - Endereço: `0x0120 + (letra - 'A')`
   - Exemplo: A → 0x0120, X → 0x0137, Z → 0x0139
   - Acesso: `lds` para ler, `sts` para escrever

2. **Temporários (t0-t31)**: Mantidos em registradores
   - Usam r16-r31 quando disponível
   - Não persistem na SRAM (otimização)
   - Endereço reservado: `0x0100 + n` (para uso futuro)

## Implementação

### Constantes Adicionadas

```python
SRAM_START = 0x0100
TEMP_VARS_ADDR = 0x0100  # 32 bytes para t0-t31
NAMED_VARS_ADDR = 0x0120  # 26 bytes para A-Z
```

### Funções de Suporte

#### 1. Classificação de Variáveis

```python
def eh_variavel_nomeada(self, nome: str) -> bool:
    """Verifica se é variável A-Z"""
    return len(nome) == 1 and nome.isupper() and nome.isalpha()

def eh_temporario(self, nome: str) -> bool:
    """Verifica se é temporário t0-t31"""
    return nome.startswith('t') and nome[1:].isdigit()
```

#### 2. Cálculo de Endereços

```python
def calcular_endereco_variavel(self, nome: str) -> int:
    """
    Calcula endereço SRAM para variável
    
    Temporários (futuro): t0 → 0x0100, t1 → 0x0101, ...
    Variáveis nomeadas: A → 0x0120, B → 0x0121, ..., Z → 0x0139
    """
    if nome.startswith('t'):
        num = int(nome[1:])
        return self.TEMP_VARS_ADDR + num
    else:
        return self.NAMED_VARS_ADDR + (ord(nome[0]) - ord('A'))
```

#### 3. Geração de Código SRAM

```python
def gerar_load_variavel(self, dest_reg: int, variavel: str) -> List[str]:
    """Gera instrução lds para carregar variável da SRAM"""
    endereco = self.calcular_endereco_variavel(variavel)
    return [
        f"    ; Carregar {variavel} da SRAM (0x{endereco:04X})",
        f"    lds r{dest_reg}, 0x{endereco:04X}"
    ]

def gerar_store_variavel(self, src_reg: int, variavel: str) -> List[str]:
    """Gera instrução sts para salvar variável na SRAM"""
    endereco = self.calcular_endereco_variavel(variavel)
    return [
        f"    ; Salvar {variavel} na SRAM (0x{endereco:04X})",
        f"    sts 0x{endereco:04X}, r{src_reg}"
    ]
```

### Modificações nas Funções Principais

#### gerar_atribuicao()

Modificada para detectar variáveis nomeadas e salvar na SRAM:

```python
# Antes: X = 10
ldi r16, 10

# Depois: X = 10
ldi r16, 10
sts 0x0137, r16  # Salvar X na SRAM
```

#### gerar_copia()

Modificada para carregar/salvar variáveis da SRAM:

```python
# Antes: Y = X (ambos em registradores)
mov r17, r16

# Depois: Y = X (ambos na SRAM)
lds r16, 0x0137  # Carregar X
sts 0x0138, r16  # Salvar Y
```

#### gerar_operacao()

Modificada para carregar operandos da SRAM quando necessário:

```python
# Antes: Z = X + Y (esperando registradores)
add r16, r17

# Depois: Z = X + Y (carregando da SRAM)
lds r16, 0x0137    # Carregar X
lds r17, 0x0138    # Carregar Y
mov r18, r16       # Copiar para registrador de trabalho
add r18, r17       # Somar
sts 0x0139, r18    # Salvar Z
```

## Testes

### Suite de Testes (test_assembly_parte11.py)

**6/6 testes passando ✅**

1. ✅ **Atribuição constante → variável**
   - `X = 10` gera `sts 0x0137, r16`
   
2. ✅ **Cópia entre variáveis**
   - `Y = X` carrega e salva na SRAM
   
3. ✅ **Operação com variáveis**
   - `Z = X + Y` usa `lds` para ambos operandos e `sts` para resultado
   
4. ✅ **Endereços SRAM corretos**
   - A=0x0120, B=0x0121, ..., X=0x0137, Y=0x0138, Z=0x0139
   
5. ✅ **Temporários vs Nomeadas**
   - t0 usa apenas registradores
   - W usa SRAM (sts)
   
6. ✅ **Operação mista**
   - `W = Z + 5` carrega Z da SRAM, soma com constante, salva W

### Exemplo de Assembly Gerado

```assembly
; Entrada: (10 X)
ldi r16, 10
sts 0x0137, r16  ; Salvar X na SRAM

; Entrada: (20 Y)
ldi r16, 20
sts 0x0138, r16  ; Salvar Y na SRAM

; Entrada: (X Y +) - operação é otimizada se não usada
; Mas se fosse necessária:
lds r16, 0x0137  ; Carregar X
lds r17, 0x0138  ; Carregar Y
add r16, r17     ; Somar
```

## Instruções AVR Utilizadas

### lds (Load Direct from SRAM)

```assembly
lds rX, 0xaddr    ; Carrega byte do endereço SRAM para registrador
                  ; Ciclos: 2
                  ; Tamanho: 4 bytes (32-bit instruction)
```

### sts (Store Direct to SRAM)

```assembly
sts 0xaddr, rX    ; Salva registrador no endereço SRAM
                  ; Ciclos: 2
                  ; Tamanho: 4 bytes (32-bit instruction)
```

## Estatísticas

- **Arquivo modificado**: `src/gerador_assembly_avr.py`
- **Linhas adicionadas**: ~140 linhas
- **Funções novas**: 5 (eh_variavel_nomeada, eh_temporario, calcular_endereco_variavel, gerar_load_variavel, gerar_store_variavel)
- **Funções modificadas**: 3 (gerar_atribuicao, gerar_copia, gerar_operacao)
- **Testes**: 6/6 passando ✅

## Benefícios

1. **Persistência**: Variáveis mantêm valores entre operações
2. **Memória Abundante**: 2KB SRAM disponível vs 32 registradores
3. **Programas Complexos**: Permite mais de 32 variáveis simultâneas
4. **Compatibilidade**: Mantém temporários em registradores para performance

## Limitações Atuais

1. **Otimizador Agressivo**: Remove código morto, dificultando teste end-to-end
2. **Sem Escape de Registrador**: Ainda não implementado spilling automático
3. **Endereço Fixo**: Não suporta arrays ou estruturas dinâmicas

## Próximos Passos (Parte 12)

- Implementar estruturas de controle completas (IF/ELSE, WHILE)
- Adicionar suporte a loops aninhados
- Implementar break/continue
- Otimizar uso de registradores com spilling para SRAM quando necessário

## Conclusão

A Parte 11 implementa com sucesso o acesso à SRAM para variáveis nomeadas (A-Z), permitindo persistência de dados e programas mais complexos. As instruções `lds` e `sts` são geradas corretamente, e todos os testes unitários passam.
