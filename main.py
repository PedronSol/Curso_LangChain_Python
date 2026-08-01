from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import Field, BaseModel
from langchain.globals import set_debug
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

set_debug(True)

# Criação de uma classe para estruturar o formato de saída da resposta
class Destino(BaseModel):
    cidade:str = Field(description="A cidade recomendada para visitar")
    motivo:str = Field(description="Motivo pelo qual é interessante visitar essa cidade")

class Restaurantes(BaseModel):
    cidade:str = Field(description="A cidade recomendada para visitar")
    restaurantes:str = Field(description="Restaurantes recomendados na cidade")

parser_destino = JsonOutputParser(pydantic_object=Destino)
parser_restaurantes = JsonOutputParser(pydantic_object=Restaurantes)

# Encadeamento de Prompts

prompt_destino = PromptTemplate(
    template="""
    Sugira uma cidade dado o meu interesse por {interesse}.

    Retorne APENAS um JSON estrito contendo as chaves 'cidade' e 'motivo'.

    {formato_de_saida}
    """,
    input_variables=["interesse"],
    partial_variables={"formato_de_saida":parser_destino.get_format_instructions()}
)

# Por funcionar em formato encadeado, o LangChain permite referenciar variáveis vindas de cadeias anteriores. Neste caso, referencia-se o campo "cidade"
# da cadeira de destino
prompt_restaurantes = PromptTemplate(
    template="""
    Sugira restaurantes populares entre locais em {cidade}.

    Retorne APENAS um JSON estrito contendo as chaves 'cidade' e 'restaurantes'.

    {formato_de_saida}
    """,
    partial_variables={"formato_de_saida":parser_restaurantes.get_format_instructions()}
)

prompt_cultural = PromptTemplate(
    template="Sugira atividades e locais culturais em {cidade}" \
    "" \
    "Retorne APENAS um JSON estrito contendo as chaves 'cidade' e 'centros_culturais'"
)

modelo = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
    model="openai/gpt-oss-120b",
    temperature=0.5
)

# Na cadeia a seguir, separada pelo operador "|" (pipe), temos o template do prompt, o modelo a ser utilizado e a forma de saída da resposta do modelo (que neste caso)
# é uma string
cadeia_destino = prompt_destino | modelo | parser_destino
cadeia_restaurantes = prompt_restaurantes | modelo | parser_restaurantes
cadeia_cultural = prompt_cultural | modelo | JsonOutputParser()

cadeia = (cadeia_destino | cadeia_restaurantes | cadeia_cultural)

resposta = cadeia.invoke(
    {
        "interesse": "praias"
    }
)

print(resposta)
