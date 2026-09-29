"""
Simulador de Autômato Finito Não-Determinístico com Transições Epsilon (AFNε).
Arquivo de referência original do projeto, integrado ao LogSentinel.
Permite executar a simulação clássica de AFNε para cadeias binárias
e também importar o motor avançado de src/afne.py.
"""

def criptografia(caracter):
    """Mapeia símbolos do alfabeto para índices da tabela de transição."""
    if caracter == "0":
        return 0
    elif caracter == "1":
        return 1
    else:
        return -1


estados = {"q0", "q1", "q2", "q3", "q4", "q5"}
alfabeto = {0, 1}
estado_inicial = "q0"
estado_final = {"q1", "q3"}

# Função de transição: [Destinos por '0', Destinos por '1', Destinos por 'ε']
funcao = {
    "q0": [set(), set(), {"q0", "q1", "q3"}],
    "q1": [{"q1"}, {"q2"}, {"q1"}],
    "q2": [{"q2"}, {"q1"}, {"q2"}],
    "q3": [{"q3"}, {"q4"}, {"q3"}],
    "q4": [{"q4"}, {"q5"}, {"q4"}],
    "q5": [{"q5"}, {"q3"}, {"q5"}]
}


def calcular_fecho_epsilon(estados_iniciais, transicoes):
    """Calcula o fecho epsilon de forma recursiva até convergência."""
    fecho = set(estados_iniciais)
    pilha = list(estados_iniciais)
    while pilha:
        atual = pilha.pop()
        destinos_eps = transicoes.get(atual, [set(), set(), set()])[-1]
        for dest in destinos_eps:
            if dest not in fecho:
                fecho.add(dest)
                pilha.append(dest)
    return fecho


def simular_afne(string_entrada: str, verboso: bool = True) -> bool:
    """Executa a simulação do AFNε sobre uma cadeia."""
    estado_atual = calcular_fecho_epsilon({estado_inicial}, funcao)
    
    if verboso:
        print(f"--- Simulação AFNε para cadeia: '{string_entrada}' ---")
        print(f"Estado Inicial com Fecho-ε: {estado_atual}")

    for idx, char in enumerate(string_entrada):
        idx_simbolo = criptografia(char)
        if idx_simbolo == -1:
            if verboso:
                print(f"Símbolo inválido '{char}' rejeitado pelo alfabeto.")
            return False

        # Mover por símbolo a partir de todos os estados alcançáveis
        proximos_estados = set()
        for estado in estado_atual:
            destinos = funcao[estado][idx_simbolo]
            proximos_estados = proximos_estados.union(destinos)

        # Aplicar fecho epsilon após o consumo do símbolo
        estado_atual = calcular_fecho_epsilon(proximos_estados, funcao)
        if verboso:
            print(f"Lendo '{char}' -> Estado atual: {estado_atual}")

    aceito = bool(estado_atual.intersection(estado_final))
    if verboso:
        if aceito:
            print(f"Resultado: Cadeia aceita! Estados finais atingidos: {estado_atual.intersection(estado_final)}")
        else:
            print(f"Resultado: Cadeia rejeitada. Estados finais: {estado_atual}")
    return aceito


if __name__ == "__main__":
    import sys
    cadeia_teste = sys.argv[1] if len(sys.argv) > 1 else "00010101"
    simular_afne(cadeia_teste)