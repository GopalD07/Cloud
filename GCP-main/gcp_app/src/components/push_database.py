import os
from typing import List
from langchain_core.documents import Document
from pymongo import MongoClient

def push_raw_documents(docs: List[Document], collection_name: str = "raw_docs") -> None:
    uri = os.getenv("MONGODB_URI")
    if not uri:
        # DB is optional; skip silently
        return
    client = MongoClient(uri)
    db = client.get_default_database() or client["resume_jd"]
    col = db[collection_name]
    payload = [{"text": d.page_content, **(d.metadata or {})} for d in docs]
    if payload:
        col.insert_many(payload)
