# Árvore Sintática Abstrata Atribuída

## Estrutura da Árvore

```
PROGRAMA : void (linha 1)
  ├─ EXPRESSAO : int (linha 3)
    └─ OPERACAO : int = + (linha 3)
      ├─ NUMERO : int = 3 (linha 3)
      └─ NUMERO : int = 5 (linha 3)
  ├─ EXPRESSAO : int (linha 4)
    └─ OPERACAO : int = - (linha 4)
      ├─ NUMERO : int = 10 (linha 4)
      └─ NUMERO : int = 3 (linha 4)
  ├─ EXPRESSAO : int (linha 5)
    └─ OPERACAO : int = * (linha 5)
      ├─ NUMERO : int = 4 (linha 5)
      └─ NUMERO : int = 7 (linha 5)
  ├─ EXPRESSAO : int (linha 6)
    └─ OPERACAO : int = / (linha 6)
      ├─ NUMERO : int = 15 (linha 6)
      └─ NUMERO : int = 3 (linha 6)
  ├─ EXPRESSAO : int (linha 7)
    └─ OPERACAO : int = % (linha 7)
      ├─ NUMERO : int = 10 (linha 7)
      └─ NUMERO : int = 3 (linha 7)
  ├─ EXPRESSAO : int (linha 8)
    └─ OPERACAO : int = ^ (linha 8)
      ├─ NUMERO : int = 2 (linha 8)
      └─ NUMERO : int = 8 (linha 8)
  ├─ EXPRESSAO : real (linha 11)
    └─ OPERACAO : real = | (linha 11)
      ├─ NUMERO : real = 10.0 (linha 11)
      └─ NUMERO : real = 3.0 (linha 11)
  ├─ EXPRESSAO : real (linha 12)
    └─ OPERACAO : real = + (linha 12)
      ├─ NUMERO : real = 15.5 (linha 12)
      └─ NUMERO : real = 2.5 (linha 12)
  ├─ EXPRESSAO : real (linha 13)
    └─ OPERACAO : real = - (linha 13)
      ├─ NUMERO : real = 20.0 (linha 13)
      └─ NUMERO : real = 4.0 (linha 13)
  ├─ EXPRESSAO : real (linha 14)
    └─ OPERACAO : real = * (linha 14)
      ├─ NUMERO : real = 3.5 (linha 14)
      └─ NUMERO : real = 2.0 (linha 14)
  ├─ EXPRESSAO : real (linha 17)
    └─ OPERACAO : real = + (linha 17)
      ├─ NUMERO : int = 5 (linha 17)
      └─ NUMERO : real = 2.5 (linha 17)
  ├─ EXPRESSAO : real (linha 18)
    └─ OPERACAO : real = - (linha 18)
      ├─ NUMERO : real = 10.0 (linha 18)
      └─ NUMERO : int = 3 (linha 18)
  ├─ EXPRESSAO : real (linha 19)
    └─ OPERACAO : real = * (linha 19)
      ├─ NUMERO : real = 4.5 (linha 19)
      └─ NUMERO : int = 2 (linha 19)
  ├─ EXPRESSAO : real (linha 22)
    └─ OPERACAO : real = ^ (linha 22)
      ├─ NUMERO : real = 2.5 (linha 22)
      └─ NUMERO : int = 3 (linha 22)
  └─ EXPRESSAO : int (linha 23)
    └─ OPERACAO : int = ^ (linha 23)
      ├─ NUMERO : int = 5 (linha 23)
      └─ NUMERO : int = 2 (linha 23)
```

## Representação JSON

```json
{
  "tipo": "PROGRAMA",
  "tipo_inferido": "void",
  "linha": 1,
  "filhos": [
    {
      "tipo": "EXPRESSAO",
      "tipo_inferido": "int",
      "linha": 3,
      "filhos": [
        {
          "tipo": "OPERACAO",
          "tipo_inferido": "int",
          "linha": 3,
          "valor": "+",
          "filhos": [
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 3,
              "valor": "3",
              "filhos": []
            },
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 3,
              "valor": "5",
              "filhos": []
            }
          ]
        }
      ]
    },
    {
      "tipo": "EXPRESSAO",
      "tipo_inferido": "int",
      "linha": 4,
      "filhos": [
        {
          "tipo": "OPERACAO",
          "tipo_inferido": "int",
          "linha": 4,
          "valor": "-",
          "filhos": [
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 4,
              "valor": "10",
              "filhos": []
            },
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 4,
              "valor": "3",
              "filhos": []
            }
          ]
        }
      ]
    },
    {
      "tipo": "EXPRESSAO",
      "tipo_inferido": "int",
      "linha": 5,
      "filhos": [
        {
          "tipo": "OPERACAO",
          "tipo_inferido": "int",
          "linha": 5,
          "valor": "*",
          "filhos": [
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 5,
              "valor": "4",
              "filhos": []
            },
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 5,
              "valor": "7",
              "filhos": []
            }
          ]
        }
      ]
    },
    {
      "tipo": "EXPRESSAO",
      "tipo_inferido": "int",
      "linha": 6,
      "filhos": [
        {
          "tipo": "OPERACAO",
          "tipo_inferido": "int",
          "linha": 6,
          "valor": "/",
          "filhos": [
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 6,
              "valor": "15",
              "filhos": []
            },
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 6,
              "valor": "3",
              "filhos": []
            }
          ]
        }
      ]
    },
    {
      "tipo": "EXPRESSAO",
      "tipo_inferido": "int",
      "linha": 7,
      "filhos": [
        {
          "tipo": "OPERACAO",
          "tipo_inferido": "int",
          "linha": 7,
          "valor": "%",
          "filhos": [
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 7,
              "valor": "10",
              "filhos": []
            },
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 7,
              "valor": "3",
              "filhos": []
            }
          ]
        }
      ]
    },
    {
      "tipo": "EXPRESSAO",
      "tipo_inferido": "int",
      "linha": 8,
      "filhos": [
        {
          "tipo": "OPERACAO",
          "tipo_inferido": "int",
          "linha": 8,
          "valor": "^",
          "filhos": [
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 8,
              "valor": "2",
              "filhos": []
            },
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 8,
              "valor": "8",
              "filhos": []
            }
          ]
        }
      ]
    },
    {
      "tipo": "EXPRESSAO",
      "tipo_inferido": "real",
      "linha": 11,
      "filhos": [
        {
          "tipo": "OPERACAO",
          "tipo_inferido": "real",
          "linha": 11,
          "valor": "|",
          "filhos": [
            {
              "tipo": "NUMERO",
              "tipo_inferido": "real",
              "linha": 11,
              "valor": "10.0",
              "filhos": []
            },
            {
              "tipo": "NUMERO",
              "tipo_inferido": "real",
              "linha": 11,
              "valor": "3.0",
              "filhos": []
            }
          ]
        }
      ]
    },
    {
      "tipo": "EXPRESSAO",
      "tipo_inferido": "real",
      "linha": 12,
      "filhos": [
        {
          "tipo": "OPERACAO",
          "tipo_inferido": "real",
          "linha": 12,
          "valor": "+",
          "filhos": [
            {
              "tipo": "NUMERO",
              "tipo_inferido": "real",
              "linha": 12,
              "valor": "15.5",
              "filhos": []
            },
            {
              "tipo": "NUMERO",
              "tipo_inferido": "real",
              "linha": 12,
              "valor": "2.5",
              "filhos": []
            }
          ]
        }
      ]
    },
    {
      "tipo": "EXPRESSAO",
      "tipo_inferido": "real",
      "linha": 13,
      "filhos": [
        {
          "tipo": "OPERACAO",
          "tipo_inferido": "real",
          "linha": 13,
          "valor": "-",
          "filhos": [
            {
              "tipo": "NUMERO",
              "tipo_inferido": "real",
              "linha": 13,
              "valor": "20.0",
              "filhos": []
            },
            {
              "tipo": "NUMERO",
              "tipo_inferido": "real",
              "linha": 13,
              "valor": "4.0",
              "filhos": []
            }
          ]
        }
      ]
    },
    {
      "tipo": "EXPRESSAO",
      "tipo_inferido": "real",
      "linha": 14,
      "filhos": [
        {
          "tipo": "OPERACAO",
          "tipo_inferido": "real",
          "linha": 14,
          "valor": "*",
          "filhos": [
            {
              "tipo": "NUMERO",
              "tipo_inferido": "real",
              "linha": 14,
              "valor": "3.5",
              "filhos": []
            },
            {
              "tipo": "NUMERO",
              "tipo_inferido": "real",
              "linha": 14,
              "valor": "2.0",
              "filhos": []
            }
          ]
        }
      ]
    },
    {
      "tipo": "EXPRESSAO",
      "tipo_inferido": "real",
      "linha": 17,
      "filhos": [
        {
          "tipo": "OPERACAO",
          "tipo_inferido": "real",
          "linha": 17,
          "valor": "+",
          "filhos": [
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 17,
              "valor": "5",
              "filhos": []
            },
            {
              "tipo": "NUMERO",
              "tipo_inferido": "real",
              "linha": 17,
              "valor": "2.5",
              "filhos": []
            }
          ]
        }
      ]
    },
    {
      "tipo": "EXPRESSAO",
      "tipo_inferido": "real",
      "linha": 18,
      "filhos": [
        {
          "tipo": "OPERACAO",
          "tipo_inferido": "real",
          "linha": 18,
          "valor": "-",
          "filhos": [
            {
              "tipo": "NUMERO",
              "tipo_inferido": "real",
              "linha": 18,
              "valor": "10.0",
              "filhos": []
            },
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 18,
              "valor": "3",
              "filhos": []
            }
          ]
        }
      ]
    },
    {
      "tipo": "EXPRESSAO",
      "tipo_inferido": "real",
      "linha": 19,
      "filhos": [
        {
          "tipo": "OPERACAO",
          "tipo_inferido": "real",
          "linha": 19,
          "valor": "*",
          "filhos": [
            {
              "tipo": "NUMERO",
              "tipo_inferido": "real",
              "linha": 19,
              "valor": "4.5",
              "filhos": []
            },
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 19,
              "valor": "2",
              "filhos": []
            }
          ]
        }
      ]
    },
    {
      "tipo": "EXPRESSAO",
      "tipo_inferido": "real",
      "linha": 22,
      "filhos": [
        {
          "tipo": "OPERACAO",
          "tipo_inferido": "real",
          "linha": 22,
          "valor": "^",
          "filhos": [
            {
              "tipo": "NUMERO",
              "tipo_inferido": "real",
              "linha": 22,
              "valor": "2.5",
              "filhos": []
            },
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 22,
              "valor": "3",
              "filhos": []
            }
          ]
        }
      ]
    },
    {
      "tipo": "EXPRESSAO",
      "tipo_inferido": "int",
      "linha": 23,
      "filhos": [
        {
          "tipo": "OPERACAO",
          "tipo_inferido": "int",
          "linha": 23,
          "valor": "^",
          "filhos": [
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 23,
              "valor": "5",
              "filhos": []
            },
            {
              "tipo": "NUMERO",
              "tipo_inferido": "int",
              "linha": 23,
              "valor": "2",
              "filhos": []
            }
          ]
        }
      ]
    }
  ]
}
```
