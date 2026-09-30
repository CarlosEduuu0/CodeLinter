"""Teste de fumaça: garante que o projeto importa e que as 5 linguagens estão registradas.

Os testes de cada linguagem (6 aceitas + 6 rejeitadas + caso-limite) entram na iteração q9.
"""

from main import LINGUAGENS, analisar


def test_cinco_linguagens_registradas():
    assert len(LINGUAGENS) == 5


def test_cadeia_vazia_nao_pertence_a_nenhuma_linguagem():
    assert not any(er or afne for _, _, er, afne in analisar(""))
