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

; === FUNÇÃO: Imprimir número decimal (0-255) ===
; Entrada: r16 = número a imprimir
print_number:
    push r16
    push r17
    push r18
    push r19
    push r20

    ; Converter para decimal e imprimir
    mov r17, r16     ; Copiar número

    ; Extrair centenas (dividir por 100)
    ldi r18, 100
    clr r19          ; Contador de centenas
div_100:
    cp r17, r18
    brlo print_centenas
    sub r17, r18
    inc r19
    rjmp div_100

print_centenas:
    ; Imprimir centenas se > 0
    tst r19
    breq skip_centenas
    mov r16, r19
    subi r16, -48    ; Converter para ASCII
    call uart_transmit
    ldi r20, 1       ; Flag: imprimiu dígito
    rjmp extract_dezenas

skip_centenas:
    clr r20          ; Flag: não imprimiu ainda

extract_dezenas:
    ; Extrair dezenas (dividir por 10)
    ldi r18, 10
    clr r19          ; Contador de dezenas
div_10:
    cp r17, r18
    brlo print_dezenas
    sub r17, r18
    inc r19
    rjmp div_10

print_dezenas:
    ; Imprimir dezenas se > 0 ou se já imprimiu centenas
    tst r19
    brne print_dezenas_digit
    tst r20          ; Já imprimiu centenas?
    breq print_unidades

print_dezenas_digit:
    mov r16, r19
    subi r16, -48    ; Converter para ASCII
    call uart_transmit

print_unidades:
    ; Sempre imprimir unidades
    mov r16, r17
    subi r16, -48    ; Converter para ASCII
    call uart_transmit

    pop r20
    pop r19
    pop r18
    pop r17
    pop r16
    ret

; === FUNÇÃO: Imprimir nova linha ===
print_newline:
    push r16
    ldi r16, 13      ; CR
    call uart_transmit
    ldi r16, 10      ; LF
    call uart_transmit
    pop r16
    ret

; === FUNÇÃO: Imprimir espaço ===
print_space:
    push r16
    ldi r16, 32      ; Espaço
    call uart_transmit
    pop r16
    ret

; === FUNÇÃO: Programa Principal (gerado a partir do TAC) ===
programa_principal:
    push r16
    push r17
    push r18

    ldi r16, 0  ; FIB = 0
    ldi r16, 1  ; FIB = 1
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 1  ; N = 1 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L0:
    ; ifFalse 1 goto L1 - sempre verdadeiro, não pula
    rjmp L0
L1:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 2  ; N = 2 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L2:
    ; ifFalse 1 goto L3 - sempre verdadeiro, não pula
    rjmp L2
L3:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 3  ; N = 3 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L4:
    ; ifFalse 1 goto L5 - sempre verdadeiro, não pula
    rjmp L4
L5:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 4  ; N = 4 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L6:
    ; ifFalse 1 goto L7 - sempre verdadeiro, não pula
    rjmp L6
L7:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 5  ; N = 5 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L8:
    ; ifFalse 1 goto L9 - sempre verdadeiro, não pula
    rjmp L8
L9:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 6  ; N = 6 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L10:
    ; ifFalse 1 goto L11 - sempre verdadeiro, não pula
    rjmp L10
L11:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 7  ; N = 7 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L12:
    ; ifFalse 1 goto L13 - sempre verdadeiro, não pula
    rjmp L12
L13:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 8  ; N = 8 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L14:
    ; ifFalse 1 goto L15 - sempre verdadeiro, não pula
    rjmp L14
L15:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 9  ; N = 9 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L16:
    ; ifFalse 1 goto L17 - sempre verdadeiro, não pula
    rjmp L16
L17:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 10  ; N = 10 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L18:
    ; ifFalse 1 goto L19 - sempre verdadeiro, não pula
    rjmp L18
L19:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 11  ; N = 11 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L20:
    ; ifFalse 1 goto L21 - sempre verdadeiro, não pula
    rjmp L20
L21:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 12  ; N = 12 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L22:
    ; ifFalse 1 goto L23 - sempre verdadeiro, não pula
    rjmp L22
L23:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 13  ; N = 13 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L24:
    ; ifFalse 1 goto L25 - sempre verdadeiro, não pula
    rjmp L24
L25:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 14  ; N = 14 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L26:
    ; ifFalse 1 goto L27 - sempre verdadeiro, não pula
    rjmp L26
L27:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 15  ; N = 15 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L28:
    ; ifFalse 1 goto L29 - sempre verdadeiro, não pula
    rjmp L28
L29:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 16  ; N = 16 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L30:
    ; ifFalse 1 goto L31 - sempre verdadeiro, não pula
    rjmp L30
L31:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 17  ; N = 17 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L32:
    ; ifFalse 1 goto L33 - sempre verdadeiro, não pula
    rjmp L32
L33:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 18  ; N = 18 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L34:
    ; ifFalse 1 goto L35 - sempre verdadeiro, não pula
    rjmp L34
L35:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 19  ; N = 19 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L36:
    ; ifFalse 1 goto L37 - sempre verdadeiro, não pula
    rjmp L36
L37:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 20  ; N = 20 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L38:
    ; ifFalse 1 goto L39 - sempre verdadeiro, não pula
    rjmp L38
L39:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 21  ; N = 21 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L40:
    ; ifFalse 1 goto L41 - sempre verdadeiro, não pula
    rjmp L40
L41:
    ldi r17, 0  ; A = 0 (constante)
    ; Salvar A na SRAM (0x0120)
    sts 0x0120, r17
    ldi r17, 1  ; B = 1 (constante)
    ; Salvar B na SRAM (0x0121)
    sts 0x0121, r17
    ldi r17, 22  ; N = 22 (constante)
    ; Salvar N na SRAM (0x012D)
    sts 0x012D, r17
L42:
    ; ifFalse 1 goto L43 - sempre verdadeiro, não pula
    rjmp L42
L43:

    pop r18
    pop r17
    pop r16
    ret

; === SEÇÃO DE DADOS (strings em .text) ===
.section .text

; Mensagens do sistema
msg_startup:
    .asciz "Compilador RPN - Arduino Uno\r\n"

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
