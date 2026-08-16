from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate(
    input_variables=["name"],
    template="Hi, i'm {name}. Tell me a joke about {name}!"
)

text = prompt_template.format(name="Felipe")

print(text)
