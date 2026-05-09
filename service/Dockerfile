FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPIA TODO EL PROYECTO (Incluyendo la carpeta service)
COPY . .

# Agrega la raíz al path de Python
ENV PYTHONPATH=/app

# Puerto que usa el contenedor
EXPOSE 8080

# EL COMANDO CORRECTO: Entra a service y busca app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "service.app:app"]
