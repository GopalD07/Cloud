import os
import tempfile
from typing import Optional
from google.cloud import storage
from langchain_community.vectorstores import FAISS

def _client():
    return storage.Client()

def download_faiss_from_gcs(bucket_name: str, prefix: str, local_dir: str) -> bool:
    """Download FAISS index files from GCS into `local_dir`. Returns True if any file was downloaded."""
    client = _client()
    bucket = client.bucket(bucket_name)
    blobs = list(client.list_blobs(bucket, prefix=prefix))
    if not blobs:
        return False
    os.makedirs(local_dir, exist_ok=True)
    for b in blobs:
        # Preserve directory structure after prefix
        rel = b.name[len(prefix):].lstrip("/")
        dest_path = os.path.join(local_dir, rel)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        b.download_to_filename(dest_path)
    return True

def upload_faiss_to_gcs(bucket_name: str, prefix: str, local_dir: str) -> None:
    """Upload all files under `local_dir` to `gs://bucket/prefix/` preserving structure."""
    client = _client()
    bucket = client.bucket(bucket_name)
    for root, _, files in os.walk(local_dir):
        for fname in files:
            local_path = os.path.join(root, fname)
            rel_path = os.path.relpath(local_path, start=local_dir)
            blob = bucket.blob(os.path.join(prefix, rel_path))
            blob.upload_from_filename(local_path)
