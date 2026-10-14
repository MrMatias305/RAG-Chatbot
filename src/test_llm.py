from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()

response = client.responses.create(
    model='gpt-4.1-mini',
    input="Explain AI in 2 sentences.",
)

print(response.output_text)