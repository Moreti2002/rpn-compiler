#!/usr/bin/env python3
"""
Otimizador TAC - Compilador RPN
================================

Implementa otimizações no código TAC (Three Address Code):
- Parte 5: Constant Folding (dobramento de constantes)
- Parte 6: Constant Propagation (propagação de constantes)
- Parte 7: Dead Code Elimination (eliminação de código morto)

Author: Compilador RPN - Fase 4
Date: 22/11/2025
"""

from typing import List, Dict, Any, Optional, Set
import copy


class InstrucaoTAC:
    """Representa uma instrução TAC"""
    
    def __init__(self, tipo: str, resultado: str = None, operando1: str = None, 
                 operador: str = None, operando2: str = None, linha: int = None):
        self.tipo = tipo
        self.resultado = resultado
        self.operando1 = operando1
        self.operador = operador
        self.operando2 = operando2
        self.linha = linha
    
    def __repr__(self):
        if self.tipo == 'ATRIBUICAO':
            return f"{self.resultado} = {self.operando1}"
        elif self.tipo == 'OPERACAO':
            return f"{self.resultado} = {self.operando1} {self.operador} {self.operando2}"
        elif self.tipo == 'COPIA':
            return f"{self.resultado} = {self.operando1}"
        elif self.tipo == 'IF_FALSE':
            return f"ifFalse {self.operando1} goto {self.resultado}"
        elif self.tipo == 'GOTO':
            return f"goto {self.resultado}"
        elif self.tipo == 'ROTULO':
            return f"{self.resultado}:"
        else:
            return f"{self.tipo}: {self.resultado}"


class OtimizadorTAC:
    """Otimizador de código TAC"""
    
    def __init__(self):
        self.valores_constantes = {}  # Mapeia variáveis para valores constantes conhecidos
        self.uso_variaveis = {}       # Conta quantas vezes cada variável é usada
        self.estatisticas = {
            'constant_folding': 0,
            'constant_propagation': 0,
            'dead_code_elimination': 0,
            'instrucoes_removidas': 0
        }
    
    def eh_constante(self, valor: str) -> bool:
        """
        Verifica se um valor é uma constante numérica
        
        Args:
            valor: String representando o valor
            
        Returns:
            True se é uma constante numérica
        """
        if valor is None:
            return False
        
        try:
            float(valor)
            return True
        except (ValueError, TypeError):
            return False
    
    def obter_valor_numerico(self, valor: str) -> Optional[float]:
        """
        Obtém o valor numérico de uma string
        
        Args:
            valor: String representando o valor
            
        Returns:
            Valor numérico ou None
        """
        try:
            return float(valor)
        except (ValueError, TypeError):
            return None
    
    def calcular_operacao(self, op1: float, operador: str, op2: float) -> Optional[float]:
        """
        Calcula o resultado de uma operação
        
        Args:
            op1: Primeiro operando
            operador: Operador (+, -, *, /, %, ^, |, >, <, ==, !=, >=, <=)
            op2: Segundo operando
            
        Returns:
            Resultado da operação ou None se inválido
        """
        try:
            if operador == '+':
                return op1 + op2
            elif operador == '-':
                return op1 - op2
            elif operador == '*':
                return op1 * op2
            elif operador == '/':
                if op2 == 0:
                    return None  # Divisão por zero
                return op1 / op2
            elif operador == '|':  # Divisão real
                if op2 == 0:
                    return None
                return op1 / op2
            elif operador == '%':
                if op2 == 0:
                    return None
                return op1 % op2
            elif operador == '^':
                return op1 ** op2
            # Operadores relacionais
            elif operador == '>':
                return 1.0 if op1 > op2 else 0.0
            elif operador == '<':
                return 1.0 if op1 < op2 else 0.0
            elif operador == '==':
                return 1.0 if op1 == op2 else 0.0
            elif operador == '!=':
                return 1.0 if op1 != op2 else 0.0
            elif operador == '>=':
                return 1.0 if op1 >= op2 else 0.0
            elif operador == '<=':
                return 1.0 if op1 <= op2 else 0.0
            else:
                return None
        except (ZeroDivisionError, OverflowError, ValueError):
            return None
    
    def formatar_numero(self, valor: float) -> str:
        """
        Formata um número para string (inteiro se possível)
        
        Args:
            valor: Número a formatar
            
        Returns:
            String formatada
        """
        if valor == int(valor):
            return str(int(valor))
        return str(valor)
    
    def constant_folding(self, instrucoes: List[InstrucaoTAC]) -> List[InstrucaoTAC]:
        """
        Parte 5: Constant Folding - Dobramento de constantes
        
        Detecta operações entre constantes e calcula o resultado em tempo de compilação.
        Exemplo: t0 = 2 + 3  →  t0 = 5
        
        Args:
            instrucoes: Lista de instruções TAC originais
            
        Returns:
            Lista de instruções otimizadas
        """
        otimizadas = []
        folding_count = 0
        
        for instrucao in instrucoes:
            if instrucao.tipo == 'OPERACAO':
                # Verificar se ambos operandos são constantes
                if self.eh_constante(instrucao.operando1) and self.eh_constante(instrucao.operando2):
                    op1 = self.obter_valor_numerico(instrucao.operando1)
                    op2 = self.obter_valor_numerico(instrucao.operando2)
                    
                    resultado = self.calcular_operacao(op1, instrucao.operador, op2)
                    
                    if resultado is not None:
                        # Substituir operação por atribuição direta
                        nova_instrucao = InstrucaoTAC(
                            tipo='ATRIBUICAO',
                            resultado=instrucao.resultado,
                            operando1=self.formatar_numero(resultado),
                            linha=instrucao.linha
                        )
                        otimizadas.append(nova_instrucao)
                        folding_count += 1
                        continue
                
            # Manter instrução original se não foi otimizada
            otimizadas.append(copy.copy(instrucao))
        
        self.estatisticas['constant_folding'] = folding_count
        return otimizadas
    
    def constant_propagation(self, instrucoes: List[InstrucaoTAC]) -> List[InstrucaoTAC]:
        """
        Parte 6: Constant Propagation - Propagação de constantes
        
        Substitui variáveis por seus valores constantes conhecidos.
        Exemplo: t0 = 5; t1 = t0 + 3  →  t0 = 5; t1 = 8
        
        Args:
            instrucoes: Lista de instruções TAC
            
        Returns:
            Lista de instruções otimizadas
        """
        otimizadas = []
        valores = {}  # Mapa de variáveis para valores constantes
        propagation_count = 0
        
        for instrucao in instrucoes:
            nova_instrucao = copy.copy(instrucao)
            
            # Atualizar mapa de valores conhecidos
            if instrucao.tipo == 'ATRIBUICAO' and self.eh_constante(instrucao.operando1):
                valores[instrucao.resultado] = instrucao.operando1
            
            # Invalidar valor se variável é modificada de forma não-constante
            elif instrucao.tipo in ['OPERACAO', 'COPIA', 'IF_FALSE']:
                if instrucao.resultado in valores:
                    del valores[instrucao.resultado]
            
            # Propagar constantes em operações
            if instrucao.tipo == 'OPERACAO':
                # Substituir operando1 se for constante conhecida
                if instrucao.operando1 in valores:
                    nova_instrucao.operando1 = valores[instrucao.operando1]
                    propagation_count += 1
                
                # Substituir operando2 se for constante conhecida
                if instrucao.operando2 in valores:
                    nova_instrucao.operando2 = valores[instrucao.operando2]
                    propagation_count += 1
                
                # Tentar fazer folding após propagação
                if self.eh_constante(nova_instrucao.operando1) and self.eh_constante(nova_instrucao.operando2):
                    op1 = self.obter_valor_numerico(nova_instrucao.operando1)
                    op2 = self.obter_valor_numerico(nova_instrucao.operando2)
                    resultado = self.calcular_operacao(op1, nova_instrucao.operador, op2)
                    
                    if resultado is not None:
                        nova_instrucao = InstrucaoTAC(
                            tipo='ATRIBUICAO',
                            resultado=instrucao.resultado,
                            operando1=self.formatar_numero(resultado),
                            linha=instrucao.linha
                        )
                        # Registrar novo valor constante
                        valores[instrucao.resultado] = self.formatar_numero(resultado)
            
            # Propagar em cópias
            elif instrucao.tipo == 'COPIA':
                if instrucao.operando1 in valores:
                    nova_instrucao.operando1 = valores[instrucao.operando1]
                    propagation_count += 1
                
                # Se copia uma constante, registrar
                if self.eh_constante(nova_instrucao.operando1):
                    valores[instrucao.resultado] = nova_instrucao.operando1
            
            # Propagar em condicionais
            elif instrucao.tipo == 'IF_FALSE':
                if instrucao.operando1 in valores:
                    nova_instrucao.operando1 = valores[instrucao.operando1]
                    propagation_count += 1
            
            otimizadas.append(nova_instrucao)
        
        self.estatisticas['constant_propagation'] = propagation_count
        return otimizadas
    
    def analisar_uso_variaveis(self, instrucoes: List[InstrucaoTAC]) -> Dict[str, int]:
        """
        Analisa quantas vezes cada variável é usada
        
        Args:
            instrucoes: Lista de instruções TAC
            
        Returns:
            Dicionário mapeando variável para número de usos
        """
        uso = {}
        
        for instrucao in instrucoes:
            # Contar uso como operando
            if instrucao.operando1 and not self.eh_constante(instrucao.operando1):
                uso[instrucao.operando1] = uso.get(instrucao.operando1, 0) + 1
            
            if instrucao.operando2 and not self.eh_constante(instrucao.operando2):
                uso[instrucao.operando2] = uso.get(instrucao.operando2, 0) + 1
        
        return uso
    
    def dead_code_elimination(self, instrucoes: List[InstrucaoTAC]) -> List[InstrucaoTAC]:
        """
        Parte 7: Dead Code Elimination - Eliminação de código morto
        
        Remove instruções que calculam valores nunca usados.
        
        Args:
            instrucoes: Lista de instruções TAC
            
        Returns:
            Lista de instruções otimizadas
        """
        # Analisar uso de variáveis
        uso = self.analisar_uso_variaveis(instrucoes)
        
        otimizadas = []
        removidas = 0
        
        for instrucao in instrucoes:
            # Nunca remover: rótulos, gotos, if_false
            if instrucao.tipo in ['ROTULO', 'GOTO', 'IF_FALSE']:
                otimizadas.append(copy.copy(instrucao))
                continue
            
            # Nunca remover atribuições a variáveis (não temporários)
            if instrucao.resultado and not instrucao.resultado.startswith('t'):
                otimizadas.append(copy.copy(instrucao))
                continue
            
            # Remover se resultado nunca é usado
            if instrucao.resultado and instrucao.resultado not in uso:
                removidas += 1
                continue
            
            # Manter instrução
            otimizadas.append(copy.copy(instrucao))
        
        self.estatisticas['dead_code_elimination'] = removidas
        self.estatisticas['instrucoes_removidas'] = removidas
        return otimizadas
    
    def otimizar(self, instrucoes: List[InstrucaoTAC], nivel: str = 'completo') -> List[InstrucaoTAC]:
        """
        Aplica otimizações no código TAC
        
        Args:
            instrucoes: Lista de instruções TAC originais
            nivel: 'folding', 'propagation', 'dead_code', 'completo'
            
        Returns:
            Lista de instruções otimizadas
        """
        # Resetar estatísticas
        self.estatisticas = {
            'constant_folding': 0,
            'constant_propagation': 0,
            'dead_code_elimination': 0,
            'instrucoes_removidas': 0
        }
        
        resultado = instrucoes
        
        if nivel in ['folding', 'completo']:
            resultado = self.constant_folding(resultado)
        
        if nivel in ['propagation', 'completo']:
            resultado = self.constant_propagation(resultado)
        
        if nivel in ['dead_code', 'completo']:
            resultado = self.dead_code_elimination(resultado)
        
        return resultado
    
    def obter_estatisticas(self) -> Dict[str, int]:
        """Retorna estatísticas das otimizações aplicadas"""
        return self.estatisticas.copy()


def imprimir_comparacao(original: List[InstrucaoTAC], otimizado: List[InstrucaoTAC]):
    """
    Imprime comparação lado a lado entre TAC original e otimizado
    
    Args:
        original: Instruções TAC originais
        otimizado: Instruções TAC otimizadas
    """
    print("\n" + "=" * 80)
    print("COMPARAÇÃO: TAC ORIGINAL vs TAC OTIMIZADO")
    print("=" * 80)
    print()
    print(f"{'ORIGINAL':<40} {'OTIMIZADO':<40}")
    print("-" * 80)
    
    max_len = max(len(original), len(otimizado))
    
    for i in range(max_len):
        linha_orig = str(original[i]) if i < len(original) else ""
        linha_otim = str(otimizado[i]) if i < len(otimizado) else ""
        
        print(f"{linha_orig:<40} {linha_otim:<40}")
    
    print("-" * 80)
    print(f"Total de instruções: {len(original):<28} {len(otimizado):<40}")
    reducao = len(original) - len(otimizado)
    if reducao > 0:
        percentual = (reducao / len(original)) * 100
        print(f"\n✓ Redução de {reducao} instruções ({percentual:.1f}%)")
    print()
