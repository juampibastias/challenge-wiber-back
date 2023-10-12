# Usa una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos (si tienes uno)
COPY requirements.txt /app/

# Instala las dependencias (si tienes un archivo de requisitos)
RUN pip install --no-cache-dir -r requirements.txt

# Copia los archivos de tu aplicación al contenedor
COPY . /app/

# Expone el puerto en el que tu aplicación va a escuchar
EXPOSE 5000

# Comando para ejecutar tu aplicación cuando el contenedor se inicie
CMD ["python", "app.py"]
