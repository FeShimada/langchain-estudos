# 4 — Pipeline de processamento

## A proposta

Até agora cada chain era uma fila só: entrada → template → model → saída. Aqui a saída de **uma chain inteira** vira a entrada de outra:

> traduzir para inglês → resumir a tradução em 10 palavras

São duas chamadas ao LLM, uma alimentando a outra. E o encaixe usa a promessa do arquivo 1: *a chain montada também é um Runnable*. Ou seja, ela cabe dentro de outra chain como se fosse uma peça solta.

## O código

```python
chain_translate = template_translate | llm | StrOutputParser()

pipeline = {"text": chain_translate} | template_summary | llm | StrOutputParser()

result = pipeline.invoke({"text": "Oi, tudo bem?"})
```

Duas coisas novas nessa segunda linha: o `StrOutputParser` finalmente aparecendo, e um **dicionário** no começo de um `|`.

## StrOutputParser — o encaixe que faltava

Ele é o Runnable mais simples que existe: recebe o `AIMessage` e devolve o `.content`.

```python
llm | StrOutputParser()   # em vez de result.content na mão
```

Aqui ele não é conforto, é **necessidade**. O `template_summary` espera uma string na lacuna `{text}`. Se `chain_translate` terminasse no `llm`, o valor entregue seria um `AIMessage` — e o `PromptTemplate` não reclama, ele só chama `str()` no objeto:

```
Summarize this in 1 sentence (max 10 words): content='Hi, how are you?' additional_kwargs={} response_metadata={} tool_calls=[] ...
```

O prompt vai poluído para o modelo e o resumo sai estranho. **Erro silencioso** — o tipo mais chato de caçar. A regra: sempre que a saída de um LLM for reentrar num template, feche a chain com `StrOutputParser()`.

## O dicionário vira RunnableParallel

```python
{"text": chain_translate} | template_summary
```

Um `dict` não é Runnable — mas o LangChain **converte automaticamente**. Na hora do `|`, o `dict` não sabe lidar com um `PromptTemplate`, então o Python devolve a operação para o lado direito (`Runnable.__ror__`), que passa o dicionário pelo `coerce_to_runnable` e o transforma num **`RunnableParallel`**.

Traduzindo o que ele faz: *"pegue a entrada, rode cada valor deste dicionário sobre ela, e devolva um dicionário com as mesmas chaves e os resultados"*.

```python
{"text": chain_translate}
# entra {"text": "Oi, tudo bem?"}  →  sai {"text": "Hi, how are you?"}
```

Por que dar essa volta em vez de só `chain_translate | template_summary`? Porque **template espera dicionário, chain devolve string**. O `RunnableParallel` é o adaptador: reembala a string numa chave com o nome certo.

Com mais de uma chave, os ramos rodam **concorrentemente** (o `RunnableParallel` dispara cada um numa thread) — daí o "parallel" do nome. Com uma chave só, como aqui, ele é puro encanamento.

```python
{"en": chain_translate, "original": RunnablePassthrough()}   # dois ramos, ao mesmo tempo
```

## O fluxo

```
{"text": "Oi, tudo bem?"}
   ↓  [RunnableParallel]  ── roda chain_translate sobre a entrada inteira
   │      {"text": "Oi, tudo bem?"} → [template_translate] → [llm] → [StrOutputParser]
   ↓
{"text": "Hi, how are you?"}
   ↓  [template_summary]
"Summarize this in 1 sentence (max 10 words): Hi, how are you?"
   ↓  [llm]
AIMessage
   ↓  [StrOutputParser]
"A friendly greeting asking how someone is doing."
```

## Cuidado com os dois `text`

O nome `text` aparece três vezes no script, e **são papéis diferentes**:

| Onde | Papel |
|---|---|
| `template_translate` → `input_variables=["text"]` | a lacuna que recebe o português |
| chave do dict `{"text": ...}` | o nome que o `template_summary` vai procurar |
| `template_summary` → `input_variables=["text"]` | a lacuna que recebe o inglês |

Funciona porque os nomes batem por coincidência — os dois templates usaram `text`. Se o segundo fosse `{content}`, a chave do dicionário teria que virar `"content"`, senão dá `KeyError` na formatação. É o mesmo **contrato entre peças** do arquivo 2: a saída de uma precisa ter o formato que a próxima espera.

## O preço

Duas chamadas de LLM por `invoke()` — dobro de latência, dobro de custo, e o segundo modelo só vê o que o primeiro produziu. Se a tradução sair errada, o resumo herda o erro sem ter como perceber. Pipeline longo é poderoso, mas cada elo é um ponto de falha a mais.
