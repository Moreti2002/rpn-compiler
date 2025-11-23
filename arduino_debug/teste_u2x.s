; Teste de baud rate - envia 'U' (0x55 = 01010101) repetidamente
; Use um osciloscópio ou logic analyzer no pino TX para medir
; Ou teste diferentes baud rates no monitor serial

#include <avr/io.h>

.section .text
.global main

main:
    ; Stack
    ldi r16, 0xff
    out 0x3d, r16
    ldi r16, 0x08
    out 0x3e, r16

    ; === TESTE 1: BAUD 9600 (UBRR = 103) ===
    ; Desabilitar
    ldi r16, 0x00
    sts 0xC1, r16
    
    ; Limpar
    sts 0xC0, r16
    
    ; Formato 8N1
    ldi r16, 0x06
    sts 0xC2, r16
    
    ; Baud rate - TENTAR COM U2X ATIVADO
    ; Com U2X=1: UBRR = (F_CPU / (8 * BAUD)) - 1
    ; Para 9600 @ 16MHz com U2X: UBRR = 207
    ldi r16, 0x02    ; Ativar U2X0 (bit 1)
    sts 0xC0, r16
    
    ldi r16, 207     ; UBRR para 9600 com U2X
    sts 0xC4, r16
    ldi r16, 0
    sts 0xC5, r16
    
    ; Habilitar TX
    ldi r16, 0x08
    sts 0xC1, r16
    
    ; Delay estabilização
    ldi r18, 255
dly:
    dec r18
    brne dly

    ; Enviar mensagem
    ldi r16, 'T'
    call tx
    ldi r16, 'E'
    call tx
    ldi r16, 'S'
    call tx
    ldi r16, 'T'
    call tx
    ldi r16, ' '
    call tx
    ldi r16, 'U'
    call tx
    ldi r16, '2'
    call tx
    ldi r16, 'X'
    call tx
    ldi r16, 13
    call tx
    ldi r16, 10
    call tx

fim:
    rjmp fim

tx:
    push r17
wait:
    lds r17, 0xC0
    sbrs r17, 5
    rjmp wait
    sts 0xC6, r16
    pop r17
    ret
