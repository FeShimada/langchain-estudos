# 1 — Hello World

**Chat model** = o objeto que representa o LLM. Um controle remoto padronizado: seja Gemini, GPT ou Claude, você sempre chama `.invoke()`.

```python
load_dotenv()                                              # carrega GOOGLE_API_KEY do .env
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")     # amarrado ao Google
message = llm.invoke("Hello world!")                       # string → AIMessage
print(message.content)
```

**`load_dotenv()`** — o LangChain acha a chave sozinho nas variáveis de ambiente. Por isso não passamos a chave na mão.

**`.invoke()`** — o verbo universal do LangChain ("execute isto com esta entrada"). Aparece em prompts, parsers e chains com o mesmo sentido.

**O retorno não é string** — é um `AIMessage`:

| | |
|---|---|
| `.content` | o texto da resposta |
| `.response_metadata` | infos do provedor |
| `.usage_metadata` | tokens gastos (custo) |

Daí o `.content`.
