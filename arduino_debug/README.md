# Arduino Debug Files

Esta pasta contém arquivos Assembly (.s) criados durante o debug e testes da comunicação UART com o Arduino Uno.

## Arquivos de Teste

### Testes UART Básicos
- `teste_u2x.s` - **SUCESSO** - Teste que identificou a necessidade do modo U2X
- `teste_hardcoded.s` - Teste com caracteres hard-coded (sem strings)
- `teste_sem_data.s` - Teste sem seção .data
- `teste_minimo.s` - Teste UART minimalista

### Testes de Leitura de Strings
- `teste_lpm.s` - Teste da instrução `lpm` para ler da Flash
- `teste_text.s` - **SUCESSO** - String em .text funcionou

### Testes UART Multi-baud
- `teste_uart_debug.s` - UART com reset completo
- `teste_uart_multibaud.s` - Teste com múltiplos baud rates
- `teste_uart_correto.s` - Tentativa de correção UART

### Outros Testes
- `teste_led_blink.s` - Teste de piscar LED (verificar execução)
- `teste_simples*.s` - Várias iterações do programa simples

## Problemas Identificados e Soluções

1. **Baud rate incorreto** → Solução: Modo U2X (UBRR = 207)
2. **Strings em .data** → Solução: Strings em .text
3. **Instrução `ld`** → Solução: Usar `lpm` para Flash

## Arquivo Final Funcional

O arquivo `programa_final.s` no diretório `output/` incorpora todas as correções.
