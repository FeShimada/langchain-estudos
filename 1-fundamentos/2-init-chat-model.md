# 2 — init_chat_model

Importar `ChatGoogleGenerativeAI` direto amarra o código ao Google. `init_chat_model` é uma **fábrica**: trocar de provedor vira trocar uma string. É o padrão do LangChain 1.x.

```python
from langchain.chat_models import init_chat_model      # pacote genérico, sem menção ao Google

gemini = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
gemini.invoke("Hello world!").content                  # uso idêntico ao exemplo 1
```

- `"gemini-2.5-flash"` → **qual** modelo
- `model_provider` → **de quem** é. Opcional quando dá para deduzir pelo nome (`gpt-*` → OpenAI), mas explícito é mais legível.

Trocar de modelo é só isto:

```python
init_chat_model("gpt-5", model_provider="openai")
init_chat_model("claude-opus-5", model_provider="anthropic")
```

O pacote da integração ainda precisa estar instalado — o que sumiu foi o acoplamento no *seu* código.

Todos os chat models têm a mesma interface (`.invoke`, `.stream`, `.batch`). Essa padronização é o que torna as **chains** possíveis.
