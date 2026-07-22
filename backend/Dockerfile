# syntax=docker/dockerfile:1
FROM python:3.13-slim

WORKDIR /app

# Copy dependencies first for layer caching
COPY requirements.txt .

# Install production dependencies
RUN grep -v 'pytest' requirements.txt > /tmp/requirements-prod.txt && \
    pip install --no-cache-dir -r /tmp/requirements-prod.txt

# Copy application source code
COPY main.py .
COPY src/ src/

# Create non-root user
RUN addgroup --system --gid 1001 shovels && \
    adduser --system --uid 1001 --gid 1001 shovels && \
    chown -R shovels:shovels /app

USER shovels

# HuggingFace Spaces default port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; exit(0 if urllib.request.urlopen('http://localhost:7860/health').status == 200 else 1)"

# Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
