FROM python:3.10-slim

WORKDIR /app

# 1. Instalar dependencias primero para aprovechar el cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONPATH=/app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "service.app:app"]
# 2. Copiar el resto de la aplicación al contenedor
COPY . .

# 3. Exponer el puerto que definiste en tu docker-compose
EXPOSE 8080

# 4. El comando para arrancar la app usando el módulo service
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "service.app:app"]
