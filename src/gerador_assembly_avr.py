#!/usr/bin/env python3
"""
Gerador de Assembly AVR (ATmega328P - Arduino Uno)
==================================================

Converte código TAC otimizado para Assembly AVR.
Implementação modular seguindo o plano incremental.

Parte 9: Prólogo e Epílogo
- Template básico de Assembly AVR
- Configuração inicial (stack, UART)
- Loop principal
- Geração de arquivo .s compilável

Usage:
    from src.gerador_assembly_avr import GeradorAssemblyAVR
    
    gerador = GeradorAssemblyAVR()
    assembly = gerador.gerar(instrucoes_tac)
    gerador.salvar('output/programa.s')
"""

import sys
import os
from typing import List, Dict, Optional
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.otimizador_tac import InstrucaoTAC


class GeradorAssemblyAVR:
    """
    Gerador de código Assembly AVR para ATmega328P (Arduino Uno)
    
    Características:
    - Prólogo: Configuração de stack e UART
    - Epílogo: Loop infinito
    - Seções: .text, .data, .bss
    - UART para debug via serial
    """
    
    # Constantes do ATmega328P
    RAMEND = 0x08FF           # Final da RAM
    STACK_LOW = 0xFF          # SPL inicial
    STACK_HIGH = 0x08         # SPH inicial
    
    # Endereços dos registradores
    SPL_ADDR = 0x3D           # Stack Pointer Low
    SPH_ADDR = 0x3E           # Stack Pointer High
    
    # UART (USART0)
    UCSR0A_ADDR = 0xC0        # Control and Status Register A
    UCSR0B_ADDR = 0xC1        # Control and Status Register B
    UCSR0C_ADDR = 0xC2        # Control and Status Register C
    UBRR0L_ADDR = 0xC4        # Baud Rate Register Low
    UBRR0H_ADDR = 0xC5        # Baud Rate Register High
    UDR0_ADDR = 0xC6          # Data Register
    
    # Bits UART
    UDRE0_BIT = 5             # Data Register Empty
    TXEN0_BIT = 3             # Transmitter Enable
    RXEN0_BIT = 4             # Receiver Enable
    
    # Configurações UART
    BAUD_9600 = 103           # UBRR para 9600 baud @ 16MHz
    BAUD_115200 = 8           # UBRR para 115200 baud @ 16MHz
    FORMAT_8N1 = 0x06         # 8 bits, sem paridade, 1 stop bit
    
    def __init__(self, baud_rate: int = 9600):
        """
        Inicializa o gerador de Assembly
        
        Args:
            baud_rate: Taxa de transmissão UART (9600 ou 115200)
        """
        self.baud_rate = baud_rate
        self.baud_value = self.BAUD_9600 if baud_rate == 9600 else self.BAUD_115200
        
        # Código assembly gerado
        self.codigo: List[str] = []
        
        # Seções
        self.secao_data: List[str] = []
        self.secao_bss: List[str] = []
        self.secao_text: List[str] = []
        
        # Estatísticas
        self.num_variaveis = 0
        self.num_temporarios = 0
        self.num_labels = 0
    
    def gerar_prologo(self):
        """
        Gera o prólogo do programa Assembly
        
        Inclui:
        - Diretivas e includes
        - Configuração do stack pointer
        - Configuração UART
        - Inicialização de registradores
        """
        prologo = []
        
        # Header e includes
        prologo.append("; ===========================================================================")
        prologo.append("; Programa gerado pelo Compilador RPN para Arduino Uno (ATmega328P)")
        prologo.append("; ===========================================================================")
        prologo.append("")
        prologo.append("#include <avr/io.h>")
        prologo.append("")
        
        # Constantes
        prologo.append("; === CONSTANTES ===")
        prologo.append(f".equ STACK_LOW, {self.STACK_LOW:#04x}")
        prologo.append(f".equ STACK_HIGH, {self.STACK_HIGH:#04x}")
        prologo.append(f".equ SPL_ADDR, {self.SPL_ADDR:#04x}")
        prologo.append(f".equ SPH_ADDR, {self.SPH_ADDR:#04x}")
        prologo.append("")
        
        # Constantes UART
        prologo.append("; === UART CONSTANTES ===")
        prologo.append(f".equ UCSR0A_ADDR, {self.UCSR0A_ADDR:#04x}")
        prologo.append(f".equ UCSR0B_ADDR, {self.UCSR0B_ADDR:#04x}")
        prologo.append(f".equ UCSR0C_ADDR, {self.UCSR0C_ADDR:#04x}")
        prologo.append(f".equ UBRR0L_ADDR, {self.UBRR0L_ADDR:#04x}")
        prologo.append(f".equ UBRR0H_ADDR, {self.UBRR0H_ADDR:#04x}")
        prologo.append(f".equ UDR0_ADDR, {self.UDR0_ADDR:#04x}")
        prologo.append(f".equ UDRE0_BIT, {self.UDRE0_BIT}")
        prologo.append(f".equ BAUD_RATE, {self.baud_value}  ; {self.baud_rate} baud @ 16MHz")
        prologo.append("")
        
        # Seção .text - código
        prologo.append("; === CÓDIGO PRINCIPAL ===")
        prologo.append(".section .text")
        prologo.append(".global main")
        prologo.append("")
        prologo.append("main:")
        
        # Setup inicial
        prologo.append("    ; Configurar registrador zero (usado em operações adc)")
        prologo.append("    clr r0")
        prologo.append("")
        
        # Configurar stack
        prologo.append("    ; Configurar Stack Pointer")
        prologo.append("    ldi r16, STACK_LOW")
        prologo.append("    out SPL_ADDR, r16")
        prologo.append("    ldi r16, STACK_HIGH")
        prologo.append("    out SPH_ADDR, r16")
        prologo.append("")
        
        # Configurar UART
        prologo.append("    ; Configurar UART")
        prologo.append("    call setup_uart")
        prologo.append("")
        
        # Mensagem de inicialização
        prologo.append("    ; Enviar mensagem de inicialização")
        prologo.append("    call print_startup_message")
        prologo.append("")
        
        # Chamar programa principal
        prologo.append("    ; Executar programa principal")
        prologo.append("    call programa_principal")
        prologo.append("")
        
        return prologo
    
    def gerar_epilogo(self):
        """
        Gera o epílogo do programa Assembly
        
        Inclui:
        - Loop infinito principal
        - Funções auxiliares (UART, etc.)
        """
        epilogo = []
        
        # Loop infinito
        epilogo.append("; === LOOP INFINITO ===")
        epilogo.append("loop_forever:")
        epilogo.append("    rjmp loop_forever")
        epilogo.append("")
        
        # Função setup UART
        epilogo.append("; === FUNÇÃO: Configurar UART ===")
        epilogo.append("setup_uart:")
        epilogo.append("    push r16")
        epilogo.append("")
        epilogo.append("    ; Configurar baud rate")
        epilogo.append("    ldi r16, BAUD_RATE")
        epilogo.append("    sts UBRR0L_ADDR, r16")
        epilogo.append("    ldi r16, 0")
        epilogo.append("    sts UBRR0H_ADDR, r16")
        epilogo.append("")
        epilogo.append("    ; Habilitar transmissão")
        epilogo.append("    ldi r16, (1 << 3)  ; TXEN0")
        epilogo.append("    sts UCSR0B_ADDR, r16")
        epilogo.append("")
        epilogo.append("    ; Configurar formato: 8N1")
        epilogo.append("    ldi r16, (1 << 2) | (1 << 1)")
        epilogo.append("    sts UCSR0C_ADDR, r16")
        epilogo.append("")
        epilogo.append("    pop r16")
        epilogo.append("    ret")
        epilogo.append("")
        
        # Função enviar caractere UART
        epilogo.append("; === FUNÇÃO: Enviar caractere via UART ===")
        epilogo.append("; Entrada: r16 = caractere a enviar")
        epilogo.append("uart_transmit:")
        epilogo.append("    push r17")
        epilogo.append("")
        epilogo.append("uart_wait:")
        epilogo.append("    ; Aguardar buffer vazio")
        epilogo.append("    lds r17, UCSR0A_ADDR")
        epilogo.append("    sbrs r17, UDRE0_BIT")
        epilogo.append("    rjmp uart_wait")
        epilogo.append("")
        epilogo.append("    ; Enviar caractere")
        epilogo.append("    sts UDR0_ADDR, r16")
        epilogo.append("")
        epilogo.append("    pop r17")
        epilogo.append("    ret")
        epilogo.append("")
        
        # Função enviar string
        epilogo.append("; === FUNÇÃO: Enviar string via UART ===")
        epilogo.append("; Entrada: Z aponta para string (terminada em 0)")
        epilogo.append("uart_print_string:")
        epilogo.append("    push r16")
        epilogo.append("    push ZL")
        epilogo.append("    push ZH")
        epilogo.append("")
        epilogo.append("print_loop:")
        epilogo.append("    ld r16, Z+")
        epilogo.append("    tst r16")
        epilogo.append("    breq print_done")
        epilogo.append("    call uart_transmit")
        epilogo.append("    rjmp print_loop")
        epilogo.append("")
        epilogo.append("print_done:")
        epilogo.append("    pop ZH")
        epilogo.append("    pop ZL")
        epilogo.append("    pop r16")
        epilogo.append("    ret")
        epilogo.append("")
        
        # Mensagem de startup
        epilogo.append("; === FUNÇÃO: Imprimir mensagem de inicialização ===")
        epilogo.append("print_startup_message:")
        epilogo.append("    push ZL")
        epilogo.append("    push ZH")
        epilogo.append("")
        epilogo.append("    ldi ZL, lo8(msg_startup)")
        epilogo.append("    ldi ZH, hi8(msg_startup)")
        epilogo.append("    call uart_print_string")
        epilogo.append("")
        epilogo.append("    pop ZH")
        epilogo.append("    pop ZL")
        epilogo.append("    ret")
        epilogo.append("")
        
        # Placeholder para programa principal
        epilogo.append("; === FUNÇÃO: Programa Principal (gerado a partir do TAC) ===")
        epilogo.append("programa_principal:")
        epilogo.append("    ; TODO: Código gerado a partir das instruções TAC")
        epilogo.append("    ; (será implementado nas Partes 10-12)")
        epilogo.append("    ret")
        epilogo.append("")
        
        return epilogo
    
    def gerar_secao_data(self):
        """
        Gera a seção .data (dados inicializados)
        """
        data = []
        
        data.append("; === SEÇÃO DE DADOS ===")
        data.append(".section .data")
        data.append("")
        
        # Mensagens
        data.append("; Mensagens do sistema")
        data.append('msg_startup:')
        data.append('    .asciz "Compilador RPN - Arduino Uno\\r\\n"')
        data.append("")
        
        # Dados adicionais serão adicionados nas próximas partes
        data.append("; Variáveis do programa (serão adicionadas nas próximas partes)")
        data.append("")
        
        return data
    
    def gerar_secao_bss(self):
        """
        Gera a seção .bss (dados não inicializados)
        """
        bss = []
        
        bss.append("; === SEÇÃO BSS (não inicializada) ===")
        bss.append(".section .bss")
        bss.append("")
        
        # Reservar espaço para variáveis
        bss.append("; Área para variáveis temporárias")
        bss.append("temp_vars:")
        bss.append("    .space 32  ; 32 bytes para temporários (t0-t31)")
        bss.append("")
        
        bss.append("; Área para variáveis nomeadas")
        bss.append("named_vars:")
        bss.append("    .space 26  ; 26 bytes para variáveis A-Z")
        bss.append("")
        
        return bss
    
    def gerar(self, instrucoes_tac: Optional[List[InstrucaoTAC]] = None) -> str:
        """
        Gera o código Assembly completo
        
        Args:
            instrucoes_tac: Lista de instruções TAC (opcional para Parte 9)
            
        Returns:
            String com código Assembly completo
        """
        # Limpar código anterior
        self.codigo = []
        
        # Gerar prólogo
        self.codigo.extend(self.gerar_prologo())
        
        # Gerar epílogo
        self.codigo.extend(self.gerar_epilogo())
        
        # Gerar seção de dados
        self.codigo.extend(self.gerar_secao_data())
        
        # Gerar seção BSS
        self.codigo.extend(self.gerar_secao_bss())
        
        # Retornar código completo
        return '\n'.join(self.codigo)
    
    def salvar(self, caminho: str):
        """
        Salva o código Assembly em arquivo
        
        Args:
            caminho: Caminho do arquivo de saída (.s)
        """
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.codigo))
    
    def obter_estatisticas(self) -> Dict:
        """
        Retorna estatísticas da geração
        
        Returns:
            Dicionário com estatísticas
        """
        return {
            'linhas_codigo': len(self.codigo),
            'baud_rate': self.baud_rate,
            'variaveis': self.num_variaveis,
            'temporarios': self.num_temporarios,
            'labels': self.num_labels
        }


def main():
    """Função de teste - Parte 9"""
    print("=" * 80)
    print("GERADOR DE ASSEMBLY AVR - PARTE 9: PRÓLOGO E EPÍLOGO")
    print("=" * 80)
    print()
    
    # Criar gerador
    gerador = GeradorAssemblyAVR(baud_rate=9600)
    
    # Gerar código
    print("Gerando código Assembly...")
    assembly = gerador.gerar()
    
    # Salvar em arquivo
    output_path = "output/programa_parte9.s"
    gerador.salvar(output_path)
    
    # Estatísticas
    stats = gerador.obter_estatisticas()
    print(f"✓ Código Assembly gerado: {stats['linhas_codigo']} linhas")
    print(f"✓ Arquivo salvo: {output_path}")
    print(f"✓ Baud rate: {stats['baud_rate']}")
    print()
    
    # Mostrar primeiras linhas
    print("Primeiras 30 linhas do código gerado:")
    print("-" * 80)
    linhas = assembly.split('\n')
    for i, linha in enumerate(linhas[:30], 1):
        print(f"{i:3d} | {linha}")
    print("-" * 80)
    print()
    
    # Instruções de compilação
    print("Para compilar e testar:")
    print(f"  avr-gcc -mmcu=atmega328p {output_path} -o output/programa.elf")
    print("  avr-objcopy -O ihex -j .text -j .data output/programa.elf output/programa.hex")
    print("  avrdude -p atmega328p -c arduino -P /dev/ttyUSB0 -b 115200 -U flash:w:output/programa.hex")
    print()


if __name__ == '__main__':
    main()
