# Use Python 3.11 slim image
FROM python:3.11-slim

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend files
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app

# Copy frontend files
COPY frontend ./frontend

# Expose port (Railway will set PORT env variable)
ENV PORT=8000
EXPOSE 8000

# Run the application
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
