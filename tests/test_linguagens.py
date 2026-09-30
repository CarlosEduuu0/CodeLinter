"""Testes das 5 linguagens: a ER e o AFNε precisam reconhecer exatamente a mesma linguagem.

Duas verificações para cada ER:
1. Casos escolhidos à mão (CASOS_TESTE, em validators.py): 6+ aceitas, 6+ rejeitadas e casos-limite.
   Cada caso é conferido na ER e no AFNε.
2. Cadeias aleatórias: milhares de cadeias montadas com símbolos "perigosos" de cada linguagem.
   Para cada uma, a resposta da ER tem que ser igual à do AFNε.
"""

import random

import pytest

from automatos import afne_er1, afne_er2, afne_er3, afne_er4, afne_er5
from terminal_ER.validators import CASOS_TESTE

# AFNε de cada ER, na mesma ordem de CASOS_TESTE.
AFNES = [afne_er1.aceita, afne_er2.aceita, afne_er3.aceita, afne_er4.aceita, afne_er5.aceita]

CASOS = [
    pytest.param(er, afne, cadeia, esperado, id=f"{nome.split(':')[0]}-{cadeia!r}")
    for (nome, er, casos), afne in zip(CASOS_TESTE, AFNES)
    for cadeia, esperado in casos
]


@pytest.mark.parametrize("er, afne, cadeia, esperado", CASOS)
def test_caso_na_er_e_no_afne(er, afne, cadeia, esperado):
    assert er(cadeia) == esperado, "a ER respondeu diferente do esperado"
    assert afne(cadeia) == esperado, "o AFNε respondeu diferente do esperado"


def test_minimo_de_casos_por_er():
    """A lauda pede no mínimo 6 aceitas e 6 rejeitadas por ER."""
    for nome, _, casos in CASOS_TESTE[: len(AFNES)]:
        aceitas = sum(1 for _, esperado in casos if esperado)
        rejeitadas = len(casos) - aceitas
        assert aceitas >= 6 and rejeitadas >= 6, nome


# ---------- cadeias aleatórias ----------

def aleatorias(pedacos, quantidade=3000, max_pedacos=10, semente=42):
    """Gera cadeias juntando pedaços sorteados (letras, símbolos ou palavras inteiras)."""
    sorteio = random.Random(semente)
    return [
        "".join(sorteio.choice(pedacos) for _ in range(sorteio.randint(0, max_pedacos)))
        for _ in range(quantidade)
    ]


def quase_tokens(quantidade=3000, semente=42):
    """Prefixos parecidos com sk_live_ + sufixos de 22 a 26 caracteres (em volta dos 24)."""
    sorteio = random.Random(semente)
    prefixos = ["sk_live_"] * 5 + ["sk_test_", "SK_LIVE_", "sk_live", "sk__live_", "live_", ""]
    return [
        sorteio.choice(prefixos)
        + "".join(sorteio.choice("aZ09sklivAz8" * 5 + "_!ç") for _ in range(sorteio.randint(22, 26)))
        for _ in range(quantidade)
    ]


def mutacoes(indice, quantidade=3000, semente=42):
    """Pega as cadeias aceitas da ER e aplica de 1 a 3 mutações (apagar, trocar ou inserir)."""
    sorteio = random.Random(semente)
    validas = [cadeia for cadeia, esperado in CASOS_TESTE[indice][2] if esperado]
    simbolos = "aZ09_ .,'\"(){}*=/-+eE\n\tç"
    resultado = []
    for _ in range(quantidade):
        cadeia = list(sorteio.choice(validas))
        for _ in range(sorteio.randint(1, 3)):
            pos = sorteio.randint(0, len(cadeia))
            acao = sorteio.choice(["apagar", "trocar", "inserir"])
            if acao == "inserir" or not cadeia:
                cadeia.insert(pos, sorteio.choice(simbolos))
            elif acao == "apagar":
                del cadeia[min(pos, len(cadeia) - 1)]
            else:
                cadeia[min(pos, len(cadeia) - 1)] = sorteio.choice(simbolos)
        resultado.append("".join(cadeia))
    return resultado


def imports_aleatorios(quantidade=4000, semente=42):
    """Começa com algo parecido com 'import' e junta nomes, vírgulas e espaços."""
    sorteio = random.Random(semente)
    inicios = ["import ", "import ", "import ", "import", "imports ", "from ", "impor ", ""]
    pedacos = ["os", "sys", "path", "import", ".", "_", "x1", ",", ",", " ", " ", "\t",
               "ç", "(", "'", "-"]
    return [
        sorteio.choice(inicios)
        + "".join(sorteio.choice(pedacos) for _ in range(sorteio.randint(0, 8)))
        for _ in range(quantidade)
    ]


GERADORES = [
    lambda: aleatorias(list("abzABZ019_-ç² ")),
    lambda: quase_tokens() + aleatorias(list("sk_liveA9")),
    lambda: aleatorias(list("+-.eEx") + list("0123456789") * 2, max_pedacos=8),
    lambda: imports_aleatorios(),
    lambda: aleatorias(list("/*\nab ") + ["//", "/*", "*/"], max_pedacos=8),
]


@pytest.mark.parametrize("indice", range(len(AFNES)), ids=[f"ER-0{i + 1}" for i in range(len(AFNES))])
def test_er_e_afne_concordam_em_cadeias_aleatorias(indice):
    nome, er, _ = CASOS_TESTE[indice]
    afne = AFNES[indice]
    for cadeia in GERADORES[indice]() + mutacoes(indice):
        assert er(cadeia) == afne(cadeia), f"{nome}: ER e AFNε discordam em {cadeia!r}"
