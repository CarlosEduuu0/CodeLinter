"""analisador.py - varredura linha a linha, extração, sanitização e relatórios."""
import html
import json
from collections import Counter
from pathlib import Path

from expressoes import EXPRESSOES, POR_ID

MASCARA_CPF = "**.***.***-**"


class EntradaInvalida(Exception):
    pass


# ---------------------------------------------------------------- entrada
def ler_arquivo(caminho):
    p = Path(caminho)
    if not p.exists():
        raise EntradaInvalida(f"arquivo não encontrado: {caminho}")
    if not p.is_file():
        raise EntradaInvalida(f"'{caminho}' não é um arquivo")
    dados = p.read_bytes()
    if b"\x00" in dados:
        raise EntradaInvalida("o arquivo parece binário, não é um log de texto")
    return validar_texto(dados.decode("utf-8", errors="replace"))


def validar_texto(texto):
    if texto is None or not texto.strip():
        raise EntradaInvalida("entrada vazia: informe um arquivo .log/.txt ou cole o texto do log")
    return texto.splitlines()


# ---------------------------------------------------------------- extração
def fronteira_ok(texto, ini, fim):
    """Substitui o lookaround (proibido): o trecho não pode ser parte de um token maior."""
    antes = texto[ini - 1] if ini > 0 else ""
    depois = texto[fim] if fim < len(texto) else ""
    if antes and (antes.isalnum() or antes == "."):
        return False
    if depois and depois.isalnum():
        return False
    if depois == "." and fim + 1 < len(texto) and texto[fim + 1].isdigit():
        return False
    return True


def encontrar(er, texto):
    for m in er.regex.finditer(texto):
        if er.fronteira and not fronteira_ok(texto, m.start(), m.end()):
            continue
        yield m


def cpf_dv_valido(cpf):
    d = [int(c) for c in cpf if c.isdigit()]
    if len(d) != 11 or len(set(d)) == 1:
        return False
    for n in (9, 10):
        s = sum(d[i] * (n + 1 - i) for i in range(n))
        if d[n] != (s * 10 % 11) % 10:
            return False
    return True


def sanitizar_linha(linha, mascarar_ip=False):
    trocas = [(m.start(), m.end(), MASCARA_CPF) for m in encontrar(POR_ID["ER-05"], linha)]
    if mascarar_ip:
        for m in encontrar(POR_ID["ER-01"], linha):
            partes = m.group(0).split(":")[0].split(".")
            trocas.append((m.start(), m.end(), ".".join(partes[:3] + ["xxx"])))
    for ini, fim, novo in sorted(trocas, reverse=True):
        linha = linha[:ini] + novo + linha[fim:]
    return linha


# ---------------------------------------------------------------- análise
def analisar(linhas, mascarar_ip=False, validar_afn=False):
    c = Counter()
    ocorr, tipos, origens = Counter(), Counter(), Counter()
    incidentes, sanitizadas = [], []
    cpf_total = cpf_valido = 0

    for n, bruta in enumerate(linhas, 1):
        linha = bruta.rstrip("\r\n")
        c["total_linhas"] += 1
        if not linha.strip():
            c["linhas_vazias"] += 1
            sanitizadas.append(linha)
            continue
        c["linhas_analisadas"] += 1
        achados = {er.id: [m.group(0) for m in encontrar(er, er.pre(linha))] for er in EXPRESSOES}
        for er in EXPRESSOES:
            ocorr[er.id] += len(achados[er.id])
            if validar_afn:
                for trecho in achados[er.id]:
                    if not er.reconhece_afn(trecho):
                        c["divergencias_afn"] += 1

        ips, datas = achados["ER-01"], achados["ER-02"]
        origem = ips[0].split(":")[0] if ips else None
        c["linhas_sem_ip"] += not ips
        c["linhas_sem_timestamp"] += not datas
        c["linhas_sem_estrutura"] += (not ips and not datas)

        ameacas = [("SQLi", t) for t in achados["ER-03"]] + [("Path Traversal", t) for t in achados["ER-04"]]
        sanit = sanitizar_linha(linha, mascarar_ip)
        sanitizadas.append(sanit)
        if ameacas:
            c["linhas_com_ameaca"] += 1
        gravidade = "crítica" if len({t for t, _ in ameacas}) > 1 else "alta"
        for tipo, trecho in ameacas:
            tipos[tipo] += 1
            if origem:
                origens[origem] += 1
            incidentes.append({"linha": n, "tipo": tipo, "trecho": trecho, "origem": origem,
                               "timestamp": datas[0] if datas else None, "gravidade": gravidade,
                               "linha_sanitizada": sanit})
        for cpf in achados["ER-05"]:
            cpf_total += 1
            cpf_valido += cpf_dv_valido(cpf)

    resumo = {k: c[k] for k in ("total_linhas", "linhas_vazias", "linhas_analisadas", "linhas_com_ameaca",
                                "linhas_sem_ip", "linhas_sem_timestamp", "linhas_sem_estrutura")}
    if validar_afn:
        resumo["divergencias_afn"] = c["divergencias_afn"]
    relatorio = {
        "resumo": resumo,
        "ocorrencias_por_er": {er.id + " " + er.nome: ocorr[er.id] for er in EXPRESSOES},
        "ameacas_por_tipo": dict(tipos),
        "top_origens_maliciosas": [{"ip": ip, "ameacas": n} for ip, n in origens.most_common(5)],
        "cpfs": {"mascarados": cpf_total, "com_digito_verificador_valido": cpf_valido},
        "incidentes": incidentes,
    }
    return relatorio, sanitizadas


# ---------------------------------------------------------------- saídas
def relatorio_html(rel):
    e = html.escape
    linhas = "".join(
        f"<tr><td>{i['linha']}</td><td>{e(i['tipo'])}</td><td>{e(i['gravidade'])}</td>"
        f"<td>{e(str(i['origem']))}</td><td>{e(str(i['timestamp']))}</td><td><code>{e(i['trecho'])}</code></td></tr>"
        for i in rel["incidentes"])
    res = "".join(f"<li>{e(k)}: <b>{v}</b></li>" for k, v in rel["resumo"].items())
    er = "".join(f"<li>{e(k)}: <b>{v}</b></li>" for k, v in rel["ocorrencias_por_er"].items())
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>LogSentinel</title>
<style>body{{font-family:sans-serif;margin:2rem}}table{{border-collapse:collapse}}td,th{{border:1px solid #999;padding:4px 8px}}th{{background:#eee}}</style></head>
<body><h1>LogSentinel - Relatório de incidentes</h1><h2>Resumo</h2><ul>{res}</ul>
<h2>Ocorrências por expressão regular</h2><ul>{er}</ul>
<h2>Incidentes ({len(rel['incidentes'])})</h2>
<table><tr><th>Linha</th><th>Tipo</th><th>Gravidade</th><th>Origem</th><th>Data/hora</th><th>Trecho</th></tr>{linhas}</table>
<p>CPFs mascarados: {rel['cpfs']['mascarados']}</p></body></html>"""


def salvar_saidas(rel, sanitizadas, pasta):
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / "relatorio.json").write_text(json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")
    (pasta / "relatorio.html").write_text(relatorio_html(rel), encoding="utf-8")
    (pasta / "log_sanitizado.log").write_text("\n".join(sanitizadas) + "\n", encoding="utf-8")
    return [pasta / "relatorio.json", pasta / "relatorio.html", pasta / "log_sanitizado.log"]
