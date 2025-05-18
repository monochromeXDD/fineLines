# ** NOT USING LANGGRAPH **
# langgraph is for advanced ppurposes, we'll keep it simple for the prototype

# retrieval

from modelInstantiation import llm
from embedVectorDB import vector_store
from langchain_core.documents import Document
def retrieve(query,vector_store):
    return vector_store.similarity_search(query)

def generate_answer(ret_doc,ques):
    doc_content = "\n\n".join(doc.page_content for doc in ret_doc)
    prompt = f"You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise. Question: {ques} Context: {doc_content} Answer:"" "
    response = llm.invoke(prompt)
    return response.content
    

query=input("\n ask someting:")
retrieved_docs = retrieve(query,vector_store)
print(generate_answer(retrieved_docs,query))
#for returning the sources: https://python.langchain.com/docs/how_to/qa_sources/