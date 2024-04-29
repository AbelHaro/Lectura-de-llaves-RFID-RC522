FROM ubuntu

# Instalar Python 3 y Flask
RUN apt update
RUN apt install python3 python3-pip -y
RUN apt install python3-flask -y
RUN apt install python3-requests -y

# Establecer el directorio de trabajo y copiar los archivos
WORKDIR /home/
COPY initdb.py .
COPY api.py .
COPY start.sh .

# Dar permisos de ejecución al script
RUN chmod +x start.sh

# Exponer el puerto
EXPOSE 5000

# Ejecutar los scripts
CMD ["./start.sh"]
