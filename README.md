# CodeLinter

Trabalho de Linguagens Formais e Autômatos (CESUPA).

**Problema:** em revisão de código é útil reconhecer automaticamente certos trechos, como nomes de variáveis fora do padrão, chaves secretas esquecidas no código, números, imports e comentários.

**Solução:** um mini-linter que recebe uma cadeia e diz a quais de 5 linguagens ela pertence. Cada linguagem é reconhecida de duas formas equivalentes: por uma **Expressão Regular** (módulo `re` do Python) e por um **AFNε** simulado no próprio código. O programa mostra as duas respostas lado a lado.

## Requisitos

- Python 3.10 ou superior
- `pytest` (só para rodar os testes)

## Instalação e execução

```bash
pip install -r src/requirements.txt
cd src
python main.py
```

No Windows, se `python` não funcionar, use `py`.

O menu tem três opções:

1. **Analisar uma cadeia** nas 5 linguagens (ER e AFNε lado a lado).
2. **Ver o passo a passo** de um AFNε: os estados ativos a cada símbolo lido.
3. **Analisar o arquivo de exemplos** (`src/data/exemplos.txt`).

Para testar comentários de várias linhas, digite `\n` no lugar da quebra de linha.

## Testes

Na raiz do projeto:

```bash
python -m pytest
```

São 86 testes. Os resultados e a análise estão em [docs/analise_testes.md](docs/analise_testes.md).

## Expressões Regulares

| | Linguagem | ER no código | AFNε | Documentação |
|---|---|---|---|---|
| ER-01 | Identificador camelCase | `[a-z][a-zA-Z0-9]*` | 9 estados | [afne_er1.md](src/data/afn_diagrams/afne_er1.md) |
| ER-02 | Token secreto Stripe | `sk_live_[0-9a-zA-Z]{24}` | 33 estados | [afne_er2.md](src/data/afn_diagrams/afne_er2.md) |
| ER-03 | Número decimal | `[+-]?[0-9]+\.[0-9]+` | 11 estados | [afne_er3.md](src/data/afn_diagrams/afne_er3.md) |
| ER-04 | Import Python | `import\s+[a-zA-Z0-9_.]+(\s*,\s*[a-zA-Z0-9_.]+)*` | 12 estados | [afne_er4.md](src/data/afn_diagrams/afne_er4.md) |
| ER-05 | Comentário | `(//.*\|/\*[\s\S]*?\*/)` | 12 estados | [afne_er5.md](src/data/afn_diagrams/afne_er5.md) |

**Os 5 diagramas juntos:** [docs/diagramas.md](docs/diagramas.md).

A documentação de cada ER traz o nome e a finalidade, o alfabeto, a descrição da linguagem, a ER na notação formal e no código, a explicação dos operadores, o **diagrama do AFNε** (estado inicial, finais, transições e movimentos ε), a tabela de transições e os casos de teste.

## Estrutura

```
src/
├── main.py                  programa interativo
├── requirements.txt         dependências
├── terminal_ER/validators.py   as 5 ERs e os casos de teste (CASOS_TESTE)
├── automatos/afne_er1..5.py    os 5 AFNε (função aceita)
└── data/
    ├── exemplos.txt         dados de exemplo
    └── afn_diagrams/        documentação e diagramas de cada ER
tests/                       testes automatizados (pytest)
docs/analise_testes.md       análise dos resultados dos testes
docs/diagramas.md            os 5 diagramas dos AFNε
```

## Contribuições

| Integrante | Contribuição |
|---|---|
| Carlos Eduardo Cardoso Silva | Estrutura inicial do projeto, as 5 Expressões Regulares, os AFNε originais (formato com `criptografia()` e dicionário de transições) e os primeiros casos de teste |
| Ricardo | Correção do fecho-ε, AFNε completos e equivalentes às ERs, ajustes nas ERs 01, 03 e 04, programa interativo, testes automatizados e documentação |

## Uso de Inteligência Artificial

Usamos o assistente de IA Claude (Anthropic) como apoio nas seguintes tarefas:

- revisão do código e diagnóstico do erro no cálculo do fecho-ε;
- sugestões para completar os AFNε e ajustar as ERs;
- geração de casos de teste e dos testes com cadeias aleatórias;
- redação da documentação e geração dos diagramas a partir do código.

Todo o conteúdo foi revisado pela equipe, que entende, explica e consegue modificar o código, os autômatos e a documentação.
