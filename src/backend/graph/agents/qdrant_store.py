from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore

from langchain.tools.retriever import create_retriever_tool

from .config import qdrant_url

model_name = "intfloat/multilingual-e5-large-instruct"

embeddings = HuggingFaceEndpointEmbeddings(
    model=model_name,
    task="feature-extraction"
)

qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="TaroUser",
    url=qdrant_url
)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)

retriever = create_retriever_tool(
    retriever=qdrant.as_retriever(),
    name='History chat with user',
    description='Use this when you need info from chat history'
)

