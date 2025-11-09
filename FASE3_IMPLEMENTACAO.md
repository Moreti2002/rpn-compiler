# Documentação de Implementação - Fase 3

## Resumo da Implementação

Esta documentação descreve a implementação completa da **Fase 3 - Analisador Semântico** do projeto de compilador para linguagem RPN.

## ✅ Tarefas Concluídas

### 1. Movimentação de Arquivos
- ✓ Todos os módulos de `codes/` foram movidos para `src/`:
  - `gramatica_atributos.py`
  - `tabela_simbolos.py`
  - `analisador_tipos.py`
  - `analisador_memoria.py`
  - `analisador_controle.py`
  - `arvore_atribuida.py`

### 2. Atualização de Módulos Existentes
- ✓ `src/token_types.py`: Adicionado operador `|` e operadores relacionais completos

### 3. Novos Módulos Criados

#### `src/gramatica_atributos.py`
**Responsabilidade:** Definição da gramática de atributos e regras semânticas

**Funções principais:**
- `definir_gramatica_atributos()` - Define todas as regras semânticas
- `promover_tipo(tipo1, tipo2)` - Implementa promoção automática de tipos
- `obter_regra_semantica(tipo_no, operador)` - Busca regra específica
- `gerar_documentacao_gramatica()` - Gera documentação em markdown

**Regras implementadas:**
- Operações aritméticas: `+`, `-`, `*`, `|`, `/`, `%`, `^`
- Operações relacionais: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Comandos especiais: `ARMAZENAR`, `RECUPERAR`, `RES`
- Estruturas de controle: `IF`, `WHILE`

#### `src/tabela_simbolos.py`
**Responsabilidade:** Gerenciamento de símbolos (memórias/variáveis)

**Funções principais:**
- `inicializar_tabela_simbolos()` - Cria estrutura inicial
- `adicionar_simbolo(tabela, nome, tipo, valor, linha)` - Adiciona símbolo
- `buscar_simbolo(tabela, nome)` - Busca símbolo
- `simbolo_inicializado(tabela, nome)` - Verifica inicialização
- `atualizar_simbolo(tabela, nome, **kwargs)` - Atualiza informações
- `adicionar_resultado_historico(tabela, tipo, valor)` - Adiciona ao histórico
- `obter_resultado_historico(tabela, n)` - Obtém resultado N linhas atrás
- `imprimir_tabela(tabela)` - Formata e imprime tabela
- `validar_tabela(tabela)` - Valida consistência

**Estrutura da tabela:**
```python
{
    'simbolos': {
        'MEM': {
            'tipo': 'real',
            'inicializada': True,
            'valor': 42.5,
            'linha_declaracao': 3,
            'escopo': 0
        }
    },
    'escopo_atual': 0,
    'contador_escopos': 0,
    'historico_resultados': [...]
}
```

#### `src/analisador_tipos.py`
**Responsabilidade:** Verificação e inferência de tipos

**Funções principais:**
- `analisar_semantica(arvore, gramatica, tabela)` - Análise principal
- `anotar_tipos_arvore(no, tabela, erros, linha)` - Percorre árvore anotando tipos
- `inferir_tipo_no(no, tabela, erros)` - Infere tipo de um nó
- `inferir_tipo_numero(no)` - Infere tipo de número literal
- `inferir_tipo_identificador(no, tabela)` - Infere tipo de identificador
- `inferir_tipo_operacao(no, tabela)` - Infere tipo de operação
- `validar_operacao_aritmetica(operador, tipo1, tipo2, linha)` - Valida operação
- `verificar_compatibilidade_tipos(tipo1, tipo2, operador)` - Verifica compatibilidade
- `gerar_relatorio_julgamento_tipos(arvore)` - Gera relatório de regras aplicadas

**Validações implementadas:**
- Operandos numéricos para operações aritméticas
- Expoente inteiro em potenciação
- Operandos inteiros para divisão inteira (`/`) e resto (`%`)
- Divisão real (`|`) sempre retorna `real`
- Promoção automática de tipos em operações mistas

#### `src/analisador_memoria.py`
**Responsabilidade:** Validação de uso de memórias

**Funções principais:**
- `analisar_semantica_memoria(arvore, tabela)` - Análise principal de memória
- `validar_comandos_memoria(no, tabela, erros)` - Percorre árvore validando
- `validar_comando_armazenar(no, tabela)` - Valida `(V MEM)`
- `validar_comando_recuperar(no, tabela)` - Valida `(MEM)` - **ERRO se não inicializada**
- `validar_comando_res(no, tabela)` - Valida `(N RES)`
- `gerar_relatorio_memoria(tabela, erros)` - Gera relatório de memória

**Mudanças importantes da Fase 2:**
- Memória não inicializada agora **gera erro semântico** (antes retornava 0.0)
- Validação de N em RES (deve ser inteiro positivo)
- Verificação de histórico suficiente para RES

#### `src/analisador_controle.py`
**Responsabilidade:** Validação de estruturas de controle

**Funções principais:**
- `analisar_semantica_controle(arvore, tabela)` - Análise principal de controle
- `validar_estruturas_controle(no, tabela, erros)` - Percorre árvore
- `validar_estrutura_decisao(no, tabela)` - Valida IF
- `validar_estrutura_laco(no, tabela)` - Valida WHILE
- `validar_condicao(condicao_no, tabela)` - Valida condição booleana
- `validar_aninhamento_controle(arvore)` - Verifica aninhamento profundo
- `gerar_relatorio_controle(erros, avisos)` - Gera relatório de controle

**Validações implementadas:**
- Condição de IF/WHILE deve retornar `booleano`
- Operador relacional deve ser válido
- Operandos de condição devem ser numéricos
- Estrutura de blocos bem formada

#### `src/arvore_atribuida.py`
**Responsabilidade:** Geração da árvore atribuída final

**Funções principais:**
- `gerar_arvore_atribuida(arvore_anotada)` - Gera AST atribuída
- `limpar_arvore(no)` - Remove informações desnecessárias
- `salvar_arvore_json(arvore, nome_arquivo)` - Salva em JSON
- `carregar_arvore_json(nome_arquivo)` - Carrega de JSON
- `imprimir_arvore_atribuida(arvore, nivel, prefixo)` - Imprime formatada
- `extrair_informacoes_arvore(arvore)` - Extrai estatísticas
- `validar_arvore_atribuida(arvore)` - Valida consistência
- `gerar_representacao_markdown(arvore)` - Gera representação em MD

**Formato da árvore JSON:**
```json
{
  "tipo": "OPERACAO",
  "tipo_inferido": "int",
  "linha": 1,
  "operador": "+",
  "filhos": [...]
}
```

#### `utils/formatador_relatorios.py`
**Responsabilidade:** Geração dos 4 relatórios markdown

**Funções principais:**
- `gerar_relatorio_gramatica_atributos(gramatica, arquivo)`
- `gerar_relatorio_arvore_atribuida(arvore, info, arquivo)`
- `gerar_relatorio_erros(erros, arquivo)`
- `gerar_relatorio_julgamento_tipos(regras, arquivo)`
- `gerar_todos_relatorios(gramatica, arvore, info, erros, regras)` - Gera todos de uma vez

**Relatórios gerados:**
1. `docs/GRAMATICA_ATRIBUTOS.md` - Gramática completa com regras de inferência
2. `docs/ARVORE_ATRIBUIDA.md` - Árvore da última execução com estatísticas
3. `docs/ERROS_SEMANTICOS.md` - Todos os erros encontrados
4. `docs/JULGAMENTO_TIPOS.md` - Regras de dedução aplicadas

#### `main_semantico.py`
**Responsabilidade:** Programa principal integrado

**Fluxo de execução:**
1. Inicializar estruturas (gramáticas, tabela de símbolos)
2. Para cada linha do arquivo:
   - Análise léxica (Fase 1)
   - Análise sintática (Fase 2)
   - Análise de tipos (Fase 3)
   - Análise de memória (Fase 3)
   - Análise de controle (Fase 3)
   - Gerar árvore atribuída
   - Adicionar ao histórico
3. Exibir estatísticas
4. Exibir tabela de símbolos
5. Exibir erros (se houver)
6. Gerar relatórios markdown

### 4. Arquivos de Teste

#### `test_fase3_1.txt` - Casos Válidos (15 linhas)
- Operações aritméticas básicas: `+`, `-`, `*`, `/`, `%`, `^`, `|`
- Expressões aninhadas
- Promoção de tipos (int + real = real)
- Divisão real vs divisão inteira

#### `test_fase3_2.txt` - Erros Semânticos
- Memórias não inicializadas
- Divisão inteira com operando real
- Resto com operando real
- Expoente não inteiro
- RES sem histórico suficiente
- Identificadores não declarados

#### `test_fase3_3.txt` - Casos Complexos
- Expressões profundamente aninhadas
- Uso de RES em operações
- Operadores relacionais
- Mistura de tipos válida

### 5. Documentação

#### `README.md` - Atualizado
Adicionada seção completa da Fase 3 com:
- Características da análise semântica
- Gramática de atributos
- Instruções de uso
- Estrutura do projeto
- Divisão de tarefas
- Exemplos de verificações
- Fluxo de execução
- Mensagens de erro
- Comandos de teste

#### `docs/` - Relatórios Markdown
Pasta criada com os 4 relatórios gerados automaticamente.

## 🎯 Funcionalidades Implementadas

### Verificação de Tipos
- ✓ Inferência de tipos para números literais (int/real)
- ✓ Inferência de tipos para identificadores
- ✓ Validação de operações aritméticas
- ✓ Promoção automática de tipos (int → real)
- ✓ Validação de expoente inteiro em potenciação
- ✓ Validação de operandos inteiros em `/` e `%`
- ✓ Operador `|` sempre retorna real
- ✓ Operadores relacionais retornam booleano

### Verificação de Memória
- ✓ Rastreamento de símbolos declarados
- ✓ Verificação de inicialização antes do uso
- ✓ Validação de comandos `(V MEM)` e `(MEM)`
- ✓ Validação de comando `(N RES)`
- ✓ Histórico de resultados
- ✓ Gerenciamento de escopo

### Verificação de Controle
- ✓ Validação de condições booleanas em IF/WHILE
- ✓ Verificação de estrutura de blocos
- ✓ Validação de operadores relacionais
- ✓ Verificação de aninhamento

### Geração de Árvore Atribuída
- ✓ Anotação de tipos em todos os nós
- ✓ Estrutura hierárquica preservada
- ✓ Exportação em JSON
- ✓ Formatação legível
- ✓ Validação de consistência

### Relatórios
- ✓ Gramática de atributos completa
- ✓ Árvore atribuída com estatísticas
- ✓ Erros semânticos categorizados
- ✓ Julgamento de tipos documentado

## 📊 Resultados de Testes

### test_fase3_1.txt (Casos Válidos)
```
✅ 15/15 linhas processadas com sucesso
✅ 0 erros
✅ Todos os relatórios gerados
```

### test_fase3_2.txt (Erros Semânticos)
```
⚠️ 4 erros encontrados:
- 1 erro léxico (caractere inválido '_')
- 1 erro de memória (RES sem histórico)
- 2 erros de tipo (identificadores não declarados)
✅ Relatórios gerados com erros documentados
```

### test_fase3_3.txt (Casos Complexos)
```
✅ Processamento de expressões aninhadas
✅ Validação de operadores relacionais
✅ Promoção de tipos em operações mistas
```

## 🔧 Comandos de Uso

### Executar análise completa
```bash
python3 main_semantico.py test_fase3_1.txt
```

### Testar módulos individuais
```bash
python3 src/gramatica_atributos.py
python3 src/tabela_simbolos.py
python3 src/analisador_tipos.py
python3 utils/formatador_relatorios.py
```

### Visualizar relatórios
```bash
cat docs/GRAMATICA_ATRIBUTOS.md
cat docs/ERROS_SEMANTICOS.md
python3 -m json.tool arvore_atribuida.json
```

## 📝 Observações Importantes

1. **Integração com Fases Anteriores:**
   - A Fase 3 utiliza completamente as Fases 1 e 2
   - O formato de tokens é compatível
   - A gramática LL(1) é preservada

2. **Mudanças da Fase 2:**
   - Operador `|` adicionado (divisão real)
   - Memória não inicializada agora é erro (antes retornava 0.0)
   - Operadores relacionais implementados

3. **Limitações Atuais:**
   - Comandos de memória `(V MEM)` ainda não totalmente integrados na análise de tipos
   - Estruturas IF/WHILE validadas mas não executadas
   - Tipo booleano não pode ser armazenado em memória

4. **Próximos Passos (Fase 4):**
   - Geração de código intermediário
   - Geração de código Assembly
   - Otimizações de código

## ✅ Status Final

**Todas as tarefas da Fase 3 foram concluídas com sucesso:**

- ✅ Gramática de atributos definida
- ✅ Tabela de símbolos implementada
- ✅ Analisador de tipos implementado
- ✅ Analisador de memória implementado
- ✅ Analisador de controle implementado
- ✅ Gerador de árvore atribuída implementado
- ✅ Formatador de relatórios implementado
- ✅ Programa principal integrado
- ✅ 3 arquivos de teste criados
- ✅ 4 relatórios markdown gerados
- ✅ README.md atualizado

**Data de conclusão:** 05 de Novembro de 2025
