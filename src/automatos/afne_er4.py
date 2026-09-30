# Letras das palavras-chave import, from, const, let, var e require:
# cada uma tem coluna própria, porque nas palavras-chave importa QUAL letra veio.
LETRAS_CHAVE = "importfcnslevaqu"
SIMBOLOS = ".,*{}()/-"


def criptografia(caracter):
    if caracter in LETRAS_CHAVE:
        return LETRAS_CHAVE.index(caracter)            # colunas 0 a 15
    elif caracter.isascii() and (caracter.isalnum() or caracter == '_'):
        return 16                                      # outra letra, dígito ou _
    elif caracter in SIMBOLOS:
        return 17 + SIMBOLOS.index(caracter)           # colunas 17 a 25
    elif caracter in ['"', "'"]:
        return 26
    elif caracter == '=':
        return 27
    elif caracter.isspace():
        return 28
    else:
        return -1

# Coluna 29 = ε
# Classes de caracteres da ER, como conjuntos de colunas:
ALFANUM = set(range(17))                         # [a-zA-Z0-9_]
ESPACO = {28}                                    # \s
ASPAS = {26}                                     # ['"]
CAMINHO = ALFANUM | {17, 24, 25}                 # [a-zA-Z0-9_./-]
NOMES_JS = ALFANUM | {20, 21, 28, 18, 19}        # [a-zA-Z0-9_{}\s,*]
NOMES_REQUIRE = ALFANUM | {20, 21, 28, 18}       # [a-zA-Z0-9_{}\s,]
MODULO_PY = ALFANUM | {17}                       # [a-zA-Z0-9_.]
NOMES_PY = ALFANUM | {18, 28, 19, 22, 23}        # [a-zA-Z0-9_,\s*()]
LISTA_IMPORT = ALFANUM | {17, 18, 28}            # [a-zA-Z0-9_.,\s]


def letra(caracter):
    return {criptografia(caracter)}


def linha(*transicoes, vazio=()):
    """Monta a linha de um estado: pares (colunas, destino) e os destinos por ε."""
    trans = [set() for _ in range(30)]
    for colunas, destino in transicoes:
        for idx in colunas:
            trans[idx].add(destino)
    trans[29] = set(vazio)
    return trans


estados = {f"q{i}" for i in range(66)}
alfabeto = set(range(29))
estado_inicial = "q0"
estado_final = {"q65"}
funcao = {
    # a primeira letra escolhe o ramo: import, from, const, let ou var
    "q0":  linha((letra('i'), "q1"), (letra('f'), "q22"), (letra('c'), "q37"),
                 (letra('l'), "q42"), (letra('v'), "q45")),

    # ---- "import" (q0..q6, como no AFNε original) ----
    "q1":  linha((letra('m'), "q2")),
    "q2":  linha((letra('p'), "q3")),
    "q3":  linha((letra('o'), "q4")),
    "q4":  linha((letra('r'), "q5")),
    "q5":  linha((letra('t'), "q6")),
    "q6":  linha((ESPACO, "q7")),
    # depois de "import ": nomes + from (q8), direto o 'módulo' (q16) ou lista Python (q20)
    "q7":  linha((ESPACO, "q7"), vazio={"q8", "q16", "q20"}),

    # ramo 1: import NOMES from 'módulo'   (JavaScript)
    "q8":  linha((NOMES_JS, "q9")),
    "q9":  linha((NOMES_JS, "q9"), (ESPACO, "q10")),
    "q10": linha((ESPACO, "q10"), (letra('f'), "q11")),
    "q11": linha((letra('r'), "q12")),
    "q12": linha((letra('o'), "q13")),
    "q13": linha((letra('m'), "q14")),
    "q14": linha((ESPACO, "q15")),
    "q15": linha((ESPACO, "q15"), vazio={"q16"}),
    # 'módulo' entre aspas
    "q16": linha((ASPAS, "q17")),
    "q17": linha((CAMINHO, "q18")),
    "q18": linha((CAMINHO, "q18"), (ASPAS, "q19")),
    "q19": linha(vazio={"q65"}),

    # ramo 4: import os, sys   (Python)
    "q20": linha((LISTA_IMPORT, "q21")),
    "q21": linha((LISTA_IMPORT, "q21"), vazio={"q65"}),

    # ---- ramo 3: from módulo import nomes   (Python) ----
    "q22": linha((letra('r'), "q23")),
    "q23": linha((letra('o'), "q24")),
    "q24": linha((letra('m'), "q25")),
    "q25": linha((ESPACO, "q26")),
    "q26": linha((ESPACO, "q26"), (MODULO_PY, "q27")),
    "q27": linha((MODULO_PY, "q27"), (ESPACO, "q28")),
    "q28": linha((ESPACO, "q28"), (letra('i'), "q29")),
    "q29": linha((letra('m'), "q30")),
    "q30": linha((letra('p'), "q31")),
    "q31": linha((letra('o'), "q32")),
    "q32": linha((letra('r'), "q33")),
    "q33": linha((letra('t'), "q34")),
    "q34": linha((ESPACO, "q35")),
    "q35": linha((ESPACO, "q35"), (NOMES_PY, "q36")),
    "q36": linha((NOMES_PY, "q36"), vazio={"q65"}),

    # ---- ramo 2: const/let/var nomes = require('módulo')   (Node.js) ----
    "q37": linha((letra('o'), "q38")),
    "q38": linha((letra('n'), "q39")),
    "q39": linha((letra('s'), "q40")),
    "q40": linha((letra('t'), "q41")),
    "q41": linha(vazio={"q48"}),
    "q42": linha((letra('e'), "q43")),
    "q43": linha((letra('t'), "q44")),
    "q44": linha(vazio={"q48"}),
    "q45": linha((letra('a'), "q46")),
    "q46": linha((letra('r'), "q47")),
    "q47": linha(vazio={"q48"}),
    "q48": linha((ESPACO, "q49")),
    "q49": linha((ESPACO, "q49"), (NOMES_REQUIRE, "q50")),
    "q50": linha((NOMES_REQUIRE, "q50"), vazio={"q51"}),
    "q51": linha((ESPACO, "q51"), ({27}, "q52")),
    "q52": linha((ESPACO, "q52"), (letra('r'), "q53")),
    "q53": linha((letra('e'), "q54")),
    "q54": linha((letra('q'), "q55")),
    "q55": linha((letra('u'), "q56")),
    "q56": linha((letra('i'), "q57")),
    "q57": linha((letra('r'), "q58")),
    "q58": linha((letra('e'), "q59")),
    "q59": linha(({22}, "q60")),
    "q60": linha((ASPAS, "q61")),
    "q61": linha((CAMINHO, "q62")),
    "q62": linha((CAMINHO, "q62"), (ASPAS, "q63")),
    "q63": linha(({23}, "q64")),
    "q64": linha(vazio={"q65"}),

    # final
    "q65": linha(),
}


def fecho_vazio(estado_atual):
    # Fecho-ε: segue as transições vazias (última coluna de cada linha)
    # repetindo até não aparecer nenhum estado novo.
    anterior = set()
    while estado_atual != anterior:
        anterior = estado_atual
        for j in list(estado_atual):
            estado_atual = estado_atual.union(funcao[j][-1])
    return estado_atual


def aceita(string):
    estado_atual = {estado_inicial}
    rejeitado = True

    for i in string:
        estado_atual = fecho_vazio(estado_atual)
        proximos = set()
        idx = criptografia(i)
        if idx == -1:
            return False
        for k in estado_atual:
            proximos = proximos.union(funcao[k][idx])
        estado_atual = proximos

    estado_atual = fecho_vazio(estado_atual)

    for i in estado_atual:
        if i in estado_final:
            rejeitado = False

    return not rejeitado


if __name__ == "__main__":
    string = "import React from 'react'"

    if aceita(string):
        print("Cadeia aceita")
    else:
        print("Cadeia nao aceita")
