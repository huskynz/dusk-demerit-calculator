# Use Python base image
FROM python:3.9-slim

# Set environment variables to prevent bytecode generation and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run with Gunicorn (adjust app:app to your actual module/app name)
CMD ["gunicorn", "--bind", "0.0.0.0:4321", "app:app"]
