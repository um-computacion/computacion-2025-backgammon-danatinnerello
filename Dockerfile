# Imagen base ligera de Python
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todo tu proyecto al contenedor
COPY . .

# Instala dependencias (si no tenés requirements.txt, podés agregarlas a mano)
RUN pip install --no-cache-dir pygame

# Establece un argumento opcional para elegir qué ejecutar (cli o main)
ARG MODO=cli

# Permite usar el argumento como variable en tiempo de ejecución
ENV MODO=${MODO}

# Comando por defecto (puede cambiarse con docker run)
CMD ["sh", "-c", "python ${MODO}.py"]
