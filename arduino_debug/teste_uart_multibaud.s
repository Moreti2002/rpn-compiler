; ===========================================================================
; Teste UART com múltiplos baud rates
; Tente receber em 9600, 19200, 38400, 57600 e 115200
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

    ; Testar com 115200 baud (UBRR = 8)
    ldi r16, 8
    ldi r17, 0
    call setup_uart_with_rate
    call send_test_message
    call delay_1s
    
    ; Testar com 57600 baud (UBRR = 16)
    ldi r16, 16
    ldi r17, 0
    call setup_uart_with_rate
    call send_test_message
    call delay_1s
    
    ; Testar com 38400 baud (UBRR = 25)
    ldi r16, 25
    ldi r17, 0
    call setup_uart_with_rate
    call send_test_message
    call delay_1s
    
    ; Testar com 19200 baud (UBRR = 51)
    ldi r16, 51
    ldi r17, 0
    call setup_uart_with_rate
    call send_test_message
    call delay_1s
    
    ; Testar com 9600 baud (UBRR = 103)
    ldi r16, 103
    ldi r17, 0
    call setup_uart_with_rate
    call send_test_message

    ; Loop infinito
loop_end:
    rjmp loop_end

; === FUNÇÃO: Setup UART com baud rate específico ===
; r16 = UBRR low, r17 = UBRR high
setup_uart_with_rate:
    push r18
    
    ; Desabilitar UART
    ldi r18, 0x00
    sts 0xC1, r18    ; UCSR0B = 0
    
    ; Configurar baud rate
    sts 0xC4, r16    ; UBRR0L
    sts 0xC5, r17    ; UBRR0H
    
    ; Configurar formato: 8N1
    ldi r18, 0x06
    sts 0xC2, r18    ; UCSR0C
    
    ; Habilitar transmissão
    ldi r18, 0x08
    sts 0xC1, r18    ; UCSR0B
    
    ; Delay estabilização
    call delay_10ms
    
    pop r18
    ret

; === FUNÇÃO: Enviar mensagem de teste ===
send_test_message:
    push r16
    
    ; Enviar "TEST\r\n"
    ldi r16, 'T'
    call uart_send_fast
    ldi r16, 'E'
    call uart_send_fast
    ldi r16, 'S'
    call uart_send_fast
    ldi r16, 'T'
    call uart_send_fast
    ldi r16, 0x0D
    call uart_send_fast
    ldi r16, 0x0A
    call uart_send_fast
    
    pop r16
    ret

; === FUNÇÃO: Enviar byte via UART (versão rápida) ===
uart_send_fast:
    push r17
    
wait_ready_fast:
    lds r17, 0xC0    ; UCSR0A
    sbrs r17, 5      ; UDRE0
    rjmp wait_ready_fast
    
    sts 0xC6, r16    ; UDR0
    
    pop r17
    ret

; === Delays ===
delay_10ms:
    push r16
    push r17
    ldi r17, 80
d10_outer:
    ldi r16, 200
d10_inner:
    dec r16
    brne d10_inner
    dec r17
    brne d10_outer
    pop r17
    pop r16
    ret

delay_1s:
    push r18
    ldi r18, 10
d1s_loop:
    call delay_100ms
    dec r18
    brne d1s_loop
    pop r18
    ret

delay_100ms:
    push r16
    push r17
    push r18
    ldi r18, 10
d100_outer:
    ldi r17, 200
d100_middle:
    ldi r16, 200
d100_inner:
    dec r16
    brne d100_inner
    dec r17
    brne d100_middle
    dec r18
    brne d100_outer
    pop r18
    pop r17
    pop r16
    ret
