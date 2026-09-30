"""CodeLinter: reconhece trechos de código-fonte com Expressões Regulares e AFNε.

Uso:
    python main.py
"""

from terminal_ER.validators import (
    validar_comentario,
    validar_identificador,
    validar_import,
    validar_ponto_flutuante,
    validar_sk_live,
)

# As 5 linguagens do projeto. Cada entrada liga o nome da linguagem à sua ER.
# Na iteração q2 cada linha ganha também o AFNε correspondente.
LINGUAGENS = [
    ("ER-01", "Identificador camelCase", validar_identificador),
    ("ER-02", "Token Stripe sk_live_", validar_sk_live),
    ("ER-03", "Número decimal/científico", validar_ponto_flutuante),
    ("ER-04", "Import de módulo", validar_import),
    ("ER-05", "Comentário", validar_comentario),
]


def analisar(cadeia: str) -> list[tuple[str, str, bool]]:
    """Testa a cadeia contra as 5 linguagens e devolve (código, nome, aceita)."""
    return [(codigo, nome, er(cadeia)) for codigo, nome, er in LINGUAGENS]


def exibir(cadeia: str, resultados: list[tuple[str, str, bool]]) -> None:
    print(f'\nEntrada: "{cadeia}"')
    for codigo, nome, aceita in resultados:
        marca = "✓" if aceita else "✗"
        print(f"  {codigo}  {nome:<28} {marca}")
    reconhecidas = [nome for _, nome, aceita in resultados if aceita]
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
