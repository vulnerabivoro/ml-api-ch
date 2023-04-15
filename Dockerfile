FROM python:3.7.16-slim-buster

WORKDIR /

# Copiar requirements
COPY ./requirements.txt .

# Instalar dependencias
RUN apt-get update && apt-get install -y gcc
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app/app.py .
COPY ./app/database.db .

EXPOSE 5000

# Iniciar aplicación
# Produccion 
# CMD ["python", "app.py"]
# Localhost
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0"]
