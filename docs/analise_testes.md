# Testes e análise dos resultados

Execução: `python -m pytest` na raiz do projeto. **86 testes, todos passando.**

## O que é testado

| Arquivo | O que verifica |
|---|---|
| `tests/test_linguagens.py` | Cada caso de `CASOS_TESTE` (em `validators.py`) na ER **e** no AFNε; mínimo de 6 aceitas e 6 rejeitadas por ER; concordância entre ER e AFNε em cadeias aleatórias |
| `tests/test_main.py` | Entrada vazia, só espaços, BOM, `\n` digitado, arquivo ausente, arquivo de exemplos, e se o passo a passo chega ao mesmo resultado de `aceita()` |

## Resultados por ER

| ER | Casos aceitos | Casos rejeitados | Cadeias aleatórias | Aceitas entre elas | ER ≠ AFNε |
|---|---|---|---|---|---|
| ER-01 · Identificador | 6 | 6 | 6.000 | 916 | **0** |
| ER-02 · Token Stripe | 6 | 9 | 9.000 | 204 | **0** |
| ER-03 · Número decimal | 6 | 7 | 6.000 | 459 | **0** |
| ER-04 · Import Python | 6 | 8 | 7.000 | 639 | **0** |
| ER-05 · Comentário | 6 | 7 | 6.000 | 1.768 | **0** |

As cadeias aleatórias vêm de dois geradores (semente fixa, resultados reproduzíveis):

- **Combinações de símbolos da linguagem**, por exemplo dígitos, sinais e pontos para a ER-03.
- **Mutações dos casos aceitos**: 1 a 3 caracteres apagados, trocados ou inseridos. Isso gera cadeias "na beirada" da linguagem, onde os erros costumam aparecer.

Em nenhuma das 34.000 cadeias a ER e o AFNε discordaram. Isso é evidência de que os dois reconhecem a mesma linguagem, como a lauda exige.

## Os testes detectam erros?

Para confirmar que o teste de concordância não passa "por acaso", uma transição de cada AFNε foi removida de propósito:

| ER | Transição removida | Divergências detectadas |
|---|---|---|
| ER-01 | q5 deixa de ler dígito | 413 |
| ER-02 | q31 deixa de ler alfanumérico | 150 |
| ER-03 | q6 deixa de ler dígito | 459 |
| ER-04 | q9 deixa de ler vírgula | 204 |
| ER-05 | q7 deixa de ler quebra de linha | 341 |

Também foi testado o **erro original do fecho-ε** (seguir as transições vazias só um passo). Ele gera centenas de divergências nas ER-01 e ER-03, as únicas com dois movimentos ε seguidos (por exemplo q0 →ε q1 →ε q2). Nas outras, seguir um passo ou todos dá no mesmo.

## Limitações

- **ER-05:** `/* a */ b */` é aceito como um único comentário. Com `fullmatch`, o `[\s\S]*?` precisa cobrir a cadeia inteira. ER e AFNε concordam.
- **ER-04:** reconhece só o import simples do Python. `from x import y` e os imports de JavaScript ficam de fora.
- **ER-03:** não aceita notação científica (`1e10`) nem números sem parte inteira (`.5`).
- **Entrada pelo teclado:** a quebra de linha precisa ser digitada como `\n`.

## Possíveis melhorias

- Aceitar notação científica na ER-03 e `from … import …` na ER-04.
- Fazer o comentário de bloco terminar no primeiro `*/`: `/\*([^*]|\*+[^*/])*\*+/`.
- Analisar um arquivo de código inteiro, procurando as 5 linguagens dentro de cada linha, e não só linhas inteiras.
