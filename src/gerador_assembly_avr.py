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
        
        # Gerenciamento de registradores (Parte 10)
        # Registradores r16-r31 disponíveis para uso geral
        self.registradores_disponiveis = list(range(16, 32))  # r16-r31
        self.mapa_variaveis: Dict[str, int] = {}  # variável → registrador
        self.registradores_em_uso: Dict[int, str] = {}  # registrador → variável
    
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
        
        # Função setup UART - implementação compatível com Arduino
        epilogo.append("; === FUNÇÃO: Configurar UART ===")
        epilogo.append("setup_uart:")
        epilogo.append("    push r16")
        epilogo.append("    push r17")
        epilogo.append("")
        epilogo.append("    ; 1. Desabilitar UART completamente")
        epilogo.append("    ldi r16, 0x00")
        epilogo.append("    sts 0xC1, r16    ; UCSR0B = 0")
        epilogo.append("")
        epilogo.append("    ; 2. Configurar formato: 8N1 (UCSZ01:0 = 11)")
        epilogo.append("    ldi r16, 0x06")
        epilogo.append("    sts 0xC2, r16    ; UCSR0C = 0b00000110")
        epilogo.append("")
        epilogo.append("    ; 3. Ativar U2X (double speed) - compatível com Arduino")
        epilogo.append("    ldi r16, 0x02")
        epilogo.append("    sts 0xC0, r16    ; UCSR0A = 0b00000010 (U2X0=1)")
        epilogo.append("")
        epilogo.append("    ; 4. Configurar baud rate: 9600 @ 16MHz com U2X")
        epilogo.append("    ; UBRR = (F_CPU / (8 * BAUD)) - 1 = 207")
        epilogo.append("    ldi r16, 207")
        epilogo.append("    ldi r17, 0")
        epilogo.append("    sts 0xC4, r16    ; UBRR0L = 207")
        epilogo.append("    sts 0xC5, r17    ; UBRR0H = 0")
        epilogo.append("")
        epilogo.append("    ; 5. Habilitar TX (TXEN0 = bit 3)")
        epilogo.append("    ldi r16, 0x08")
        epilogo.append("    sts 0xC1, r16    ; UCSR0B = 0b00001000")
        epilogo.append("")
        epilogo.append("    ; 6. Aguardar UART estabilizar")
        epilogo.append("    ldi r17, 255")
        epilogo.append("uart_init_delay:")
        epilogo.append("    dec r17")
        epilogo.append("    brne uart_init_delay")
        epilogo.append("")
        epilogo.append("    pop r17")
        epilogo.append("    pop r16")
        epilogo.append("    ret")
        epilogo.append("")
        
        # Função enviar caractere UART - versão simplificada
        epilogo.append("; === FUNÇÃO: Enviar caractere via UART ===")
        epilogo.append("; Entrada: r16 = caractere a enviar")
        epilogo.append("uart_transmit:")
        epilogo.append("    push r17")
        epilogo.append("")
        epilogo.append("uart_wait:")
        epilogo.append("    ; Aguardar buffer vazio (UDRE0 = bit 5)")
        epilogo.append("    lds r17, 0xC0    ; UCSR0A")
        epilogo.append("    sbrs r17, 5      ; Pular se UDRE0 = 1")
        epilogo.append("    rjmp uart_wait")
        epilogo.append("")
        epilogo.append("    ; Enviar byte")
        epilogo.append("    sts 0xC6, r16    ; UDR0")
        epilogo.append("")
        epilogo.append("    pop r17")
        epilogo.append("    ret")
        epilogo.append("")
        
        # Função enviar string - strings em Flash precisam de lpm!
        epilogo.append("; === FUNÇÃO: Enviar string via UART ===")
        epilogo.append("; Entrada: Z aponta para string em FLASH (terminada em 0)")
        epilogo.append("uart_print_string:")
        epilogo.append("    push r16")
        epilogo.append("    push ZL")
        epilogo.append("    push ZH")
        epilogo.append("")
        epilogo.append("print_loop:")
        epilogo.append("    lpm r16, Z+      ; Ler byte da Flash")
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
        Strings ficam em .text para serem lidas com lpm
        """
        data = []
        
        data.append("; === SEÇÃO DE DADOS (strings em .text) ===")
        data.append(".section .text")
        data.append("")
        
        # Mensagens do sistema - em .text para usar lpm
        data.append("; Mensagens do sistema")
        data.append('msg_startup:')
        data.append('    .asciz "Compilador RPN - Arduino Uno\\r\\n"')
        data.append("")
        
        # Voltar para seção .data para variáveis RAM
        data.append(".section .data")
        data.append("")
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
    
    # ========================================================================
    # PARTE 10: OPERAÇÕES ARITMÉTICAS - Gerenciamento de Registradores
    # ========================================================================
    
    def alocar_registrador(self, variavel: str) -> int:
        """
        Aloca um registrador para uma variável
        
        Args:
            variavel: Nome da variável (ex: 't0', 't1', 'X')
            
        Returns:
            Número do registrador alocado
        """
        # Se já tem registrador alocado, retornar
        if variavel in self.mapa_variaveis:
            return self.mapa_variaveis[variavel]
        
        # Alocar novo registrador
        if not self.registradores_disponiveis:
            raise RuntimeError("Sem registradores disponíveis!")
        
        reg = self.registradores_disponiveis.pop(0)
        self.mapa_variaveis[variavel] = reg
        self.registradores_em_uso[reg] = variavel
        
        return reg
    
    def liberar_registrador(self, variavel: str):
        """Libera o registrador usado por uma variável"""
        if variavel in self.mapa_variaveis:
            reg = self.mapa_variaveis[variavel]
            del self.mapa_variaveis[variavel]
            del self.registradores_em_uso[reg]
            self.registradores_disponiveis.insert(0, reg)
    
    def obter_registrador(self, variavel: str) -> int:
        """Obtém o registrador de uma variável (sem alocar novo)"""
        return self.mapa_variaveis.get(variavel, None)
    
    def eh_constante(self, valor: str) -> bool:
        """Verifica se um valor é uma constante numérica"""
        try:
            float(valor)
            return True
        except (ValueError, TypeError):
            return False
    
    # ========================================================================
    # PARTE 10: MAPEAMENTO TAC → ASSEMBLY
    # ========================================================================
    
    def processar_instrucao_tac(self, instr: InstrucaoTAC) -> List[str]:
        """
        Converte uma instrução TAC para Assembly AVR
        
        Args:
            instr: Instrução TAC
            
        Returns:
            Lista de linhas Assembly
        """
        asm = []
        
        if instr.tipo == 'ATRIBUICAO':
            asm.extend(self.gerar_atribuicao(instr))
        elif instr.tipo == 'OPERACAO':
            asm.extend(self.gerar_operacao(instr))
        elif instr.tipo == 'COPIA':
            asm.extend(self.gerar_copia(instr))
        elif instr.tipo == 'ROTULO':
            asm.extend(self.gerar_rotulo(instr))
        elif instr.tipo == 'GOTO':
            asm.extend(self.gerar_goto(instr))
        elif instr.tipo == 'IF_FALSE':
            asm.extend(self.gerar_if_false(instr))
        else:
            asm.append(f"    ; TODO: {instr.tipo} não implementado")
        
        return asm
    
    def gerar_atribuicao(self, instr: InstrucaoTAC) -> List[str]:
        """
        Gera Assembly para atribuição: resultado = valor
        
        Exemplo TAC: t0 = 5
        Assembly: ldi r16, 5
        """
        asm = []
        resultado = instr.resultado
        valor = instr.operando1
        
        # Alocar registrador para resultado
        reg_dest = self.alocar_registrador(resultado)
        
        if self.eh_constante(valor):
            # Carregar constante
            const_val = int(float(valor))
            # Limitar a 8 bits (0-255)
            const_val = const_val & 0xFF
            asm.append(f"    ldi r{reg_dest}, {const_val}  ; {resultado} = {valor}")
        else:
            # Copiar de outro registrador
            reg_src = self.obter_registrador(valor)
            if reg_src is not None:
                asm.append(f"    mov r{reg_dest}, r{reg_src}  ; {resultado} = {valor}")
            else:
                # Variável não encontrada - pode ser constante otimizada
                # Tentar tratar como constante
                if self.eh_constante(valor):
                    const_val = int(float(valor)) & 0xFF
                    asm.append(f"    ldi r{reg_dest}, {const_val}  ; {resultado} = {valor} (otimizado)")
                else:
                    # Se não é constante, alocar como 0
                    asm.append(f"    ldi r{reg_dest}, 0  ; {resultado} = {valor} (não encontrado, usando 0)")
        
        return asm
    
    def gerar_operacao(self, instr: InstrucaoTAC) -> List[str]:
        """
        Gera Assembly para operação binária
        
        Exemplo TAC: t2 = t0 + t1
        Assembly:
            mov r18, r16  ; copiar t0
            add r18, r17  ; adicionar t1
        """
        asm = []
        resultado = instr.resultado
        op1 = instr.operando1
        op2 = instr.operando2
        operador = instr.operador
        
        # Alocar registrador para resultado
        reg_dest = self.alocar_registrador(resultado)
        
        # Obter operandos
        if self.eh_constante(op1):
            # Carregar primeira constante
            val1 = int(float(op1))
            asm.append(f"    ldi r{reg_dest}, {val1}")
        else:
            reg_op1 = self.obter_registrador(op1)
            if reg_op1 is not None:
                asm.append(f"    mov r{reg_dest}, r{reg_op1}")
            else:
                asm.append(f"    ; ERRO: Variável {op1} não encontrada")
                return asm
        
        # Aplicar operação com segundo operando
        if self.eh_constante(op2):
            val2 = int(float(op2))
            # Para operações com constante, precisamos de um registrador temporário
            reg_temp = 31  # Usar r31 como temporário
            asm.append(f"    ldi r{reg_temp}, {val2}")
            reg_op2 = reg_temp
        else:
            reg_op2 = self.obter_registrador(op2)
            if reg_op2 is None:
                asm.append(f"    ; ERRO: Variável {op2} não encontrada")
                return asm
        
        # Gerar instrução de operação
        if operador == '+':
            asm.append(f"    add r{reg_dest}, r{reg_op2}  ; {resultado} = {op1} + {op2}")
        elif operador == '-':
            asm.append(f"    sub r{reg_dest}, r{reg_op2}  ; {resultado} = {op1} - {op2}")
        elif operador == '*':
            # Multiplicação é mais complexa no AVR
            asm.append(f"    mul r{reg_dest}, r{reg_op2}  ; {resultado} = {op1} * {op2}")
            asm.append(f"    mov r{reg_dest}, r0  ; resultado em r0 (8-bit)")
        elif operador == '/':
            # Divisão requer implementação de função auxiliar
            asm.append(f"    ; TODO: Divisão {op1} / {op2}")
        elif operador == '%':
            # Módulo requer implementação de função auxiliar
            asm.append(f"    ; TODO: Módulo {op1} % {op2}")
        elif operador == '^':
            # Potência requer implementação de função auxiliar
            asm.append(f"    ; TODO: Potência {op1} ^ {op2}")
        elif operador in ['>', '<', '>=', '<=', '==', '!=']:
            # Comparação
            asm.append(f"    cp r{reg_dest}, r{reg_op2}  ; comparar {op1} {operador} {op2}")
            # Resultado em flags, não em registrador
        else:
            asm.append(f"    ; ERRO: Operador {operador} não suportado")
        
        return asm
    
    def gerar_copia(self, instr: InstrucaoTAC) -> List[str]:
        """
        Gera Assembly para cópia: dest = src
        
        Exemplo TAC: X = t0
        Assembly: mov r20, r16
        """
        asm = []
        dest = instr.resultado
        src = instr.operando1
        
        reg_dest = self.alocar_registrador(dest)
        
        # Verificar se é constante
        if self.eh_constante(src):
            const_val = int(float(src)) & 0xFF
            asm.append(f"    ldi r{reg_dest}, {const_val}  ; {dest} = {src} (constante)")
        else:
            reg_src = self.obter_registrador(src)
            if reg_src is not None:
                asm.append(f"    mov r{reg_dest}, r{reg_src}  ; {dest} = {src}")
            else:
                # Variável não encontrada - usar 0
                asm.append(f"    ldi r{reg_dest}, 0  ; {dest} = {src} (não encontrado)")
        
        return asm
    
    def gerar_rotulo(self, instr: InstrucaoTAC) -> List[str]:
        """
        Gera rótulo Assembly
        
        Exemplo TAC: L0:
        Assembly: L0:
        """
        self.num_labels += 1
        return [f"{instr.resultado}:"]
    
    def gerar_goto(self, instr: InstrucaoTAC) -> List[str]:
        """
        Gera salto incondicional
        
        Exemplo TAC: goto L0
        Assembly: rjmp L0
        """
        return [f"    rjmp {instr.resultado}"]
    
    def gerar_if_false(self, instr: InstrucaoTAC) -> List[str]:
        """
        Gera salto condicional
        
        Exemplo TAC: ifFalse t0 goto L0
        Assembly: 
            tst r16
            breq L0
        """
        asm = []
        condicao = instr.operando1
        label = instr.resultado
        
        # Se condição é constante, avaliar em tempo de compilação
        if self.eh_constante(condicao):
            val = int(float(condicao))
            if val == 0:
                # Condição sempre falsa, sempre pula
                asm.append(f"    rjmp {label}  ; {condicao} é falso (constante)")
            else:
                # Condição sempre verdadeira, nunca pula
                asm.append(f"    ; ifFalse {condicao} goto {label} - sempre verdadeiro, não pula")
        else:
            reg_cond = self.obter_registrador(condicao)
            if reg_cond is not None:
                asm.append(f"    tst r{reg_cond}  ; testar {condicao}")
                asm.append(f"    breq {label}  ; saltar se zero (falso)")
            else:
                # Condição não encontrada - assumir falso e pular
                asm.append(f"    rjmp {label}  ; {condicao} não encontrado, pulando")
        
        return asm
    
    def gerar_programa_principal(self, instrucoes_tac: List[InstrucaoTAC]) -> List[str]:
        """
        Gera o corpo do programa_principal a partir das instruções TAC
        
        Args:
            instrucoes_tac: Lista de instruções TAC otimizadas
            
        Returns:
            Lista de linhas Assembly
        """
        asm = []
        asm.append("; === FUNÇÃO: Programa Principal (gerado a partir do TAC) ===")
        asm.append("programa_principal:")
        asm.append("    push r16")
        asm.append("    push r17")
        asm.append("    push r18")
        asm.append("")
        
        # Processar cada instrução TAC
        for instr in instrucoes_tac:
            linhas = self.processar_instrucao_tac(instr)
            asm.extend(linhas)
        
        asm.append("")
        asm.append("    pop r18")
        asm.append("    pop r17")
        asm.append("    pop r16")
        asm.append("    ret")
        asm.append("")
        
        return asm
    
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
        
        # Gerar epílogo (sem programa_principal se temos TAC)
        epilogo = self.gerar_epilogo()
        
        # Se temos instruções TAC, gerar programa_principal
        if instrucoes_tac:
            # Remover placeholder do epílogo
            epilogo_filtrado = []
            skip_next = False
            for i, linha in enumerate(epilogo):
                if 'FUNÇÃO: Programa Principal' in linha:
                    # Pular até encontrar a próxima linha vazia
                    skip_next = True
                    continue
                if skip_next:
                    if linha.strip() == '':
                        skip_next = False
                    continue
                epilogo_filtrado.append(linha)
            
            # Adicionar epilogo sem placeholder
            self.codigo.extend(epilogo_filtrado)
            
            # Gerar programa_principal real
            self.codigo.extend(self.gerar_programa_principal(instrucoes_tac))
        else:
            # Usar epílogo com placeholder
            self.codigo.extend(epilogo)
        
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
