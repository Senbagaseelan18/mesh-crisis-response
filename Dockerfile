FROM python:3.11-slim

WORKDIR /app

# Install FastAPI, Uvicorn, and OpenAI Client (MANDATORY for Phase 1)
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    openai \
    pydantic

# Copy all files
COPY . .

# Expose port 8000
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Start the server - PHASE 1 server
CMD ["python", "-m", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
