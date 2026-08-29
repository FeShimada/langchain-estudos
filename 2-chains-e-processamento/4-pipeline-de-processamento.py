from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

template_translate = PromptTemplate(
    input_variables=["text"],
    template="Translate this into English: {text}"
)

template_summary = PromptTemplate(
    input_variables=["text"],
    template="Summarize this in 1 sentence (max 10 words): {text}"
)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

chain_translate = template_translate | llm | StrOutputParser()

pipeline = {"text": chain_translate} | template_summary | llm | StrOutputParser()

result = pipeline.invoke({"text": "Oi, tudo bem?"})
print(result)
