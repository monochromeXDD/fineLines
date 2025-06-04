import streamlit as st
from langchain.chat_models import init_chat_model
from database import chroma_manager
import os

def create_chatbot(department="public"):
    """Create chatbot for specific department"""
    
    # Set up LLM
    os.environ["GROQ_API_KEY"] = st.secrets["groqAPI"]
    llm = init_chat_model("llama3-8b-8192", model_provider="groq")
    
    # Enhanced system prompt with citations
    sys_prompt = f"""You are an assistant for question-answering tasks using {department} department documents. 
    Use the following pieces of retrieved context to answer the question. 
    IMPORTANT: Always cite your sources by referencing the document titles and IDs provided in the context.
    If you don't know the answer, just say that you don't know. 
    Use three sentences maximum and keep the answer concise.
    Format your citations as [Source: Document Title (ID)] at the end of relevant sentences."""
    
    def retrieve_docs_with_sources(query):
        """Retrieve documents with source information"""
        return chroma_manager.search_documents(department, query, k=5)
    
    def build_prompt_with_sources(query, docs):
        """Build prompt with document sources for citation"""
        # Get conversation history
        history = ""
        if "messages" in st.session_state:
            for message in st.session_state.messages:
                history += f"{message['role']}: {message['content']}\n"
        
        # Build context with sources
        context_with_sources = ""
        for doc in docs:
            doc_id = doc.metadata.get("doc_id", "Unknown")
            title = doc.metadata.get("custom_title", "Untitled")
            context_with_sources += f"[Document: {title} (ID: {doc_id})]\n{doc.page_content}\n\n"
        
        return f"{sys_prompt}\n\nContext: {context_with_sources}\nConversation History: {history}\nQuestion: {query}\nAnswer: "
    
    # Initialize chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize Yapper TTS (only once)
    if "yapper" not in st.session_state and st.session_state.get("authStatus"):
        try:
            from yapper import Yapper
            st.session_state.yapper = Yapper()
        except ImportError:
            st.warning("Yapper-TTS not installed. TTS features disabled.")
            st.session_state.yapper = None
    
    # Display chat history
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Add TTS for assistant messages (only for authenticated users)
            if (message["role"] == "assistant" and 
                st.session_state.get("authStatus") and 
                st.session_state.get("yapper")):
                
                if st.button(f"🔊 Listen", key=f"tts_{i}_{hash(message['content'][:50])}"):
                    try:
                        # Use Yapper for TTS (plain mode = no LLM enhancement)
                        st.session_state.yapper.yap(message["content"], plain=True)
                        st.success("🔊 Audio played!")
                    except Exception as e:
                        st.error(f"TTS Error: {str(e)}")
    
    # Chat input
    if query := st.chat_input("Ask your question..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        
        # Retrieve relevant documents
        retrieved_docs = retrieve_docs_with_sources(query)
        
        if not retrieved_docs:
            with st.chat_message("assistant"):
                response = "I couldn't find any relevant documents to answer your question."
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            return
        
        # Generate response
        prompt = build_prompt_with_sources(query, retrieved_docs)
        
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Stream response
            try:
                for chunk in llm.stream(prompt):
                    full_response += chunk.content
                    response_placeholder.markdown(full_response)
            except Exception as e:
                full_response = f"Error generating response: {str(e)}"
                response_placeholder.markdown(full_response)
            
            # Display sources
            with st.expander("📚 Sources Used"):
                for doc in retrieved_docs:
                    doc_id = doc.metadata.get("doc_id", "Unknown")
                    title = doc.metadata.get("custom_title", "Untitled")
                    department_name = doc.metadata.get("department", "Unknown")
                    
                    st.write(f"**Title:** {title}")
                    st.write(f"**Document ID:** {doc_id}")
                    st.write(f"**Department:** {department_name}")
                    st.write(f"**Content Preview:** {doc.page_content[:200]}...")
                    st.divider()
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
