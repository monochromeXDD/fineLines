import streamlit as st

# Check authorization  
if not st.session_state.get("authStatus") or st.session_state.get("role") not in ["DBAHR", "DBUHR"]:
    st.warning("Unauthorized access")
    st.switch_page("app.py")
    st.stop()

st.title("👥 HR Department Chatbot")
st.write("**Access:** HR Department Documents Only")

# Navigation
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🏠 Main"):
        st.switch_page("app.py")
    
    # Admin panel access for HR admins
    if st.session_state.role == "DBAHR":
        if st.button("🛠️ HR Admin"):
            st.switch_page("pages/dbahr_panel.py")

with col2:
    st.write("")  # Spacer

# HR-specific chatbot
from chatbot.chatbot_engine import create_chatbot
create_chatbot("HR")
