# Example of Zero shot prompting
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# We are using google gemini model from openai sdk
client = OpenAI(
    api_key="AIzaSyB_71b98-uHDjVp0igqvneFgaNfyLdkafg",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Zero Shot Prompting: Directly giving the instructions to the model
SYSTEM_PROMPT = "You should only and only answer the coding related questions. Do not answer anything else. Your name is Alexa. If user asks something other than coding, just say sorry"

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "Hey There, can you tell me a joke",
        },
    ],
)

print(response.choices[0].message.content)
