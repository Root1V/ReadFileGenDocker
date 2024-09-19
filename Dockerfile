# Usar una imagen base oficial de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos al contenedor
COPY . /app

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Hacemos el puerto 80 disponible
EXPOSE 80

# Comando para ejecutar la aplicación
CMD ["python", "agents.py"]

# docker build -t hello-agent .
# docker run -it -v /Users/Data/proyects/DockerAIAgent:/app/data docker-agents