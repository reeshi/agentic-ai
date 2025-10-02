# this file is responsible for indexing phase of RAG.
import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

pdf_path = Path(__file__).parent / "nodejs.pdf"

# load this file in python program
loader = PyPDFLoader(file_path=pdf_path)
# In docs we get the data of the pdf page by page
# for eg we can access any page data by docs[page_number]
docs = loader.load()

# Split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
chunks = text_splitter.split_documents(documents=docs)


# Create vector embeddings for chunks and store it in the vector db.
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = QdrantVectorStore.from_documents(
    documents=docs,
    embedding=embedding_model,
    url=os.getenv("QDRANT_DB_URL"),
    collection_name="learning_rag",
)

print("Indexing of documents done...")
