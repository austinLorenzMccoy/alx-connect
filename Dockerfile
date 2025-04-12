# Use Python 3.8 slim image as base
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY README.md .
COPY alx_connect/ alx_connect/

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "alx_connect.main:app", "--host", "0.0.0.0", "--port", "8000"] 