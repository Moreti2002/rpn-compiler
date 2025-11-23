; Teste minimalista - apenas enviar "OK\r\n"
#include <avr/io.h>

.section .text
.global main

main:
    ; Stack
    ldi r16, 0xff
    out 0x3d, r16
    ldi r16, 0x08
    out 0x3e, r16

    ; UART: desabilitar
    ldi r16, 0x00
    sts 0xC1, r16
    
    ; Limpar flags
    sts 0xC0, r16
    
    ; Formato 8N1
    ldi r16, 0x06
    sts 0xC2, r16
    
    ; Baud 9600
    ldi r16, 103
    sts 0xC4, r16
    ldi r16, 0
    sts 0xC5, r16
    
    ; Habilitar TX
    ldi r16, 0x08
    sts 0xC1, r16
    
    ; Delay
    ldi r17, 255
delay1:
    dec r17
    brne delay1

    ; Enviar 'O'
    ldi r16, 'O'
    call send
    
    ; Enviar 'K'
    ldi r16, 'K'
    call send
    
    ; Enviar '\r'
    ldi r16, 13
    call send
    
    ; Enviar '\n'
    ldi r16, 10
    call send

end:
    rjmp end

send:
    push r17
wait:
    lds r17, 0xC0
    sbrs r17, 5
    rjmp wait
    sts 0xC6, r16
    pop r17
    ret
