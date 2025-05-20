import sys
import os
from chatLogic import retrieveDocs
from chatLogic import vectorStore
from chatLogic import llm
from chatLogic import buildPrompt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from streamlit_chat import message
import streamlit as st
st.set_page_config(page_title="Fine Lines", page_icon="🔎")
st.title("🔎 Fine Lines")
st.write("ALBWEES, you dont have to read the fine print anymore! Ask straightaway!")

if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["user"]):
        st.markdown(message["content"])

if query := st.chat_input("ask away..."):
    with st.chat_message("user"):
        st.markdown(query)
    retrievedDocs = retrieveDocs(query, vectorStore)
    context = "\n\n".join(doc.page_content for doc in retrievedDocs)
    prompt = buildPrompt(query,context)
    placeholder = st.empty()
    responseStream = llm.stream(prompt)
    finalOutput = ""
    for responseToken in responseStream:
        finalOutput += responseToken.content
        with placeholder.chat_message("assistant"):
            placeholder.markdown(finalOutput)
    st.session_state.messages.append({"role": "assistant", "content": finalOutput})