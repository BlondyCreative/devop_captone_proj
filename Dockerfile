FROM python:3.9-slim
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPIA TODO (esto copiará la carpeta service al contenedor)
COPY . .

# Agrega la raíz al PATH para que Python encuentre los módulos
ENV PYTHONPATH=/app

EXPOSE 8080

# EL CAMBIO CLAVE: service.app:app
# Esto le dice a Gunicorn: "Entra a service y busca el objeto app"
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "service:app"]
