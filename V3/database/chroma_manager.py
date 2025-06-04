import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import streamlit as st
import asyncio

# Database paths
DB_PATHS = {
    "public": "./chroma_db/public",
    "IT": "./chroma_db/it", 
    "HR": "./chroma_db/hr"
}

def get_embeddings():
    """Get embeddings function"""
    os.environ["GOOGLE_API_KEY"] = st.secrets["geminiEmbedAPI"]
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def ensure_directories():
    """Ensure database directories exist"""
    for path in DB_PATHS.values():
        try:
            if os.path.exists(path) and not os.path.isdir(path):
                os.remove(path)
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            st.error(f"Error creating directory {path}: {str(e)}")

def get_vectorstore(department):
    """Get vector store for specific department"""
    ensure_directories()
    
    db_path = DB_PATHS.get(department)
    if not db_path:
        raise ValueError(f"Invalid department: {department}")
    
    embeddings = get_embeddings()
    
    return Chroma(
        collection_name=f"{department.lower()}_collection",
        embedding_function=embeddings,
        persist_directory=db_path
    )

def process_pdf(pdf_bytes, filename):
    """Process PDF and return document chunks"""
    temp_path = f"temp_{filename}"
    with open(temp_path, "wb") as f:
        f.write(pdf_bytes)
    
    try:
        loader = PyPDFLoader(temp_path)
        pages = []
        
        async def load_pages():
            async for page in loader.alazy_load():
                pages.append(page)
        
        asyncio.run(load_pages())
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=300,
            add_start_index=True
        )
        
        return text_splitter.split_documents(pages)
        
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def add_document(department, doc_id, custom_title, documents, uploaded_by):
    """Add document to specific department's vector store"""
    try:
        vectorstore = get_vectorstore(department)
        
        # Add metadata to each chunk
        for i, doc in enumerate(documents):
            doc.metadata.update({
                "doc_id": doc_id,
                "custom_title": custom_title,
                "department": department,
                "uploaded_by": uploaded_by,
                "chunk_index": i,
                "total_chunks": len(documents)
            })
        
        # Generate unique IDs for each chunk
        chunk_ids = [f"{doc_id}_chunk_{i}" for i in range(len(documents))]
        
        vectorstore.add_documents(documents=documents, ids=chunk_ids)
        return True, f"Added {len(documents)} chunks to {department} database"
        
    except Exception as e:
        return False, f"Error adding document: {str(e)}"

def remove_document(department, doc_id):
    """Remove document from specific department's vector store"""
    try:
        vectorstore = get_vectorstore(department)
        
        # Get all documents to find matching chunk IDs
        collection = vectorstore._collection
        all_docs = collection.get()
        
        # Find IDs that start with the doc_id
        ids_to_delete = []
        if all_docs and 'ids' in all_docs:
            for stored_id in all_docs['ids']:
                if stored_id.startswith(f"{doc_id}_chunk_"):
                    ids_to_delete.append(stored_id)
        
        if ids_to_delete:
            vectorstore.delete(ids=ids_to_delete)
            return True, f"Removed {len(ids_to_delete)} chunks from {department} database"
        else:
            return False, f"No document found with ID: {doc_id}"
            
    except Exception as e:
        return False, f"Error removing document: {str(e)}"

def search_documents(department, query, k=5):
    """Search documents in specific department's database"""
    try:
        vectorstore = get_vectorstore(department)
        docs = vectorstore.similarity_search(query, k=k)
        return docs
    except Exception as e:
        st.error(f"Error searching documents: {str(e)}")
        return []
