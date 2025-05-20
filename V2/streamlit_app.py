import streamlit as st

upload_page = st.Page("upload.py",title="Upload Docs",icon="📃")
chatbot_page = st.Page("chatbot.py",title="Chatbot",icon="🗨️")

pg = st.navigation([chatbot_page,upload_page])
pg.run()