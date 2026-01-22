# Usar imagen base de Python 3.12 slim para reducir tamaño
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para Flet
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero para aprovechar caché de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación
COPY . .

# Exponer puerto 8080 (estándar de Cloud Run)
EXPOSE 8080

# Variables de entorno
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Comando para ejecutar la aplicación
# Cloud Run requiere que la app escuche en 0.0.0.0 y use el puerto de la variable PORT
CMD exec python main.py
