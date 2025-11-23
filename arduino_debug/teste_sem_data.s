; Teste idêntico ao gerador mas sem string na .data
#include <avr/io.h>

.section .text
.global main

main:
    clr r0
    
    ; Stack
    ldi r16, 0xff
    out 0x3d, r16
    ldi r16, 0x08
    out 0x3e, r16

    call setup_uart
    call print_msg
    call prog_principal

loop_forever:
    rjmp loop_forever

setup_uart:
    push r16
    push r17

    ldi r16, 0x00
    sts 0xC1, r16
    
    ldi r16, 0x06
    sts 0xC2, r16
    
    ldi r16, 0x02
    sts 0xC0, r16
    
    ldi r16, 207
    ldi r17, 0
    sts 0xC4, r16
    sts 0xC5, r17
    
    ldi r16, 0x08
    sts 0xC1, r16
    
    ldi r17, 255
dly:
    dec r17
    brne dly

    pop r17
    pop r16
    ret

uart_tx:
    push r17
wait:
    lds r17, 0xC0
    sbrs r17, 5
    rjmp wait
    sts 0xC6, r16
    pop r17
    ret

print_msg:
    push r16
    
    ; Enviar caracteres direto (sem .data)
    ldi r16, 'T'
    call uart_tx
    ldi r16, 'E'
    call uart_tx
    ldi r16, 'S'
    call uart_tx
    ldi r16, 'T'
    call uart_tx
    ldi r16, 13
    call uart_tx
    ldi r16, 10
    call uart_tx
    
    pop r16
    ret

prog_principal:
    push r16
    push r17
    push r18
    
    ldi r16, 10
    ldi r17, 20
    ldi r18, 30
    
    pop r18
    pop r17
    pop r16
    ret
