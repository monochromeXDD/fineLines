import streamlit as st

# session state
if "authStatus" not in st.session_state:
    st.session_state.authStatus = False
if "role" not in st.session_state:
    st.session_state.role = None

st.title("🔎 Fine Lines - Document Q&A System")
st.write("ALBWEES, you don't have to read the fine print anymore! Ask straightaway!")

# Guest access info
st.info("🌐 **Guest Mode**: You're currently accessing public documents. Login for department-specific access.")

# Navigation
col1, col2 = st.columns([1, 4])

with col1:
    if not st.session_state.authStatus:
        if st.button("🔐 Login"):
            st.switch_page("pages/login.py")
    else:
        st.success(f"Logged in as {st.session_state.role}")
        
        # Role-based navigation
        if st.session_state.role == "DBAM":
            if st.button("🛠️ Admin Panel"):
                st.switch_page("pages/dbam_panel.py")
        elif st.session_state.role == "DBAIT":
            if st.button("🛠️ IT Admin"):
                st.switch_page("pages/dbait_panel.py")
            if st.button("💬 IT Chatbot"):
                st.switch_page("pages/it_chatbot.py")
        elif st.session_state.role == "DBAHR":
            if st.button("🛠️ HR Admin"):
                st.switch_page("pages/dbahr_panel.py")
            if st.button("💬 HR Chatbot"):
                st.switch_page("pages/hr_chatbot.py")
        elif st.session_state.role == "DBUIT":
            if st.button("💬 IT Chatbot"):
                st.switch_page("pages/it_chatbot.py")
        elif st.session_state.role == "DBUHR":
            if st.button("💬 HR Chatbot"):
                st.switch_page("pages/hr_chatbot.py")
        
        if st.button("🚪 Logout"):
            st.session_state.authStatus = False
            st.session_state.role = None
            st.rerun()

with col2:
    st.write("")  # Spacer

# Guest chatbot (public database)
st.header("💬 Public Document Chatbot")
from chatbot.chatbot_engine import create_chatbot
create_chatbot("public")
