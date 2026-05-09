FROM python:3.10-slim

# 2. Definir el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de requerimientos primero para aprovechar el cache de Docker
COPY requirements.txt .

# 4. Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar TODO el contenido de tu carpeta local al contenedor
# Esto incluye la carpeta 'service/' y tus archivos de configuración
COPY . .

# 6. Configurar la variable de entorno para que Python reconozca la raíz como módulo
ENV PYTHONPATH=/app

# 7. Informar el puerto en el que escuchará el contenedor
EXPOSE 8080

# 8. Comando para ejecutar la aplicación con Gunicorn
# IMPORTANTE: Usamos 'service.app:app' porque tu archivo está en la subcarpeta service
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "service.app:app"]
