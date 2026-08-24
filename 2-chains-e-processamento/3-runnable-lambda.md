# 3 — RunnableLambda

## O que é "lambda"

Em Python, `lambda` é uma **função anônima escrita em uma linha** — sem `def`, sem nome, sem `return`:

```python
def dobro(x):        # função normal
    return x * 2

dobro = lambda x: x * 2   # exatamente a mesma coisa
```

A ideia é tratar a função como um **valor**: algo que você passa adiante, guarda numa variável ou entrega para outra função. Vem do *cálculo lambda*, e por isso o nome virou sinônimo de "uma funçãozinha usada como dado".

No LangChain, `RunnableLambda` significa **"uma função qualquer transformada em peça de chain"**. Apesar do nome, ela aceita qualquer callable — não precisa ser a palavra-chave `lambda`.

## O código

```python
def parse_number(text: str) -> int:
    return int(text.strip())

parse_runnable = RunnableLambda(parse_number)   # função comum → peça de chain
number = parse_runnable.invoke("10")            # 10 (int)
```

`parse_number` é uma função Python pura, sem nada de LangChain. O `RunnableLambda` a embrulha e ela ganha a interface padrão:

```python
parse_runnable.invoke("10")          # 10
parse_runnable.batch(["1", " 2 "])   # [1, 2]
```

> O script não imprime nada — `number` fica com o valor `10`, mas sem `print`. Adicione um para ver.

## Com o `lambda` de verdade

Quando a lógica cabe numa linha, dá para dispensar o `def`:

```python
parse_runnable = RunnableLambda(lambda text: int(text.strip()))
```

E dentro de uma chain, funções soltas são **convertidas automaticamente** quando o outro lado já é um Runnable:

```python
chain = parse_runnable | (lambda n: n * 2)   # vira RunnableLambda sozinho
chain.invoke("10")                            # 20
```

## RunnableLambda x @chain

São **a mesma coisa** — `@chain` devolve um `RunnableLambda`. Muda só a forma de escrever:

| | Quando usar |
|---|---|
| `@chain` | a função é sua e já nasce como peça de chain |
| `RunnableLambda(f)` | embrulhar função existente, de terceiros, ou um `lambda` inline |

Diferença prática: com `@chain` você **perde** a função original (vira Runnable e não é mais chamável). Com `RunnableLambda`, `parse_number` continua sendo uma função normal — dá para testar e reaproveitar fora da chain.

## A regra do argumento único

A função precisa receber **exatamente um argumento** — o que vier da peça anterior:

```python
def soma(a, b): return a + b
RunnableLambda(soma).invoke(1)   # TypeError: missing 1 required positional argument: 'b'
```

Para múltiplos valores, receba um dict (`{"a": 1, "b": 2}`) — foi o padrão do arquivo anterior — ou fixe o extra com `functools.partial`.
