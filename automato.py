"""
automato.py - AFNε (Autômato Finito Não Determinístico com movimentos vazios).

A simulação segue a MESMA lógica do código-base da disciplina:
  estados, alfabeto, estado_inicial, estado_final, funcao (dict de conjuntos),
  estado_atual = {estado_inicial}; para cada símbolo: fecho-ε -> mover -> ...;
  a cadeia é aceita se algum estado atual pertence ao conjunto de finais.

Diferenças (generalizações necessárias):
  * o rótulo de uma transição é um símbolo literal ou uma classe finita "[a-z]"
    (abreviação de uniões), em vez de apenas 0/1;
  * o fecho-ε é calculado até o ponto fixo (o código-base aplica um único passo);
  * o AFNε é gerado a partir da ER formal pela construção de Thompson.
"""

EPS = "ε"          # movimento vazio (palavra vazia; não é o caractere 'ε' da entrada)
_CLASSES = {}      # cache: rótulo "[...]" -> conjunto de caracteres


# --------------------------------------------------------------------------
# Rótulos: literal ou classe finita
# --------------------------------------------------------------------------
def conjunto_da_classe(rotulo):
    """'[a-c]' -> {'a','b','c'} (intervalos e escapes com barra invertida)."""
    if rotulo not in _CLASSES:
        corpo, s, i = rotulo[1:-1], set(), 0
        while i < len(corpo):
            c = corpo[i]
            if c == "\\" and i + 1 < len(corpo):
                s.add(corpo[i + 1]); i += 2
            elif i + 2 < len(corpo) and corpo[i + 1] == "-":
                s.update(chr(k) for k in range(ord(c), ord(corpo[i + 2]) + 1)); i += 3
            else:
                s.add(c); i += 1
        _CLASSES[rotulo] = frozenset(s)
    return _CLASSES[rotulo]


def casa(rotulo, caractere):
    """Equivale ao 'criptografia(caracter)' do código-base: o símbolo lido pertence ao rótulo?"""
    if len(rotulo) > 1 and rotulo[0] == "[":
        return caractere in conjunto_da_classe(rotulo)
    return rotulo == caractere


# --------------------------------------------------------------------------
# Autômato
# --------------------------------------------------------------------------
def _num(nome):
    return int(nome[1:])


class AFNe:
    def __init__(self):
        self.estados = set()
        self.alfabeto = set()          # rótulos usados (literais e classes)
        self.estado_inicial = None
        self.estado_final = set()
        self.funcao = {}               # funcao[estado][rotulo] = {destinos}

    # -- construção ---------------------------------------------------------
    def novo_estado(self):
        nome = f"q{len(self.estados)}"
        self.estados.add(nome)
        self.funcao[nome] = {}
        return nome

    def adicionar(self, origem, rotulo, destino):
        self.funcao[origem].setdefault(rotulo, set()).add(destino)
        if rotulo != EPS:
            self.alfabeto.add(rotulo)

    def renumerar(self):
        """Renomeia os estados em largura a partir do inicial (q0 = inicial)."""
        ordem, visto, fila = [], {self.estado_inicial}, [self.estado_inicial]
        while fila:
            e = fila.pop(0)
            ordem.append(e)
            for rot in sorted(self.funcao[e], key=lambda r: (r != EPS, r)):
                for d in sorted(self.funcao[e][rot], key=_num):
                    if d not in visto:
                        visto.add(d); fila.append(d)
        mapa = {e: f"q{i}" for i, e in enumerate(ordem)}
        self.funcao = {mapa[e]: {r: {mapa[d] for d in ds} for r, ds in tr.items()}
                       for e, tr in self.funcao.items() if e in mapa}
        self.estados = set(mapa.values())
        self.estado_inicial = mapa[self.estado_inicial]
        self.estado_final = {mapa[e] for e in self.estado_final if e in mapa}

    # -- simulação (mesma lógica do código-base) ------------------------------
    def fecho_epsilon(self, conjunto):
        """União com os destinos de ε (funcao[j][ε]) repetida até não crescer."""
        fecho, pilha = set(conjunto), list(conjunto)
        while pilha:
            e = pilha.pop()
            for d in self.funcao[e].get(EPS, ()):
                if d not in fecho:
                    fecho.add(d); pilha.append(d)
        return fecho

    def mover(self, estados, simbolo):
        proximo = set()
        for e in estados:
            for rotulo, destinos in self.funcao[e].items():
                if rotulo != EPS and casa(rotulo, simbolo):
                    proximo |= destinos
        return proximo

    def aceita(self, cadeia, verbose=False):
        estado_atual = self.fecho_epsilon({self.estado_inicial})
        for simbolo in cadeia:
            if verbose:
                print(f"Estado_atual: {sorted(estado_atual, key=_num)}   lendo {simbolo!r}")
            estado_atual = self.fecho_epsilon(self.mover(estado_atual, simbolo))
            if not estado_atual:
                break
        if verbose:
            print(f"Estado_atual: {sorted(estado_atual, key=_num)}")
        return any(e in self.estado_final for e in estado_atual)

    # -- documentação -----------------------------------------------------------
    def resumo(self):
        trans = sum(len(ds) for tr in self.funcao.values() for ds in tr.values())
        eps = sum(len(tr.get(EPS, ())) for tr in self.funcao.values())
        return {"estados": len(self.estados), "transicoes": trans, "transicoes_epsilon": eps,
                "estado_inicial": self.estado_inicial, "estados_finais": sorted(self.estado_final, key=_num)}

    def tabela(self):
        """Função de transição no mesmo formato do código-base (dict de conjuntos)."""
        return {e: {r: sorted(ds, key=_num) for r, ds in self.funcao[e].items()}
                for e in sorted(self.funcao, key=_num)}

    def para_dot(self, titulo="AFNe"):
        esc = lambda r: r.replace("\\", "\\\\").replace('"', '\\"').replace(" ", "␣")
        L = [f'digraph "{titulo}" {{', "  rankdir=LR;", "  node [shape=circle];",
             "  __ini [shape=point];", f"  __ini -> {self.estado_inicial};"]
        for f in sorted(self.estado_final, key=_num):
            L.append(f"  {f} [shape=doublecircle];")
        arestas = {}
        for e in self.funcao:
            for r, ds in self.funcao[e].items():
                for d in ds:
                    arestas.setdefault((e, d), []).append(r)
        for (e, d), rots in sorted(arestas.items(), key=lambda x: (_num(x[0][0]), _num(x[0][1]))):
            L.append(f'  {e} -> {d} [label="{esc(",".join(sorted(rots)))}"];')
        L.append("}")
        return "\n".join(L)


# --------------------------------------------------------------------------
# ER formal -> AST -> AFNε (construção de Thompson)
# Sintaxe aceita (subconjunto comum ao motor `re` e à notação formal):
#   literal, \c (escape), [classe], (r), r|s, rs, r*, r+, r?, r{m}, r{m,n}
# --------------------------------------------------------------------------
class _Parser:
    def __init__(self, texto):
        self.t, self.i = texto, 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def alt(self):
        ramos = [self.cat()]
        while self.peek() == "|":
            self.i += 1
            ramos.append(self.cat())
        return ramos[0] if len(ramos) == 1 else ("alt", ramos)

    def cat(self):
        itens = []
        while self.peek() not in (None, "|", ")"):
            itens.append(self.rep())
        if not itens:
            return ("eps",)
        return itens[0] if len(itens) == 1 else ("cat", itens)

    def rep(self):
        no = self.atomo()
        while self.peek() in ("*", "+", "?", "{"):
            c = self.peek()
            if c == "{":
                fim = self.t.index("}", self.i)
                corpo = self.t[self.i + 1:fim]
                self.i = fim + 1
                m, virgula, n = corpo.partition(",")
                if virgula and not n:
                    raise ValueError("{m,} não é suportado (use * ou +)")
                no = ("rep", no, int(m), int(n) if virgula else int(m))
            else:
                self.i += 1
                no = ({"*": "star", "+": "plus", "?": "opt"}[c], no)
        return no

    def atomo(self):
        c = self.peek()
        if c == "(":
            self.i += 1
            no = self.alt()
            if self.peek() != ")":
                raise ValueError("parêntese não fechado")
            self.i += 1
            return no
        if c == "[":
            fim = self.t.index("]", self.i + 1)
            rotulo = self.t[self.i:fim + 1]
            self.i = fim + 1
            return ("lit", rotulo)
        if c == "\\":
            self.i += 2
            return ("lit", self.t[self.i - 1])
        if c in "*+?{}":
            raise ValueError(f"operador '{c}' sem operando na posição {self.i}")
        self.i += 1
        return ("lit", c)


def _thompson(afn, no):
    """Devolve (inicio, fim) do fragmento; cada chamada cria estados novos."""
    t = no[0]
    if t in ("lit", "eps"):
        i, f = afn.novo_estado(), afn.novo_estado()
        afn.adicionar(i, no[1] if t == "lit" else EPS, f)
        return i, f
    if t == "cat":
        pares = [_thompson(afn, x) for x in no[1]]
        for (_, fim), (ini, _) in zip(pares, pares[1:]):
            afn.adicionar(fim, EPS, ini)
        return pares[0][0], pares[-1][1]
    if t == "alt":
        i, f = afn.novo_estado(), afn.novo_estado()
        for x in no[1]:
            a, b = _thompson(afn, x)
            afn.adicionar(i, EPS, a); afn.adicionar(b, EPS, f)
        return i, f
    if t in ("star", "plus", "opt"):
        i, f = afn.novo_estado(), afn.novo_estado()
        a, b = _thompson(afn, no[1])
        afn.adicionar(i, EPS, a); afn.adicionar(b, EPS, f)
        if t in ("star", "opt"):
            afn.adicionar(i, EPS, f)
        if t in ("star", "plus"):
            afn.adicionar(b, EPS, a)
        return i, f
    if t == "rep":                       # r{m,n} = r^m (r?)^(n-m)
        _, x, lo, hi = no
        itens = [x] * lo + [("opt", x)] * (hi - lo)
        return _thompson(afn, ("cat", itens) if itens else ("eps",))
    raise ValueError(t)


def construir_afne(er):
    p = _Parser(er)
    ast = p.alt()
    if p.i != len(er):
        raise ValueError(f"caractere inesperado na posição {p.i}: {er[p.i]!r}")
    afn = AFNe()
    ini, fim = _thompson(afn, ast)
    afn.estado_inicial, afn.estado_final = ini, {fim}
    afn.renumerar()
    return afn
