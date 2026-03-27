# Ra1_grupo5 — Analisador Léxico e Gerador de Assembly ARMv7

## Informações Institucionais

- **Instituição:** [NOME DA INSTITUIÇÃO]
- **Disciplina:** [NOME DA DISCIPLINA]
- **Professor:** [NOME DO PROFESSOR]
- **Grupo:** Ra1_grupo5

## Integrantes (ordem alfabética)

| Nome | Usuário GitHub |
|------|---------------|
| [Aluno 1 - Nome Completo] | [@usuario1](https://github.com/usuario1) |
| [Aluno 2 - Nome Completo] | [@usuario2](https://github.com/usuario2) |
| [Aluno 3 - Nome Completo] | [@usuario3](https://github.com/usuario3) |
| [Aluno 4 - Nome Completo] | [@usuario4](https://github.com/usuario4) |

---

## Descrição do Projeto

Este projeto implementa a **Fase 1** de um compilador para uma linguagem de expressões aritméticas em **Notação Polonesa Reversa (RPN)**. O programa:

1. Lê um arquivo de texto com expressões RPN
2. Realiza **análise léxica** usando Autômatos Finitos Determinísticos (AFDs) com estados implementados como funções
3. Gera **código Assembly ARMv7** compatível com o simulador [CPUlator ARMv7 DEC1-SOC (v16.1)](https://cpulator.01xz.net/?sys=arm-de1soc)

Todos os valores numéricos são representados em **precisão dupla IEEE 754 de 64 bits** nos registradores `d0–d15` do coprocessador VFP.

---

## Estrutura do Projeto

```
Ra1_grupo5/
├── main.py               # Aluno 4 — orquestrador principal
├── parse_expressao.py    # Aluno 1 — analisador léxico (AFD) + parser
├── executarExpressao.py  # Aluno 2 — executor de expressões (validação)
├── test.py               # Aluno 3 — gerador de Assembly ARMv7
├── exibirResultados.py   # Aluno 4 — exibição de resultados
├── teste_lexico.py       # Testes do analisador léxico
├── teste1.txt            # Arquivo de teste 1 (operações básicas)
├── teste2.txt            # Arquivo de teste 2 (aninhamento e memória)
├── teste3.txt            # Arquivo de teste 3 (números reais e RES encadeado)
├── assembly.s            # Último código Assembly gerado
├── teste1_tokens.txt     # Tokens gerados na última execução
└── readme.md             # Este arquivo
```

---

## Linguagem Suportada

Expressões em **notação RPN** no formato `(A B op)`, onde A e B são operandos e op é um operador.

### Operadores

| Operador | Descrição | Exemplo |
|----------|-----------|---------|
| `+` | Adição | `(3 4 +)` → 7 |
| `-` | Subtração | `(10 3 -)` → 7 |
| `*` | Multiplicação | `(5 6 *)` → 30 |
| `/` | Divisão real | `(7 2 /)` → 3.5 |
| `//` | Divisão inteira | `(17 5 //)` → 3 |
| `%` | Resto da divisão | `(17 5 %)` → 2 |
| `^` | Potenciação | `(2 8 ^)` → 256 |

### Comandos Especiais

| Comando | Descrição |
|---------|-----------|
| `(N RES)` | Retorna o resultado de N linhas anteriores |
| `(V MEM)` | Armazena o valor V na memória MEM |
| `(MEM)` | Retorna o valor armazenado em MEM |

### Expressões Aninhadas

```
(A (C D *) +)          → soma A ao produto de C e D
((A B *) (D E *) /)    → divide o produto de A*B pelo de D*E
```

---

## Como Executar

### Pré-requisitos

- Python 3.7 ou superior
- Nenhuma dependência externa (apenas biblioteca padrão)

### Execução

```bash
python main.py <arquivo_de_teste.txt>
```

**Exemplos:**

```bash
python main.py teste1.txt
python main.py teste2.txt
python main.py teste3.txt
```

O programa irá:
1. Ler e tokenizar as expressões do arquivo
2. Exibir os resultados em tabela no terminal
3. Gerar o arquivo `<nome_do_arquivo>.s` com o código Assembly
4. Gerar o arquivo `<nome_do_arquivo>_tokens.txt` com os tokens

### Como usar o Assembly no CPUlator

1. Acesse [cpulator.01xz.net](https://cpulator.01xz.net/?sys=arm-de1soc)
2. Selecione o modelo **ARMv7 DEC1-SOC (v16.1)**
3. Cole ou carregue o arquivo `.s` gerado
4. Execute o programa — os resultados aparecem nos LEDs (`0xFF200000`)

---

## Como Testar o Analisador Léxico

```bash
python teste_lexico.py
```

Executa 36 casos de teste distribuídos em 7 suites:

| Suite | Cobertura |
|-------|-----------|
| Operadores | +, -, *, /, //, %, ^ |
| Números | Inteiros, reais, notação científica, negativos |
| Palavras-chave | RES, MEM (case-insensitive) |
| Parser / AST | Expressões simples e aninhadas |
| Detecção de erros | Tokens inválidos, números malformados |
| Comentários | Linhas vazias, `#` inline |
| Posição de tokens | Linha e coluna corretas |

---

## Implementação do AFD

O analisador léxico em `parse_expressao.py` implementa um **Autômato Finito Determinístico** com cada estado como uma função Python:

| Função (estado) | Descrição |
|----------------|-----------|
| `_estado_inicio` | Estado inicial — classifica o primeiro caractere |
| `_estado_menos` | Diferencia operador `-` de número negativo |
| `_estado_op_barra` | Diferencia `/` de `//` |
| `_estado_op_estrela` | Reconhece `*` |
| `_estado_num_inteiro` | Lê dígitos inteiros |
| `_estado_num_ponto` | Valida dígito obrigatório após `.` |
| `_estado_num_decimal` | Lê parte decimal |
| `_estado_num_exp_e` | Lê `e`/`E` de notação científica |
| `_estado_num_exp_sinal` | Lê sinal opcional do expoente |
| `_estado_num_exp_digito` | Lê dígitos do expoente |
| `_estado_palavra` | Reconhece `RES` e `MEM` |

> **Nota:** Expressões regulares não são utilizadas em nenhuma parte da análise léxica.

---

## Geração de Assembly

O gerador em `test.py` produz código Assembly ARMv7 com:

- **Precisão:** IEEE 754 de 64 bits (registradores `d0–d15`, instruções `.F64`)
- **Diretiva FPU:** `.fpu vfpv3-d16`
- **Resultado nos LEDs:** endereço `0xFF200000` via `VMOV r4, r5, d0`
- **Memória:** variável `MEM_var` em `.data` (`.double 0.0`)
- **Histórico:** vetor `res_array` com N entradas de 8 bytes cada

---

## Divisão de Tarefas

| Aluno | Responsabilidade | Função principal |
|-------|-----------------|-----------------|
| Aluno 1 | Repositório + Analisador Léxico AFD | `parseExpressao` |
| Aluno 2 | Executor + Gerenciamento de Memória | `executarExpressao` |
| Aluno 3 | Gerador de Assembly + Leitura de Arquivo | `gerarAssembly`, `lerArquivo` |
| Aluno 4 | Exibição de Resultados + Interface `main` | `exibirResultados` |
