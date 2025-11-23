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

    ; 2. Configurar UCSR0A - usar modo normal (sem U2X)
    ldi r16, 0x00
    sts 0xC0, r16    ; UCSR0A = 0 (limpar flags)

    ; 3. Configurar formato: 8N1 (UCSZ01:0 = 11)
    ldi r16, 0x06
    sts 0xC2, r16    ; UCSR0C = 0b00000110

    ; 4. Configurar baud rate: 9600 @ 16MHz
    ; UBRR = (F_CPU / (16 * BAUD)) - 1 = 103
    ldi r16, 103
    ldi r17, 0
    sts 0xC4, r16    ; UBRR0L = 103
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
    ; Aguardar buffer vazio (UDRE0 = bit 5 de UCSR0A)
    lds r17, 0xC0    ; Ler UCSR0A
    sbrs r17, 5      ; Pular se UDRE0 = 1 (pronto)
    rjmp uart_wait   ; Caso contrário, continuar esperando

    ; Enviar byte
    sts 0xC6, r16    ; UDR0 = caractere

    ; Aguardar transmissão completar (TXC0 = bit 6)
uart_tx_complete:
    lds r17, 0xC0    ; Ler UCSR0A
    sbrs r17, 6      ; Pular se TXC0 = 1 (completo)
    rjmp uart_tx_complete

    ; Limpar flag TXC0 escrevendo 1
    ldi r17, 0x40    ; Bit 6
    sts 0xC0, r17    ; Limpar TXC0

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
