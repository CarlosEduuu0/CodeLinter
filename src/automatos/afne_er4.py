def criptografia(caracter):
    mapeamento = {'i': 0, 'm': 1, 'p': 2, 'o': 3, 'r': 4, 't': 5}
    return mapeamento.get(caracter, -1)

estados = {"q0", "q1", "q2", "q3", "q4", "q5", "q6"}
alfabeto = {0, 1, 2, 3, 4, 5}
estado_inicial = "q0"
estado_final = {"q6"}
funcao = {
    "q0": [{"q1"}, set(), set(), set(), set(), set(), set()],
    "q1": [set(), {"q2"}, set(), set(), set(), set(), set()],
    "q2": [set(), set(), {"q3"}, set(), set(), set(), set()],
    "q3": [set(), set(), set(), {"q4"}, set(), set(), set()],
    "q4": [set(), set(), set(), set(), {"q5"}, set(), set()],
    "q5": [set(), set(), set(), set(), set(), {"q6"}, set()],
    "q6": [set(), set(), set(), set(), set(), set(), set()]
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
    string = "import"

    if aceita(string):
        print("Cadeia aceita")
    else:
        print("Cadeia nao aceita")
