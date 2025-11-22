#!/usr/bin/env python3
"""
Compilador RPN - Fase 5: Integração com Otimizador TAC
========================================================

Este programa integra as 4 fases do compilador com as otimizações TAC:
1. Análise Léxica
2. Análise Sintática
3. Análise Semântica + Geração TAC
4. Otimização TAC (Partes 5, 6 e 7)

Otimizações implementadas:
- Constant Folding (Parte 5): Calcula operações constantes
- Constant Propagation (Parte 6): Substitui variáveis por valores conhecidos
- Dead Code Elimination (Parte 7): Remove código não utilizado

Usage:
    python3 main_fase5.py <arquivo_entrada> [--nivel <folding|propagation|dead_code|completo>]
    
Exemplo:
    python3 main_fase5.py test_completo.txt
    python3 main_fase5.py test_completo.txt --nivel completo
"""

import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional

sys.path.insert(0, str(Path(__file__).parent))

from src.lexer import parse_expressao as tokenizar
from src.parser import parsear
from src.grammar import construir_gramatica
from src.syntax_tree import converter_derivacao_para_arvore
from src.arvore_atribuida import gerar_arvore_atribuida
from src.gerador_tac import GeradorTAC
from src.otimizador_tac import OtimizadorTAC, InstrucaoTAC, imprimir_comparacao
from utils.formatador_tac import formatar_lista_tac


class CompiladorFase5:
    """Compilador completo com otimização TAC"""
    
    def __init__(self, nivel_otimizacao: str = 'completo'):
        """
        Inicializa o compilador
        
        Args:
            nivel_otimizacao: Nível de otimização a aplicar
                - 'folding': Apenas Constant Folding
                - 'propagation': Folding + Constant Propagation
                - 'dead_code': Folding + Propagation + Dead Code Elimination
                - 'completo': Todas as otimizações (padrão)
        """
        self.nivel_otimizacao = nivel_otimizacao
        self.gramatica = construir_gramatica()
        self.gerador_tac = GeradorTAC()
        self.otimizador = OtimizadorTAC()
        
        # Histórico de compilações
        self.historico_expressoes: List[str] = []
        self.historico_tac: List[str] = []
        self.total_instrucoes_original = 0
        self.total_instrucoes_otimizado = 0
        self.total_otimizacoes = {
            'constant_folding': 0,
            'constant_propagation': 0,
            'dead_code_elimination': 0
        }
    
    def compilar_expressao(self, expressao: str) -> Tuple[bool, Optional[List[InstrucaoTAC]], Optional[List[InstrucaoTAC]]]:
        """
        Compila uma expressão RPN completa (4 fases + otimização)
        
        Args:
            expressao: Expressão RPN a compilar
            
        Returns:
            Tupla (sucesso, tac_original, tac_otimizado)
        """
        try:
            # Fase 1: Análise Léxica
            tokens = tokenizar(expressao)
            
            if not tokens:
                return False, None, None
            
            # Fase 2: Análise Sintática
            resultado_parser = parsear(tokens, self.gramatica['tabela'])
            derivacao = resultado_parser['derivacao']
            
            # Fase 3: Análise Semântica + Geração TAC
            arvore_sintatica = converter_derivacao_para_arvore(derivacao)
            arvore_atribuida = gerar_arvore_atribuida(arvore_sintatica)
            
            # Gerar TAC e obter resultado
            num_instrucoes_antes = len(self.gerador_tac.instrucoes)
            resultado = self.gerador_tac.processar_no(arvore_atribuida)
            self.gerador_tac.historico_resultados.append(resultado)
            
            # As instruções TAC geradas para esta expressão
            instrucoes_original = self.gerador_tac.instrucoes[num_instrucoes_antes:]
            
            # Fase 4: Otimização TAC
            instrucoes_otimizado = self.otimizador.otimizar(
                instrucoes_original,
                self.nivel_otimizacao
            )
            
            # Atualizar estatísticas
            self.total_instrucoes_original += len(instrucoes_original)
            self.total_instrucoes_otimizado += len(instrucoes_otimizado)
            
            stats = self.otimizador.obter_estatisticas()
            for chave in self.total_otimizacoes:
                self.total_otimizacoes[chave] += stats[chave]
            
            # Adicionar ao histórico
            self.historico_expressoes.append(expressao)
            
            return True, instrucoes_original, instrucoes_otimizado
            
        except Exception as e:
            print(f"❌ Erro ao compilar '{expressao}': {e}")
            return False, None, None
    
    def _converter_tac_para_instrucoes(self, tac_linhas: List[str]) -> List[InstrucaoTAC]:
        """Converte linhas TAC (strings) para objetos InstrucaoTAC"""
        instrucoes = []
        
        for linha in tac_linhas:
            linha = linha.strip()
            if not linha:
                continue
            
            # Parsear diferentes formatos de TAC
            if '=' in linha:
                partes = linha.split('=')
                resultado = partes[0].strip()
                expressao = partes[1].strip()
                
                # Detectar tipo de operação
                operadores = ['+', '-', '*', '/', '%', '^', '|', '>', '<', '==', '!=', '>=', '<=']
                operador_encontrado = None
                
                for op in sorted(operadores, key=len, reverse=True):
                    if op in expressao:
                        operador_encontrado = op
                        break
                
                if operador_encontrado:
                    # É uma operação binária
                    partes_op = expressao.split(operador_encontrado)
                    if len(partes_op) == 2:
                        op1 = partes_op[0].strip()
                        op2 = partes_op[1].strip()
                        instrucoes.append(InstrucaoTAC('OPERACAO', resultado, op1, operador_encontrado, op2))
                else:
                    # É uma atribuição simples
                    instrucoes.append(InstrucaoTAC('ATRIBUICAO', resultado, expressao))
            
            elif linha.startswith('ifFalse'):
                # ifFalse <condicao> goto <label>
                partes = linha.split()
                if len(partes) >= 4:
                    condicao = partes[1]
                    label = partes[3]
                    instrucoes.append(InstrucaoTAC('IF_FALSE', label, condicao))
            
            elif linha.startswith('goto'):
                # goto <label>
                partes = linha.split()
                if len(partes) >= 2:
                    label = partes[1]
                    instrucoes.append(InstrucaoTAC('GOTO', label))
            
            elif linha.endswith(':'):
                # Label
                label = linha[:-1]
                instrucoes.append(InstrucaoTAC('ROTULO', label))
            
            else:
                # Outros tipos
                instrucoes.append(InstrucaoTAC('OUTRA', linha))
        
        return instrucoes
    
    def _instrucoes_para_strings(self, instrucoes: List[InstrucaoTAC]) -> List[str]:
        """Converte objetos InstrucaoTAC de volta para strings formatadas"""
        linhas = []
        
        for instr in instrucoes:
            if instr.tipo == 'ATRIBUICAO':
                linhas.append(f"{instr.resultado} = {instr.operando1}")
            elif instr.tipo == 'OPERACAO':
                linhas.append(f"{instr.resultado} = {instr.operando1} {instr.operador} {instr.operando2}")
            elif instr.tipo == 'COPIA':
                linhas.append(f"{instr.resultado} = {instr.operando1}")
            elif instr.tipo == 'IF_FALSE':
                linhas.append(f"ifFalse {instr.operando1} goto {instr.resultado}")
            elif instr.tipo == 'GOTO':
                linhas.append(f"goto {instr.resultado}")
            elif instr.tipo == 'ROTULO':
                linhas.append(f"{instr.resultado}:")
            else:
                linhas.append(str(instr))
        
        return linhas
    
    def imprimir_resultados(self, expressao: str, tac_original: List[InstrucaoTAC], 
                           tac_otimizado: List[InstrucaoTAC]):
        """Imprime os resultados da compilação e otimização"""
        print("\n" + "=" * 80)
        print(f"EXPRESSÃO: {expressao}")
        print("=" * 80)
        
        # TAC Original
        print("\nTAC ORIGINAL:")
        print("-" * 80)
        for linha in self._instrucoes_para_strings(tac_original):
            print(f"  {linha}")
        
        # TAC Otimizado
        print("\nTAC OTIMIZADO:")
        print("-" * 80)
        for linha in self._instrucoes_para_strings(tac_otimizado):
            print(f"  {linha}")
        
        # Estatísticas desta expressão
        reducao = len(tac_original) - len(tac_otimizado)
        if reducao > 0:
            percentual = (reducao / len(tac_original)) * 100
            print(f"\n✓ Redução: {reducao} instruções ({percentual:.1f}%)")
        elif reducao == 0:
            print("\n• Nenhuma otimização aplicável")
        
        stats = self.otimizador.obter_estatisticas()
        print("\nOTIMIZAÇÕES APLICADAS:")
        print(f"  • Constant Folding: {stats['constant_folding']}")
        print(f"  • Constant Propagation: {stats['constant_propagation']}")
        print(f"  • Dead Code Elimination: {stats['dead_code_elimination']}")
    
    def imprimir_relatorio_final(self):
        """Imprime relatório final com todas as estatísticas"""
        print("\n" + "=" * 80)
        print("RELATÓRIO FINAL DE OTIMIZAÇÃO")
        print("=" * 80)
        
        print(f"\nExpressões compiladas: {len(self.historico_expressoes)}")
        print(f"Nível de otimização: {self.nivel_otimizacao}")
        
        print(f"\nInstruções TAC:")
        print(f"  • Original: {self.total_instrucoes_original}")
        print(f"  • Otimizado: {self.total_instrucoes_otimizado}")
        
        if self.total_instrucoes_original > 0:
            reducao_total = self.total_instrucoes_original - self.total_instrucoes_otimizado
            percentual_total = (reducao_total / self.total_instrucoes_original) * 100
            print(f"  • Redução total: {reducao_total} instruções ({percentual_total:.1f}%)")
        
        print(f"\nTotal de otimizações aplicadas:")
        print(f"  • Constant Folding: {self.total_otimizacoes['constant_folding']}")
        print(f"  • Constant Propagation: {self.total_otimizacoes['constant_propagation']}")
        print(f"  • Dead Code Elimination: {self.total_otimizacoes['dead_code_elimination']}")
        
        total = sum(self.total_otimizacoes.values())
        print(f"  • TOTAL: {total} otimizações")
        
        print("\n" + "=" * 80)


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("Uso: python3 main_fase5.py <arquivo_entrada> [--nivel <nivel>]")
        print("\nNíveis de otimização:")
        print("  folding      - Apenas Constant Folding")
        print("  propagation  - Folding + Constant Propagation")
        print("  dead_code    - Folding + Propagation + Dead Code Elimination")
        print("  completo     - Todas as otimizações (padrão)")
        sys.exit(1)
    
    arquivo_entrada = sys.argv[1]
    
    # Processar nível de otimização
    nivel = 'completo'
    if '--nivel' in sys.argv:
        idx = sys.argv.index('--nivel')
        if idx + 1 < len(sys.argv):
            nivel = sys.argv[idx + 1]
    
    # Verificar arquivo
    caminho = Path(arquivo_entrada)
    if not caminho.exists():
        print(f"❌ Arquivo não encontrado: {arquivo_entrada}")
        sys.exit(1)
    
    # Ler expressões
    with open(caminho, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    # Filtrar linhas válidas
    expressoes = [
        linha.strip() 
        for linha in linhas 
        if linha.strip() and not linha.strip().startswith('#')
    ]
    
    print("=" * 80)
    print("COMPILADOR RPN - FASE 5: COM OTIMIZAÇÃO TAC")
    print("=" * 80)
    print(f"Arquivo: {arquivo_entrada}")
    print(f"Expressões: {len(expressoes)}")
    print(f"Nível de otimização: {nivel}")
    print("=" * 80)
    
    # Compilar
    compilador = CompiladorFase5(nivel_otimizacao=nivel)
    
    sucessos = 0
    falhas = 0
    
    for expressao in expressoes:
        sucesso, tac_original, tac_otimizado = compilador.compilar_expressao(expressao)
        
        if sucesso:
            sucessos += 1
            compilador.imprimir_resultados(expressao, tac_original, tac_otimizado)
        else:
            falhas += 1
    
    # Relatório final
    compilador.imprimir_relatorio_final()
    
    print(f"\n✅ Compilação concluída: {sucessos} sucessos, {falhas} falhas")


if __name__ == '__main__':
    main()
