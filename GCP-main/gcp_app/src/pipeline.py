from typing import Dict, Any
from src.components.loader import load_document
from src.components.Text_preprcessing import preprocess_documents
from src.components.push_database import push_raw_documents
from src.components.embedding_faiss import embed_and_store_faiss_ollama
from src.components.langchain_retrival import similarity_search
from src.components.scoring_reportformating import generate_full_report
from src.loggers import logger

def run_resume_pipeline(resume_file, jd_file, model_name: str = "text-embedding-004") -> Dict[str, Any]:
    logger.info("📥 Loading documents...")
    resume_docs = load_document(resume_file)
    jd_docs = load_document(jd_file)

    logger.info("🧹 Preprocessing (chunking) documents...")
    resume_chunks = preprocess_documents(resume_docs)
    jd_chunks = preprocess_documents(jd_docs)

    logger.info("💾 (Optional) Push raw docs to DB...")
    push_raw_documents(resume_docs + jd_docs)

    logger.info("🧠 Build / load FAISS index for resume...")
    index = embed_and_store_faiss_ollama(resume_chunks, index_name="resume_index", reuse_if_exists=True)

    logger.info("🔎 Similarity search vs JD...")
    jd_text = " ".join([d.page_content for d in jd_chunks])
    top_resume_chunks = similarity_search(query=jd_text, index=index, k=5)

    logger.info("📝 Generate final report...")
    report = generate_full_report(resume_chunks=top_resume_chunks, jd_text=jd_text)
    return report
