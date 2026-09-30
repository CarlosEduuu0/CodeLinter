"""CodeLinter: reconhece trechos de código-fonte com Expressões Regulares e AFNε.

Uso:
    python main.py
"""

from automatos import afne_er1, afne_er2, afne_er3, afne_er4, afne_er5
from terminal_ER.validators import (
    validar_comentario,
    validar_identificador,
    validar_import,
    validar_ponto_flutuante,
    validar_sk_live,
)

# As 5 linguagens do projeto: cada uma tem sua ER e o AFNε equivalente.
LINGUAGENS = [
    ("ER-01", "Identificador camelCase", validar_identificador, afne_er1.aceita),
    ("ER-02", "Token Stripe sk_live_", validar_sk_live, afne_er2.aceita),
    ("ER-03", "Número decimal", validar_ponto_flutuante, afne_er3.aceita),
    ("ER-04", "Import Python", validar_import, afne_er4.aceita),
    ("ER-05", "Comentário", validar_comentario, afne_er5.aceita),
]


def analisar(cadeia: str) -> list[tuple[str, str, bool, bool]]:
    """Testa a cadeia nas 5 linguagens e devolve (código, nome, resultado da ER, resultado do AFNε)."""
    return [
        (codigo, nome, er(cadeia), afne(cadeia)) for codigo, nome, er, afne in LINGUAGENS
    ]


def marca(aceita: bool) -> str:
    return "✓" if aceita else "✗"


def exibir(cadeia: str, resultados: list[tuple[str, str, bool, bool]]) -> None:
    print(f'\nEntrada: "{cadeia}"')
    print(f"  {'':5}  {'Linguagem':<28} {'ER':^4} {'AFNε':^4}")
    for codigo, nome, pela_er, pelo_afne in resultados:
        print(f"  {codigo}  {nome:<28} {marca(pela_er):^4} {marca(pelo_afne):^4}")
    reconhecidas = [nome for _, nome, pela_er, _ in resultados if pela_er]
    if reconhecidas:
        print(f"Resultado: a cadeia pertence a {', '.join(reconhecidas)}.")
    else:
        print("Resultado: a cadeia não pertence a nenhuma das 5 linguagens.")


def main() -> None:
    print("CodeLinter · digite uma cadeia para analisar (ou 'sair').")
    while True:
        try:
            cadeia = input("\n> ")
        except (EOFError, KeyboardInterrupt):
            break
        if cadeia.strip().lower() == "sair":
            break
        exibir(cadeia, analisar(cadeia))
    print("Até mais!")


if __name__ == "__main__":
    main()
