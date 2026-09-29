# LogSentinel - Analisador léxico e extrator de ameaças em logs web
Trabalho do 1º Bimestre - Linguagens Formais e Autômatos. Python 3.9+ (somente biblioteca padrão).

## Execução
```bash
python main.py --demo                      # analisa dados/exemplo.log
python main.py caminho/log.txt --mascarar-ip --validar-afn
python main.py                             # cole o log no terminal e finalize com FIM
python main.py --texto "1.2.3.4 GET /a?id=1'%20OR%20'1'='1"
python main.py --testar ER-03 "union select"   # simula o AFNε passo a passo (demonstração)
python main.py --fichas > FICHAS_ER.md         # ficha de cada ER para o relatório
python main.py --diagramas                     # gera diagramas/ER-0X.dot
dot -Tpng diagramas/ER-04.dot -o diagramas/ER-04.png   # requer Graphviz
python testes.py                               # testes (6+ aceitas, 6+ rejeitadas, limites, ER x AFNε)
```
Saídas em `saida/`: `relatorio.json`, `relatorio.html`, `log_sanitizado.log`.

## Arquitetura
- `automato.py`: classe `AFNe` (estados, alfabeto, estado_inicial, estado_final, funcao com ε; simulação com a lógica do código-base) e construção de Thompson a partir da ER.
- `expressoes.py`: as 5 ERs (ER formal, sintaxe do código, equivalência, testes, limites).
- `analisador.py`: leitura/validação da entrada, extração, sanitização (CPF/IP), relatórios.
- `main.py`: interface de linha de comando. `testes.py`: testes automatizados.

## Contribuições dos integrantes
| Integrante | Contribuição |
|---|---|
| (preencher) | (preencher) |

## Referências
Documentação do módulo `re` do Python; Guia de Sintaxe da disciplina; construção de Thompson (Hopcroft, Motwani, Ullman).
