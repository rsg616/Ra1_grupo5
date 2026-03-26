# ---------------------------------------------
#  main.py  -  Aluno 4
#  Orquestra todo o pipeline do programa
#
#  Uso: python main.py <arquivo_de_teste.txt>
# ---------------------------------------------
import sys
import os

from parse_expressao    import parseExpressao
from executarExpressao import executarExpressao
from test     import gerarAssembly
from exibirResultados  import exibirResultados


# ---------------------------------------------
#  lerArquivo
# ---------------------------------------------
def lerArquivo(caminho):
    """
    Le o arquivo de entrada e retorna as linhas validas
    (ignora linhas vazias e comentarios com #).

    Parametros:
        caminho - str : caminho do arquivo .txt

    Retorna:
        list[str] : linhas validas do arquivo
    """
    if not os.path.exists(caminho):
        print(f"[ERRO] Arquivo nao encontrado: {caminho}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
    except Exception as e:
        print(f"[ERRO] Falha ao abrir o arquivo: {e}", file=sys.stderr)
        sys.exit(1)

    validas = []
    for linha in linhas:
        linha = linha.rstrip('\n')
        if linha.strip() and not linha.strip().startswith('#'):
            validas.append(linha.strip())

    if not validas:
        print(f"[AVISO] Arquivo '{caminho}' nao contem expressoes validas.")
        sys.exit(0)

    return validas


# ---------------------------------------------
#  main
# ---------------------------------------------
def main():
    # -- argumento de linha de comando --
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo_de_teste.txt>")
        sys.exit(1)

    caminho = sys.argv[1]

    print(f"\n[INFO] Lendo arquivo: {caminho}")

    # -- Aluno 3: le o arquivo --
    linhas = lerArquivo(caminho)
    print(f"[INFO] {len(linhas)} expressao(oes) encontrada(s)\n")

    # -- estado compartilhado entre expressoes --
    mem  = {"MEM": 0.0}
    hist = []

    expressoes      = []   # textos originais
    resultados      = []   # floats calculados
    lista_tokens    = []   # tokens por linha (para Assembly)

    # -- Alunos 1 e 2: parse + execucao --
    for i, linha in enumerate(linhas):
        try:
            tokens, _ = parseExpressao(linha, num_linha=i + 1)
            resultado = executarExpressao(tokens, mem, hist)

            expressoes.append(linha)
            resultados.append(resultado)
            lista_tokens.append(tokens)

        except SyntaxError as e:
            print(f"[ERRO LEXICO/SINTATICO] Linha {i+1}: {e}", file=sys.stderr)
            expressoes.append(linha)
            resultados.append(None)
            lista_tokens.append([])

        except Exception as e:
            print(f"[ERRO EXECUCAO] Linha {i+1}: {e}", file=sys.stderr)
            expressoes.append(linha)
            resultados.append(None)
            lista_tokens.append([])

    # -- Aluno 4: exibe resultados --
    exibirResultados(expressoes, resultados)

    # -- Aluno 3: gera Assembly --
    nome_base  = os.path.splitext(os.path.basename(caminho))[0]
    saida_asm  = f"{nome_base}.s"
    gerarAssembly(lista_tokens, caminho_saida=saida_asm)
    print(f"[INFO] Assembly gerado -> {saida_asm}\n")


if __name__ == "__main__":
    main()