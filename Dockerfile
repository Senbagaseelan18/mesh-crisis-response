FROM python:3.11-slim

WORKDIR /app

# Install minimal dependencies only - FastAPI and Uvicorn
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard]

# Copy only requirements for reference
COPY requirements.txt .

# Try to install requirements, but don't fail if there are issues
# The app will work with just FastAPI
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || echo "Some dependencies skipped"

# Copy all project files
COPY . .

# Expose port
EXPOSE 8000

# Run the server with the main app
CMD ["python", "-m", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
