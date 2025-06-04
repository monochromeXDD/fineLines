import streamlit as st
from database.users_db import authenticate_user

st.title("🔐 Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

col1, col2 = st.columns(2)

with col1:
    if st.button("Login"):
        if username and password:
            success, role = authenticate_user(username, password)
            if success:
                st.session_state.authStatus = True
                st.session_state.role = role
                st.success(f"Logged in successfully as {role}")
                
                # Redirect based on role
                if role == "DBAM":
                    st.switch_page("pages/dbam_panel.py")
                elif role in ["DBAIT", "DBUIT"]:
                    st.switch_page("pages/it_chatbot.py")
                elif role in ["DBAHR", "DBUHR"]:
                    st.switch_page("pages/hr_chatbot.py")
                else:
                    st.switch_page("app.py")
            else:
                st.error("Invalid credentials")
        else:
            st.error("Please enter both username and password")

with col2:
    if st.button("Back to Main"):
        st.switch_page("app.py")

# Display test credentials
st.subheader("Test Credentials")
st.code("""
Master Admin: admin / admin123
IT Admin: itadmin / itpass123  
HR Admin: hradmin / hrpass123
IT User: ituser / ituser123
HR User: hruser / hruser123
""")
