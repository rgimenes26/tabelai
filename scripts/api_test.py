from google import genai
from google.genai import types
from google.genai.types import (
    Content,
    CreateCachedContentConfig,
    GenerateContentConfig,
    Part,
)
import pathlib

PROJECT_ID = "adept-rock-465214-t0"  # @param {type: "string", placeholder: "[your-project-id]", isTemplate: true}
LOCATION = "us-east1" 
MODEL_ID = "gemini-2.5-pro"  

# media = pathlib.Path("scripts")

# client = genai.Client(api_key="AIzaSyDXfkh34h8TVCMsBkqYX706qwDjyKZr13o")
client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
    # http_options=types.HttpOptions(api_version='v1')
    # api_key="AIzaSyDXfkh34h8TVCMsBkqYX706qwDjyKZr13o",
)

response = client.models.generate_content(
    model="gemini-2.5-pro", 
    contents="Palmeiras tem mundial ? "
)
print(response.text)

response.usage_metadata
response.prompt_feedback





## TESTE FILE
myfile = client.files.upload(file=media.joinpath("cnh.pdf"))
file_name = myfile.name
print(file_name)  # "files/*"

myfile = client.files.get(name=file_name)
print(myfile)


response = client.models.generate_content(
    model="gemini-2.5-pro", 
    contents=[
        "Qual o CPF e outros dados pessoais do documento?",
        myfile
    ],
)
print(response.text)

##list Files
for f in client.files.list():
  print("  ", f.name)


## TESTE CONTEXT CACHING

fileurl_CompraVendaModel = "gs://tabelai-models/ModelCompraVenda_2025_07_19.pdf"

# modelBase = client.files.upload(file=media.joinpath("models", "ModelCompraVenda_2025_07_19.pdf"))
# file_name = modelBase.name
# print(file_name)  # "files/nb2ca3voopht"

# myfile = client.files.get(name=file_name)
# print(myfile)



system_instruction = """
Você é um Escrevente de um Tabelionato de Notas. Sua função é garantir a máxima precisão e conformidade legal na elaboração de documentos.
Sua Missão Principal: A partir dos documentos de identificação que serão fornecidos (como CNH, RG, certidões de nascimento, casamento, óbito, etc.), seu dever é preencher com exatidão o modelo de escritura de venda e compra que está anexado em sua base de dados. 
Sempre faça a correta concordância verbal e nominal.
Recursos à sua Disposição:
Documentos das Partes: Arquivos contendo os dados necessários para o preenchimento.
Base de Dados de Modelos: Minuta de escritura de compra e venda padronizada pelo tabelionato.
Regras de Execução (Mandatórias e Inalteráveis):
Você deve seguir rigorosamente as seguintes diretrizes ao processar cada solicitação:
Substituição de Campos (Amarelo): Todas as palavras e símbolos destacados em amarelo nos modelos são variáveis. Você deve substituí-los precisamente pelos dados correspondentes encontrados nos documentos fornecidos.
Ignorar Orientações (Vermelho): As palavras e frases destacadas em vermelho são exclusivamente orientações, diretrizes ou instruções internas para o escrevente. Elas NÃO devem, em nenhuma hipótese, constar no texto final da procuração gerada, a menos que uma instrução específica determine o contrário de forma explícita.
Tratamento de Dados Faltantes: Se, após analisar os documentos fornecidos, uma informação necessária para preencher um campo estiver ausente, você DEVE inserir um marcador de lugar no formato *{palavra}*. Exemplos:
Se a profissão não for encontrada: *{profissão}*
Se o número de um documento estiver faltando: *{número do RG}*
Se uma data específica estiver ausente: *{data de expedição}*
Se um valor monetário não for informado: *{valor}*
Formato da Data de Lavratura: A data de lavratura do ato (a data em que a procuração é gerada) deve seguir obrigatoriamente o seguinte formato, utilizando o mês e o ano da data atual da geração. O dia deve ser sempre representado por asteriscos. Formato Padrão: Aos *** (**) dias do mês de [mês por extenso] ([número do mês]) do ano de [ano por extenso] ([ano em números]). Exemplo para uma solicitação em maio de 2025: Aos *** (**) dias do mês de maio (5) do ano de dois mil e vinte e cinco (2025).
Fidelidade Absoluta ao Modelo: O texto do modelo fornecido na base de dados é final e não pode ser alterado, modificado, expandido ou resumido. Sua tarefa se limita estritamente a substituir os campos em amarelo e a aplicar as regras acima. Não insira, sob nenhuma circunstância, informações, cláusulas ou dados que não estejam previstos na minuta original, a não ser que haja uma determinação expressa em contrário para aquela solicitação específica.
Sua execução deve ser precisa, literal e livre de qualquer criatividade ou interpretação que vá além destas regras.
"""

cached_content = client.caches.create(
    model=MODEL_ID,
    config=CreateCachedContentConfig(
        contents=[
            Content(
                role="user",
                parts=[
                    Part.from_uri(
                        file_uri="gs://tabelai-models/ModelCompraVenda_2025_07_19.pdf",
                        mime_type="application/pdf",
                    ),
                ],
            )
        ],
        system_instruction=system_instruction,
        ttl="600s",
    ),
)

response = client.models.generate_content(
    model=MODEL_ID,
    contents="Ato hibrido. Dispensa de apresentação das certidões dos distribuidores. Joao vendedor e Marcos Rogerio comprador assinam eletronicamente. Imóvel rural. ",
    config=GenerateContentConfig(
        cached_content=cached_content.name,
        temperature=0,
    ),
)

response = client.models.generate_content(
    model=MODEL_ID,
    contents="Quem foi o ultimo comprador de imóvel ? ",
    config=GenerateContentConfig(
        cached_content=cached_content.name,
        temperature=0,
    ),
)




# context = client.contexts.create(
cached_content = client.caches.create(
    # displayName="compraVenda",
    model=MODEL_ID,
    config=types.CreateCachedContentConfig(
        displayName="compraVenda",
        system_instruction=system_instruction,
        contents=[
            Part.from_uri(
                file_uri="gs://tabelai-models/ModelCompraVenda_2025_07_19.pdf",
                mime_type="application/pdf",
            ),
        ],
    )
    
    # system_instruction=system_instruction,
    # ttl="600s",
)

cached_content.display_name
client.caches.list()

#EXPORT
## MArkdown
with open("response.md", "w") as tfile:
    tfile.write(response.text)
## html
from markdown import markdown
with open("response.html", "w") as tfile:
    tfile.write(markdown(response.text))
[
   "CABEÇA",
 *['teste' for _ in range(10)]
   
]