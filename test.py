import os

# ============================================================
#  Grupo: Ra1_grupo5
#  Disciplina: [NOME DA DISCIPLINA]
#  Professor:  [NOME DO PROFESSOR]
#  Integrantes (ordem alfabetica):
#    [Aluno 1] - github: [usuario1]
#    [Aluno 2] - github: [usuario2]
#    [Aluno 3] - github: [usuario3]
#    [Aluno 4] - github: [usuario4]
#
#  Aluno 3 - gerarAssembly e lerArquivo
#  Gera codigo Assembly ARMv7 com precisao IEEE 754 de 64 bits
#  usando registradores de dupla precisao d0-d15 (VFP).
# ============================================================

TOKEN_NUM       = "NUM"
TOKEN_OP        = "OP"
TOKEN_LPAREN    = "LPAREN"
TOKEN_RPAREN    = "RPAREN"
TOKEN_RES       = "RES"
TOKEN_MEM_STORE = "MEM_STORE"
TOKEN_MEM_LOAD  = "MEM_LOAD"


# ---------------------------------------------
#  Cabecalho ARMv7 + habilitacao VFP
# ---------------------------------------------
def _cabecalho(instrucoes):
    instrucoes += [
        ".syntax unified",
        ".arch armv7-a",
        ".fpu vfpv3-d16",
        ".text",
        ".global main",
        "main:",
        "",
        "    @ Habilitar VFP (dupla precisao IEEE 754 64 bits)",
        "    MRC p15, 0, r0, c1, c0, 2",
        "    ORR r0, r0, #0xF00000",
        "    MCR p15, 0, r0, c1, c0, 2",
        "    ISB",
        "    MOV r0, #0x40000000",
        "    VMSR FPEXC, r0",
        "",
    ]


# ---------------------------------------------
#  Exibe resultado d{dreg} nos LEDs (0xFF200000)
#  Registrador de dupla precisao 64 bits IEEE 754
# ---------------------------------------------
def _mostrar_resultado(instrucoes, dreg):
    instrucoes += [
        f"",
        f"    @ Exibe resultado de d{dreg} nos LEDs (IEEE 754 64 bits)",
        f"    PUSH {{r4, r5}}",
        f"    VMOV r4, r5, d{dreg}        @ r4=LSB, r5=MSB do double",
        f"    LDR r1, =0xFF200000",
        f"    STR r5, [r1]               @ MSB (parte alta do double)",
        f"    MOV r0, #0",
        f"    STR r0, [r1]               @ apaga",
        f"    STR r4, [r1]               @ LSB (parte baixa do double)",
        f"    MOV r0, #0",
        f"    STR r0, [r1]               @ apaga",
        f"    POP {{r4, r5}}",
    ]


# ---------------------------------------------
#  Gera instrucoes para (N RES)
#  Todos os valores sao doubles (8 bytes cada)
# ---------------------------------------------
def _gerar_res(instrucoes, creg, linha_idx, literais):
    reg_n    = creg - 1
    lbl_ok   = f"res_ok_{linha_idx}_{creg}"
    lbl_end  = f"res_end_{linha_idx}_{creg}"
    lbl_zero = f"num_{len(literais)}"
    literais.append((lbl_zero, "0.0"))

    instrucoes += [
        f"",
        f"    @ (N RES) - busca resultado N posicoes atras (64 bits)",
        f"    VCVT.S32.F64 s31, d{reg_n}",   # converte double N para int32 em s31
        f"    VMOV r1, s31",                   # r1 = N
        f"    MOV r2, #{linha_idx}",           # r2 = indice da linha atual
        f"    SUB r1, r2, r1",                 # r1 = linha_atual - N
        f"    CMP r1, #0",
        f"    BGE {lbl_ok}",
        f"    @ indice invalido -> carrega 0.0",
        f"    LDR r2, ={lbl_zero}",
        f"    VLDR d{reg_n}, [r2]",
        f"    B {lbl_end}",
        f"{lbl_ok}:",
        f"    LDR r2, =res_array",
        f"    ADD r2, r2, r1, LSL #3",         # endereco = base + idx*8 (double = 8 bytes)
        f"    VLDR d{reg_n}, [r2]",            # carrega resultado anterior
        f"{lbl_end}:",
    ]


# ---------------------------------------------
#  Funcao principal
# ---------------------------------------------
def gerarAssembly(lista_tokens_por_linha, caminho_saida="assembly.s"):
    """
    Recebe uma lista onde cada elemento eh a lista de tokens de uma linha.
    Gera Assembly ARMv7 com precisao IEEE 754 de 64 bits e salva em caminho_saida.

    Parametros:
        lista_tokens_por_linha  - list[list[Token]]
        caminho_saida           - str, caminho do arquivo .s gerado

    Retorna:
        caminho_saida
    """
    instrucoes = []
    literais   = []   # (label, valor_double) para secao .data
    memorias   = []   # labels de variaveis MEM criadas

    _cabecalho(instrucoes)

    for linha_idx, tokens in enumerate(lista_tokens_por_linha):
        creg              = 0      # indice do registrador d atual (pilha virtual)
        ultimo_foi_numero = False  # flag para distinguir (V MEM) de (MEM)

        instrucoes.append(f"    @ ---- linha {linha_idx} ----")

        for tok in tokens:

            # -- Ignora parenteses --
            if tok.tipo in (TOKEN_LPAREN, TOKEN_RPAREN):
                continue

            # -- Numero: carrega literal de 64 bits em d{creg} --
            elif tok.tipo == TOKEN_NUM:
                label = f"num_{len(literais)}"
                literais.append((label, tok.valor))
                instrucoes += [
                    f"",
                    f"    @ Carrega {tok.valor} -> d{creg}  (IEEE 754 64 bits)",
                    f"    LDR r0, ={label}",
                    f"    VLDR d{creg}, [r0]",
                ]
                creg += 1
                ultimo_foi_numero = True

            # -- Operador aritmetico --
            elif tok.tipo == TOKEN_OP:
                ultimo_foi_numero = False
                rdir = creg - 1
                resq = creg - 2
                op   = tok.valor

                instrucoes.append(f"")
                instrucoes.append(f"    @ Operacao {op}: d{resq} {op} d{rdir} -> d{resq}  (F64)")

                if op == '+':
                    instrucoes.append(f"    VADD.F64 d{resq}, d{resq}, d{rdir}")

                elif op == '-':
                    instrucoes.append(f"    VSUB.F64 d{resq}, d{resq}, d{rdir}")

                elif op == '*':
                    instrucoes.append(f"    VMUL.F64 d{resq}, d{resq}, d{rdir}")

                elif op == '/':
                    instrucoes.append(f"    VDIV.F64 d{resq}, d{resq}, d{rdir}")

                elif op == '//':
                    # divisao inteira: divide, trunca para int, converte de volta
                    instrucoes += [
                        f"    VDIV.F64 d{resq}, d{resq}, d{rdir}",
                        f"    VCVT.S32.F64 s31, d{resq}",   # trunca para int32 em s31
                        f"    VCVT.F64.S32 d{resq}, s31",   # converte int32 de volta para double
                    ]

                elif op == '%':
                    # resto: a - trunc(a/b)*b
                    stmp = creg   # registrador temporario (fora da pilha atual)
                    instrucoes += [
                        f"    VDIV.F64 d{stmp}, d{resq}, d{rdir}",
                        f"    VCVT.S32.F64 s31, d{stmp}",   # trunca quociente
                        f"    VCVT.F64.S32 d{stmp}, s31",   # de volta para double
                        f"    VMUL.F64 d{stmp}, d{stmp}, d{rdir}",
                        f"    VSUB.F64 d{resq}, d{resq}, d{stmp}",
                    ]

                elif op == '^':
                    # potenciacao por multiplicacao repetida (expoente inteiro positivo)
                    stmp = creg
                    lbl  = f"pow_{len(literais)}"
                    lbl1 = f"num_{len(literais)}"
                    literais.append((lbl1, "1.0"))
                    instrucoes += [
                        f"    VCVT.S32.F64 s31, d{rdir}",   # expoente int32 em s31
                        f"    VMOV r1, s31",                  # r1 = contador do loop
                        f"    LDR r2, ={lbl1}",
                        f"    VLDR d{stmp}, [r2]",            # d{stmp} = acumulador = 1.0
                        f"{lbl}_loop:",
                        f"    CMP r1, #0",
                        f"    BLE {lbl}_end",
                        f"    VMUL.F64 d{stmp}, d{stmp}, d{resq}",
                        f"    SUB r1, r1, #1",
                        f"    B {lbl}_loop",
                        f"{lbl}_end:",
                        f"    VMOV.F64 d{resq}, d{stmp}",
                    ]

                creg -= 1   # resultado fica em d{resq}, d{rdir} liberado

            # -- MEM_STORE: (V MEM) se pilha tem valor, (MEM) se vazia --
            elif tok.tipo == TOKEN_MEM_STORE:
                var_label = "MEM_var"
                if var_label not in memorias:
                    memorias.append(var_label)

                if ultimo_foi_numero and creg >= 1:
                    # (V MEM): salva d{creg-1} em MEM_var, mantém o valor na pilha
                    rtop = creg - 1
                    instrucoes += [
                        f"",
                        f"    @ (V MEM): salva d{rtop} em MEM_var (64 bits)",
                        f"    LDR r1, ={var_label}",
                        f"    VSTR d{rtop}, [r1]",
                    ]
                else:
                    # (MEM): carrega MEM_var para o topo da pilha
                    instrucoes += [
                        f"",
                        f"    @ (MEM): carrega MEM_var -> d{creg} (64 bits)",
                        f"    LDR r1, ={var_label}",
                        f"    VLDR d{creg}, [r1]",
                    ]
                    creg += 1

                ultimo_foi_numero = False

            # -- MEM_LOAD: sempre carrega --
            elif tok.tipo == TOKEN_MEM_LOAD:
                var_label = "MEM_var"
                if var_label not in memorias:
                    memorias.append(var_label)
                instrucoes += [
                    f"",
                    f"    @ MEM_LOAD -> d{creg} (64 bits)",
                    f"    LDR r1, ={var_label}",
                    f"    VLDR d{creg}, [r1]",
                ]
                creg += 1
                ultimo_foi_numero = False

            # -- RES --
            elif tok.tipo == TOKEN_RES:
                _gerar_res(instrucoes, creg, linha_idx, literais)
                ultimo_foi_numero = False
                # creg nao muda: N foi substituido pelo valor buscado no mesmo registrador

        # -- Fim da linha: salva resultado d0 em res_array e exibe nos LEDs --
        if creg > 0:
            instrucoes += [
                f"",
                f"    @ Salva resultado da linha {linha_idx} em res_array (8 bytes)",
                f"    LDR r1, =res_array",
                f"    MOV r2, #{linha_idx}",
                f"    ADD r1, r1, r2, LSL #3",   # base + idx*8 (double = 8 bytes)
                f"    VSTR d0, [r1]",
            ]
            _mostrar_resultado(instrucoes, 0)

        instrucoes.append("")

    # -- Epilogo --
    instrucoes += [
        "    @ Fim da execucao",
        "    BX LR",
        "",
    ]

    # -- Secao .data (alinhada a 8 bytes para doubles) --
    instrucoes += [".data", ".align 3", ""]

    for mem_lbl in memorias:
        instrucoes += [f"{mem_lbl}:", "    .double 0.0", ""]

    total_linhas = len(lista_tokens_por_linha)
    instrucoes += [
        ".align 3",
        "res_array:",
        f"    .space {total_linhas * 8}   @ {total_linhas} doubles de 8 bytes (IEEE 754 64 bits)",
        "",
    ]

    for label, val in literais:
        instrucoes += [".align 3", f"{label}:", f"    .double {val}", ""]

    # -- Grava arquivo --
    os.makedirs(os.path.dirname(caminho_saida) if os.path.dirname(caminho_saida) else ".", exist_ok=True)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write("\n".join(instrucoes) + "\n")

    return caminho_saida


# ---------------------------------------------
#  Testes
# ---------------------------------------------
def rodar_testes():
    from parse_expressao import parseExpressao

    casos = [
        "(3 4 +)",
        "(3.14 2.0 *)",
        "(17 5 //)",
        "(17 5 %)",
        "(2 8 ^)",
        "(42.5 MEM)",
        "(MEM)",
        "(1 RES)",
    ]

    lista_tokens = []
    print("Tokens gerados por linha:")
    print("=" * 50)
    for i, expr in enumerate(casos):
        tokens, _ = parseExpressao(expr, num_linha=i)
        lista_tokens.append(tokens)
        print(f"  [{i:02d}] {expr}")
        for t in tokens:
            print(f"        {t.tipo:<12} | {repr(t.valor)}")

    saida = gerarAssembly(lista_tokens, caminho_saida="assembly.s")
    print(f"\nAssembly gerado -> {saida}")
    print("\nConteudo do arquivo:")
    print("=" * 50)
    with open(saida) as f:
        for i, linha in enumerate(f, start=1):
            print(f"  {i:03d}  {linha}", end="")


if __name__ == "__main__":
    rodar_testes()
