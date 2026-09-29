"""
expressoes.py - As 5 Expressões Regulares do LogSentinel.

Fonte única da verdade: o texto em `sintaxe` é (1) compilado pelo motor `re` do
Python, usado no programa, e (2) lido pelo construtor de AFNε (automato.py).
Assim, ER do código, AFNε e testes representam a mesma linguagem.
Sem retroreferências, lookaround, recursão ou condicionais.
"""
import re
from urllib.parse import unquote_plus

from automato import construir_afne


# ---- pré-processamentos (não fazem parte da ER; definem a cadeia analisada) ----
def _nenhum(t):
    return t


def _minusculas(t):
    return t.lower()


def _decodificar_minusculas(t):
    return unquote_plus(t).lower()


# ---- fragmentos de sintaxe (motor re) ----
OCTETO = r"(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])"
IPV4 = OCTETO + r"\." + OCTETO + r"\." + OCTETO + r"\." + OCTETO + r"(:[0-9]{1,5})?"

ISO = (r"[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])"
       r"T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]+)?(Z|[+-][0-9]{2}:[0-9]{2})")
CLF = (r"(0[1-9]|[12][0-9]|3[01])/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
       r"/[0-9]{4}:([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9] [+-][0-9]{4}")
DATA = ISO + "|" + CLF

SQLI = (r"'[ ]*(or|and)[ ]+'[a-z0-9]+'[ ]*=[ ]*'[a-z0-9]+"
        r"|[ ](or|and)[ ]+[0-9]+[ ]*=[ ]*[0-9]+"
        r"|union[ ]+(all[ ]+)?select"
        r"|;[ ]*drop[ ]+table"
        r"|'[ ]*--")

TRAVERSAL = r"((\.|%2e){2}(/|%2f|\\|%5c))+[a-z0-9_./%-]*"

CPF = r"[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}|[0-9]{11}"


class ER:
    def __init__(self, id, nome, funcao, alfabeto, linguagem, formal, sintaxe, equivalencia,
                 aceitas, rejeitadas, limites, limite_texto, pre=_nenhum, fronteira=False):
        self.id, self.nome, self.funcao = id, nome, funcao
        self.alfabeto, self.linguagem, self.formal = alfabeto, linguagem, formal
        self.sintaxe, self.equivalencia = sintaxe, equivalencia
        self.aceitas, self.rejeitadas, self.limites = aceitas, rejeitadas, limites
        self.limite_texto, self.pre, self.fronteira = limite_texto, pre, fronteira
        self.regex = re.compile(sintaxe)
        self._afn = None

    def afn(self):
        if self._afn is None:
            self._afn = construir_afne(self.sintaxe)
        return self._afn

    def reconhece_regex(self, cadeia):      # correspondência completa (fullmatch)
        return self.regex.fullmatch(cadeia) is not None

    def reconhece_afn(self, cadeia, verbose=False):
        return self.afn().aceita(cadeia, verbose)


D = "D = (0|1|...|9)"
EXPRESSOES = [
    ER("ER-01", "Endereço IPv4 com porta opcional", "Identifica a origem (IP:porta) de cada requisição.",
       "Σ = {0,...,9} ∪ {'.', ':'}",
       "Quatro octetos de 0 a 255, sem zero à esquerda, separados por '.', seguidos opcionalmente de ':' e 1 a 5 dígitos.",
       D + "; O = 25(0|...|5) | 2(0|...|4)D | 1DD | (1|...|9|ε)D ; ER = O'.'O'.'O'.'O(':'D{1,5})?",
       IPV4,
       "[0-9] = (0|...|9); {1,5} = D | DD | DDD | DDDD | DDDDD; '?' = (r|ε); '\\.' = ponto literal.",
       ["192.168.1.1:8080", "10.0.0.1", "255.255.255.255", "203.0.113.7:80", "8.8.8.8:65535", "0.0.0.0"],
       ["256.1.1.1", "192.168.1", "192.168.1.1:", "1.2.3.4.5", "192.168.01.1", "192.168.1.1:123456", "a.b.c.d", ""],
       ["0.0.0.0", "255.255.255.255", "192.168.1.1:"],
       "Aceita portas > 65535 (até 5 dígitos) e não valida se o IP é roteável. Sem lookaround, a extração depende de um filtro de fronteira no código.",
       fronteira=True),
    ER("ER-02", "Data/hora ISO 8601 ou log padrão (CLF)", "Valida a marca temporal de cada acesso.",
       "Σ = {0,...,9} ∪ {Jan,...} letras do nome dos meses ∪ {'-', ':', '.', '/', 'T', 'Z', '+', ' '}",
       "ISO 8601 com fuso (AAAA-MM-DDThh:mm:ss[.frac](Z|±hh:mm)) ou formato CLF do Apache (dd/Mon/AAAA:hh:mm:ss ±hhmm).",
       "ER = ISO | CLF; ISO = A'-'M'-'DT H':'S':'S(.D+)?(Z|(+|-)DD':'DD); CLF = Dd'/'Mes'/'AAAA':'H':'S':'S' '(+|-)DDDD",
       DATA,
       "[0-9]{4} = DDDD; (0[1-9]|1[0-2]) = meses 01..12; [+-] = (+|-); '|' = união entre os dois formatos.",
       ["2026-09-29T12:53:00-03:00", "2026-09-29T12:53:00Z", "2026-12-31T23:59:59+00:00",
        "2026-01-01T00:00:00.123Z", "29/Sep/2026:12:53:00 -0300", "01/Jan/2026:00:00:00 +0000"],
       ["2026-13-01T10:00:00Z", "2026-09-29 12:53:00", "2026-09-29T24:00:00Z", "29/Sept/2026:12:53:00 -0300",
        "29/Sep/2026:12:60:00 -0300", "2026-09-29T12:53:00", "32/Sep/2026:12:53:00 -0300", ""],
       ["2026-12-31T23:59:59+00:00", "01/Jan/2026:00:00:00 +0000"],
       "Não verifica dias por mês (ex.: 31/02) nem ano bissexto: isso não é regular de forma simples.",
       fronteira=True),
    ER("ER-03", "Injeção de SQL (SQLi)", "Detecta padrões maliciosos em URL/query string.",
       "Σ = letras minúsculas ∪ {0,...,9} ∪ {espaço, ', =, ;, -}",
       "Fragmentos de ataque: tautologia com aspas (' or '1'='1), tautologia numérica ( or 1=1), UNION [ALL] SELECT, ; DROP TABLE e comentário '--' após aspa.",
       "ER = '_*(or|and)_+'X+'_*='_*'X+ | _(or|and)_+D+_*=_*D+ | union_+(all_+)?select | ;_*drop_+table | '_*-- ; _ = espaço, X = (a|...|z|0|...|9)",
       SQLI,
       "[ ] = espaço; '+' = rr*; '*' = fecho de Kleene; (all[ ]+)? = (all_+|ε); '|' = união dos 5 padrões.",
       ["' or '1'='1", "' and 'a'='a", "union select", "union all select", " or 1=1", "; drop table", "'--", "union   select"],
       ["union", "select", "' or", "or 1=1", "drop table", "unionselect", "'a'='a", ""],
       ["'--", "union   select", "' or"],
       "Heurística lexical: gera falsos positivos em texto legítimo e não detecta ofuscações (comentários /**/, hex). Requer pré-processamento (decodificar URL + minúsculas), fora da ER.",
       pre=_decodificar_minusculas),
    ER("ER-04", "Traversal de diretório (Path Traversal)", "Identifica navegação indevida no sistema de arquivos.",
       "Σ = {., /, \\, %} ∪ {a,...,z} ∪ {0,...,9} ∪ {_, -}",
       "Um ou mais segmentos de retorno ('..' ou '%2e' duas vezes, seguido de '/', '%2f', '\\' ou '%5c'), opcionalmente seguidos do caminho alvo.",
       "ER = ((.|%2e)(.|%2e)(/|%2f|'\\'|%5c))+ P*; P = (a|...|z|0|...|9|_|.|/|%|-)",
       TRAVERSAL,
       "{2} = concatenação de 2 cópias; '+' = rr*; '*' = fecho; [a-z0-9_./%-] = união finita (o '-' final é literal); '\\\\' = barra invertida literal.",
       ["../", "..\\", "%2e%2e%2f", "../../etc/passwd", "..%2f", "%2e./windows/win.ini", "%2e%2e%5cboot.ini"],
       [".", "..", "./", "/etc/passwd", "%2e%2e", "...", "a../", "%2e/", ""],
       ["../", "..%2f", "..."],
       "Sem decodificar a URL antes, variantes como %252e (dupla codificação) não são detectadas. '..' legítimo dentro de nomes de arquivo pode gerar alarme falso.",
       pre=_minusculas),
    ER("ER-05", "Máscara de dados sensíveis (CPF)", "Localiza CPFs no payload para substituir por **.***.***-**.",
       "Σ = {0,...,9} ∪ {'.', '-'}",
       "CPF formatado (000.000.000-00) ou apenas 11 dígitos.",
       D + "; ER = DDD'.'DDD'.'DDD'-'DD | D{11}",
       CPF,
       "[0-9]{3} = DDD; {11} = 11 cópias de D; '|' = união dos dois formatos; '\\.' = ponto literal.",
       ["123.456.789-09", "000.000.000-00", "529.982.247-25", "12345678909", "00000000000", "999.999.999-99"],
       ["123.456.789-0", "123456789-09", "123.456.789.09", "1234567890", "123456789012", "abc.def.ghi-jk", "123.456.78909", ""],
       ["000.000.000-00", "00000000000", "1234567890"],
       "Não verifica os dígitos verificadores (cálculo módulo 11 não é regular): o programa faz essa checagem à parte, apenas para o relatório. 11 dígitos soltos podem ser outra coisa (telefone, ID).",
       fronteira=True),
]
POR_ID = {e.id: e for e in EXPRESSOES}


def ficha_markdown(er):
    r = er.afn().resumo()
    ac = "\n".join(f"  - `{c}`" + ("  *(caso-limite)*" if c in er.limites else "") for c in er.aceitas)
    rj = "\n".join(f"  - `{c}`" + ("  *(caso-limite)*" if c in er.limites else "") for c in er.rejeitadas)
    return f"""## {er.id} - {er.nome}
- **Função no programa:** {er.funcao}
- **Alfabeto:** {er.alfabeto}
- **Linguagem L:** {er.linguagem}
- **ER formal:** `{er.formal}`
- **Sintaxe implementada (copiada do código):** `{er.sintaxe}`
- **Equivalência:** {er.equivalencia}
- **AFNε:** {r['estados']} estados, {r['transicoes']} transições ({r['transicoes_epsilon']} movimentos ε); inicial {r['estado_inicial']}; final {', '.join(r['estados_finais'])}
- **Aceitas ({len(er.aceitas)}):**
{ac}
- **Rejeitadas ({len(er.rejeitadas)}):**
{rj}
- **Limite:** {er.limite_texto}
"""
