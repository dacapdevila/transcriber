FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Crear carpeta de trabajo
WORKDIR /app

# Copiar archivos
COPY requirements.txt .
COPY transcribe_and_translate.py .

# Instalar paquetes de Python
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "transcribe_and_translate.py"]