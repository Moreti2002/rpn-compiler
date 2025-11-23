; ===========================================================================
; Teste UART com configuração robusta
; ===========================================================================

#include <avr/io.h>

.equ STACK_LOW, 0xff
.equ STACK_HIGH, 0x08
.equ SPL_ADDR, 0x3d
.equ SPH_ADDR, 0x3e

.section .text
.global main

main:
    ; Configurar Stack Pointer
    ldi r16, STACK_LOW
    out SPL_ADDR, r16
    ldi r16, STACK_HIGH
    out SPH_ADDR, r16

    ; Configurar UART com reset completo
    call setup_uart_robust

    ; Delay para estabilização
    call delay_100ms

    ; Enviar caractere 'U' (0x55 = 01010101 - padrão para testar baud rate)
    ldi r16, 0x55
    call uart_send
    
    ; Enviar 'A'
    ldi r16, 0x41
    call uart_send
    
    ; Enviar '\r'
    ldi r16, 0x0D
    call uart_send
    
    ; Enviar '\n'
    ldi r16, 0x0A
    call uart_send

    ; Loop infinito
loop_end:
    rjmp loop_end

; === FUNÇÃO: Setup UART Robusto ===
setup_uart_robust:
    push r16
    push r17

    ; 1. DESABILITAR completamente o UART primeiro
    ldi r16, 0x00
    sts 0xC1, r16    ; UCSR0B = 0 (desliga tudo)
    
    ; 2. Limpar flag de erro
    ldi r16, 0x00
    sts 0xC0, r16    ; UCSR0A = 0
    
    ; 3. Configurar baud rate para 9600 @ 16MHz
    ; UBRR = (F_CPU / (16 * BAUD)) - 1 = (16000000 / (16 * 9600)) - 1 = 103.1666 ≈ 103
    ldi r16, 103
    ldi r17, 0
    sts 0xC4, r16    ; UBRR0L
    sts 0xC5, r17    ; UBRR0H
    
    ; 4. Configurar formato: 8N1 (8 bits, no parity, 1 stop bit)
    ; UCSZ01 = 1, UCSZ00 = 1 (bits 2 e 1)
    ldi r16, 0x06    ; 0b00000110
    sts 0xC2, r16    ; UCSR0C
    
    ; 5. HABILITAR apenas transmissão (TXEN0 = bit 3)
    ldi r16, 0x08    ; 0b00001000
    sts 0xC1, r16    ; UCSR0B

    pop r17
    pop r16
    ret

; === FUNÇÃO: Enviar byte via UART ===
; r16 = byte a enviar
uart_send:
    push r17
    
wait_ready:
    ; Esperar UDRE0 (Data Register Empty) = bit 5 de UCSR0A
    lds r17, 0xC0    ; UCSR0A
    sbrs r17, 5      ; Pular se bit 5 está setado
    rjmp wait_ready
    
    ; Enviar byte
    sts 0xC6, r16    ; UDR0
    
    ; Pequeno delay entre caracteres
    push r18
    ldi r18, 50
delay_char:
    dec r18
    brne delay_char
    pop r18
    
    pop r17
    ret

; === Delay ~100ms @ 16MHz ===
delay_100ms:
    push r16
    push r17
    push r18

    ldi r18, 10      ; Loop externo

delay_100_outer:
    ldi r17, 200     ; Loop médio

delay_100_middle:
    ldi r16, 200     ; Loop interno

delay_100_inner:
    dec r16
    brne delay_100_inner

    dec r17
    brne delay_100_middle

    dec r18
    brne delay_100_outer

    pop r18
    pop r17
    pop r16
    ret
