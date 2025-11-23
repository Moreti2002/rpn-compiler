; Teste com .data mas enviando caractere por caractere
#include <avr/io.h>

.section .text
.global main

main:
    clr r0
    ldi r16, 0xff
    out 0x3d, r16
    ldi r16, 0x08
    out 0x3e, r16

    call setup_uart
    
    ; Enviar "OK" hard-coded
    ldi r16, 'O'
    call uart_tx
    ldi r16, 'K'
    call uart_tx
    ldi r16, 13
    call uart_tx
    ldi r16, 10
    call uart_tx

fim:
    rjmp fim

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
d:
    dec r17
    brne d
    pop r17
    pop r16
    ret

uart_tx:
    push r17
w:
    lds r17, 0xC0
    sbrs r17, 5
    rjmp w
    sts 0xC6, r16
    pop r17
    ret

.section .data
msg:
    .asciz "Teste data\r\n"
