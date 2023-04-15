FROM python:3.7.16-slim-buster

WORKDIR /app

# Copiar archivos de la aplicación
COPY requirements.txt .
COPY app.py .
COPY database.db .

# Instalar dependencias
RUN apt-get update && apt-get install -y gcc
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer puerto
EXPOSE 5000

# Iniciar aplicación
CMD ["python", "app.py"]
