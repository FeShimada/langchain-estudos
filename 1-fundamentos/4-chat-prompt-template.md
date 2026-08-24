# 4 — ChatPromptTemplate

Molde de **conversa** — um roteiro de diálogo: cada linha tem um papel e uma fala, e cada fala tem suas lacunas.

| Papel | Para que serve |
|---|---|
| `system` | bastidor: persona, tom, regras, formato |
| `user` | a fala da pessoa (= `human`) |
| `assistant` | respostas anteriores do modelo → histórico |

```python
system = ("system", "you are an assistant that answers questions in a {style} style")
user = ("user", "{question}")                    # variáveis em mensagens diferentes

chat_prompt = ChatPromptTemplate([system, user]) # lista ordenada — a ordem importa

messages = chat_prompt.format_messages(style="funny", question="Who is Alan Turing?")
result = model.invoke(messages)                  # o model aceita a lista direto
```

`.format_messages()` devolve `[SystemMessage(...), HumanMessage(...)]` — objetos com o papel preservado, não uma string.

O loop de `print` é só didático, para ver o que vai ao modelo:

```
system: you are an assistant that answers questions in a funny style
human: Who is Alan Turing?
```

Você escreveu `"user"` e saiu `human`: o LangChain normaliza os papéis, `user` → `HumanMessage`. Mesmo conceito, dois nomes.

## O incômodo que sobra

```python
messages = chat_prompt.format_messages(...)   # 1) monta
result = model.invoke(messages)               # 2) envia
```

A saída do passo 1 é sempre a entrada do passo 2. É isso que as **chains** automatizam com `|`.
