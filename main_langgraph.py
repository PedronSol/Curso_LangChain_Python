from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

api_key=os.getenv("GROQ_API_KEY")

modelo_llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    model="openai/gpt-oss-120b",
    temperature=0.5,
    api_key=api_key
)

prompt_consultor_praia = ChatPromptTemplate.from_messages(
    [
        ("system", "Apresente-se como Sra. Praia. Você é uma especialista em viagens com destinos para praia."),
        ("human", "{query}")
    ],
)

prompt_consultor_montanha = ChatPromptTemplate.from_messages(
    [
        ("system", "Apresente-se como Sr. Montanha. Você é um especialista em viagens com destinos para montanhas e atividades radicais."),
        ("human", "{query}")
    ],
)


cadeia_praias = prompt_consultor_praia | modelo_llm | StrOutputParser()
cadeia_montanhas = prompt_consultor_montanha | modelo_llm | StrOutputParser()

prompt_roteador = ChatPromptTemplate.from_messages(
    [
     ("system", "Responda apenas com 'praia' ou 'montanha'"),
     ("human", "{query}")   
    ]
)

print(assistente.invoke({"query": "Gostaria de uma experiência completamente nova e diferente."}))