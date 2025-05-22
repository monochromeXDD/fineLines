from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from embed import chromaDir
from embed import embedModel
chatModel = "granite3.3:2b"
llm = ChatOllama(
    model = chatModel,
    temperature=0.3
)
embeddings = OllamaEmbeddings(model=embedModel)
vectorStore = Chroma(
    collection_name = "fineLines",
    embedding_function = embeddings,
    persist_directory=chromaDir
)

sysPrompt = f"You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise. If theres previous conversation in the context, answer accordingly."
