import streamlit as st
from database.users_db import authenticate_user as db_authenticate_user

def authenticateUser(username, password):
    """
    Authenticate user credentials using the database
    Returns: (success: bool, role: str)
    """
    return db_authenticate_user(username, password)

def logout():
    """
    Logout function to clear session state
    """
    st.session_state.authStatus = False
    st.session_state.role = None
    st.session_state.displayRole = None
    st.success("Logged out successfully!")
    st.switch_page("app.py")

# Role descriptions for display purposes
ROLE_DESCRIPTIONS = {
    "DBAM": "Database Master Admin",
    "DBAIT": "IT Database Admin", 
    "DBAHR": "HR Database Admin",
    "DBUIT": "IT Database User",
    "DBUHR": "HR Database User"
}

def get_role_description(role):
    """Get human-readable role description"""
    return ROLE_DESCRIPTIONS.get(role, role)

def check_admin_access(role):
    """Check if user has admin access"""
    return role in ["DBAM", "DBAIT", "DBAHR"]

def get_user_department(role):
    """Get user's department based on role"""
    if "IT" in role:
        return "IT"
    elif "HR" in role:
        return "HR"
    return "public"

def check_role_access(required_roles, user_role):
    """Check if user role has access to specific functionality"""
    if isinstance(required_roles, str):
        required_roles = [required_roles]
    return user_role in required_roles
