from openai import OpenAI
from dotenv import load_dotenv
import requests

load_dotenv()

client = OpenAI()


def get_whether(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"

    return "Something went wrong, please try again"


def main():
    user_query = input(">")
    response = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": user_query}]
    )

    print(f"🤖: {response.choices[0].message.content}")


main()
