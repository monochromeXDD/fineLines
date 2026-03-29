import streamlit as st

st.set_page_config(page_title="FineLines - Guest", page_icon="assets/alba_logo.png",initial_sidebar_state="collapsed")
st.logo(image="assets/alba_logo.png", size="large", icon_image="assets/alba_logo.png", link="https://www.albasmelter.com/")
# session state
if "authStatus" not in st.session_state:
    st.session_state.authStatus = False
if "role" not in st.session_state:
    st.session_state.role = None

# Navigation
col1, col2, col3 = st.columns([0.33, 0.33, 0.33])

with col3:
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

# Guest access info
with col2:
    st.image("assets/alba_logo.png", width=512)  # Spacer

with col1:
    st.markdown(f"Current Role: {st.session_state.role}")
st.title("🔎 Fine Lines")
st.write("ALBWEES, you don't have to read the fine print anymore! Ask straightaway!")




# Guest chatbot (public database)
from chatbot.chatbot_engine import create_chatbot
create_chatbot("public")
