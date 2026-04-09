FROM python:3.11-slim

WORKDIR /app

# Install FastAPI and Uvicorn only
RUN pip install --no-cache-dir fastapi uvicorn[standard]

# Copy project files
COPY . .

# Expose port 8000
EXPOSE 8000

# Start server with minimal config
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
