import pdfplumber
import os
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from constants import TEXT_SPLITTER_CONFIG
from utils.file_utils import save_uploaded_file  # Import the file saving function

def extract_pdf_content(file_path):
    documents = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                tables = page.extract_tables()
                table_texts = []
                
                if tables:
                    for table in tables:
                        if table:
                            # Fixed syntax: added missing parenthesis and fixed indentation
                            rows = [
                                ", ".join(str(cell) if cell is not None else "" for cell in row
                                ) for row in table if row
                            ]
                            table_str = "\n".join(rows)
                            if table_str.strip():
                                table_texts.append(table_str)
                
                if table_texts:
                    content = f"Page {i+1} Text:\n{text.strip()}\n\nTables:\n" + "\n\n".join(table_texts)
                else:
                    content = f"Page {i+1} Text:\n{text.strip()}"
                
                if content.strip():
                    doc = Document(
                        page_content=content,
                        metadata={
                            "source": os.path.basename(file_path),
                            "path": file_path,
                            "page": i + 1
                        }
                    )
                    documents.append(doc)
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")
    return documents

def process_documents(uploaded_files):
    all_docs = []
    for file in uploaded_files:
        file_path = save_uploaded_file(file)  # Save the file
        all_docs.extend(extract_pdf_content(file_path))
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=TEXT_SPLITTER_CONFIG["chunk_size"],
        chunk_overlap=TEXT_SPLITTER_CONFIG["chunk_overlap"]
    )
    return splitter.split_documents(all_docs)