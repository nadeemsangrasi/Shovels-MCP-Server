FROM python:3.13-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port for HuggingFace Spaces
EXPOSE 7860

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
