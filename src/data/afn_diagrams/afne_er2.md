# ER-02 · Token secreto da Stripe (`sk_live_`)

## Nome e finalidade

**Token Stripe `sk_live_`.** Reconhece chaves secretas de produção da Stripe (plataforma de pagamentos): o prefixo `sk_live_` seguido de exatamente 24 caracteres alfanuméricos. Em um linter, serve para **segurança**: detectar quando alguém deixou uma chave de pagamento real escrita no código, que qualquer pessoa com acesso ao repositório poderia usar.

## Alfabeto

Σ = {s, k, _, l, i, v, e} ∪ A, em que A = {a, …, z, A, …, Z, 0, …, 9} (alfanuméricos ASCII).

| Símbolo | Na `criptografia()` |
|---|---|
| `s`, `k`, `_`, `l`, `i`, `v`, `e` | colunas 0 a 6 (uma para cada letra do prefixo) |
| qualquer outro alfanumérico ASCII | coluna 7 |
| ε | coluna 8 |

As letras do prefixo têm coluna própria porque, no prefixo, o autômato precisa saber **qual** letra leu. No sufixo, qualquer alfanumérico serve: por isso as transições do sufixo usam todas as colunas menos a do `_` (o conjunto `ALFA_NUM` do código).

## Linguagem reconhecida

Cadeias formadas por `sk_live_` seguido de **exatamente 24** caracteres alfanuméricos, nem 23, nem 25. O token tem sempre 32 caracteres.

## Expressão Regular

**Notação formal:**

```
s · k · _ · l · i · v · e · _ · A · A · … · A      (A repetido 24 vezes)
```

com A = (a ∪ … ∪ z ∪ A ∪ … ∪ Z ∪ 0 ∪ … ∪ 9).

**Sintaxe no código** (`src/terminal_ER/validators.py`):

```python
SK_LIVE_PATTERN = r"sk_live_[0-9a-zA-Z]{24}"
```

## Operadores utilizados

| Operador | Na notação formal | No Python | Papel nesta ER |
|---|---|---|---|
| Concatenação | `·` | escrever lado a lado | `sk_live_` é a concatenação de 8 símbolos fixos |
| União | `∪` | `[0-9a-zA-Z]` | cada posição do sufixo aceita qualquer alfanumérico |
| Repetição exata | escrever A · A · … · A | `{24}` | `{24}` é só um **atalho** do Python para concatenar A 24 vezes; a notação formal não tem esse operador |

## AFNε

Arquivo: `src/automatos/afne_er2.py`

- **Estado inicial:** q0
- **Estados finais:** {q32}
- **Estados:** 33 (q0 a q32)
- **Movimentos vazios:** nenhum. A ER-02 é só concatenação, sem `∪` nem `*` fora das classes de caracteres, então não há bifurcação nem repetição para modelar. A coluna ε existe (coluna 8), mas fica vazia. Todo AFD é um AFNε que simplesmente não usa ε.

```mermaid
flowchart LR
    inicio(( )) --> q0
    q0((q0))
    q1((q1))
    q2((q2))
    q3((q3))
    q4((q4))
    q5((q5))
    q6((q6))
    q7((q7))
    q8((q8))
    q9((q9))
    q10((q10))
    q11((q11))
    q12((q12))
    q13((q13))
    q14((q14))
    q15((q15))
    q16((q16))
    q17((q17))
    q18((q18))
    q19((q19))
    q20((q20))
    q21((q21))
    q22((q22))
    q23((q23))
    q24((q24))
    q25((q25))
    q26((q26))
    q27((q27))
    q28((q28))
    q29((q29))
    q30((q30))
    q31((q31))
    q32(((q32)))
    q0 -- "s" --> q1
    q1 -- "k" --> q2
    q2 -- "_" --> q3
    q3 -- "l" --> q4
    q4 -- "i" --> q5
    q5 -- "v" --> q6
    q6 -- "e" --> q7
    q7 -- "_" --> q8
    q8 -- "A" --> q9
    q9 -- "A" --> q10
    q10 -- "A" --> q11
    q11 -- "A" --> q12
    q12 -- "A" --> q13
    q13 -- "A" --> q14
    q14 -- "A" --> q15
    q15 -- "A" --> q16
    q16 -- "A" --> q17
    q17 -- "A" --> q18
    q18 -- "A" --> q19
    q19 -- "A" --> q20
    q20 -- "A" --> q21
    q21 -- "A" --> q22
    q22 -- "A" --> q23
    q23 -- "A" --> q24
    q24 -- "A" --> q25
    q25 -- "A" --> q26
    q26 -- "A" --> q27
    q27 -- "A" --> q28
    q28 -- "A" --> q29
    q29 -- "A" --> q30
    q30 -- "A" --> q31
    q31 -- "A" --> q32
    style inicio fill:none,stroke:none
```

**Tabela de transições** (→ = inicial, * = final, – = sem transição; A = qualquer alfanumérico):

| Estado | `s` | `k` | `_` | `l` | `i` | `v` | `e` | `outro` |
|---|---|---|---|---|---|---|---|---|
| → q0 | {q1} | – | – | – | – | – | – | – |
| q1 | – | {q2} | – | – | – | – | – | – |
| q2 | – | – | {q3} | – | – | – | – | – |
| q3 | – | – | – | {q4} | – | – | – | – |
| q4 | – | – | – | – | {q5} | – | – | – |
| q5 | – | – | – | – | – | {q6} | – | – |
| q6 | – | – | – | – | – | – | {q7} | – |
| q7 | – | – | {q8} | – | – | – | – | – |
| q8 | {q9} | {q9} | – | {q9} | {q9} | {q9} | {q9} | {q9} |
| q9 | {q10} | {q10} | – | {q10} | {q10} | {q10} | {q10} | {q10} |
| q10 | {q11} | {q11} | – | {q11} | {q11} | {q11} | {q11} | {q11} |
| q11 | {q12} | {q12} | – | {q12} | {q12} | {q12} | {q12} | {q12} |
| q12 | {q13} | {q13} | – | {q13} | {q13} | {q13} | {q13} | {q13} |
| q13 | {q14} | {q14} | – | {q14} | {q14} | {q14} | {q14} | {q14} |
| q14 | {q15} | {q15} | – | {q15} | {q15} | {q15} | {q15} | {q15} |
| q15 | {q16} | {q16} | – | {q16} | {q16} | {q16} | {q16} | {q16} |
| q16 | {q17} | {q17} | – | {q17} | {q17} | {q17} | {q17} | {q17} |
| q17 | {q18} | {q18} | – | {q18} | {q18} | {q18} | {q18} | {q18} |
| q18 | {q19} | {q19} | – | {q19} | {q19} | {q19} | {q19} | {q19} |
| q19 | {q20} | {q20} | – | {q20} | {q20} | {q20} | {q20} | {q20} |
| q20 | {q21} | {q21} | – | {q21} | {q21} | {q21} | {q21} | {q21} |
| q21 | {q22} | {q22} | – | {q22} | {q22} | {q22} | {q22} | {q22} |
| q22 | {q23} | {q23} | – | {q23} | {q23} | {q23} | {q23} | {q23} |
| q23 | {q24} | {q24} | – | {q24} | {q24} | {q24} | {q24} | {q24} |
| q24 | {q25} | {q25} | – | {q25} | {q25} | {q25} | {q25} | {q25} |
| q25 | {q26} | {q26} | – | {q26} | {q26} | {q26} | {q26} | {q26} |
| q26 | {q27} | {q27} | – | {q27} | {q27} | {q27} | {q27} | {q27} |
| q27 | {q28} | {q28} | – | {q28} | {q28} | {q28} | {q28} | {q28} |
| q28 | {q29} | {q29} | – | {q29} | {q29} | {q29} | {q29} | {q29} |
| q29 | {q30} | {q30} | – | {q30} | {q30} | {q30} | {q30} | {q30} |
| q30 | {q31} | {q31} | – | {q31} | {q31} | {q31} | {q31} | {q31} |
| q31 | {q32} | {q32} | – | {q32} | {q32} | {q32} | {q32} | {q32} |
| *q32 | – | – | – | – | – | – | – | – |

### Como o autômato foi montado

- **q0 a q8:** um estado para cada símbolo do prefixo `sk_live_`. Errou uma letra, não há transição, e a cadeia morre.
- **q8 a q32:** um estado para cada caractere do sufixo. Cada estado aceita qualquer alfanumérico e avança para o próximo. É como uma **contagem**: estar em q20 significa "já li 12 caracteres do sufixo".
- **q32 é o único final:** só chega lá quem leu exatamente 24 caracteres. Com 23 a máquina para em q31 (não final). Com 25 ela tenta sair de q32, que não tem transição, e a cadeia é rejeitada.

No código, cada estado do sufixo é uma linha do dicionário `funcao` que chama `gerar_transicao_sufixo()` com o próximo estado: `"q8": gerar_transicao_sufixo("q9")`, `"q9": gerar_transicao_sufixo("q10")` e assim por diante, até q31 → q32. É o mesmo padrão do código original, só que com 24 linhas em vez de 4.

## Casos de teste

| Cadeia | Esperado | Observação |
|---|---|---|
| `'sk_live_1234567890abcdef12345678'` | aceita |  |
| `'sk_live_ABCDEFGHIJKLMNOPQRSTUVWX'` | aceita |  |
| `'sk_live_a1B2c3D4e5F6g7H8i9J0k1L2'` | aceita |  |
| `'sk_live_000000000000000000000000'` | aceita |  |
| `'sk_live_ZzZzZzZzZzZzZzZzZzZzZzZz'` | aceita |  |
| `'sk_live_sklivesklivesklivesklive'` | aceita | caso-limite: sufixo com as letras do prefixo |
| `'sk_test_1234567890abcdef12345678'` | rejeita |  |
| `'sk_live_curto'` | rejeita |  |
| `'sk_live_12345678901234567890123'` | rejeita | caso-limite: 23 caracteres |
| `'sk_live_1234567890abcdef123456789'` | rejeita | caso-limite: 25 caracteres |
| `'sk_live_1234567890!@#$%^&*()123'` | rejeita |  |
| `'sk_live_1234567890abcdef1234567_'` | rejeita | "_" não é alfanumérico |
| `'SK_LIVE_1234567890abcdef12345678'` | rejeita | prefixo em maiúsculas |
| `'sk_live_skliveskliveskliveskli'` | rejeita | 22 caracteres com as letras do prefixo |
| `''` | rejeita |  |
