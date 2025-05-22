from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chat_models import init_chat_model
from embed import chromaDir
from embed import embedModel
import os
from apiKeys import groqAPI
chatModel = "granite3.3:2b"
#llm = ChatOllama(
#    model = chatModel,
#    temperature=0.3
#)



os.environ["GROQ_API_KEY"] = groqAPI

llm = init_chat_model("llama3-8b-8192", model_provider="groq")

embeddings = OllamaEmbeddings(model=embedModel)
vectorStore = Chroma(
    collection_name = "fineLines",
    embedding_function = embeddings,
    persist_directory=chromaDir
)

sysPrompt = f"You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise. If theres previous conversation in the context, answer accordingly."