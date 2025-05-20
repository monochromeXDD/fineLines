from langchain_community.document_loaders import PyPDFLoader
import asyncio
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
chunkSize = 1500
chunkOverlap = 300
chromaDir = "./chromaLangchain" # config
embedModel = "nomic-embed-text:latest" # config
def processPDF(pdf_bytes):
    with open("temp.pdf", "wb") as f:
        f.write(pdf_bytes)
    
    loader = PyPDFLoader("temp.pdf")
    pages = []
    async def main():
        async for page in loader.alazy_load():
            pages.append(page)
    asyncio.run(main())
    textSplitter = RecursiveCharacterTextSplitter(
        chunk_size = chunkSize, #config
        chunk_overlap = chunkOverlap, #config
        add_start_index = True
    )
    allSplits = textSplitter.split_documents(pages)
    if os.path.exists("temp.pdf"):
        os.remove("temp.pdf")
    return allSplits



embeddings = OllamaEmbeddings(model=embedModel)
def embedMaster(allSplits):
    #for non-existing dB
    if not os.path.exists(os.path.join(chromaDir,"chroma.sqlite3")):
        vectorStore = Chroma(
            collection_name = "fineLines",
            embedding_function = embeddings,
            persist_directory=chromaDir
        )
        vectorStore.add_documents(documents=allSplits)
        return
    else:
        print("dB already exists. adding new docs:")
        vectorStore = Chroma(
            collection_name = "fineLines",
            embedding_function = embeddings,
            persist_directory=chromaDir
        )
        vectorStore.add_documents(documents=allSplits)
        return 2