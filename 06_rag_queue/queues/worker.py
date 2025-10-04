import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()

embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

vector_db = QdrantVectorStore.from_existing_collection(
    collection_name="learning_rag",
    embedding=embedding_model,
    url=os.getenv("QDRANT_DB_URL"),
)


def process_query(query: str):
    # Relevant chunks from the vector db
    search_results = vector_db.similarity_search(query=query)

    context = "\n\n\n".join(
        [
            f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}"
            for result in search_results
        ]
    )

    SYSTEM_PROMPT = f"""
        Your are a helpful AI Assistant who answers user query based on the available context retrieved from a PDF file along with page_contents and page_number.

        You should only answer the user based on the following context and navigate the user to open the right page number to know more

        Context:
        {context}
    """

    # give the context and user query to the llm so that if form a user answer.
    response = openai_client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
    )

    return response.choices[0].message.content
