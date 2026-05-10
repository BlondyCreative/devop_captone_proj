FROM python:3.9-slim
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPIA TODO (esto copiará la carpeta service al contenedor)
COPY . .

# Agrega la raíz al PATH para que Python encuentre los módulos
ENV PYTHONPATH=/app

EXPOSE 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "service:app"]
