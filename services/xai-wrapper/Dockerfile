FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose port
EXPOSE 8009

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8009"] 