FROM python:3.10-slim

WORKDIR /app

# 1. Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copiar todo el código (incluyendo la carpeta service)
COPY . .

# 3. Puerto correcto (Capstone suele usar 8080 o 5000, 
# según tu docker-compose anterior era 8080)
EXPOSE 8080

# 4. El comando CLAVE: service.app:app 
# Esto le dice: "Entra a la carpeta service y busca app.py"
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "service.app:app"]
