"""Testes das 5 linguagens: a ER e o AFNε precisam reconhecer exatamente a mesma linguagem.

Duas verificações para cada ER:
1. Casos escolhidos à mão (CASOS_TESTE, em validators.py): 6+ aceitas, 6+ rejeitadas e casos-limite.
   Cada caso é conferido na ER e no AFNε.
2. Cadeias aleatórias: milhares de cadeias montadas com símbolos "perigosos" de cada linguagem.
   Para cada uma, a resposta da ER tem que ser igual à do AFNε.
"""

import random

import pytest

from automatos import afne_er1, afne_er2, afne_er3
from terminal_ER.validators import CASOS_TESTE

# AFNε de cada ER, na mesma ordem de CASOS_TESTE.
AFNES = [afne_er1.aceita, afne_er2.aceita, afne_er3.aceita]

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


GERADORES = [
    lambda: aleatorias(list("abzABZ019_-ç² ")),
    lambda: quase_tokens() + aleatorias(list("sk_liveA9")),
    lambda: aleatorias(list("+-.eEx") + list("0123456789") * 2, max_pedacos=8),
]


@pytest.mark.parametrize("indice", range(len(AFNES)), ids=[f"ER-0{i + 1}" for i in range(len(AFNES))])
def test_er_e_afne_concordam_em_cadeias_aleatorias(indice):
    nome, er, _ = CASOS_TESTE[indice]
    afne = AFNES[indice]
    for cadeia in GERADORES[indice]():
        assert er(cadeia) == afne(cadeia), f"{nome}: ER e AFNε discordam em {cadeia!r}"
