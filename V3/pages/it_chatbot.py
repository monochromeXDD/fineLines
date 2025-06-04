import streamlit as st

# Check authorization
if not st.session_state.get("authStatus") or st.session_state.get("role") not in ["DBAIT", "DBUIT"]:
    st.warning("Unauthorized access")
    st.switch_page("app.py")
    st.stop()

st.title("💻 IT Department Chatbot")
st.write("**Access:** IT Department Documents Only")

# Navigation
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🏠 Main"):
        st.switch_page("app.py")
    
    # Admin panel access for IT admins
    if st.session_state.role == "DBAIT":
        if st.button("🛠️ IT Admin"):
            st.switch_page("pages/dbait_panel.py")

with col2:
    st.write("")  # Spacer

# IT-specific chatbot
from chatbot.chatbot_engine import create_chatbot
create_chatbot("IT")
