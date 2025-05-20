from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from embed import chromaDir
from embed import embedModel
chatModel = "mistral:7b-instruct"
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

def retrieveDocs(queried,vectorStore):
    return vectorStore.similarity_search(queried)

def buildPrompt(queried,contexted):
    return f"You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise. Question: {queried} Context: {contexted} Answer:"" "
    