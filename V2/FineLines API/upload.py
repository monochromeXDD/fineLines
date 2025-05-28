import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from embed import processPDF
from embed import embedMaster

def uploadDocs():
    st.set_page_config(page_title="Upload Documents", page_icon="🔎")
    st.title("🔎 Upload Documents")
    st.write(f"Hi, {st.user.name}, ")
    st.button("Logout",on_click=st.logout)
    uploaded_files = st.file_uploader("upload PDF(s)",type="pdf",accept_multiple_files=True)
    if uploaded_files is not None:
        file_names = [file.name for file in uploaded_files]
        st.info(f"File(s) uploaded: {', '.join(file_names)}")
        st.write(f"File(s) {', '.join(file_names)} are being processed")
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        # logic for embedding
        splits = processPDF(bytes_data) # returns allSplits
        type = embedMaster(splits)
        if (type==1):
            st.success(f"created a new dB successfully with {len(splits)} new chunks.")
        elif (type==2):
            st.success(f"added {len(splits)} new chunks to the existing dB")
        else:
            st.info("some error dw whart")

def loginScreen():
    st.header("admin access req to make changes to the dB")
    st.subheader("please login:")
    st.button("Log in with Google",on_click=st.login)
    st.stop()


if not st.user.is_logged_in:
    loginScreen()
    st.stop()
else:
    uploadDocs()
