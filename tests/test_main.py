"""Testes do programa interativo (main.py): entradas, arquivo de exemplos e passo a passo."""

import pytest

from main import (
    ARQUIVO_EXEMPLOS,
    LINGUAGENS,
    analisar,
    erro_de_entrada,
    ler_exemplos,
    opcao_arquivo,
    passo_a_passo,
    preparar_entrada,
)
from terminal_ER.validators import CASOS_TESTE


def test_cinco_linguagens_registradas():
    assert len(LINGUAGENS) == 5


def test_entrada_vazia_gera_mensagem():
    assert erro_de_entrada("") is not None


def test_entrada_so_com_espacos_gera_mensagem():
    assert erro_de_entrada("   ") is not None


def test_entrada_normal_nao_gera_erro():
    assert erro_de_entrada("userName") is None


def test_bom_e_removido_e_barra_n_vira_quebra_de_linha():
    assert preparar_entrada("﻿import os") == "import os"
    assert preparar_entrada("/* a\\nb */") == "/* a\nb */"


def test_arquivo_ausente_gera_mensagem(tmp_path, capsys):
    opcao_arquivo(tmp_path / "nao_existe.txt")
    assert "não encontrado" in capsys.readouterr().out


def test_exemplos_tem_cadeias_aceitas_e_rejeitadas_de_cada_er():
    cadeias = ler_exemplos(ARQUIVO_EXEMPLOS)
    for indice in range(5):
        respostas = {analisar(cadeia)[indice][2] for cadeia in cadeias}
        assert respostas == {True, False}, LINGUAGENS[indice][0]


def test_er_e_afne_concordam_no_arquivo_de_exemplos():
    for cadeia in ler_exemplos(ARQUIVO_EXEMPLOS):
        for codigo, _, pela_er, pelo_afne in analisar(cadeia):
            assert pela_er == pelo_afne, f"{codigo}: {cadeia!r}"


@pytest.mark.parametrize("indice", range(5), ids=[f"ER-0{i + 1}" for i in range(5)])
def test_passo_a_passo_chega_ao_mesmo_resultado_de_aceita(indice, capsys):
    afne = LINGUAGENS[indice][3]
    for cadeia, _ in CASOS_TESTE[indice][2]:
        assert passo_a_passo(afne, cadeia) == afne.aceita(cadeia), repr(cadeia)
    capsys.readouterr()
