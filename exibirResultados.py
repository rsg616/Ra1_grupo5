# ============================================================
#  Grupo: Ra1_grupo5
#  Disciplina: [NOME DA DISCIPLINA]
#  Professor:  [NOME DO PROFESSOR]
#  Integrantes (ordem alfabetica):
#    [Aluno 1 - Nome Completo] - github: [usuario1]
#    [Aluno 2 - Nome Completo] - github: [usuario2]
#    [Aluno 3 - Nome Completo] - github: [usuario3]
#    [Aluno 4 - Nome Completo] - github: [usuario4]
#
#  Aluno 4 - exibirResultados e Interface do Usuario
#  Formata e exibe os resultados das expressoes processadas.
# ============================================================


def exibirResultados(expressoes, resultados):
    """
    Exibe os resultados das expressoes de forma formatada.

    Parametros:
        expressoes  - list[str]   : textos originais de cada linha
        resultados  - list[float] : resultados calculados por executarExpressao
    """
    print()
    print("=" * 52)
    print(f"  {'LINHA':<6} {'EXPRESSAO':<28} {'RESULTADO':>12}")
    print("=" * 52)

    for i, (expr, resultado) in enumerate(zip(expressoes, resultados), start=1):
        if resultado is None:
            valor_fmt = "ERRO"
        else:
            valor_fmt = _formatar(resultado)

        # trunca expressoes longas para caber na tabela
        expr_exib = expr if len(expr) <= 26 else expr[:23] + "..."
        print(f"  {i:<6} {expr_exib:<28} {valor_fmt:>12}")

    print("=" * 52)
    print()


def _formatar(valor):
    """
    Formata float com uma casa decimal para reais,
    sem decimais para inteiros.

    Exemplos:
        7.0    -> '7'
        3.5    -> '3.5'
        5.14   -> '5.1'
        1024.0 -> '1024'
    """
    if valor == int(valor):
        return str(int(valor))
    else:
        return f"{valor:.1f}"