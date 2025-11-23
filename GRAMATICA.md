# Documentação da Gramática LL(1)

## Regras de Produção

```
PROGRAMA → EXPRESSAO
EXPRESSAO → ( CONTEUDO )
CONTEUDO → CONTEUDO_REAL
CONTEUDO_REAL → OPERACAO_OU_COMANDO
OPERACAO_OU_COMANDO → numero RESTO_NUMERO
OPERACAO_OU_COMANDO → identificador RESTO_IDENTIFICADOR
OPERACAO_OU_COMANDO → EXPRESSAO OPERANDO OPERADOR_TOTAL
RESTO_NUMERO → numero OPERADOR_ARIT
RESTO_NUMERO → identificador
RESTO_NUMERO → RES
RESTO_IDENTIFICADOR → numero OPERADOR_ARIT
RESTO_IDENTIFICADOR → identificador OPERADOR_ARIT
RESTO_IDENTIFICADOR → EXPRESSAO OPERADOR_TOTAL
RESTO_IDENTIFICADOR → ε
OPERADOR_TOTAL → OPERADOR_ARIT
OPERADOR_TOTAL → OPERADOR_REL BLOCO PALAVRA_CONTROLE
PALAVRA_CONTROLE → BLOCO IF
PALAVRA_CONTROLE → WHILE
BLOCO → EXPRESSAO
BLOCO → BLOCO_COMPOSTO
BLOCO_COMPOSTO → ( LISTA_EXPRESSOES )
LISTA_EXPRESSOES → EXPRESSAO LISTA_EXPRESSOES
LISTA_EXPRESSOES → EXPRESSAO
OPERACAO → OPERANDO OPERANDO OPERADOR_ARIT
OPERANDO → numero
OPERANDO → identificador
OPERANDO → EXPRESSAO
OPERADOR_ARIT → +
OPERADOR_ARIT → -
OPERADOR_ARIT → *
OPERADOR_ARIT → /
OPERADOR_ARIT → %
OPERADOR_ARIT → ^
OPERADOR_REL → >
OPERADOR_REL → <
OPERADOR_REL → ==
OPERADOR_REL → !=
OPERADOR_REL → >=
OPERADOR_REL → <=
```

## Extensão: Blocos Compostos

A gramática foi estendida para suportar **blocos compostos** em estruturas de controle.

### Sintaxe

**Bloco Simples** (original):
```
(cond (expr) WHILE)
(cond (expr_true) (expr_false) IF)
```

**Bloco Composto** (novo):
```
(cond ((expr1) (expr2) ...) WHILE)
(cond ((expr1) (expr2)) ((expr3) (expr4)) IF)
```

### Exemplos

**Fatorial com WHILE composto**:
```
(5 NUM)
(1 FAT)
(NUM 1 > (((FAT NUM *) FAT) ((NUM 1 -) NUM)) WHILE)
```

**IF com blocos compostos**:
```
(X 10 > (((X 1 -) X) (1 FLAG)) ((0 FLAG)) IF)
```

Ver documentação completa em: `docs/BLOCOS_COMPOSTOS.md`

## Conjuntos FIRST

| Não-Terminal | FIRST |
|--------------|-------|
| CONTEUDO | { (, identificador, numero } |
| CONTEUDO_REAL | { (, identificador, numero } |
| EXPRESSAO | { ( } |
| OPERACAO | { (, identificador, numero } |
| OPERACAO_OU_COMANDO | { (, identificador, numero } |
| OPERADOR_ARIT | { %, *, +, -, /, ^ } |
| OPERADOR_REL | { !=, <, <=, ==, >, >= } |
| OPERADOR_TOTAL | { !=, %, *, +, -, /, <, <=, ==, >, >=, ^ } |
| OPERANDO | { (, identificador, numero } |
| PALAVRA_CONTROLE | { (, WHILE } |
| PROGRAMA | { ( } |
| RESTO_IDENTIFICADOR | { (, identificador, numero, ε } |
| RESTO_NUMERO | { RES, identificador, numero } |

## Conjuntos FOLLOW

| Não-Terminal | FOLLOW |
|--------------|--------|
| CONTEUDO | { ) } |
| CONTEUDO_REAL | { ) } |
| EXPRESSAO | { !=, $, %, (, *, +, -, /, <, <=, ==, >, >=, IF, WHILE, ^, identificador, numero } |
| OPERACAO | {  } |
| OPERACAO_OU_COMANDO | { ) } |
| OPERADOR_ARIT | { ) } |
| OPERADOR_REL | { ( } |
| OPERADOR_TOTAL | { ) } |
| OPERANDO | { !=, %, (, *, +, -, /, <, <=, ==, >, >=, ^, identificador, numero } |
| PALAVRA_CONTROLE | { ) } |
| PROGRAMA | { $ } |
| RESTO_IDENTIFICADOR | { ) } |
| RESTO_NUMERO | { ) } |

## Tabela de Análise LL(1)

| Não-Terminal | Terminal | Produção |
|--------------|----------|----------|
| CONTEUDO | ( | CONTEUDO_REAL |
| CONTEUDO | identificador | CONTEUDO_REAL |
| CONTEUDO | numero | CONTEUDO_REAL |
| CONTEUDO_REAL | ( | OPERACAO_OU_COMANDO |
| CONTEUDO_REAL | identificador | OPERACAO_OU_COMANDO |
| CONTEUDO_REAL | numero | OPERACAO_OU_COMANDO |
| EXPRESSAO | ( | ( CONTEUDO ) |
| OPERACAO | ( | OPERANDO OPERANDO OPERADOR_ARIT |
| OPERACAO | identificador | OPERANDO OPERANDO OPERADOR_ARIT |
| OPERACAO | numero | OPERANDO OPERANDO OPERADOR_ARIT |
| OPERACAO_OU_COMANDO | ( | EXPRESSAO OPERANDO OPERADOR_TOTAL |
| OPERACAO_OU_COMANDO | identificador | identificador RESTO_IDENTIFICADOR |
| OPERACAO_OU_COMANDO | numero | numero RESTO_NUMERO |
| OPERADOR_ARIT | % | % |
| OPERADOR_ARIT | * | * |
| OPERADOR_ARIT | + | + |
| OPERADOR_ARIT | - | - |
| OPERADOR_ARIT | / | / |
| OPERADOR_ARIT | ^ | ^ |
| OPERADOR_REL | != | != |
| OPERADOR_REL | < | < |
| OPERADOR_REL | <= | <= |
| OPERADOR_REL | == | == |
| OPERADOR_REL | > | > |
| OPERADOR_REL | >= | >= |
| OPERADOR_TOTAL | != | OPERADOR_REL EXPRESSAO PALAVRA_CONTROLE |
| OPERADOR_TOTAL | % | OPERADOR_ARIT |
| OPERADOR_TOTAL | * | OPERADOR_ARIT |
| OPERADOR_TOTAL | + | OPERADOR_ARIT |
| OPERADOR_TOTAL | - | OPERADOR_ARIT |
| OPERADOR_TOTAL | / | OPERADOR_ARIT |
| OPERADOR_TOTAL | < | OPERADOR_REL EXPRESSAO PALAVRA_CONTROLE |
| OPERADOR_TOTAL | <= | OPERADOR_REL EXPRESSAO PALAVRA_CONTROLE |
| OPERADOR_TOTAL | == | OPERADOR_REL EXPRESSAO PALAVRA_CONTROLE |
| OPERADOR_TOTAL | > | OPERADOR_REL EXPRESSAO PALAVRA_CONTROLE |
| OPERADOR_TOTAL | >= | OPERADOR_REL EXPRESSAO PALAVRA_CONTROLE |
| OPERADOR_TOTAL | ^ | OPERADOR_ARIT |
| OPERANDO | ( | EXPRESSAO |
| OPERANDO | identificador | identificador |
| OPERANDO | numero | numero |
| PALAVRA_CONTROLE | ( | EXPRESSAO IF |
| PALAVRA_CONTROLE | WHILE | WHILE |
| PROGRAMA | ( | EXPRESSAO |
| RESTO_IDENTIFICADOR | ( | EXPRESSAO OPERADOR_TOTAL |
| RESTO_IDENTIFICADOR | ) | ε |
| RESTO_IDENTIFICADOR | identificador | identificador OPERADOR_ARIT |
| RESTO_IDENTIFICADOR | numero | numero OPERADOR_ARIT |
| RESTO_NUMERO | RES | RES |
| RESTO_NUMERO | identificador | identificador |
| RESTO_NUMERO | numero | numero OPERADOR_ARIT |

## Exemplo de Árvore Sintática

Expressão: `((105/)(32^)*)`

```
EXPRESSAO
  └─ OPERACAO: *
    ├─ EXPRESSAO
      └─ OPERACAO: /
        ├─ NUMERO: 10
        └─ NUMERO: 5
    └─ EXPRESSAO
      └─ OPERACAO: ^
        ├─ NUMERO: 3
        └─ NUMERO: 2
```

Árvore completa salva em: `arvore_sintatica.json`
