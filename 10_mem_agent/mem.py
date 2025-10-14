import os
from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

config = {
    "embedder": {
        "provider": "openai",
        "config": {"api_key": OPENAI_API_KEY, "model": "text-embedding-3-small"},
    },
    "llm": {
        "provider": "openai",
        "config": {"api_key": OPENAI_API_KEY, "model": "gpt-4.1"},
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {"host": "localhost", "port": 6333},
    },
}

client = OpenAI()
mem_client = Memory.from_config(config_dict=config)
messages = []

while True:
    user_query = input("> ")
    if user_query == "exit":
        break

    # Search the relevant memory of the query
    search_memory = mem_client.search(query=user_query, user_id="Rishikesh")

    memories = [
        f"ID: {mem.get('id')}\nMemory: {mem.get('memory')}"
        for mem in search_memory.get("results")
    ]

    SYSTEM_PROMPT = f"""
        Here is the context about the users
        {memories}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ],
    )

    ai_response = response.choices[0].message.content

    print("AI: ", ai_response)

    mem_client.add(
        user_id="Rishikesh",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response},
        ],
    )

    print("Message added in memory")
