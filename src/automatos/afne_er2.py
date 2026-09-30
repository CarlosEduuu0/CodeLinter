def criptografia(caracter):
    mapeamento = {'s': 0, 'k': 1, '_': 2, 'l': 3, 'i': 4, 'v': 5, 'e': 6}
    if caracter in mapeamento:
        return mapeamento[caracter]
    elif caracter.isalnum():
        return 7
    else:
        return -1

ALFA_NUM = {0, 1, 3, 4, 5, 6, 7}

def gerar_transicao_sufixo(proximo_estado):
    trans = [set() for _ in range(9)]
    for idx in ALFA_NUM:
        trans[idx] = {proximo_estado}
    return trans

estados = {f"q{i}" for i in range(13)}
alfabeto = set(range(8))
estado_inicial = "q0"
estado_final = {"q12"}
funcao = {
    "q0":  [{"q1"}, set(), set(), set(), set(), set(), set(), set(), set()],
    "q1":  [set(), {"q2"}, set(), set(), set(), set(), set(), set(), set()],
    "q2":  [set(), set(), {"q3"}, set(), set(), set(), set(), set(), set()],
    "q3":  [set(), set(), set(), {"q4"}, set(), set(), set(), set(), set()],
    "q4":  [set(), set(), set(), set(), {"q5"}, set(), set(), set(), set()],
    "q5":  [set(), set(), set(), set(), set(), {"q6"}, set(), set(), set()],
    "q6":  [set(), set(), set(), set(), set(), set(), {"q7"}, set(), set()],
    "q7":  [set(), set(), {"q8"}, set(), set(), set(), set(), set(), set()],
    "q8":  gerar_transicao_sufixo("q9"),
    "q9":  gerar_transicao_sufixo("q10"),
    "q10": gerar_transicao_sufixo("q11"),
    "q11": gerar_transicao_sufixo("q12"),
    "q12": [set() for _ in range(9)]
}

string = "sk_live_a1B2"

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