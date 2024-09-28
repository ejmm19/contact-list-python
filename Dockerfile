# Usa una imagen base de Python
FROM python:3.10.12-slim

# Instala ping (iputils)
RUN apt-get update && apt-get install -y iputils-ping

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt /app/

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de la aplicación al contenedor
COPY . /app



# Expone el puerto 5000
EXPOSE 5000


# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
