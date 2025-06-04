import streamlit as st
from database import chroma_manager
from database.docs_metadata_db import add_document_metadata, remove_document_metadata, get_documents_by_department

# Check authorization
if not st.session_state.get("authStatus") or st.session_state.get("role") != "DBAHR":
    st.warning("Unauthorized access")
    st.switch_page("app.py")
    st.stop()

st.title("👥 HR Admin Panel")
st.write("**Role:** HR Database Admin - Manage HR department documents")

# Navigation
col1, col2 = st.columns(2)
with col1:
    if st.button("🏠 Back to Main"):
        st.switch_page("app.py")
with col2:
    if st.button("💬 HR Chatbot"):
        st.switch_page("pages/hr_chatbot.py")

# Upload Section
st.header("📤 Upload HR Document")

col1, col2 = st.columns(2)
with col1:
    doc_id = st.text_input("Document ID")
with col2:
    version = st.text_input("Version", value="1.0")

custom_title = st.text_input("Custom Title")
uploaded_file = st.file_uploader("Choose PDF file", type="pdf")

if st.button("Upload Document"):
    if not all([doc_id, custom_title, uploaded_file]):
        st.error("Please fill all fields and select a file")
    else:
        with st.spinner("Processing document..."):
            try:
                documents = chroma_manager.process_pdf(uploaded_file.read(), uploaded_file.name)
                
                success, message = chroma_manager.add_document(
                    "HR", doc_id, custom_title, documents, "hradmin"
                )
                
                if success:
                    add_document_metadata(
                        doc_id, custom_title, uploaded_file.name, "HR", 
                        "hradmin", version, len(uploaded_file.read()), len(documents)
                    )
                    st.success(f"✅ Document uploaded to HR database")
                else:
                    st.error(f"❌ Upload failed: {message}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Remove Section
st.header("🗑️ Remove HR Document")
remove_doc_id = st.text_input("Document ID to Remove")

if st.button("Remove Document"):
    if remove_doc_id:
        success, message = chroma_manager.remove_document("HR", remove_doc_id)
        if success:
            remove_document_metadata(remove_doc_id)
            st.success(f"✅ Document removed from HR database")
        else:
            st.error(f"❌ {message}")

# HR Documents List
st.header("📋 HR Documents")
documents = get_documents_by_department("HR")

if documents:
    for doc in documents:
        doc_id, title, filename, version, upload_date, uploaded_by, chunk_count = doc
        
        with st.expander(f"📄 {title}"):
            st.write(f"**ID:** {doc_id}")
            st.write(f"**Version:** {version}")
            st.write(f"**Uploaded:** {upload_date}")
            st.write(f"**Chunks:** {chunk_count}")
else:
    st.info("No HR documents found")
