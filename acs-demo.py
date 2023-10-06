
import openai
import os
import json
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions


openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
deployment_name = "gpt-35-turbo-test"

user_prompt = "What is John's job in the movie John Wick?"

response = openai.ChatCompletion.create(
    engine= deployment_name,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f'{user_prompt}'},
    ]
)

answer = response['choices'][0]['message']['content']


# Contruct request
request = AnalyzeTextOptions(text=answer)


#########   validate content safety   #########

# Create a Content Safety client and authenticate with Azure Key Credential
client = ContentSafetyClient(
    endpoint=os.getenv("AZURE_ACSAFETY_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("AZURE_ACSAFETY_KEY"))
    
)

# Analyze text
try:
    response = client.analyze_text(request)
except HttpResponseError as e:
    print("Analyze text failed.")
    if e.error:
        print(f"Error code: {e.error.code}")
        print(f"Error message: {e.error.message}")
        raise
    print(e)
    raise

if response.hate_result:
    print(f"Hate severity: {response.hate_result.severity}")
if response.self_harm_result:
    print(f"SelfHarm severity: {response.self_harm_result.severity}")
if response.sexual_result:
    print(f"Sexual severity: {response.sexual_result.severity}")
if response.violence_result:
    print(f"Violence severity: {response.violence_result.severity}")


