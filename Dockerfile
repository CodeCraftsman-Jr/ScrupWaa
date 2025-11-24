# Appwrite Function Dockerfile
# Python 3.11 runtime for Universal Phone Scraper

FROM python:3.11-slim

# Set working directory
WORKDIR /usr/code

# Install system dependencies for lxml
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set Python to unbuffered mode for better logging
ENV PYTHONUNBUFFERED=1

# Appwrite function entrypoint
CMD ["python", "function_main.py"]
