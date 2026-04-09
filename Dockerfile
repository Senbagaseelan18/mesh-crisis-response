FROM python:3.11-slim

WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port 7860 (HF Spaces standard)
EXPOSE 7860

# Start server directly with uvicorn
CMD ["python", "-c", "from server.app import main; main()"]
