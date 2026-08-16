# CLAUDE.md

Este arquivo fornece orientações ao Claude Code (claude.ai/code) ao trabalhar com o código deste repositório.

## Visão Geral do Projeto

Projeto de estudo de LangChain (Python) com scripts de exemplo independentes, organizados em diretórios numerados por tópico (ex.: `1-fundamentos/`). Cada script é um exemplo autocontido executado diretamente — não há ponto de entrada de aplicação, etapa de build ou suíte de testes.

## Ambiente & Comandos

- **Sempre ative o venv antes de rodar os scripts** — o `python3` do sistema não tem as dependências instaladas e falha com `ModuleNotFoundError` (ex.: `No module named 'langchain_core'`):
  ```bash
  source venv/bin/activate
  ```
  O virtualenv fica em `./venv` (Python 3.14). Alternativa sem ativar: usar `venv/bin/python` no lugar de `python3`.
- Instalar dependências:
  ```bash
  venv/bin/pip install -r requirements.txt
  ```
- As chaves de API (`GOOGLE_API_KEY`, `OPENAI_API_KEY`) ficam em `.env` e são carregadas por script com `load_dotenv()` do `python-dotenv` — novos scripts que chamam um LLM precisam dessas duas linhas no topo.

### Executando os exemplos

```bash
python3 1-fundamentos/1-hello-world.py       # Hello world com ChatGoogleGenerativeAI (Gemini)
python3 1-fundamentos/2-init-chat-model.py   # Inicialização de modelo com init_chat_model
python3 1-fundamentos/3-prompt-template.py   # Uso de PromptTemplate (não chama LLM)
```

Os comandos acima assumem o venv ativado (`source venv/bin/activate`).

## Convenções

- Usa LangChain 1.x (além de `langgraph`); prefira as APIs atuais da versão 1.x, como `langchain.chat_models.init_chat_model`, em vez de padrões pré-1.0 depreciados.
- O LLM padrão nos exemplos é o Gemini (`gemini-2.5-flash`) via `langchain-google-genai`; `langchain-openai` também está instalado.
- Ao adicionar exemplos, siga o padrão de nomes existente: pastas de tópico numeradas (`N-topico/`) contendo scripts numerados (`N-descricao.py`), um conceito por arquivo.
