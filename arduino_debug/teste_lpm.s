; Teste lpm com string em Flash
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
    
    ; Carregar endereço da string
    ldi ZL, lo8(msg)
    ldi ZH, hi8(msg)
    call print_string

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

print_string:
    push r16
    push ZL
    push ZH
loop:
    lpm r16, Z+
    tst r16
    breq done
    call uart_tx
    rjmp loop
done:
    pop ZH
    pop ZL
    pop r16
    ret

.section .data
msg:
    .asciz "LPM TEST\r\n"
