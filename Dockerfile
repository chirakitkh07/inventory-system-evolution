# Dockerfile — Inventory Management System v2.0

FROM python:3.13-slim

# Metadata
LABEL maintainer="dev-team" \
      version="2.0.0" \
      description="Inventory Management System — Containerised CLI"

# Set working directory
WORKDIR /app

# Install dependencies first (layer cache optimisation)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Data volume for persistent inventory JSON
VOLUME ["/app/data"]

# Default command
CMD ["python", "main.py"]
