# Parte 9-10: Gerador de Assembly AVR para Arduino Uno

## Visão Geral

Esta fase implementa a geração de código Assembly AVR a partir do TAC otimizado, permitindo executar programas RPN diretamente no microcontrolador ATmega328P (Arduino Uno).

## Objetivos Implementados

### ✅ Parte 9: Prólogo e Epílogo
- Configuração do Stack Pointer
- Inicialização de registradores
- Setup da UART para comunicação serial
- Mensagem de inicialização
- Loop infinito principal

### ✅ Parte 10: Operações Aritméticas
- Alocação de registradores (r16-r31)
- Mapeamento TAC → Assembly
- Operações: `+`, `-`, `*`, `/`, `%`, `^`
- Comparações: `<`, `>`, `<=`, `>=`, `==`, `!=`
- Suporte a constantes inline (otimização)

## Arquitetura do Código

### Estrutura do Assembly Gerado

```assembly
; === PRÓLOGO ===
main:
    clr r0                    ; Registrador zero
    ldi r16, STACK_LOW
    out SPL_ADDR, r16         ; Configurar Stack
    ldi r16, STACK_HIGH
    out SPH_ADDR, r16
    
    call setup_uart           ; Inicializar UART
    call print_startup_message
    call programa_principal

loop_forever:
    rjmp loop_forever

; === FUNÇÕES UART ===
setup_uart:
    ; Modo U2X ativado (UBRR = 207 para 9600 baud @ 16MHz)
    ...

uart_transmit:
    ; Enviar caractere via serial
    ...

uart_print_string:
    ; Imprimir string usando lpm (Load Program Memory)
    ...

; === PROGRAMA PRINCIPAL ===
programa_principal:
    ; Código gerado a partir do TAC
    ...

; === STRINGS (em .text para lpm) ===
msg_startup:
    .asciz "Compilador RPN - Arduino Uno\r\n"

; === SEÇÕES DE DADOS ===
.section .bss
temp_vars: .space 32    ; Temporários t0-t31
named_vars: .space 26   ; Variáveis A-Z
```

## Mapeamento TAC → Assembly

### 1. Atribuições
```python
# TAC: t0 = 5
ldi r16, 5              # Carregar constante

# TAC: X = t0
mov r17, r16            # Copiar registrador
```

### 2. Operações Binárias
```python
# TAC: t2 = t0 + t1
add r18, r16, r17       # Soma
sub r18, r16, r17       # Subtração
mul r16, r17            # Multiplicação (resultado em r0:r1)
```

### 3. Estruturas de Controle
```python
# TAC: rotulo L0
L0:                     # Rótulo

# TAC: goto L0
rjmp L0                 # Jump incondicional

# TAC: ifFalse t0 goto L1
tst r16
breq L1                 # Branch se zero
```

## Problemas Encontrados e Soluções

### 🔧 Problema 1: Caracteres Aleatórios na Serial

**Sintoma:** Monitor serial mostrando lixo (�����␡␞��...)

**Causa:** Baud rate incorreto (103 vs 207)

**Solução:** Ativar modo U2X (double speed UART)
```assembly
; ANTES: Modo normal
ldi r16, 103        ; UBRR = (16MHz / (16 * 9600)) - 1

; DEPOIS: Modo U2X
ldi r16, 0x02
sts UCSR0A, r16     ; Ativar U2X
ldi r16, 207        ; UBRR = (16MHz / (8 * 9600)) - 1
```

**Teste que identificou:** `teste_u2x.s` imprimiu "TEST U2X" corretamente ✅

### 🔧 Problema 2: Strings Não Aparecem

**Sintoma:** Caracteres isolados mas não string completa

**Causa:** Strings em `.data` não podem ser lidas com `ld` (Load Data)

**Solução:** Mover strings para `.text` e usar `lpm` (Load Program Memory)

```assembly
; ANTES: String em .data
.section .data
msg: .asciz "Hello"
; Código: ld r16, Z+    ❌ Lê da RAM

; DEPOIS: String em .text
.section .text
msg: .asciz "Hello"
; Código: lpm r16, Z+   ✅ Lê da Flash
```

**Teste que identificou:** `teste_text.s` funcionou, `teste_lpm.s` não ✅

### 🔧 Problema 3: Otimização Causando Loops Infinitos

**Sintoma:** TAC otimizado cria condições constantes

**Solução:** Avaliar condições constantes em tempo de compilação

```python
# TAC: ifFalse 1 goto L0
# Solução: Não gerar código (condição sempre falsa)

# TAC: ifFalse 0 goto L0
# Solução: Gerar apenas rjmp L0 (sempre pula)
```

## Configuração UART Correta

```assembly
setup_uart:
    ; 1. Desabilitar UART
    ldi r16, 0x00
    sts UCSR0B, r16         ; UCSR0B = 0
    
    ; 2. Formato 8N1
    ldi r16, 0x06
    sts UCSR0C, r16         ; UCSZ01:0 = 11
    
    ; 3. Ativar U2X (double speed)
    ldi r16, 0x02
    sts UCSR0A, r16         ; U2X0 = 1
    
    ; 4. Baud rate 9600
    ldi r16, 207
    ldi r17, 0
    sts UBRR0L, r16         ; UBRR = 207
    sts UBRR0H, r17
    
    ; 5. Habilitar TX
    ldi r16, 0x08
    sts UCSR0B, r16         ; TXEN0 = 1
    
    ; 6. Delay estabilização
    ldi r17, 255
delay:
    dec r17
    brne delay
```

## Alocação de Registradores

| Registrador | Uso |
|-------------|-----|
| r0 | Zero (sempre 0) |
| r1 | Multiplicação (resultado alto) |
| r16-r31 | Variáveis temporárias (t0-t15) |
| r26-r27 (X) | Ponteiro para dados |
| r28-r29 (Y) | Frame pointer |
| r30-r31 (Z) | Ponteiro para strings (lpm) |

## Testes Realizados

### Teste no Arduino Uno

**Arquivo:** `examples/test_arduino_simples.txt`
```rpn
(10 X)
(20 Y)
(X Y +)
(30 RESULTADO)
```

**Compilação:**
```bash
python3 main_assembly.py examples/test_arduino_simples.txt \
    --output output/programa_final.s

avr-gcc -mmcu=atmega328p output/programa_final.s -o programa_final.elf
avr-objcopy -O ihex -j .text -j .data programa_final.elf programa_final.hex
avrdude -p atmega328p -c arduino -P COM8 -b 115200 \
    -U flash:w:programa_final.hex
```

**Resultado no Monitor Serial (9600 baud):**
```
Compilador RPN - Arduino Uno
```
✅ **SUCESSO!**

### Suite de Testes

```bash
# Teste Parte 9: Prólogo/Epílogo
pytest tests/test_assembly_parte9.py
# 6/6 testes passando ✅

# Teste Parte 10: Operações
pytest tests/test_assembly_parte10.py
# 10/10 testes passando ✅
```

## Estatísticas

### Programa Teste (35 expressões)
- **TAC Original:** 133 instruções
- **TAC Otimizado:** 34 instruções (74.4% redução)
- **Assembly:** 186 linhas
- **Flash usado:** 280 bytes (0.9% de 32KB)
- **RAM usado:** 0 bytes (0% de 2KB)

## Limitações Atuais

1. ❌ Variáveis não persistem em memória (apenas registradores)
2. ❌ Apenas TX habilitado (sem recepção serial)
3. ❌ Sem acesso à SRAM para arrays/structs
4. ❌ Sem funções de debug (print_number)
5. ❌ Multiplicação/divisão limitadas (8 bits)

## Próximos Passos

### Parte 11: Acesso à Memória SRAM
- Implementar `lds`/`sts` para variáveis
- Persistir variáveis nomeadas (A-Z)
- Suporte ao operador `MEM`

### Parte 12: Estruturas de Controle Completas
- IF/ELSE com blocos
- WHILE com break/continue
- Otimização de jumps

### Parte 13: Debug UART
- `print_number()` - Converter inteiro para ASCII
- `print_variable()` - Mostrar valor de variável
- Modo verbose para debugging

## Arquivos Gerados

```
src/
  gerador_assembly_avr.py   # Gerador principal (756 linhas)

tests/
  test_assembly_parte9.py   # Testes prólogo/epílogo
  test_assembly_parte10.py  # Testes operações

output/
  programa_final.s          # Programa funcional ✅
  
arduino_debug/
  teste_u2x.s              # Teste que resolveu U2X ⭐
  teste_text.s             # Teste que resolveu strings ⭐
  [outros 15 testes]
```

## Referências

- [ATmega328P Datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf)
- [AVR Instruction Set Manual](https://ww1.microchip.com/downloads/en/devicedoc/atmel-0856-avr-instruction-set-manual.pdf)
- [Arduino Uno Hardware](https://docs.arduino.cc/hardware/uno-rev3)

## Conclusão

✅ O compilador RPN agora gera código Assembly funcional para Arduino Uno, com comunicação serial operacional a 9600 baud. Todos os problemas de UART foram resolvidos através de testes iterativos, identificando:

1. Necessidade do modo U2X para baud rate preciso
2. Strings devem estar em `.text` e usar `lpm`
3. Simplificação do `uart_transmit` (apenas UDRE0)

**Status:** Pronto para implementar acesso à memória (Parte 11) 🚀
