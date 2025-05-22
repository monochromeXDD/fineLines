import sys
import os
from chatLogic import vectorStore
from chatLogic import llm
from streamlit_chat import message
import streamlit as st
from chatLogic import sysPrompt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
st.set_page_config(page_title="Fine Lines", page_icon="🔎")
st.title("🔎 Fine Lines")
st.write("ALBWEES, you dont have to read the fine print anymore! Ask straightaway!")

if "messages" not in st.session_state:
    st.session_state.messages = []

def retrieveDocs(queried,vectorStore):
    history = ""
    for message in st.session_state.messages:
        if(message["role"] == "user"):
            history = history + message["content"] + "\n"
    fullQuery = queried + history
    return vectorStore.similarity_search(fullQuery)


def buildPrompt(queried,contexted):
    contextHistory = ""
    for message in st.session_state.messages:
        contextHistory = contextHistory + "role:" + message["role"] + "\n" + "content:" + message["content"] + "\n"
    fullContext = contexted + contextHistory
    return f"{sysPrompt} + Question: {queried} Context: {fullContext} Answer: "


def chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if query := st.chat_input("ask away..."):
        with st.chat_message("user"):
            st.markdown(query)
        retrievedDocs = retrieveDocs(query, vectorStore)
        context = "\n\n".join(doc.page_content for doc in retrievedDocs)
        print(context)
        prompt = buildPrompt(query,context)
        st.session_state.messages.append({"role": "user", "content": query})
        placeholder = st.empty()
        responseStream = llm.stream(prompt)
        finalOutput = ""
        with placeholder.chat_message("assistant"):
            for responseToken in responseStream:
                finalOutput += responseToken.content
                placeholder.markdown(finalOutput)
        st.session_state.messages.append({"role": "assistant", "content": finalOutput})
        
chat()
