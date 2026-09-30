def criptografia(caracter):
    if caracter == '/':
        return 0
    elif caracter != '\n':
        return 1
    else:
        return -1

estados = {"q0", "q1", "q2", "q3", "q4", "q5"}
alfabeto = {0, 1}
estado_inicial = "q0"
estado_final = {"q2", "q3", "q4", "q5"}
funcao = {
    "q0": [{"q1"}, set(), set()],
    "q1": [{"q2"}, set(), set()],
    "q2": [set(), set(), {"q3", "q5"}],
    "q3": [{"q4"}, {"q4"}, set()],
    "q4": [set(), set(), {"q3", "q5"}],
    "q5": [set(), set(), set()]
}

string = "// TODO: fix bug"

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