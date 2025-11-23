# Extensão da Gramática - Blocos Compostos

## Motivação
A sintaxe original do WHILE permitia apenas uma expressão no bloco:
```
(cond (expr) WHILE)
```

Isso impossibilitava loops úteis que precisam executar múltiplas ações, como:
- Multiplicar E decrementar um contador
- Atualizar múltiplas variáveis
- Executar sequências de operações

## Nova Sintaxe

### WHILE com Bloco Simples (compatível com versão anterior)
```
(operando1 operando2 op_rel (expressao) WHILE)
```

Exemplo:
```
(N 0 > ((N 1 -) N) WHILE)
```

### WHILE com Bloco Composto (novo)
```
(operando1 operando2 op_rel ((expr1) (expr2) (expr3) ...) WHILE)
```

Exemplo - Fatorial:
```
(5 NUM)
(1 FAT)
(NUM 1 > (((FAT NUM *) FAT) ((NUM 1 -) NUM)) WHILE)
```

Neste exemplo, a cada iteração do loop:
1. `((FAT NUM *) FAT)` - Multiplica FAT por NUM e armazena em FAT
2. `((NUM 1 -) NUM)` - Decrementa NUM

### IF com Blocos Compostos
A mesma sintaxe se aplica ao IF:

```
(cond ((expr1) (expr2)) ((expr3) (expr4)) IF)
```

## Implementação

### Parser (src/parser.py)
- Função `parse_bloco_composto()`: Detecta se bloco é simples ou composto
- Se encontrar `(` após o `(` inicial, trata como bloco composto
- Coleta todas as expressões até encontrar `)`

### Árvore Sintática (src/syntax_tree.py)
- Novo tipo de nó: `BLOCO_COMPOSTO`
- Contém lista de expressões no atributo `expressoes`

### Gerador TAC (src/gerador_tac.py)
- Ao processar LACO ou DECISAO, verifica se bloco é `BLOCO_COMPOSTO`
- Se sim, processa cada expressão da lista sequencialmente
- Mantém mesma estrutura de labels e saltos

## Exemplos de Uso

### Fatorial (1! até 8!)
Ver: `examples/fatorial.txt`

### Fibonacci
```
(0 A)
(1 B)
(24 N)
(N 0 > (((A B +) TEMP) (B A) (TEMP B) ((N 1 -) N)) WHILE)
```

### Contador com Impressão
```
(0 CONT)
(CONT 10 < (((CONT 1 +) CONT) (CONT R)) WHILE)
```

## Compatibilidade

✅ **Retrocompatível**: Código antigo com blocos simples continua funcionando
✅ **Fase 2**: Atende requisito de "criar e documentar sintaxe para laços"
✅ **RPN**: Mantém padrão pós-fixado entre parênteses
✅ **TAC**: Gera código intermediário correto
✅ **Assembly**: Compila para AVR sem problemas

## Limitações

⚠️ **Debug Mode**: Uso de `--debug` com muitas expressões pode esgotar registradores
- Solução: Usar `--nivel completo` sem `--debug`, ou reduzir número de testes

## Status

- ✅ Parser modificado
- ✅ Syntax Tree atualizado
- ✅ Gerador TAC adaptado
- ✅ Teste fatorial funcionando (1! até 8!)
- ⏳ Fibonacci pendente
- ⏳ Documentação da gramática completa
