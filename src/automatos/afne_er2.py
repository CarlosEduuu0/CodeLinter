def criptografia(caracter):
    mapeamento = {'s': 0, 'k': 1, '_': 2, 'l': 3, 'i': 4, 'v': 5, 'e': 6}
    if caracter in mapeamento:
        return mapeamento[caracter]
    elif caracter.isascii() and caracter.isalnum():
        return 7
    else:
        return -1

ALFA_NUM = {0, 1, 3, 4, 5, 6, 7}

def gerar_transicao_sufixo(proximo_estado):
    trans = [set() for _ in range(9)]
    for idx in ALFA_NUM:
        trans[idx] = {proximo_estado}
    return trans

TAMANHO_SUFIXO = 24

estados = {f"q{i}" for i in range(8 + TAMANHO_SUFIXO + 1)}
alfabeto = set(range(8))
estado_inicial = "q0"
estado_final = {"q32"}
funcao = {
    "q0":  [{"q1"}, set(), set(), set(), set(), set(), set(), set(), set()],
    "q1":  [set(), {"q2"}, set(), set(), set(), set(), set(), set(), set()],
    "q2":  [set(), set(), {"q3"}, set(), set(), set(), set(), set(), set()],
    "q3":  [set(), set(), set(), {"q4"}, set(), set(), set(), set(), set()],
    "q4":  [set(), set(), set(), set(), {"q5"}, set(), set(), set(), set()],
    "q5":  [set(), set(), set(), set(), set(), {"q6"}, set(), set(), set()],
    "q6":  [set(), set(), set(), set(), set(), set(), {"q7"}, set(), set()],
    "q7":  [set(), set(), {"q8"}, set(), set(), set(), set(), set(), set()],
}

# Sufixo de 24 caracteres alfanuméricos: q8 -> q9 -> ... -> q32,
# um estado para cada caractere lido.
for n in range(8, 8 + TAMANHO_SUFIXO):
    funcao[f"q{n}"] = gerar_transicao_sufixo(f"q{n + 1}")
funcao["q32"] = [set() for _ in range(9)]


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
    string = "sk_live_a1B2c3D4e5F6g7H8i9J0k1L2"

    if aceita(string):
        print("Cadeia aceita")
    else:
        print("Cadeia nao aceita")
