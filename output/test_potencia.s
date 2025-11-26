; ===========================================================================
; Programa gerado pelo Compilador RPN para Arduino Uno (ATmega328P)
; ===========================================================================

#include <avr/io.h>

; === CONSTANTES ===
.equ STACK_LOW, 0xff
.equ STACK_HIGH, 0x08
.equ SPL_ADDR, 0x3d
.equ SPH_ADDR, 0x3e

; === CÓDIGO PRINCIPAL ===
.section .text
.global main

main:
    ; Configurar registrador zero (usado em operações adc)
    clr r0

    ; Configurar Stack Pointer
    ldi r16, STACK_LOW
    out SPL_ADDR, r16
    ldi r16, STACK_HIGH
    out SPH_ADDR, r16

    ; Configurar UART
    call setup_uart

    ; Enviar mensagem de inicialização
    call print_startup_message

    ; Executar programa principal
    call programa_principal

; === LOOP INFINITO ===
loop_forever:
    rjmp loop_forever

; === FUNÇÃO: Configurar UART ===
setup_uart:
    push r16
    push r17

    ; 1. Desabilitar UART completamente
    ldi r16, 0x00
    sts 0xC1, r16    ; UCSR0B = 0

    ; 2. Configurar formato: 8N1 (UCSZ01:0 = 11)
    ldi r16, 0x06
    sts 0xC2, r16    ; UCSR0C = 0b00000110

    ; 3. Ativar U2X (double speed) - compatível com Arduino
    ldi r16, 0x02
    sts 0xC0, r16    ; UCSR0A = 0b00000010 (U2X0=1)

    ; 4. Configurar baud rate: 9600 @ 16MHz com U2X
    ; UBRR = (F_CPU / (8 * BAUD)) - 1 = 207
    ldi r16, 207
    ldi r17, 0
    sts 0xC4, r16    ; UBRR0L = 207
    sts 0xC5, r17    ; UBRR0H = 0

    ; 5. Habilitar TX (TXEN0 = bit 3)
    ldi r16, 0x08
    sts 0xC1, r16    ; UCSR0B = 0b00001000

    ; 6. Aguardar UART estabilizar
    ldi r17, 255
uart_init_delay:
    dec r17
    brne uart_init_delay

    pop r17
    pop r16
    ret

; === FUNÇÃO: Enviar caractere via UART ===
; Entrada: r16 = caractere a enviar
uart_transmit:
    push r17

uart_wait:
    ; Aguardar buffer vazio (UDRE0 = bit 5)
    lds r17, 0xC0    ; UCSR0A
    sbrs r17, 5      ; Pular se UDRE0 = 1
    rjmp uart_wait

    ; Enviar byte
    sts 0xC6, r16    ; UDR0

    pop r17
    ret

; === FUNÇÃO: Enviar string via UART ===
; Entrada: Z aponta para string em FLASH (terminada em 0)
uart_print_string:
    push r16
    push ZL
    push ZH

print_loop:
    lpm r16, Z+      ; Ler byte da Flash
    tst r16
    breq print_done
    call uart_transmit
    rjmp print_loop

print_done:
    pop ZH
    pop ZL
    pop r16
    ret

; === FUNÇÃO: Imprimir mensagem de inicialização ===
print_startup_message:
    push ZL
    push ZH

    ldi ZL, lo8(msg_startup)
    ldi ZH, hi8(msg_startup)
    call uart_print_string

    pop ZH
    pop ZL
    ret

; === FUNÇÃO: Imprimir número decimal (0-255) ===
; Entrada: r16 = número a imprimir
print_number:
    push r16
    push r17
    push r18
    push r19
    push r20

    ; Converter para decimal e imprimir
    mov r17, r16     ; Copiar número

    ; Extrair centenas (dividir por 100)
    ldi r18, 100
    clr r19          ; Contador de centenas
div_100:
    cp r17, r18
    brlo print_centenas
    sub r17, r18
    inc r19
    rjmp div_100

print_centenas:
    ; Imprimir centenas se > 0
    tst r19
    breq skip_centenas
    mov r16, r19
    subi r16, -48    ; Converter para ASCII
    call uart_transmit
    ldi r20, 1       ; Flag: imprimiu dígito
    rjmp extract_dezenas

skip_centenas:
    clr r20          ; Flag: não imprimiu ainda

extract_dezenas:
    ; Extrair dezenas (dividir por 10)
    ldi r18, 10
    clr r19          ; Contador de dezenas
div_10:
    cp r17, r18
    brlo print_dezenas
    sub r17, r18
    inc r19
    rjmp div_10

print_dezenas:
    ; Imprimir dezenas se > 0 ou se já imprimiu centenas
    tst r19
    brne print_dezenas_digit
    tst r20          ; Já imprimiu centenas?
    breq print_unidades

print_dezenas_digit:
    mov r16, r19
    subi r16, -48    ; Converter para ASCII
    call uart_transmit

print_unidades:
    ; Sempre imprimir unidades
    mov r16, r17
    subi r16, -48    ; Converter para ASCII
    call uart_transmit

    pop r20
    pop r19
    pop r18
    pop r17
    pop r16
    ret

; === FUNÇÃO: Imprimir nova linha ===
print_newline:
    push r16
    ldi r16, 13      ; CR
    call uart_transmit
    ldi r16, 10      ; LF
    call uart_transmit
    pop r16
    ret

; === FUNÇÃO: Imprimir espaço ===
print_space:
    push r16
    ldi r16, 32      ; Espaço
    call uart_transmit
    pop r16
    ret

; === FUNÇÃO: Programa Principal (gerado a partir do TAC) ===
programa_principal:
    push r16
    push r17
    push r18

    ldi r16, 2  ; t0 = 2
    ldi r17, 3  ; t1 = 3
    mov r18, r16  ; copiar operando1
    ; t2 = t0 ^ t1
    ; Verificar se expoente == 0
    tst r17
    brne pow_init_0
    ldi r18, 1  ; base^0 = 1
    rjmp pow_done_0
pow_init_0:
    mov r19, r17  ; contador = expoente
    dec r19  ; contador-- (ja temos base)
pow_loop_0:
    tst r19
    breq pow_done_0  ; se contador == 0, terminou
    mul r18, r16  ; resultado *= base
    mov r18, r0  ; pegar resultado de 8-bit
    dec r19  ; contador--
    rjmp pow_loop_0
pow_done_0:
    ; r18 contem base^expoente
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r18
    ; DEBUG: Imprimir A
    push r16
    mov r16, r18
    call print_number
    call print_newline
    pop r16
    ldi r19, 3  ; t3 = 3
    ldi r20, 2  ; t4 = 2
    mov r21, r19  ; copiar operando1
    ; t5 = t3 ^ t4
    ; Verificar se expoente == 0
    tst r20
    brne pow_init_1
    ldi r21, 1  ; base^0 = 1
    rjmp pow_done_1
pow_init_1:
    mov r22, r20  ; contador = expoente
    dec r22  ; contador-- (ja temos base)
pow_loop_1:
    tst r22
    breq pow_done_1  ; se contador == 0, terminou
    mul r21, r19  ; resultado *= base
    mov r21, r0  ; pegar resultado de 8-bit
    dec r22  ; contador--
    rjmp pow_loop_1
pow_done_1:
    ; r21 contem base^expoente
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r21
    ; DEBUG: Imprimir B
    push r16
    mov r16, r21
    call print_number
    call print_newline
    pop r16
    ldi r22, 5  ; t6 = 5
    ldi r23, 2  ; t7 = 2
    mov r24, r22  ; copiar operando1
    ; t8 = t6 ^ t7
    ; Verificar se expoente == 0
    tst r23
    brne pow_init_2
    ldi r24, 1  ; base^0 = 1
    rjmp pow_done_2
pow_init_2:
    mov r25, r23  ; contador = expoente
    dec r25  ; contador-- (ja temos base)
pow_loop_2:
    tst r25
    breq pow_done_2  ; se contador == 0, terminou
    mul r24, r22  ; resultado *= base
    mov r24, r0  ; pegar resultado de 8-bit
    dec r25  ; contador--
    rjmp pow_loop_2
pow_done_2:
    ; r24 contem base^expoente
    ; Salvar C na SRAM (0x0122)
    sts 0x0122, r24
    ; DEBUG: Imprimir C
    push r16
    mov r16, r24
    call print_number
    call print_newline
    pop r16
    ldi r25, 10  ; t9 = 10
    ldi r26, 0  ; t10 = 0
    mov r27, r25  ; copiar operando1
    ; t11 = t9 ^ t10
    ; Verificar se expoente == 0
    tst r26
    brne pow_init_3
    ldi r27, 1  ; base^0 = 1
    rjmp pow_done_3
pow_init_3:
    mov r28, r26  ; contador = expoente
    dec r28  ; contador-- (ja temos base)
pow_loop_3:
    tst r28
    breq pow_done_3  ; se contador == 0, terminou
    mul r27, r25  ; resultado *= base
    mov r27, r0  ; pegar resultado de 8-bit
    dec r28  ; contador--
    rjmp pow_loop_3
pow_done_3:
    ; r27 contem base^expoente
    ; Salvar D na SRAM (0x0123)
    sts 0x0123, r27
    ; DEBUG: Imprimir D
    push r16
    mov r16, r27
    call print_number
    call print_newline
    pop r16
    ldi r28, 2  ; t12 = 2
    ldi r29, 5  ; t13 = 5
    mov r30, r28  ; copiar operando1
    ; t14 = t12 ^ t13
    ; Verificar se expoente == 0
    tst r29
    brne pow_init_4
    ldi r30, 1  ; base^0 = 1
    rjmp pow_done_4
pow_init_4:
    mov r31, r29  ; contador = expoente
    dec r31  ; contador-- (ja temos base)
pow_loop_4:
    tst r31
    breq pow_done_4  ; se contador == 0, terminou
    mul r30, r28  ; resultado *= base
    mov r30, r0  ; pegar resultado de 8-bit
    dec r31  ; contador--
    rjmp pow_loop_4
pow_done_4:
    ; r30 contem base^expoente
    ; Salvar E na SRAM (0x0124)
    sts 0x0124, r30
    ; DEBUG: Imprimir E
    push r16
    mov r16, r30
    call print_number
    call print_newline
    pop r16

    pop r18
    pop r17
    pop r16
    ret

; === SEÇÃO DE DADOS (strings em .text) ===
.section .text

; Mensagens do sistema
msg_startup:
    .asciz "Compilador RPN - Arduino Uno\r\n"

.section .data

; Variáveis do programa (serão adicionadas nas próximas partes)

; === SEÇÃO BSS (não inicializada) ===
.section .bss

; Área para variáveis temporárias
temp_vars:
    .space 32  ; 32 bytes para temporários (t0-t31)

; Área para variáveis nomeadas
named_vars:
    .space 26  ; 26 bytes para variáveis A-Z
