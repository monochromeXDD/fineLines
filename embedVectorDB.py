# from the bert paper and langchain doc:
''' Embedding models transform human language into a format that machines can understand and compare with speed and accuracy. 
These models take text as input and produce a fixed-length array of numbers, a numerical fingerprint of the text's semantic meaning. 
Embeddings allow search system to find relevant documents not just based on keyword matches, but on semantic understanding.'''
# the default openAI embed model is not used here purposefully to prevent closed-sources projects from seeping in with monthly API bills and privacy concernms
# the main choice was between ollama and huggingFace embedding models because they're open source and are natively supported by langChain
# curretly choosing ollama because ill be using running the LLM locally too (gemma)
# gemma because it is quantization aware
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from textSplitter import all_splits #imporrting the text splits of the pdf
import os
''' chromaDir = "./chroma_langchain_db"
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = Chroma(
collection_name="finePrinter",
embedding_function= embeddings,
persist_directory=chromaDir,
)
if not os.path.exists(os.path.join(chromaDir,"index")):
    print("embedding and saving the chunks...")
    document_ids=vector_store.add_documents(documents=all_splits)
    print(f"these are the docuemnt ids of the first 3 embedded chunks: {document_ids[:3]}")
else:
    print("vector db already exists, skipping embeddings:")
'''

import os
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from textSplitter import all_splits

chromaDir = "./chroma_langchain_db"
embeddings = OllamaEmbeddings(model="nomic-embed-text")

print(f"Checking directory: {chromaDir}")
if os.path.exists(chromaDir):
    print(f"Directory '{chromaDir}' exists with contents: {os.listdir(chromaDir)}")
else:
    print(f"Directory '{chromaDir}' does not exist.")

if not os.path.exists(os.path.join(chromaDir, "index")):
    print("embedding and saving the chunks...")
    vector_store = Chroma(
        collection_name="finePrinter",
        embedding_function=embeddings,
        persist_directory=chromaDir,
    )
    document_ids = vector_store.add_documents(documents=all_splits)
    print(f"These are the document ids of the first 3 embedded chunks: {document_ids[:3]}")
else:
    print("vector db already exists, skipping embeddings:")
    vector_store = Chroma(
        collection_name="finePrinter",
        embedding_function=embeddings,
        persist_directory=chromaDir,
    )