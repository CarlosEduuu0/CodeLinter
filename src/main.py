"""CodeLinter: reconhece trechos de código-fonte com Expressões Regulares e AFNε.

Uso:
    python main.py
"""

import sys
from pathlib import Path

from automatos import afne_er1, afne_er2, afne_er3, afne_er4, afne_er5
from terminal_ER.validators import (
    validar_comentario,
    validar_identificador,
    validar_import,
    validar_ponto_flutuante,
    validar_sk_live,
)

ARQUIVO_EXEMPLOS = Path(__file__).parent / "data" / "exemplos.txt"

# As 5 linguagens do projeto: cada uma tem sua ER e o AFNε equivalente.
LINGUAGENS = [
    ("ER-01", "Identificador camelCase", validar_identificador, afne_er1),
    ("ER-02", "Token Stripe sk_live_", validar_sk_live, afne_er2),
    ("ER-03", "Número decimal", validar_ponto_flutuante, afne_er3),
    ("ER-04", "Import Python", validar_import, afne_er4),
    ("ER-05", "Comentário", validar_comentario, afne_er5),
]


def preparar_entrada(texto: str) -> str:
    """Remove o BOM (caractere invisível que alguns terminais inserem) e converte
    a sequência digitada \\n em quebra de linha, para testar comentários de bloco."""
    return texto.replace("﻿", "").replace("\\n", "\n")


def erro_de_entrada(cadeia: str) -> str | None:
    """Devolve uma mensagem de erro quando a entrada não pode ser analisada."""
    if cadeia == "":
        return "Entrada vazia: digite pelo menos um caractere."
    if cadeia.strip() == "":
        return "A entrada só tem espaços: nenhuma das 5 linguagens aceita isso."
    return None


def analisar(cadeia: str) -> list[tuple[str, str, bool, bool]]:
    """Testa a cadeia nas 5 linguagens e devolve (código, nome, resultado da ER, resultado do AFNε)."""
    return [
        (codigo, nome, er(cadeia), afne.aceita(cadeia))
        for codigo, nome, er, afne in LINGUAGENS
    ]


def marca(aceita: bool) -> str:
    return "✓" if aceita else "✗"


def exibir(cadeia: str, resultados: list[tuple[str, str, bool, bool]]) -> None:
    print(f"\nEntrada: {cadeia!r}")
    print(f"  {'':5}  {'Linguagem':<26} {'ER':^4} {'AFNε':^4}")
    for codigo, nome, pela_er, pelo_afne in resultados:
        aviso = "  ← ER e AFNε discordam!" if pela_er != pelo_afne else ""
        print(f"  {codigo}  {nome:<26} {marca(pela_er):^4} {marca(pelo_afne):^4}{aviso}")
    reconhecidas = [nome for _, nome, pela_er, _ in resultados if pela_er]
    if reconhecidas:
        print(f"Resultado: a cadeia pertence a {', '.join(reconhecidas)}.")
    else:
        print("Resultado: a cadeia não pertence a nenhuma das 5 linguagens.")


def ordenar(estados: set[str]) -> str:
    return "{" + ", ".join(sorted(estados, key=lambda q: int(q[1:]))) + "}"


def passo_a_passo(afne, cadeia: str) -> bool:
    """Mostra os estados do AFNε a cada símbolo lido (mesma lógica de aceita())."""
    estado_atual = afne.fecho_vazio({afne.estado_inicial})
    print(f"  início           → {ordenar(estado_atual)}")
    for simbolo in cadeia:
        idx = afne.criptografia(simbolo)
        if idx == -1:
            print(f"  lê {simbolo!r:<6} fora do alfabeto → cadeia rejeitada")
            return False
        proximos = set()
        for q in estado_atual:
            proximos = proximos.union(afne.funcao[q][idx])
        estado_atual = afne.fecho_vazio(proximos)
        print(f"  lê {simbolo!r:<6}       → {ordenar(estado_atual)}")
        if not estado_atual:
            print("  nenhum estado ativo → cadeia rejeitada")
            return False
    aceita = bool(estado_atual & afne.estado_final)
    finais = ordenar(afne.estado_final)
    if aceita:
        print(f"  fim: contém um estado final {finais} → cadeia ACEITA")
    else:
        print(f"  fim: nenhum estado final {finais} → cadeia REJEITADA")
    return aceita


def ler_cadeia() -> str | None:
    cadeia = preparar_entrada(input("Cadeia (use \\n para quebra de linha): "))
    erro = erro_de_entrada(cadeia)
    if erro:
        print(erro)
        return None
    return cadeia


def opcao_analisar() -> None:
    cadeia = ler_cadeia()
    if cadeia is not None:
        exibir(cadeia, analisar(cadeia))


def opcao_passo_a_passo() -> None:
    for i, (codigo, nome, _, _) in enumerate(LINGUAGENS, start=1):
        print(f"  {i}. {codigo} {nome}")
    escolha = preparar_entrada(input("Qual linguagem (1-5)? ")).strip()
    if escolha not in {"1", "2", "3", "4", "5"}:
        print("Opção inválida: digite um número de 1 a 5.")
        return
    cadeia = ler_cadeia()
    if cadeia is None:
        return
    codigo, nome, er, afne = LINGUAGENS[int(escolha) - 1]
    print(f"\nAFNε da {codigo} ({nome}) lendo {cadeia!r}:")
    passo_a_passo(afne, cadeia)
    print(f"Conferência pela ER: {'aceita' if er(cadeia) else 'rejeita'}.")


def ler_exemplos(caminho: Path) -> list[str]:
    """Lê uma cadeia por linha, ignorando linhas vazias e comentários (#)."""
    linhas = caminho.read_text(encoding="utf-8").splitlines()
    return [
        preparar_entrada(linha)
        for linha in linhas
        if linha.strip() and not linha.startswith("#")
    ]


def opcao_arquivo(caminho: Path = ARQUIVO_EXEMPLOS) -> None:
    try:
        cadeias = ler_exemplos(caminho)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho}")
        return
    if not cadeias:
        print("O arquivo não tem nenhuma cadeia para analisar.")
        return
    print(f"\nAnalisando {len(cadeias)} cadeias de {caminho.name}\n")
    print(f"  {'Cadeia':<40} Reconhecida como")
    for cadeia in cadeias:
        resultados = analisar(cadeia)
        nomes = [nome for _, nome, pela_er, _ in resultados if pela_er] or ["—"]
        discordam = any(pela_er != pelo_afne for *_, pela_er, pelo_afne in resultados)
        aviso = "  ← ER e AFNε discordam!" if discordam else ""
        print(f"  {cadeia!r:<40} {', '.join(nomes)}{aviso}")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    opcoes = {"1": opcao_analisar, "2": opcao_passo_a_passo, "3": opcao_arquivo}
    while True:
        print("\n=== CodeLinter ===")
        print("1. Analisar uma cadeia nas 5 linguagens")
        print("2. Ver o passo a passo de um AFNε")
        print("3. Analisar o arquivo de exemplos")
        print("0. Sair")
        try:
            escolha = preparar_entrada(input("> ")).strip()
        except (EOFError, KeyboardInterrupt):
            break
        if escolha == "0":
            break
        if escolha not in opcoes:
            print("Opção inválida: digite 0, 1, 2 ou 3.")
            continue
        try:
            opcoes[escolha]()
        except (EOFError, KeyboardInterrupt):
            break
    print("Até mais!")


if __name__ == "__main__":
    main()
