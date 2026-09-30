def criptografia(caracter):
    if caracter in ['+', '-']:
        return 0
    elif caracter.isascii() and caracter.isdigit():
        return 1
    elif caracter == '.':
        return 2
    elif caracter in ['e', 'E']:
        return 3
    else:
        return -1

# Colunas: 0 = sinal, 1 = dígito, 2 = ponto, 3 = expoente (e/E), 4 = ε
estados = {f"q{i}" for i in range(22)}
alfabeto = {0, 1, 2, 3}
estado_inicial = "q0"
estado_final = {"q17"}
funcao = {
    # sinal opcional
    "q0":  [{"q1"}, set(), set(), set(), {"q1"}],
    # escolhe o formato: "3.14" (q2), ".5" (q12) ou "1e10" (q15)
    "q1":  [set(), set(), set(), set(), {"q2", "q12", "q15"}],
    # formato 1: dígitos + ponto + dígitos opcionais
    "q2":  [set(), {"q3"}, set(), set(), set()],
    "q3":  [set(), set(), set(), set(), {"q4", "q5"}],
    "q4":  [set(), {"q4"}, set(), set(), {"q5"}],
    "q5":  [set(), set(), {"q7"}, set(), set()],
    "q7":  [set(), {"q8"}, set(), set(), {"q11"}],
    "q8":  [set(), set(), set(), set(), {"q9", "q11"}],
    "q9":  [set(), {"q10"}, set(), set(), {"q11"}],
    "q10": [set(), set(), set(), set(), {"q9", "q11"}],
    "q11": [set(), set(), set(), set(), {"q6"}],
    # formato 2: ponto + dígitos
    "q12": [set(), set(), {"q13"}, set(), set()],
    "q13": [set(), {"q14"}, set(), set(), set()],
    "q14": [set(), set(), set(), set(), {"q13", "q6"}],
    # fim da mantissa com ponto: expoente é opcional
    "q6":  [set(), set(), set(), set(), {"q17", "q18"}],
    # formato 3: dígitos + expoente obrigatório
    "q15": [set(), {"q16"}, set(), set(), set()],
    "q16": [set(), set(), set(), set(), {"q15", "q18"}],
    # expoente: e/E + sinal opcional + dígitos
    "q18": [set(), set(), set(), {"q19"}, set()],
    "q19": [{"q20"}, set(), set(), set(), {"q20"}],
    "q20": [set(), {"q21"}, set(), set(), set()],
    "q21": [set(), set(), set(), set(), {"q20", "q17"}],
    # final
    "q17": [set(), set(), set(), set(), set()],
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
    string = "-3.14e+10"

    if aceita(string):
        print("Cadeia aceita")
    else:
        print("Cadeia nao aceita")
