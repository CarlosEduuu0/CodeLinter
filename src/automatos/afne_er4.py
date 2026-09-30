def criptografia(caracter):
    mapeamento = {'i': 0, 'm': 1, 'p': 2, 'o': 3, 'r': 4, 't': 5}
    if caracter in mapeamento:
        return mapeamento[caracter]
    elif caracter.isascii() and (caracter.isalnum() or caracter in ['_', '.']):
        return 6
    elif caracter.isspace():
        return 7
    elif caracter == ',':
        return 8
    else:
        return -1

# Colunas: 0 a 5 = letras de "import", 6 = outro caractere de nome ([a-zA-Z0-9_.]),
# 7 = espaço, 8 = vírgula, 9 = ε.
# As colunas 0 a 6 juntas formam os caracteres de nome de módulo.
estados = {f"q{i}" for i in range(12)}
alfabeto = set(range(9))
estado_inicial = "q0"
estado_final = {"q11"}
funcao = {
    # "import", letra por letra (q0..q6, como no AFNε original)
    "q0":  [{"q1"}, set(), set(), set(), set(), set(), set(), set(), set(), set()],
    "q1":  [set(), {"q2"}, set(), set(), set(), set(), set(), set(), set(), set()],
    "q2":  [set(), set(), {"q3"}, set(), set(), set(), set(), set(), set(), set()],
    "q3":  [set(), set(), set(), {"q4"}, set(), set(), set(), set(), set(), set()],
    "q4":  [set(), set(), set(), set(), {"q5"}, set(), set(), set(), set(), set()],
    "q5":  [set(), set(), set(), set(), set(), {"q6"}, set(), set(), set(), set()],
    # espaço(s) depois de import
    "q6":  [set(), set(), set(), set(), set(), set(), set(), {"q7"}, set(), set()],
    "q7":  [{"q8"}, {"q8"}, {"q8"}, {"q8"}, {"q8"}, {"q8"}, {"q8"}, {"q7"}, set(), set()],
    # nome do módulo; depois dele: fim (q11) ou mais um módulo (q9)
    "q8":  [{"q8"}, {"q8"}, {"q8"}, {"q8"}, {"q8"}, {"q8"}, {"q8"}, set(), set(), {"q9", "q11"}],
    # espaços opcionais, vírgula, espaços opcionais
    "q9":  [set(), set(), set(), set(), set(), set(), set(), {"q9"}, {"q10"}, set()],
    "q10": [{"q8"}, {"q8"}, {"q8"}, {"q8"}, {"q8"}, {"q8"}, {"q8"}, {"q10"}, set(), set()],
    # final
    "q11": [set(), set(), set(), set(), set(), set(), set(), set(), set(), set()]
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
    string = "import os, sys"

    if aceita(string):
        print("Cadeia aceita")
    else:
        print("Cadeia nao aceita")
