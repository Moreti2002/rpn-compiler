; ===========================================================================
; Teste simples: Piscar LED do Arduino (pin 13 = PB5)
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

    ; Configurar PB5 (pin 13) como saída
    ; DDRB = 0x24 (endereço)
    ldi r16, 0x20    ; bit 5 = 0x20
    out 0x04, r16    ; DDRB

loop:
    ; Ligar LED (PORTB |= 0x20)
    sbi 0x05, 5      ; PORTB, bit 5

    ; Delay ~0.5s
    call delay_500ms

    ; Desligar LED (PORTB &= ~0x20)
    cbi 0x05, 5      ; PORTB, bit 5

    ; Delay ~0.5s
    call delay_500ms

    rjmp loop

; === Delay aproximado 500ms @ 16MHz ===
delay_500ms:
    push r16
    push r17
    push r18

    ldi r18, 20      ; Loop externo

delay_outer:
    ldi r17, 250     ; Loop médio

delay_middle:
    ldi r16, 200     ; Loop interno

delay_inner:
    dec r16
    brne delay_inner

    dec r17
    brne delay_middle

    dec r18
    brne delay_outer

    pop r18
    pop r17
    pop r16
    ret
