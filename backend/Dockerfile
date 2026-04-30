# Backend Dockerfile for DataSage ML Platform
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1


RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Install optional ML packages not in requirements.txt (version resolved at build time)
RUN pip install imbalanced-learn shap

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy all application source code
COPY . .

# Create non-root user for security (optional for dev, good practice)
RUN useradd -m -u 1000 datasage && \
    chown -R datasage:datasage /app

# Create directories for storage
RUN mkdir -p /app/storage /app/models && \
    chown -R datasage:datasage /app/storage /app/models

# Switch to non-root user
USER datasage

# Expose port
EXPOSE 8000

# Use entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Default command (can be overridden in docker-compose)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]