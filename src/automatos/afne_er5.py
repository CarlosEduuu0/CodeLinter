def criptografia(caracter):
    if caracter == '/':
        return 0
    elif caracter == '*':
        return 1
    elif caracter == '\n':
        return 2
    else:
        return 3

# Colunas: 0 = '/', 1 = '*', 2 = quebra de linha, 3 = qualquer outro caractere, 4 = ε
estados = {f"q{i}" for i in range(12)}
alfabeto = {0, 1, 2, 3}
estado_inicial = "q0"
estado_final = {"q5", "q11"}
funcao = {
    "q0":  [{"q1"}, set(), set(), set(), set()],
    # depois da primeira '/': outra '/' abre comentário de linha, '*' abre bloco
    "q1":  [{"q2"}, {"q6"}, set(), set(), set()],
    # comentário de linha: qualquer caractere menos quebra de linha, repetido
    "q2":  [set(), set(), set(), set(), {"q3", "q5"}],
    "q3":  [{"q4"}, {"q4"}, set(), {"q4"}, set()],
    "q4":  [set(), set(), set(), set(), {"q3", "q5"}],
    "q5":  [set(), set(), set(), set(), set()],
    # comentário de bloco: qualquer caractere (inclusive quebra de linha), repetido
    "q6":  [set(), set(), set(), set(), {"q7", "q9"}],
    "q7":  [{"q8"}, {"q8"}, {"q8"}, {"q8"}, set()],
    "q8":  [set(), set(), set(), set(), {"q7", "q9"}],
    # fechamento '*/'
    "q9":  [set(), {"q10"}, set(), set(), set()],
    "q10": [{"q11"}, set(), set(), set(), set()],
    "q11": [set(), set(), set(), set(), set()],
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
    string = "// TODO: fix bug"

    if aceita(string):
        print("Cadeia aceita")
    else:
        print("Cadeia nao aceita")
