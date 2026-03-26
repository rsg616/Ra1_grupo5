# ---------------------------------------------
#  exibir_resultados.py  -  Aluno 4
#  Formata e exibe os resultados das expressoes
# ---------------------------------------------


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