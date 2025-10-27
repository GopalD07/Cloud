import os, tempfile, shutil
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_core.documents import Document
from src.utils.gcs_faiss import download_faiss_from_gcs, upload_faiss_to_gcs

def _embeddings():
    project = os.getenv("GCP_PROJECT")
    location = os.getenv("GCP_LOCATION", "us-central1")
    model = os.getenv("EMBEDDING_MODEL", "text-embedding-004")
    if not project:
        raise RuntimeError("GCP_PROJECT env var is required for Vertex AI embeddings.")
    return VertexAIEmbeddings(model_name=model, project=project, location=location)

def embed_and_store_faiss_ollama(documents: List[Document], index_name: str, reuse_if_exists: bool = True) -> FAISS:
    """Create (or load) a FAISS index for provided documents using Vertex AI embeddings.

    Index is stored locally under /tmp/faiss/{index_name} and synchronized with GCS if configured.

    Set GCS_BUCKET to enable persistence.

    """
    emb = _embeddings()
    local_dir = os.path.join("/tmp", "faiss", index_name)
    os.makedirs(local_dir, exist_ok=True)
    gcs_bucket = os.getenv("GCS_BUCKET")
    gcs_prefix = f"faiss_indices/{index_name}"

    # Try download from GCS if reuse requested
    if reuse_if_exists and gcs_bucket:
        downloaded = download_faiss_from_gcs(gcs_bucket, gcs_prefix, local_dir)
    else:
        downloaded = False

    if downloaded:
        vs = FAISS.load_local(local_dir, emb, allow_dangerous_deserialization=True)
        return vs

    # Build new index
    vs = FAISS.from_documents(documents, emb)
    vs.save_local(local_dir)
    if gcs_bucket:
        upload_faiss_to_gcs(gcs_bucket, gcs_prefix, local_dir)
    return vs
