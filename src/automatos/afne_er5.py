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

string = "import"

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