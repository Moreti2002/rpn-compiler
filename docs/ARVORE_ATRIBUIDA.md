# Árvore Sintática Abstrata Atribuída

*Gerado em: 2025-11-05 07:18:08*

---

## Estatísticas da Árvore

- **Total de nós:** 7
- **Profundidade máxima:** 4
- **Total de linhas processadas:** 1
- **Operadores utilizados:** nenhum

## Distribuição de Tipos de Nós

| Tipo de Nó | Quantidade |
|------------|------------|
| EXPRESSAO | 2 |
| NUMERO | 3 |
| OPERACAO | 2 |

## Estrutura da Árvore

Representação hierárquica com tipos inferidos:

```
EXPRESSAO : int (linha 1)
  └─ OPERACAO : int = + (linha 1)
    ├─ EXPRESSAO : int (linha 1)
      └─ OPERACAO : int = / (linha 1)
        ├─ NUMERO : int = 15 (linha 1)
        └─ NUMERO : int = 3 (linha 1)
    └─ NUMERO : int = 2 (linha 1)
```

## Legenda

- **TIPO** : tipo_inferido = valor [operador] (linha)
- Tipos possíveis: `int`, `real`, `booleano`
- `├─` indica filho não-terminal
- `└─` indica último filho

