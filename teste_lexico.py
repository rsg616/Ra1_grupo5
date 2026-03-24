import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse_expressao import (
    AnalisadorLexico, ParserRPN, parseExpressao,
    TOKEN_NUM, TOKEN_OP, TOKEN_LPAREN, TOKEN_RPAREN,
    TOKEN_RES, TOKEN_MEM_STORE, TOKEN_MEM_LOAD, TOKEN_EOF
)

_total  = 0
_passed = 0
_failed = 0


def _run(nome, fn):
    global _total, _passed, _failed
    _total += 1
    try:
        fn()
        print(f"  [OK]  {nome}")
        _passed += 1
    except AssertionError as e:
        print(f"  [FAIL] {nome}: {e}")
        _failed += 1
    except Exception as e:
        print(f"  [ERR]  {nome}: {type(e).__name__}: {e}")
        _failed += 1


def _tokens_tipos(linha):
    return [t.tipo for t in AnalisadorLexico(linha, 0).tokenizar()]


def _tokens_valores(linha):
    return [t.valor for t in AnalisadorLexico(linha, 0).tokenizar()]


def suite_operadores():
    print("\n[SUITE] Operadores")

    def t_soma():
        assert _tokens_tipos("(3 4 +)") == [TOKEN_LPAREN, TOKEN_NUM, TOKEN_NUM, TOKEN_OP, TOKEN_RPAREN]

    def t_sub():
        assert _tokens_valores("(10 3 -)") == ['(', '10', '3', '-', ')']

    def t_mul():
        assert _tokens_valores("(5 6 *)") == ['(', '5', '6', '*', ')']

    def t_div():
        assert _tokens_valores("(20 4 /)") == ['(', '20', '4', '/', ')']

    def t_div_inteira():
        assert _tokens_valores("(17 5 //)") == ['(', '17', '5', '//', ')']

    def t_mod():
        assert _tokens_valores("(17 5 %)") == ['(', '17', '5', '%', ')']

    def t_pot():
        assert _tokens_valores("(2 8 ^)") == ['(', '2', '8', '^', ')']

    _run("soma (+)",              t_soma)
    _run("subtracao (-)",         t_sub)
    _run("multiplicacao (*)",     t_mul)
    _run("divisao (/)",           t_div)
    _run("divisao inteira (//)",  t_div_inteira)
    _run("modulo (%)",            t_mod)
    _run("potencia (^)",          t_pot)


def suite_numeros():
    print("\n[SUITE] Numeros")

    def t_inteiro():
        toks = AnalisadorLexico("42", 0).tokenizar()
        assert len(toks) == 1 and toks[0].tipo == TOKEN_NUM and toks[0].valor == "42"

    def t_real_ponto():
        assert AnalisadorLexico("3.14", 0).tokenizar()[0].valor == "3.14"

    def t_real_notacao_e():
        assert AnalisadorLexico("1e10", 0).tokenizar()[0].valor == "1e10"

    def t_real_notacao_e_sinal():
        assert AnalisadorLexico("2.5e-3", 0).tokenizar()[0].valor == "2.5e-3"

    def t_negativo():
        toks = AnalisadorLexico("(-3 4 +)", 0).tokenizar()
        nums = [t for t in toks if t.tipo == TOKEN_NUM]
        assert nums[0].valor == "-3"

    def t_real_negativo():
        toks = AnalisadorLexico("(-42.5 MEM)", 0).tokenizar()
        nums = [t for t in toks if t.tipo == TOKEN_NUM]
        assert nums[0].valor == "-42.5"

    _run("inteiro",             t_inteiro)
    _run("real com ponto",      t_real_ponto)
    _run("notacao cientifica",  t_real_notacao_e)
    _run("notacao cient. neg.", t_real_notacao_e_sinal)
    _run("numero negativo",     t_negativo)
    _run("real negativo",       t_real_negativo)


def suite_palavras_chave():
    print("\n[SUITE] Palavras-chave")

    def t_res():
        assert TOKEN_RES in [t.tipo for t in AnalisadorLexico("(1 RES)", 0).tokenizar()]

    def t_mem_store():
        assert TOKEN_MEM_STORE in [t.tipo for t in AnalisadorLexico("(42.5 MEM)", 0).tokenizar()]

    def t_mem_load():
        assert TOKEN_MEM_STORE in [t.tipo for t in AnalisadorLexico("(MEM)", 0).tokenizar()]

    def t_res_minusculo():
        assert TOKEN_RES in [t.tipo for t in AnalisadorLexico("(1 res)", 0).tokenizar()]

    def t_mem_minusculo():
        assert TOKEN_MEM_STORE in [t.tipo for t in AnalisadorLexico("(42.5 mem)", 0).tokenizar()]

    _run("RES reconhecido",         t_res)
    _run("MEM store reconhecido",   t_mem_store)
    _run("MEM load reconhecido",    t_mem_load)
    _run("RES case-insensitive",    t_res_minusculo)
    _run("MEM case-insensitive",    t_mem_minusculo)


def suite_parser():
    print("\n[SUITE] Parser / AST")

    def t_ast_soma():
        _, arv = parseExpressao("(3 4 +)")
        assert arv.tipo == "OP" and arv.valor == "+"
        assert arv.filhos[0].valor == "3" and arv.filhos[1].valor == "4"

    def t_ast_aninhado():
        _, arv = parseExpressao("(3 (2 4 *) +)")
        assert arv.tipo == "OP" and arv.filhos[1].tipo == "OP"

    def t_ast_res():
        _, arv = parseExpressao("(1 RES)")
        assert arv.tipo == "RES" and arv.valor == 1

    def t_ast_mem_store():
        _, arv = parseExpressao("(42.5 MEM)")
        assert arv.tipo == "MEM_STORE" and arv.valor == "42.5"

    def t_ast_mem_load():
        _, arv = parseExpressao("(MEM)")
        assert arv.tipo == "MEM_LOAD"

    def t_ast_duplo_aninhado():
        _, arv = parseExpressao("((3 4 +) (2 5 *) -)")
        assert arv.tipo == "OP" and arv.filhos[0].tipo == "OP" and arv.filhos[1].tipo == "OP"

    _run("AST soma simples",        t_ast_soma)
    _run("AST aninhado direito",    t_ast_aninhado)
    _run("AST RES",                 t_ast_res)
    _run("AST MEM_STORE",           t_ast_mem_store)
    _run("AST MEM_LOAD",            t_ast_mem_load)
    _run("AST duplamente aninhado", t_ast_duplo_aninhado)


def suite_erros():
    print("\n[SUITE] Deteccao de erros")

    def t_identificador_desconhecido():
        try:
            AnalisadorLexico("(3 4 FOO)", 0).tokenizar()
            assert False
        except SyntaxError:
            pass

    def t_ponto_sem_digito():
        try:
            AnalisadorLexico("3.", 0).tokenizar()
            assert False
        except SyntaxError:
            pass

    def t_expoente_sem_digito():
        try:
            AnalisadorLexico("1e+", 0).tokenizar()
            assert False
        except SyntaxError:
            pass

    def t_caractere_invalido():
        try:
            AnalisadorLexico("(3 @ 4 +)", 0).tokenizar()
            assert False
        except SyntaxError:
            pass

    def t_token_extra():
        toks = AnalisadorLexico("(3 4 +) 99", 0).tokenizar()
        try:
            ParserRPN(toks).parse()
            assert False
        except SyntaxError:
            pass

    _run("identificador desconhecido", t_identificador_desconhecido)
    _run("ponto sem digito apos",      t_ponto_sem_digito)
    _run("expoente sem digito",        t_expoente_sem_digito)
    _run("caractere invalido @",       t_caractere_invalido)
    _run("token extra apos expressao", t_token_extra)


def suite_comentarios():
    print("\n[SUITE] Comentarios e linhas vazias")

    def t_linha_vazia():
        tokens, arvore = parseExpressao("")
        assert tokens == [] and arvore is None

    def t_so_espacos():
        tokens, arvore = parseExpressao("   ")
        assert tokens == [] and arvore is None

    def t_comentario():
        tokens, arvore = parseExpressao("# comentario")
        assert tokens == [] and arvore is None

    def t_comentario_inline():
        toks = AnalisadorLexico("(3 4 +) # resultado = 7", 0).tokenizar()
        tipos = [t.tipo for t in toks]
        assert tipos[-1] == TOKEN_RPAREN

    _run("linha vazia",         t_linha_vazia)
    _run("so espacos",          t_so_espacos)
    _run("linha de comentario", t_comentario)
    _run("comentario inline",   t_comentario_inline)


def suite_posicao():
    print("\n[SUITE] Posicao dos tokens (linha/coluna)")

    def t_coluna_lparen():
        toks = AnalisadorLexico("(3 4 +)", 5).tokenizar()
        assert toks[0].coluna == 0 and toks[0].linha == 5

    def t_coluna_num():
        toks = AnalisadorLexico("(3 4 +)", 1).tokenizar()
        num_tok = next(t for t in toks if t.tipo == TOKEN_NUM and t.valor == "3")
        assert num_tok.coluna == 1

    def t_coluna_op():
        toks = AnalisadorLexico("(3 4 +)", 1).tokenizar()
        op_tok = next(t for t in toks if t.tipo == TOKEN_OP)
        assert op_tok.coluna == 5

    _run("coluna do LPAREN", t_coluna_lparen)
    _run("coluna do NUM",    t_coluna_num)
    _run("coluna do OP",     t_coluna_op)


def main():
    print("=" * 60)
    print("  TESTES DO ANALISADOR LEXICO - Aluno 1")
    print("=" * 60)

    suite_operadores()
    suite_numeros()
    suite_palavras_chave()
    suite_parser()
    suite_erros()
    suite_comentarios()
    suite_posicao()

    print("\n" + "=" * 60)
    print(f"  RESULTADO: {_passed}/{_total} OK  |  {_failed} FALHA(S)")
    print("=" * 60)

    sys.exit(0 if _failed == 0 else 1)


if __name__ == "__main__":
    main()