"""LogSentinel - analisador léxico e extrator de ameaças em logs web (LFA)."""
import argparse
import sys
from pathlib import Path

from analisador import EntradaInvalida, analisar, ler_arquivo, salvar_saidas, validar_texto
from expressoes import EXPRESSOES, POR_ID, ficha_markdown

AQUI = Path(__file__).parent


def ler_stdin_interativo():
    if sys.stdin.isatty():
        print("Cole o log e finalize com uma linha contendo apenas FIM (ou Ctrl+D):")
        buf = []
        for linha in sys.stdin:
            if linha.strip() == "FIM":
                break
            buf.append(linha)
        return "".join(buf)
    return sys.stdin.read()


def obter_linhas(args):
    if args.demo:
        return ler_arquivo(AQUI / "dados" / "exemplo.log")
    if args.texto is not None:
        return validar_texto(args.texto)
    if args.arquivo:
        return ler_arquivo(args.arquivo)
    return validar_texto(ler_stdin_interativo())


def comando_testar(er_id, cadeia):
    er = POR_ID.get(er_id.upper())
    if er is None:
        print(f"[ERRO] ER desconhecida: {er_id}. Use: {', '.join(POR_ID)}")
        return 2
    print(f"{er.id} - {er.nome}\nSintaxe: {er.sintaxe}\nCadeia : {cadeia!r}\n\n--- simulação do AFNε ---")
    afn = er.afn()
    ok_afn = afn.aceita(cadeia, verbose=True)
    ok_re = er.reconhece_regex(cadeia)
    print(f"\nAFNε : {'Cadeia aceita' if ok_afn else 'Cadeia nao aceita'}")
    print(f"re.fullmatch: {'aceita' if ok_re else 'rejeita'}")
    if ok_afn != ok_re:
        print("[ALERTA] divergência entre AFNε e motor de ER!")
        return 3
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("arquivo", nargs="?", help="arquivo .log/.txt (sem argumento: cole o texto no terminal)")
    ap.add_argument("--texto", help="analisa o texto informado diretamente")
    ap.add_argument("--demo", action="store_true", help="usa dados/exemplo.log")
    ap.add_argument("--saida", default=str(AQUI / "saida"), help="pasta de saída (JSON, HTML, log sanitizado)")
    ap.add_argument("--mascarar-ip", action="store_true", help="anonimiza o último octeto dos IPs no log sanitizado")
    ap.add_argument("--validar-afn", action="store_true", help="confere cada trecho extraído também no AFNε")
    ap.add_argument("--fichas", action="store_true", help="imprime a ficha (Markdown) das 5 ERs")
    ap.add_argument("--diagramas", nargs="?", const=str(AQUI / "diagramas"), help="gera os AFNε em .dot (Graphviz)")
    ap.add_argument("--testar", nargs=2, metavar=("ER-0X", "CADEIA"), help="simula uma cadeia no AFNε passo a passo")
    args = ap.parse_args(argv)

    if args.fichas:
        print("# Fichas das Expressões Regulares\n")
        for er in EXPRESSOES:
            print(ficha_markdown(er))
        return 0
    if args.diagramas:
        pasta = Path(args.diagramas)
        pasta.mkdir(parents=True, exist_ok=True)
        for er in EXPRESSOES:
            (pasta / f"{er.id}.dot").write_text(er.afn().para_dot(er.id), encoding="utf-8")
            print(f"gerado {pasta / (er.id + '.dot')}  {er.afn().resumo()['estados']} estados")
        print("Para imagem: dot -Tpng diagramas/ER-01.dot -o diagramas/ER-01.png")
        return 0
    if args.testar:
        return comando_testar(*args.testar)

    try:
        linhas = obter_linhas(args)
    except EntradaInvalida as e:
        print(f"[ERRO] {e}")
        return 1
    rel, sanit = analisar(linhas, args.mascarar_ip, args.validar_afn)
    arquivos = salvar_saidas(rel, sanit, args.saida)

    r = rel["resumo"]
    print("=== LogSentinel - resumo ===")
    print(f"Linhas: {r['total_linhas']} (vazias: {r['linhas_vazias']}, analisadas: {r['linhas_analisadas']})")
    print(f"Linhas com ameaça: {r['linhas_com_ameaca']} | sem IP: {r['linhas_sem_ip']} | "
          f"sem data/hora: {r['linhas_sem_timestamp']} | sem estrutura: {r['linhas_sem_estrutura']}")
    print("Ameaças por tipo:", rel["ameacas_por_tipo"] or "nenhuma")
    print("Origens mais frequentes:", rel["top_origens_maliciosas"] or "nenhuma")
    print(f"CPFs mascarados: {rel['cpfs']['mascarados']}")
    if args.validar_afn:
        print(f"Divergências AFNε x re: {r['divergencias_afn']}")
    print("\nIncidentes:")
    for i in rel["incidentes"]:
        print(f"  linha {i['linha']:>3} | {i['tipo']:<14} | {i['gravidade']:<7} | origem {i['origem']} | {i['trecho']}")
    print("\nArquivos gerados:", *[str(a) for a in arquivos], sep="\n  ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
