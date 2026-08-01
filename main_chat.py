from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

modelo = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    model="openai/gpt-oss-120b",
    temperature=0.5
)

# Exemplo de interação com IA sem memória. Neste exemplo, o modelo utilizado não é capaz de armazenar as informações entre as respostas, fazendo com que
# não haja a criação do contexto e, portanto, melhor interação entre usuário e modelo

lista_perguntas = [
    "Quero visitar um no Brasil, que seja famoso por suas praias e sua cultura. Poderia sugerir?",
    "Qual a melhor época do ano para ir?"
]

# for pergunta in lista_perguntas:
#     resposta = modelo.invoke(pergunta)
#     print(f"Usuário: {pergunta}\n")
#     print(f"IA: {resposta.content}n")

# Para adicionar histórico no chat de interação com o modelo, é preciso inserir este histórico a cada interação do usuário com o modelo
prompt_sugestao = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um guia de viagem especializado em destinos brasileiros. Apresente-se como Sr. Passeios"),
        ("placeholder", "{historico}"),
        ("human", "{query}")
    ]
)

cadeia = prompt_sugestao | modelo | StrOutputParser()

memoria = {}
sessao = "aula_langchain"

def historico_sessao(sessao: str):
    if sessao not in memoria:
        memoria[sessao] = InMemoryChatMessageHistory()
    return memoria[sessao]

cadeia_com_memoria = RunnableWithMessageHistory(
    runnable=cadeia,
    get_session_history=historico_sessao,
    input_messages_key="query",
    history_messages_key="historico"
)

for pergunta in lista_perguntas:
    resposta = cadeia_com_memoria.invoke(
        {"query": pergunta},
        config={"session_id":sessao}
    )
    print(f"Usuário: {pergunta}\n")
    print(f"IA: {resposta}n")