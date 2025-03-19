# Usa una imagen de Python ligera
FROM python:3.10-slim

# Configura el directorio de trabajo
WORKDIR /app

# Copia el archivo de dependencias y lo instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido de la app
COPY app /app/app

# Expone el puerto de la API
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
