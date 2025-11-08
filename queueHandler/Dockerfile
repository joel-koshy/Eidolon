# --- Stage 1: Base image ---
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# --- Stage 2: Install system dependencies ---
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
    && rm -rf /var/lib/apt/lists/*

# --- Stage 3: Install Python dependencies ---
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 4: Copy backend code ---
COPY ./ /app/

# --- Stage 5: Expose API port ---
EXPOSE 8000

# --- Stage 6: Default command (FastAPI + uvicorn) ---
# You can override this in docker-compose for worker
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
