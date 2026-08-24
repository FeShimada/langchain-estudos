# 2 — Chains com decorators

## A proposta

Até aqui as peças da chain eram todas do LangChain (template, model). O `@chain` permite **encaixar uma função sua** na fila — qualquer lógica Python: calcular, limpar texto, buscar no banco, chamar uma API.

```python
from langchain_core.runnables import chain

@chain
def square(input_dict: dict) -> dict:
    x = input_dict["x"]
    return {"square_result": x * x}
```

O decorator transforma a função num **`RunnableLambda`** — a mesma interface de todo o resto. Por isso ela ganha `|`, `.invoke()`, `.stream()`, `.batch()` de graça:

```python
square.invoke({"x": 10})            # {'square_result': 100}
square.batch([{"x": 2}, {"x": 3}])  # [{'square_result': 4}, {'square_result': 9}]
```

Em troca, ela **deixa de ser chamável como função normal** — `square({"x": 10})` levanta `TypeError: 'RunnableLambda' object is not callable`. Agora é uma peça de chain, não uma função.

## O encaixe

```python
chain2 = square | question_template2 | model
result = chain2.invoke({"x": 10})
```

```
{"x": 10} → [square] → {"square_result": 100} → [question_template2] → "Tell me about the number 100" → [model] → AIMessage
```

O que faz isso funcionar é a **combinação de nomes**: `square` devolve um dict com a chave `square_result`, que é exatamente o `input_variables` do `question_template2`.

```python
return {"square_result": x * x}              # a chave que sai...
input_variables=["square_result"]            # ...é a lacuna que entra
```

Errou o nome da chave → `KeyError` na hora de formatar o prompt. **É esse o contrato entre peças de uma chain:** a saída de uma precisa ter o formato que a próxima espera.

## Cuidado com o shadowing

```python
from langchain_core.runnables import chain   # o decorator
...
chain = question_template | model            # ⚠️ sobrescreve o decorator
```

A variável `chain` na linha 24 apaga o decorator importado. Aqui não quebra porque o `@chain` já tinha sido aplicado antes (linha 7) — mas se você adicionar outra função decorada **depois** dessa linha:

```
TypeError: 'RunnableSequence' object is not callable
```

Vale renomear a variável para `joke_chain` ou similar. Repare também que essa `chain` nem é usada no script — quem roda é a `chain2`.
