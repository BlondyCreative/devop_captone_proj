FROM python:3.10-slim

WORKDIR /app

# 1. Instalar dependencias primero para aprovechar el cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONPATH=/app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "service.app:app"]
