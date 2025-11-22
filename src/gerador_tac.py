#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Caminho: src/gerador_tac.py

"""
Gerador de Three Address Code (TAC)
Fase 4 - Geração de Código Intermediário

Este módulo gera código intermediário em formato TAC a partir da árvore sintática atribuída.
"""

import sys
import os
from typing import List, Dict, Optional, Any, Union

# Adicionar diretório ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class InstrucaoTAC:
    """
    Representa uma instrução Three Address Code
    
    Formato geral: resultado = operando1 operador operando2
    """
    
    def __init__(self, tipo: str, resultado: Optional[str] = None, 
                 operando1: Optional[str] = None, operador: Optional[str] = None,
                 operando2: Optional[str] = None, linha: Optional[int] = None):
        """
        Inicializa uma instrução TAC
        
        Args:
            tipo: Tipo da instrução (ATRIBUICAO, OPERACAO, COPIA, etc.)
            resultado: Variável que recebe o resultado
            operando1: Primeiro operando
            operador: Operador (+, -, *, /, etc.)
            operando2: Segundo operando
            linha: Linha original no código fonte
        """
        self.tipo = tipo
        self.resultado = resultado
        self.operando1 = operando1
        self.operador = operador
        self.operando2 = operando2
        self.linha = linha
    
    def __str__(self) -> str:
        """Representação em string da instrução TAC"""
        if self.tipo == 'ATRIBUICAO':
            # resultado = valor
            return f"{self.resultado} = {self.operando1}"
        
        elif self.tipo == 'OPERACAO':
            # resultado = operando1 op operando2
            return f"{self.resultado} = {self.operando1} {self.operador} {self.operando2}"
        
        elif self.tipo == 'COPIA':
            # resultado = operando1
            return f"{self.resultado} = {self.operando1}"
        
        elif self.tipo == 'ROTULO':
            # L0:
            return f"{self.resultado}:"
        
        elif self.tipo == 'GOTO':
            # goto L0
            return f"goto {self.resultado}"
        
        elif self.tipo == 'IF':
            # if operando1 goto resultado
            return f"if {self.operando1} goto {self.resultado}"
        
        elif self.tipo == 'IF_FALSE':
            # ifFalse operando1 goto resultado
            return f"ifFalse {self.operando1} goto {self.resultado}"
        
        else:
            return f"# Instrução desconhecida: {self.tipo}"
    
    def __repr__(self) -> str:
        return self.__str__()


class GeradorTAC:
    """
    Gerador de código Three Address Code (TAC)
    
    Responsável por converter a árvore sintática atribuída em código TAC.
    """
    
    def __init__(self):
        """Inicializa o gerador de TAC"""
        self.instrucoes: List[InstrucaoTAC] = []
        self.contador_temporarios = 0
        self.contador_rotulos = 0
        self.tabela_simbolos: Dict[str, str] = {}
        self.historico_resultados: List[str] = []  # Para comando RES
    
    def novo_temporario(self) -> str:
        """
        Cria uma nova variável temporária
        
        Returns:
            Nome da variável temporária (t0, t1, t2, ...)
        """
        temp = f"t{self.contador_temporarios}"
        self.contador_temporarios += 1
        return temp
    
    def novo_rotulo(self) -> str:
        """
        Cria um novo rótulo
        
        Returns:
            Nome do rótulo (L0, L1, L2, ...)
        """
        rotulo = f"L{self.contador_rotulos}"
        self.contador_rotulos += 1
        return rotulo
    
    def adicionar_instrucao(self, instrucao: InstrucaoTAC) -> None:
        """
        Adiciona uma instrução à lista de instruções TAC
        
        Args:
            instrucao: Instrução a ser adicionada
        """
        self.instrucoes.append(instrucao)
    
    def obter_atributo(self, no: Any, atributo: str, padrao: Any = None) -> Any:
        """
        Obtém atributo de um nó, seja objeto ou dicionário
        
        Args:
            no: Nó da árvore (objeto ou dict)
            atributo: Nome do atributo
            padrao: Valor padrão se não encontrar
            
        Returns:
            Valor do atributo ou padrão
        """
        # Se é um dicionário
        if isinstance(no, dict):
            return no.get(atributo, padrao)
        
        # Se é um objeto com atributos
        if hasattr(no, atributo):
            return getattr(no, atributo, padrao)
        
        # Se é uma tupla, tentar primeiro elemento
        if isinstance(no, tuple) and len(no) > 0:
            return self.obter_atributo(no[0], atributo, padrao)
        
        return padrao
    
    def gerar_tac(self, arvore_atribuida: Union[Dict, Any, tuple]) -> List[InstrucaoTAC]:
        """
        Gera código TAC a partir da árvore sintática atribuída
        
        Args:
            arvore_atribuida: Árvore sintática com tipos inferidos
                             Pode ser dict, objeto ou tupla (tupla: usa primeiro elemento)
            
        Returns:
            Lista de instruções TAC geradas
        """
        self.instrucoes = []
        self.contador_temporarios = 0
        self.contador_rotulos = 0
        self.historico_resultados = []
        
        # Se for tupla, pegar primeiro elemento (árvore atribuída)
        if isinstance(arvore_atribuida, tuple):
            if len(arvore_atribuida) == 0:
                raise Exception("Tupla vazia recebida como árvore atribuída")
            arvore_atribuida = arvore_atribuida[0]
        
        # Processar o nó raiz
        resultado = self.processar_no(arvore_atribuida)
        
        # Adicionar resultado ao histórico (para RES)
        if resultado and resultado != 'UNKNOWN':
            self.historico_resultados.append(resultado)
        
        return self.instrucoes
    
    def processar_no(self, no: Union[Dict, Any]) -> str:
        """
        Processa um nó da árvore e retorna o nome da variável que contém seu resultado
        
        Args:
            no: Nó da árvore sintática atribuída (pode ser dict ou objeto)
            
        Returns:
            Nome da variável (temporária ou não) que contém o resultado
        """
        # Obter tipo do nó
        tipo = self.obter_atributo(no, 'tipo', '')
        linha = self.obter_atributo(no, 'linha', None)
        
        # NÚMERO: cria temporário e atribui valor
        if tipo == 'NUMERO':
            temp = self.novo_temporario()
            valor = self.obter_atributo(no, 'valor', '0')
            
            instrucao = InstrucaoTAC(
                tipo='ATRIBUICAO',
                resultado=temp,
                operando1=str(valor),
                linha=linha
            )
            self.adicionar_instrucao(instrucao)
            return temp
        
        # IDENTIFICADOR: retorna o nome da variável
        elif tipo == 'IDENTIFICADOR':
            return str(self.obter_atributo(no, 'valor', 'UNKNOWN'))
        
        # OPERAÇÃO: processa recursivamente os operandos
        elif tipo == 'OPERACAO':
            operador = self.obter_atributo(no, 'valor', '+')
            filhos = self.obter_atributo(no, 'filhos', [])
            
            if len(filhos) < 2:
                raise Exception(f"Operação {operador} requer 2 operandos")
            
            # Processar operandos (recursivamente)
            operando1_var = self.processar_no(filhos[0])
            operando2_var = self.processar_no(filhos[1])
            
            # Criar temporário para o resultado
            temp_resultado = self.novo_temporario()
            
            # Criar instrução de operação
            instrucao = InstrucaoTAC(
                tipo='OPERACAO',
                resultado=temp_resultado,
                operando1=operando1_var,
                operador=operador,
                operando2=operando2_var,
                linha=linha
            )
            self.adicionar_instrucao(instrucao)
            
            return temp_resultado
        
        # EXPRESSÃO: processa recursivamente
        elif tipo == 'EXPRESSAO':
            filhos = self.obter_atributo(no, 'filhos', [])
            if filhos:
                return self.processar_no(filhos[0])
            return 'UNKNOWN'
        
        # COMANDO_ARMAZENAR: (V MEM) → MEM = V
        elif tipo == 'COMANDO_ARMAZENAR':
            filhos = self.obter_atributo(no, 'filhos', [])
            
            if len(filhos) < 2:
                raise Exception("COMANDO_ARMAZENAR requer 2 operandos (valor e identificador)")
            
            # Processar o valor (pode ser número, expressão, etc.)
            valor_var = self.processar_no(filhos[0])
            
            # Obter nome da variável de memória
            identificador = self.obter_atributo(filhos[1], 'valor', 'MEM')
            
            # Criar instrução de cópia: MEM = valor
            instrucao = InstrucaoTAC(
                tipo='COPIA',
                resultado=identificador,
                operando1=valor_var,
                linha=linha
            )
            self.adicionar_instrucao(instrucao)
            
            # Registrar na tabela de símbolos
            self.tabela_simbolos[identificador] = valor_var
            
            return identificador
        
        # COMANDO_RECUPERAR: (MEM) → t0 = MEM
        elif tipo == 'COMANDO_RECUPERAR':
            filhos = self.obter_atributo(no, 'filhos', [])
            
            if not filhos:
                raise Exception("COMANDO_RECUPERAR requer um identificador")
            
            # Obter nome da variável de memória
            identificador = self.obter_atributo(filhos[0], 'valor', 'MEM')
            
            # Criar temporário para receber o valor
            temp = self.novo_temporario()
            
            # Criar instrução de cópia: t0 = MEM
            instrucao = InstrucaoTAC(
                tipo='COPIA',
                resultado=temp,
                operando1=identificador,
                linha=linha
            )
            self.adicionar_instrucao(instrucao)
            
            return temp
        
        # COMANDO_RES: (N RES) → acessa resultado N linhas anteriores
        elif tipo == 'COMANDO_RES':
            filhos = self.obter_atributo(no, 'filhos', [])
            
            if not filhos:
                raise Exception("COMANDO_RES requer um número")
            
            # Obter o índice N
            n_valor = self.obter_atributo(filhos[0], 'valor', '1')
            
            try:
                n = int(float(n_valor))
            except ValueError:
                raise Exception(f"COMANDO_RES: índice inválido '{n_valor}'")
            
            # Verificar se o histórico tem resultados suficientes
            if n <= 0 or n > len(self.historico_resultados):
                raise Exception(f"COMANDO_RES: índice {n} fora do histórico (disponível: 1-{len(self.historico_resultados)})")
            
            # Acessar resultado do histórico (N linhas para trás)
            # histórico[-1] é o último, [-2] é o penúltimo, etc.
            resultado_anterior = self.historico_resultados[-n]
            
            # Criar temporário para receber o valor
            temp = self.novo_temporario()
            
            # Criar instrução de cópia: t0 = resultado_anterior
            instrucao = InstrucaoTAC(
                tipo='COPIA',
                resultado=temp,
                operando1=resultado_anterior,
                linha=linha
            )
            self.adicionar_instrucao(instrucao)
            
            return temp
        
        # Outros tipos ainda não implementados
        else:
            print(f"Aviso: Tipo de nó '{tipo}' ainda não implementado no gerador TAC")
            return 'UNKNOWN'
    
    def salvar_tac(self, nome_arquivo: str) -> None:
        """
        Salva o código TAC em um arquivo de texto
        
        Args:
            nome_arquivo: Caminho do arquivo de saída
        """
        try:
            # Criar diretório se não existir
            dir_saida = os.path.dirname(nome_arquivo)
            if dir_saida and not os.path.exists(dir_saida):
                os.makedirs(dir_saida)
            
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("THREE ADDRESS CODE (TAC)\n")
                f.write("=" * 60 + "\n\n")
                
                if not self.instrucoes:
                    f.write("# Nenhuma instrução gerada\n")
                else:
                    for i, instrucao in enumerate(self.instrucoes, 1):
                        f.write(f"{i:3d}. {instrucao}\n")
                
                f.write("\n" + "=" * 60 + "\n")
                f.write(f"Total de instruções: {len(self.instrucoes)}\n")
                f.write(f"Temporários utilizados: {self.contador_temporarios}\n")
                f.write(f"Rótulos criados: {self.contador_rotulos}\n")
                f.write("=" * 60 + "\n")
            
            print(f"✓ TAC salvo em: {nome_arquivo}")
            
        except Exception as e:
            print(f"✗ Erro ao salvar TAC: {e}")
            raise
    
    def imprimir_estatisticas(self) -> None:
        """Imprime estatísticas do código TAC gerado"""
        print("\n" + "=" * 60)
        print("ESTATÍSTICAS DO TAC")
        print("=" * 60)
        print(f"Total de instruções:      {len(self.instrucoes)}")
        print(f"Temporários utilizados:   {self.contador_temporarios}")
        print(f"Rótulos criados:          {self.contador_rotulos}")
        print("=" * 60)


# Função auxiliar para teste
def teste_gerador_tac():
    """Teste básico do gerador TAC"""
    print("=" * 60)
    print("TESTE: Gerador TAC")
    print("=" * 60)
    
    # Simular uma árvore para (3 5 +)
    arvore_teste = {
        'tipo': 'EXPRESSAO',
        'filhos': [
            {
                'tipo': 'OPERACAO',
                'valor': '+',
                'linha': 1,
                'filhos': [
                    {
                        'tipo': 'NUMERO',
                        'valor': '3',
                        'linha': 1
                    },
                    {
                        'tipo': 'NUMERO',
                        'valor': '5',
                        'linha': 1
                    }
                ]
            }
        ]
    }
    
    # Gerar TAC
    gerador = GeradorTAC()
    instrucoes = gerador.gerar_tac(arvore_teste)
    
    # Exibir resultado
    print("\nÁrvore de entrada: (3 5 +)")
    print("\nTAC gerado:")
    print("-" * 60)
    for i, instrucao in enumerate(instrucoes, 1):
        print(f"{i}. {instrucao}")
    print("-" * 60)
    
    gerador.imprimir_estatisticas()
    
    # Salvar em arquivo
    gerador.salvar_tac("output/tac_teste.txt")
    
    print("\n✓ Teste concluído com sucesso!")


if __name__ == '__main__':
    # Executar teste se rodado diretamente
    teste_gerador_tac()