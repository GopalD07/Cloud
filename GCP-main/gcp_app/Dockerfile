# Python base
FROM python:3.11-slim

# Prevent python from writing .pyc files and buffering stdout/err
ENV PYTHONDONTWRITEBYTECODE=1         PYTHONUNBUFFERED=1

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends         build-essential         curl         && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Streamlit expects these for Cloud Run
ENV PORT=8080
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Default command
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8080"]
