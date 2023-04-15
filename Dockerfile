FROM python:3.7.16-slim-buster

WORKDIR /

# Copiar requirements
COPY ./requirements.txt .

# Instalar dependencias
RUN apt-get update && apt-get install -y gcc
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /

# Exponer puerto
EXPOSE 5000

# Iniciar aplicación
CMD ["python", "app/app.py"]
