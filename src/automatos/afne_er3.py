def criptografia(caracter):
    if caracter in ['+', '-']:
        return 0
    elif caracter.isdigit():
        return 1
    elif caracter == '.':
        return 2
    else:
        return -1

estados = {f"q{i}" for i in range(12)}
alfabeto = {0, 1, 2}
estado_inicial = "q0"
estado_final = {"q3", "q4", "q5", "q8", "q9", "q10", "q11"}
funcao = {
    "q0":  [{"q1"}, set(), set(), {"q1"}],
    "q1":  [set(), set(), set(), {"q2"}],
    "q2":  [set(), {"q3"}, set(), set()],
    "q3":  [set(), set(), set(), {"q4", "q5"}],
    "q4":  [set(), {"q4"}, set(), {"q5"}],
    "q5":  [set(), set(), {"q7"}, set()],
    "q6":  [set(), set(), set(), set()],
    "q7":  [set(), {"q8"}, set(), set()],
    "q8":  [set(), set(), set(), {"q9", "q11"}],
    "q9":  [set(), {"q10"}, set(), {"q11"}],
    "q10": [set(), set(), set(), {"q9", "q11"}],
    "q11": [set(), set(), set(), set()]
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
    string = "-12.50"

    if aceita(string):
        print("Cadeia aceita")
    else:
        print("Cadeia nao aceita")
