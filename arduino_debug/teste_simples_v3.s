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

    ; Configurar baud rate (9600 @ 16MHz)
    ldi r16, 103
    ldi r17, 0
    sts 0xC4, r16    ; UBRR0L
    sts 0xC5, r17    ; UBRR0H

    ; Habilitar transmissão (TXEN0 = bit 3)
    ldi r16, 0x08
    sts 0xC1, r16    ; UCSR0B

    ; Configurar formato: 8 bits, 1 stop, sem paridade
    ldi r16, 0x06
    sts 0xC2, r16    ; UCSR0C

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
    sbrs r17, 5      ; Testar bit UDRE0
    rjmp uart_wait

    ; Enviar caractere
    sts 0xC6, r16    ; UDR0

    pop r17
    ret

; === FUNÇÃO: Enviar string via UART ===
; Entrada: Z aponta para string (terminada em 0)
uart_print_string:
    push r16
    push ZL
    push ZH

print_loop:
    ld r16, Z+
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

; === FUNÇÃO: Programa Principal (gerado a partir do TAC) ===
programa_principal:
    push r16
    push r17
    push r18

    ldi r16, 10  ; X = 10 (constante)
    ldi r17, 20  ; Y = 20 (constante)
    ldi r18, 30  ; RESULTADO = 30 (constante)

    pop r18
    pop r17
    pop r16
    ret

; === SEÇÃO DE DADOS ===
.section .data

; Mensagens do sistema
msg_startup:
    .asciz "Compilador RPN - Arduino Uno\r\n"

; Variáveis do programa (serão adicionadas nas próximas partes)

; === SEÇÃO BSS (não inicializada) ===
.section .bss

; Área para variáveis temporárias
temp_vars:
    .space 32  ; 32 bytes para temporários (t0-t31)

; Área para variáveis nomeadas
named_vars:
    .space 26  ; 26 bytes para variáveis A-Z
