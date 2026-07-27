FROM python:3.10-slim

# Install system dependencies for psycopg2-binary and general builds
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port for Gunicorn
EXPOSE 8080

# Start the app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "wsgi:app"]