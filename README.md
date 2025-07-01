# 🗣️ Transcriber & Translator

Este proyecto permite convertir el audio de un archivo `.mp4` (en inglés) a texto transcripto en español, utilizando Whisper y Google Translate, todo dentro de un contenedor Docker.

---

## ✅ Requisitos

- Docker instalado y funcionando
- `ffmpeg` ya viene dentro del contenedor (no hace falta instalarlo localmente)
- Un archivo de video `.mp4` en la carpeta `videos/` (o cualquier otra ruta local)

---

## 🛠️ Instalación

1. Clonar el proyecto:

``` bash
    git clone https://github.com/tu-usuario/transcriber.git
    cd transcriber
```

2. Crear la carpeta para los videos:

``` bash
    docker build -t transcriber .
```

3. Colocar tu archivo .mp4 dentro de la carpeta videos/ (ej: videos/test.mp4)

## Uso de la aplicación

1. Como construir la imagen (se hace solo una vez)

``` bash
    docker build -t transcriber .
```

2. Como ejecutar el script:
``` bash
    docker run --rm -v "$(pwd):/app" transcriber videos/test.mp4
```
## 🧠 ¿Qué hace?
- Transcribe el audio en inglés del archivo .mp4 usando Whisper local (sin usar API)
- Traduce el texto al castellano usando deep-translator

## Estructura del proyecto

```
    transcriber/
    ├── Dockerfile
    ├── requirements.txt
    ├── transcribe_and_translate.py
    └── videos/
        └── test.mp4  # <-- tu video va acá
```
