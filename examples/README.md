# Exemplos de Código RPN

Esta pasta contém arquivos de exemplo com expressões em Notação Polonesa Reversa (RPN) para teste do compilador.

## Arquivos de Teste por Fase

### Fase 1-2: Léxico e Sintaxe
- `ex01.txt` - Exemplo básico inicial
- `test1.txt`, `test2.txt`, `test3.txt` - Testes simples
- `texto1.txt`, `texto2.txt`, `texto3.txt` - Textos de teste

### Fase 3: Análise Semântica
- `test_fase3_1.txt` - Testes semânticos básicos
- `test_fase3_2.txt` - Testes intermediários
- `test_fase3_3.txt` - Testes avançados
- `test_valido.txt` - Programa validado

### Fase 4-5: TAC e Otimização
- `test_parte5.txt` - Testes específicos da Parte 5
- `test_tac_simples.txt` - TAC simples
- `test_tac_comandos.txt` - Comandos TAC
- `test_tac_controle.txt` - Estruturas de controle
- `test_otimizacao_simples.txt` - Otimizações básicas

### Fase 6: Estruturas de Controle
- `test_if_while.txt` - Testes de IF e WHILE
- `test_simples.txt` - Programa simples

### Fase 9-10: Assembly AVR
- `test_arduino_simples.txt` - **Programa testado no Arduino** ✅
- `test_completo.txt` - Teste completo (35 expressões)
- `test_debug.txt` - Debug Assembly

## Uso

```bash
# Compilar até TAC otimizado
python3 main.py examples/test_completo.txt

# Gerar Assembly para Arduino
python3 main_assembly.py examples/test_arduino_simples.txt --output output/programa.s
```

## Formato RPN

Cada linha contém uma expressão em RPN entre parênteses:
```
(10 20 + X)          # X = 10 + 20
(X 5 * RESULTADO)    # RESULTADO = X * 5
```
