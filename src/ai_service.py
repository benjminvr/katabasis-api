import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_MODEL")

def get_chat_response(messages):
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=messages,
        max_tokens=200,
        temperature=0.9,
        top_p=1.0
    )

    return response.choices[0].message.content