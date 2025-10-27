from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

def similarity_search(query: str, index: FAISS, k: int = 5) -> List[Document]:
    return index.similarity_search(query, k=k)
