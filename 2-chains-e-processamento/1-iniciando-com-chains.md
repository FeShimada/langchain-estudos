# 1 — Iniciando com chains

## A proposta

Nos fundamentos, tudo era dois passos manuais — e **a saída de um é sempre a entrada do próximo**:

```python
texto = prompt.format(name="Felipe")
resposta = model.invoke(texto)
```

Na vida real a fila é maior: `buscar docs → montar prompt → chamar LLM → extrair texto → virar JSON → validar`. Uma **chain** declara essa fila de uma vez, igual ao pipe do terminal (`cat x | grep erro | wc -l`).

```
{"name": "Felipe"} → [question_template] → "Hi, I'm Felipe!..." → [model] → AIMessage → .content
```

## Por que funciona: o Runnable

Quase toda peça do LangChain (prompts, modelos, parsers, retrievers, funções suas) implementa a mesma interface — **Runnable**: todas respondem a `.invoke()`, `.stream()`, `.batch()`.

Como falam a mesma língua, se encaixam. O `|` (LCEL) diz *"ligue a saída desta peça na entrada da próxima"*. E o resultado da composição **também é um Runnable** — por isso a chain tem `.invoke()` e cabe dentro de outra chain. É LEGO: peça solta e peça montada têm o mesmo encaixe.

## O código

```python
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

chain = question_template | model            # NÃO executa nada — só monta a receita
result = chain.invoke({"name": "Felipe"})    # aqui sim
print(result.content)
```

**`temperature`** — o quanto o modelo arrisca nas palavras. `0.0` determinístico (extração, classificação) · `1.0` criativo (piadas, textos). `0.5` é o meio-termo.

**Entrada é dicionário**, não string: quem recebe primeiro é o template, que precisa saber qual valor vai em qual lacuna. As chaves são os `input_variables`.

**Saída é a da última peça.** Como a última é o model, vem `AIMessage` — daí o `.content`.

## De graça em qualquer chain

```python
chain.stream({"name": "Felipe"})                      # token a token
chain.batch([{"name": "Felipe"}, {"name": "Ana"}])    # em paralelo
```

Mais `.ainvoke()`/`.astream()` e rastreamento no LangSmith.

## Próxima peça

Cansou do `.content`? Encaixe mais um Runnable no fim:

```python
chain = question_template | model | StrOutputParser()   # já sai string pura
```

O `StrOutputParser` só recebe o `AIMessage` e devolve o `.content`. É assim que a chain cresce.
