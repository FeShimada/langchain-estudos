# 3 — PromptTemplate

Molde de **texto** — o modelo de carta com lacunas: *"Prezado(a) ______, seu pedido nº ______"*.

Este script **não chama LLM**. Só monta a string.

```python
prompt_template = PromptTemplate(
    input_variables=["name"],                                 # contrato: falta variável → erro
    template="Hi, i'm {name}. Tell me a joke about {name}!"    # as duas lacunas, um argumento só
)
text = prompt_template.format(name="Felipe")   # → "Hi, i'm Felipe. Tell me a joke about Felipe!"
```

`PromptTemplate.from_template("...")` deduz as variáveis sozinho.

## Por que não f-string?

Uma f-string vira string comum e morre ali. O template é um objeto que continua vivo: **valida** as variáveis, é **reutilizável** e é um **Runnable** — encaixa numa chain com `|`. Essa última é a vantagem decisiva.

## PromptTemplate x ChatPromptTemplate

| | `PromptTemplate` | `ChatPromptTemplate` |
|---|---|---|
| Método | `.format()` | `.format_messages()` |
| Retorno | uma **string** | uma **lista de mensagens** |
| Papéis | não existe | `system` / `user` / `assistant` |
| Histórico | não | sim |

Modelos modernos são de **conversa** e tratam cada papel de forma diferente: `system` = regras e persona, `user` = a pergunta, `assistant` = o que já foi respondido.

Com `PromptTemplate` você manda um bloco de texto solto — vira uma única mensagem de usuário, sem como separar regra de pergunta.

**Regra prática:** com chat model (quase sempre), use `ChatPromptTemplate`. `PromptTemplate` serve para tarefas de uma tacada só, sem conversa nem persona.
