# isascii() garante o mesmo alfabeto da ER ([a-z], [A-Z], [0-9]):
# sem ele, 'ç'.islower() e '²'.isdigit() também dariam True.
def criptografia(caracter):
    if caracter.isascii() and caracter.islower():
        return 0
    elif caracter.isascii() and caracter.isupper():
        return 1
    elif caracter.isascii() and caracter.isdigit():
        return 2
    else:
        return -1

estados = {"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8"}
alfabeto = {0, 1, 2}
estado_inicial = "q0"
estado_final = {"q8"}
funcao = {
    "q0": [{"q1"}, set(), set(), set()],
    "q1": [set(), set(), set(), {"q2", "q8"}],
    "q2": [set(), set(), set(), {"q3", "q5"}],
    "q3": [{"q4"}, {"q4"}, set(), set()],
    "q4": [set(), set(), set(), {"q7"}],
    "q5": [set(), set(), {"q6"}, set()],
    "q6": [set(), set(), set(), {"q7"}],
    "q7": [set(), set(), set(), {"q2", "q8"}],
    "q8": [set(), set(), set(), set()]
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
    string = "userName"

    if aceita(string):
        print("Cadeia aceita")
    else:
        print("Cadeia nao aceita")
