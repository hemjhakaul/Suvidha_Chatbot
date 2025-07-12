import os
import base64
from constants import SAVE_DIR, FILE_LOG

def create_download_link(file_path, file_name):
    try:
        if not os.path.exists(file_path):
            return f"❌ File not found: {file_name}"
        with open(file_path, "rb") as f:
            bytes_data = f.read()
        b64 = base64.b64encode(bytes_data).decode()
        return f'<a href="data:application/pdf;base64,{b64}" download="{file_name}">📥 Download {file_name}</a>'
    except Exception as e:
        return f"❌ Error creating download link: {str(e)}"

def check_new_files(files):
    processed_files = set()
    if os.path.exists(FILE_LOG):
        with open(FILE_LOG, "r") as f:
            processed_files = set(line.strip() for line in f.readlines() if line.strip())
    
    new_files = []
    duplicates = []
    for file in files:
        if file.name not in processed_files:
            new_files.append(file)
        else:
            duplicates.append(file.name)
    return new_files, duplicates

def update_file_log(files):
    try:
        with open(FILE_LOG, "a") as f:
            for file in files:
                f.write(file.name + "\n")
    except Exception as e:
        raise Exception(f"Error updating file log: {str(e)}")

def save_uploaded_file(uploaded_file):
    file_path = os.path.join(SAVE_DIR, uploaded_file.name)
    uploaded_file.seek(0)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    return file_path