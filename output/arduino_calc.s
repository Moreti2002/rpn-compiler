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

    ; 2. Configurar formato: 8N1 (UCSZ01:0 = 11)
    ldi r16, 0x06
    sts 0xC2, r16    ; UCSR0C = 0b00000110

    ; 3. Ativar U2X (double speed) - compatível com Arduino
    ldi r16, 0x02
    sts 0xC0, r16    ; UCSR0A = 0b00000010 (U2X0=1)

    ; 4. Configurar baud rate: 9600 @ 16MHz com U2X
    ; UBRR = (F_CPU / (8 * BAUD)) - 1 = 207
    ldi r16, 207
    ldi r17, 0
    sts 0xC4, r16    ; UBRR0L = 207
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
    ; Aguardar buffer vazio (UDRE0 = bit 5)
    lds r17, 0xC0    ; UCSR0A
    sbrs r17, 5      ; Pular se UDRE0 = 1
    rjmp uart_wait

    ; Enviar byte
    sts 0xC6, r16    ; UDR0

    pop r17
    ret

; === FUNÇÃO: Enviar string via UART ===
; Entrada: Z aponta para string em FLASH (terminada em 0)
uart_print_string:
    push r16
    push ZL
    push ZH

print_loop:
    lpm r16, Z+      ; Ler byte da Flash
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
    push r19
    push r20
    push r21
    push r22
    push r23

    ; Calcular valores
    ldi r16, 100  ; A = 100
    ldi r17, 25   ; B = 25
    ldi r18, 5    ; C = 5
    
    ; SOMA = A + B
    mov r19, r16
    add r19, r17  ; r19 = 125
    
    ; SUB = A - B
    mov r20, r16
    sub r20, r17  ; r20 = 75
    
    ; MULT = A * B (8-bit)
    mul r16, r17  ; resultado em r1:r0
    mov r21, r0   ; r21 = parte baixa (196)
    
    ; DIV = A / B
    mov r22, r16
    clr r23
div_loop:
    cp r22, r17
    brlo div_done
    sub r22, r17
    inc r23
    rjmp div_loop
div_done:
    mov r22, r23  ; r22 = 4
    
    ; POT = C ^ 3 (5 * 5 * 5)
    mov r23, r18
    mul r23, r18
    mov r23, r0   ; 25
    mul r23, r18
    mov r23, r0   ; r23 = 125
    
    ; Imprimir resultados
    ldi ZL, lo8(msg_a)
    ldi ZH, hi8(msg_a)
    call uart_print_string
    mov r24, r16
    call print_number
    
    ldi ZL, lo8(msg_b)
    ldi ZH, hi8(msg_b)
    call uart_print_string
    mov r24, r17
    call print_number
    
    ldi ZL, lo8(msg_c)
    ldi ZH, hi8(msg_c)
    call uart_print_string
    mov r24, r18
    call print_number
    
    ldi ZL, lo8(msg_soma)
    ldi ZH, hi8(msg_soma)
    call uart_print_string
    mov r24, r19
    call print_number
    
    ldi ZL, lo8(msg_sub)
    ldi ZH, hi8(msg_sub)
    call uart_print_string
    mov r24, r20
    call print_number
    
    ldi ZL, lo8(msg_mult)
    ldi ZH, hi8(msg_mult)
    call uart_print_string
    mov r24, r21
    call print_number
    
    ldi ZL, lo8(msg_div)
    ldi ZH, hi8(msg_div)
    call uart_print_string
    mov r24, r22
    call print_number
    
    ldi ZL, lo8(msg_pot)
    ldi ZH, hi8(msg_pot)
    call uart_print_string
    mov r24, r23
    call print_number

    pop r23
    pop r22
    pop r21
    pop r20
    pop r19
    pop r18
    pop r17
    pop r16
    ret

; === FUNÇÃO: Imprimir número (0-255) ===
; Entrada: r24 = número a imprimir
print_number:
    push r16
    push r17
    push r18
    push r19
    push r20
    
    mov r20, r24  ; Salvar número original
    
    ; Extrair centenas
    ldi r17, 100
    clr r18
centenas_loop:
    cp r20, r17
    brlo centenas_done
    sub r20, r17
    inc r18
    rjmp centenas_loop
centenas_done:
    
    ; Imprimir centenas (se > 0)
    tst r18
    breq dezenas_start
    mov r16, r18
    subi r16, -48  ; Converter para ASCII
    call uart_transmit
    
dezenas_start:
    ; Extrair dezenas
    ldi r17, 10
    clr r19
dezenas_loop:
    cp r20, r17
    brlo dezenas_done
    sub r20, r17
    inc r19
    rjmp dezenas_loop
dezenas_done:
    
    ; Imprimir dezenas (se centenas > 0 OU dezenas > 0)
    tst r18
    brne print_dezenas
    tst r19
    breq unidades_start
print_dezenas:
    mov r16, r19
    subi r16, -48
    call uart_transmit
    
unidades_start:
    ; Imprimir unidades (sempre)
    mov r16, r20
    subi r16, -48
    call uart_transmit
    
    ; Imprimir nova linha
    ldi r16, '\r'
    call uart_transmit
    ldi r16, '\n'
    call uart_transmit
    
    pop r20
    pop r19
    pop r18
    pop r17
    pop r16
    ret

; === STRINGS (na mesma seção .text) ===
msg_startup:
    .asciz "Compilador RPN - Arduino Uno\r\n"

msg_a:
    .asciz "A = "
msg_b:
    .asciz "B = "
msg_c:
    .asciz "C = "
msg_soma:
    .asciz "SOMA = "
msg_sub:
    .asciz "SUB = "
msg_mult:
    .asciz "MULT = "
msg_div:
    .asciz "DIV = "
msg_pot:
    .asciz "POT = "

.section .data

; Variáveis do programa (serão adicionadas nas próximas partes)

; === SEÇÃO BSS (não inicializada) ===
.section .bss

; Área para variáveis temporárias
temp_vars:
    .space 32  ; 32 bytes para temporários (t0-t31)

; Área para variáveis nomeadas
named_vars:
    .space 26  ; 26 bytes para variáveis A-Z
