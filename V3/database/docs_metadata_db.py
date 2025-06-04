import sqlite3
import os
from datetime import datetime

DB_PATH = "database/docs_metadata.db"

def init_docs_metadata_db():
    """Initialize document metadata database"""
    os.makedirs("database", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS docs_metadata (
            doc_id TEXT PRIMARY KEY,
            custom_title TEXT NOT NULL,
            filename TEXT NOT NULL,
            department TEXT NOT NULL,
            version TEXT DEFAULT '1.0',
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            uploaded_by TEXT NOT NULL,
            file_size INTEGER,
            chunk_count INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

def add_document_metadata(doc_id, custom_title, filename, department, uploaded_by, version="1.0", file_size=0, chunk_count=0):
    """Add document metadata to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO docs_metadata 
            (doc_id, custom_title, filename, department, uploaded_by, version, file_size, chunk_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (doc_id, custom_title, filename, department, uploaded_by, version, file_size, chunk_count))
        
        conn.commit()
        return True, "Document metadata added successfully"
    except sqlite3.IntegrityError:
        return False, "Document ID already exists"
    except Exception as e:
        return False, f"Error adding metadata: {str(e)}"
    finally:
        conn.close()

def remove_document_metadata(doc_id):
    """Remove document metadata from database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM docs_metadata WHERE doc_id = ?', (doc_id,))
    rows_affected = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return rows_affected > 0

def get_documents_by_department(department):
    """Get all documents for a specific department"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT doc_id, custom_title, filename, version, upload_date, uploaded_by, chunk_count
        FROM docs_metadata WHERE department = ?
        ORDER BY upload_date DESC
    ''', (department,))
    
    results = cursor.fetchall()
    conn.close()
    
    return results

def get_all_documents():
    """Get all documents (for master admin)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT doc_id, custom_title, filename, department, version, upload_date, uploaded_by, chunk_count
        FROM docs_metadata
        ORDER BY department, upload_date DESC
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    return results

def document_exists(doc_id):
    """Check if document ID exists"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT 1 FROM docs_metadata WHERE doc_id = ?', (doc_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result is not None

# Initialize database on import
init_docs_metadata_db()
