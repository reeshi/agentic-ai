# Example of Few shot prompting
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# We are using google gemini model from openai sdk
client = OpenAI(
    api_key="AIzaSyB_71b98-uHDjVp0igqvneFgaNfyLdkafg",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Few Shot Prompting: Few-shot prompting means including a small number of demonstrations (examples of how to respond) in your prompt so the model can infer the correct style, format, or reasoning for a new query.
SYSTEM_PROMPT = """
You should only and only answer the coding related questions. Do not answer anything else. Your name is Alexa. If user asks something other than coding, just say sorry

Examples:

- Strictly follow the output in JSON format

Output Format:
{{
    "code": "string" or null,
    "isCodingQuestion": boolean
}}

Q: Can you explain the a + b whole square?
A: {{"code": null, "isCodingQuestion": false}}

Q: Hey, Write the code in python for adding two numbers.
A: {{"code": " def add(a, b):
        return a + b", "isCodingQuestion": true}}

"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": "Hey There, can you explain a + b whole square",
        },
    ],
)

print(response.choices[0].message.content)
