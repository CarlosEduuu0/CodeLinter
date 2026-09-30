def criptografia(caracter):
    if caracter.islower():
        return 0
    elif caracter.isupper():
        return 1
    elif caracter.isdigit():
        return 2
    else:
        return -1

estados = {"q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8"}
alfabeto = {0, 1, 2}
estado_inicial = "q0"
estado_final = {"q1", "q4", "q6", "q7", "q8"}
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

string = "userName"

estado_atual = {estado_inicial}
rejeitado = True

for i in string:
    for j in list(estado_atual):
        estado_atual = estado_atual.union(funcao[j][-1])
    proximos = set()
    idx = criptografia(i)
    if idx == -1:
        estado_atual = set()
        break
    for k in estado_atual:
        proximos = proximos.union(funcao[k][idx])
    estado_atual = proximos

for j in list(estado_atual):
    estado_atual = estado_atual.union(funcao[j][-1])

for i in estado_atual:
    if i in estado_final:
        rejeitado = False

if rejeitado:
    print("Cadeia nao aceita")
else:
    print("Cadeia aceita")