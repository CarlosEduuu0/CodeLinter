import re

CAMEL_CASE_PATTERN: str = r"[a-z][a-zA-Z0-9]*"
def validar_identificador(cadeia: str) -> bool:
    """Valida se a cadeia inteira é um identificador camelCase válido."""
    return bool(
        re.fullmatch(CAMEL_CASE_PATTERN, cadeia)
    )



SK_LIVE_PATTERN: str = r"sk_live_[0-9a-zA-Z]{24}"

def validar_sk_live(cadeia: str) -> bool:
    """Valida se a cadeia corresponde exatamente ao formato de token da Stripe."""
    return bool(re.fullmatch(SK_LIVE_PATTERN, cadeia))


FLOAT_PATTERN: str = r"[+-]?[0-9]+\.[0-9]+"

def validar_ponto_flutuante(cadeia: str) -> bool:
    """Valida números decimais com sinal opcional, como -12.50 ou 3.14."""
    return bool(re.fullmatch(FLOAT_PATTERN, cadeia))


MODULE_IMPORT_PATTERN: str = r"import\s+[a-zA-Z0-9_.]+(\s*,\s*[a-zA-Z0-9_.]+)*"

def validar_import(cadeia: str) -> bool:
    """Valida se a linha é um import Python de um ou mais módulos (import os, sys)."""
    return bool(re.fullmatch(MODULE_IMPORT_PATTERN, cadeia))



COMMENT_PATTERN: str = r"(//.*|/\*[\s\S]*?\*/)"

def validar_comentario(cadeia: str) -> bool:
    """Valida se a cadeia é um comentário de linha ou de bloco completo."""
    return bool(re.fullmatch(COMMENT_PATTERN, cadeia))

# Casos de teste de cada ER: (cadeia, esperado).
# Usados aqui no __main__ e também pelos testes automatizados em tests/.
CASOS_TESTE = [
    ("ER-01: Identificadores", validar_identificador, [
        # Aceitas
        ("totalValue", True), ("userName", True), ("v1", True),
        ("getHTTPResponse2", True), ("a1b2c3", True),
        ("x", True),                  # caso-limite: menor identificador possível
        # Rejeitadas
        ("2nota", False), ("nome-completo", False), ("User", False),
        ("user_id", False),           # snake_case não é camelCase
        ("ação", False),              # caso-limite: letra fora do alfabeto ASCII
        ("", False),                  # caso-limite: cadeia vazia
    ]),
    ("ER-02: Token API (sk_live)", validar_sk_live, [
        # Aceitas
        ("sk_live_1234567890abcdef12345678", True),
        ("sk_live_ABCDEFGHIJKLMNOPQRSTUVWX", True),
        ("sk_live_a1B2c3D4e5F6g7H8i9J0k1L2", True),
        ("sk_live_000000000000000000000000", True),
        ("sk_live_ZzZzZzZzZzZzZzZzZzZzZzZz", True),
        ("sk_live_sklivesklivesklivesklive", True),  # caso-limite: sufixo com as letras do prefixo
        # Rejeitadas
        ("sk_test_1234567890abcdef12345678", False),
        ("sk_live_curto", False),
        ("sk_live_12345678901234567890123", False),   # caso-limite: 23 caracteres
        ("sk_live_1234567890abcdef123456789", False),  # caso-limite: 25 caracteres
        ("sk_live_1234567890!@#$%^&*()123", False),
        ("sk_live_1234567890abcdef1234567_", False),  # "_" não é alfanumérico
        ("SK_LIVE_1234567890abcdef12345678", False),  # prefixo em maiúsculas
        ("sk_live_skliveskliveskliveskli", False),  # 22 caracteres com as letras do prefixo
        ("", False),
    ]),
    ("ER-03: Número decimal", validar_ponto_flutuante, [
        # Aceitas
        ("-12.50", True), ("3.14", True), ("+0.5", True), ("0.0005", True),
        ("1234567.89", True),
        ("0.0", True),                # caso-limite: menor decimal possível (1 dígito de cada lado)
        # Rejeitadas
        ("--3.14", False), ("3.14.15", False), ("1e10", False),
        ("42", False),                # caso-limite: inteiro não é decimal
        (".5", False),                # caso-limite: falta a parte inteira
        ("3.", False),                # caso-limite: faltam as casas decimais
        ("", False),
    ]),
    ("ER-04: Import de módulo (Python)", validar_import, [
        # Aceitas
        ("import math", True),
        ("import os.path", True),
        ("import os, sys", True),
        ("import os,sys,json", True),
        ("import numpy_v2", True),
        ("import a", True),                  # caso-limite: módulo de 1 caractere
        # Rejeitadas
        ("import", False),
        ("require('fs')", False),
        ("from os import path", False),      # outra forma de import, fora desta linguagem
        ("include <stdio.h>", False),
        ("import os,", False),               # caso-limite: vírgula sem o próximo módulo
        ("import os sys", False),            # módulos sem vírgula
        ("imports math", False),             # palavra-chave errada
        ("", False),
    ]),
    ("ER-05: Comentários", validar_comentario, [
        # Aceitas
        ("// comentario simples", True),
        ("/* bloco curto */", True),
        ("/* bloco\nmultilinha */", True),
        ("// TODO: corrigir", True),
        ("//", True),                 # caso-limite: comentário de linha vazio
        ("/**/", True),               # caso-limite: bloco vazio
        # Rejeitadas
        ("int x = 10; // inline", False),
        ("/* sem fechar", False),
        ("comentario sem barra", False),
        ("*/ bloco invertido /*", False),
        ("/*/", False),               # caso-limite: o '*' da abertura não serve para fechar
        ("// linha\noutra linha", False),  # comentário de linha não atravessa a quebra
        ("", False),
    ])
]

if __name__ == "__main__":
    for nome_er, funcao, casos in CASOS_TESTE:
        print(f"=== {nome_er} ===")
        for cadeia, esperado in casos:
            resultado = funcao(cadeia)
            status = "PASSOU" if resultado == esperado else "FALHOU"
            print(f"  [{status}] Entrada: {repr(cadeia)} -> Retorno: {resultado}")
        print()