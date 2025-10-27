from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_core.documents import Document
import os, tempfile

def _save_to_tmp(uploaded_file) -> str:
    # uploaded_file is a streamlit UploadedFile
    suffix = os.path.splitext(uploaded_file.name)[-1].lower()
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, 'wb') as f:
        f.write(uploaded_file.read())
    return path

def load_document(uploaded_file) -> List[Document]:
    """Load a resume or JD file into LangChain Documents."""
    path = _save_to_tmp(uploaded_file)
    ext = os.path.splitext(path)[-1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(path)
    elif ext in (".docx", ".doc"):
        loader = Docx2txtLoader(path)
    else:
        loader = TextLoader(path)
    docs = loader.load()
    # Clean temporary file; loaders have read it
    try:
        os.remove(path)
    except Exception:
        pass
    return docs
