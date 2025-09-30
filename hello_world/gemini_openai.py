from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

# We are using google gemini model from openai sdk
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "system",
            "content": "You are expert in math and only and only ans maths related query. if the query is not related to maths than don't answer the query",
        },
        {
            "role": "user",
            "content": "Hey There, can you write a python code which add two numbers",
        },
    ],
)

print(response.choices[0].message.content)
