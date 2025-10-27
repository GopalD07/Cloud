# AI Resume & JD Analyzer (GCP-ready)

Streamlit app + LangChain: compare a resume to a Job Description, produce SWOT, ATS score, and suggestions.
Uses Vertex AI Embeddings + FAISS. FAISS persisted to Google Cloud Storage (GCS).

## Environment variables

Required at runtime (Cloud Run):

- `GCP_PROJECT` – your GCP project ID
- `GCP_LOCATION` – region for Vertex AI (e.g., `us-central1`, `us-east1`, `europe-west4`, `asia-south1`)
- `GCS_BUCKET` – a GCS bucket name for storing FAISS indices
- `MONGODB_URI` – optional MongoDB Atlas URI (if you use the DB push step)
- `EMBEDDING_MODEL` – Vertex embeddings model id (default: `text-embedding-004`)

## Local dev (optional)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Set env vars (or use a .env file)
export GCP_PROJECT=your-project
export GCP_LOCATION=us-central1
export GCS_BUCKET=your-bucket
export EMBEDDING_MODEL=text-embedding-004

streamlit run main.py
```

Make sure your local env is authenticated to GCP (e.g., `gcloud auth application-default login`).

## Build & Deploy to Cloud Run

```bash
gcloud config set project YOUR_PROJECT_ID
gcloud services enable artifactregistry.googleapis.com run.googleapis.com aiplatform.googleapis.com storage.googleapis.com

# Create a repo if you don't have one yet
gcloud artifacts repositories create containers --repository-format=docker --location=us --description="App images"

# Build image (you can also use Cloud Build)
gcloud builds submit --tag us-docker.pkg.dev/YOUR_PROJECT_ID/containers/resume-jd-app:latest

# (Optional) create the GCS bucket
gsutil mb -l us-central1 gs://YOUR_BUCKET_NAME

# Deploy to Cloud Run
gcloud run deploy resume-jd-app       --image us-docker.pkg.dev/YOUR_PROJECT_ID/containers/resume-jd-app:latest       --region us-central1       --allow-unauthenticated       --platform managed       --set-env-vars GCP_PROJECT=YOUR_PROJECT_ID,GCP_LOCATION=us-central1,GCS_BUCKET=YOUR_BUCKET_NAME,EMBEDDING_MODEL=text-embedding-004
```

If you use MongoDB Atlas, add `--set-env-vars MONGODB_URI=...`.

## Notes

- FAISS is stored in `/tmp` at runtime and synchronized to `gs://$GCS_BUCKET/faiss_indices/`.
- On first run (or cold start), the app builds the FAISS index and uploads it.
- Subsequent runs try to load the existing index from GCS before re-embedding.
