import streamlit as st
from database import chroma_manager
from database.docs_metadata_db import add_document_metadata, remove_document_metadata, get_all_documents

# Check authorization
if not st.session_state.get("authStatus") or st.session_state.get("role") != "DBAM":
    st.warning("Unauthorized access")
    st.switch_page("app.py")
    st.stop()

st.title("🛠️ Master Admin Panel")
st.write("**Role:** Database Master Admin - Manage all department databases")

# Navigation
if st.button("🏠 Back to Main"):
    st.switch_page("app.py")

# Upload Section
st.header("📤 Upload Document")

col1, col2 = st.columns(2)
with col1:
    department = st.selectbox("Target Database", ["public", "IT", "HR"])
with col2:
    doc_id = st.text_input("Document ID", help="Unique identifier for the document")

custom_title = st.text_input("Custom Title", help="Human-readable title for the document")
uploaded_file = st.file_uploader("Choose PDF file", type="pdf")

if st.button("Upload Document"):
    if not all([doc_id, custom_title, uploaded_file]):
        st.error("Please fill all fields and select a file")
    else:
        with st.spinner("Processing document..."):
            try:
                # Process PDF
                documents = chroma_manager.process_pdf(uploaded_file.read(), uploaded_file.name)
                
                # Add to vector store
                success, message = chroma_manager.add_document(
                    department, doc_id, custom_title, documents, "admin"
                )
                
                if success:
                    # Add metadata to SQL database
                    meta_success, meta_message = add_document_metadata(
                        doc_id, custom_title, uploaded_file.name, department, 
                        "admin", "1.0", len(uploaded_file.read()), len(documents)
                    )
                    
                    if meta_success:
                        st.success(f"✅ Document uploaded successfully to {department} database")
                        st.info(f"Created {len(documents)} chunks")
                    else:
                        st.warning(f"Document uploaded but metadata error: {meta_message}")
                else:
                    st.error(f"❌ Upload failed: {message}")
                    
            except Exception as e:
                st.error(f"Error processing document: {str(e)}")

# Remove Section
st.header("🗑️ Remove Document")

remove_doc_id = st.text_input("Document ID to Remove")
remove_department = st.selectbox("From Database", ["public", "IT", "HR"], key="remove_dept")

if st.button("Remove Document", type="secondary"):
    if remove_doc_id:
        # Remove from vector store
        success, message = chroma_manager.remove_document(remove_department, remove_doc_id)
        
        if success:
            # Remove from metadata database
            remove_document_metadata(remove_doc_id)
            st.success(f"✅ Document {remove_doc_id} removed from {remove_department} database")
        else:
            st.error(f"❌ Removal failed: {message}")
    else:
        st.error("Please enter Document ID")

# Document List
st.header("📋 All Documents")

documents = get_all_documents()
if documents:
    for doc in documents:
        doc_id, title, filename, dept, version, upload_date, uploaded_by, chunk_count = doc
        
        with st.expander(f"📄 {title} ({dept})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**ID:** {doc_id}")
                st.write(f"**Department:** {dept}")
                st.write(f"**Filename:** {filename}")
                st.write(f"**Version:** {version}")
                st.write(f"**Uploaded:** {upload_date}")
                st.write(f"**Chunks:** {chunk_count}")
            
            with col2:
                if st.button(f"🗑️ Delete", key=f"del_{doc_id}"):
                    # Remove from both vector store and metadata
                    vs_success, vs_message = chroma_manager.remove_document(dept, doc_id)
                    if vs_success:
                        remove_document_metadata(doc_id)
                        st.success(f"Deleted {doc_id}")
                        st.rerun()
                    else:
                        st.error(vs_message)
else:
    st.info("No documents in database")
