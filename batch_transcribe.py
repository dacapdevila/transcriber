import whisper
from deep_translator import GoogleTranslator
from pathlib import Path
import subprocess

model = whisper.load_model("base")

input_folder = Path("videos")
output_folder = Path("outputs")

def get_video_duration(video_path: Path) -> float:
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-of",
             "default=noprint_wrappers=1:nokey=1", str(video_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        return float(result.stdout)
    except Exception:
        return -1  # duración inválida

def transcribe_and_translate(video_path: Path, result=None):
    print(f"🎧 Procesando: {video_path}")

    if result is None:
        result = model.transcribe(str(video_path), fp16=False)

    text = result["text"].strip()
    lang = result["language"]
    print(f"🌐 Idioma detectado: {lang}")

    relative_path = video_path.relative_to(input_folder)
    output_base = output_folder / relative_path.parent / video_path.stem
    output_base.parent.mkdir(parents=True, exist_ok=True)

    if lang == "en":
        en_path = output_base.with_name(output_base.name + "_en.txt")
        es_path = output_base.with_name(output_base.name + "_es.txt")

        en_path.write_text(text, encoding="utf-8")
        print(f"✅ Transcripción en inglés guardada: {en_path}")

        translated_parts = []
        for part in split_text(text):
            translated_parts.append(GoogleTranslator(source='en', target='es').translate(part))
        translated = "\n".join(translated_parts)

        es_path.write_text(translated, encoding="utf-8")
        print(f"✅ Traducción al español guardada: {es_path}")
    else:
        lang_path = output_base.with_name(output_base.name + f"_{lang}.txt")
        lang_path.write_text(text, encoding="utf-8")
        print(f"✅ Transcripción en {lang} guardada: {lang_path}")

def process_all_videos():
    print("🚀 Iniciando procesamiento masivo de videos...")
    video_files = [f for f in input_folder.rglob("*.mp4") if f.is_file()]

    if not video_files:
        print("⚠️ No se encontraron archivos .mp4 en la carpeta 'videos'.")
        return

    max_files = 3
    processed_count = 0
    success_count = 0
    skipped_count = 0
    error_count = 0

    for i, video in enumerate(video_files, start=1):
        duration = get_video_duration(video)
        if duration > 420:
            print(f"⏩ Salteado por ser mayor a 7 minutos ({duration:.2f} segundos): {video.name}")
            skipped_count += 1
            continue

        try:
            result = model.transcribe(str(video), fp16=False)
            lang = result["language"]
        except Exception as e:
            print(f"❌ Error transcribiendo para detección de idioma {video.name}: {e}")
            error_count += 1
            continue

        output_base = output_folder / video.relative_to(input_folder).parent / video.stem

        if lang == "en":
            en_path = output_base.with_name(output_base.name + "_en.txt")
            es_path = output_base.with_name(output_base.name + "_es.txt")
            if en_path.exists() or es_path.exists():
                print(f"⏩ Ya procesado, se omite: {video.name}")
                skipped_count += 1
                continue
        else:
            lang_path = output_base.with_name(output_base.name + f"_{lang}.txt")
            if lang_path.exists():
                print(f"⏩ Ya procesado, se omite: {video.name}")
                skipped_count += 1
                continue

        if processed_count >= max_files:
            print("⏹️ Límite alcanzado (3 archivos por ejecución).")
            break

        print(f"\n📁 [{i}/{len(video_files)}]")
        try:
            transcribe_and_translate(video, result)
            processed_count += 1
            success_count += 1
        except Exception as e:
            print(f"❌ Error procesando {video.name}: {e}")
            error_count += 1

    print("\n🎉 Proceso finalizado.")
    print(f"\n🧾 Resumen:")
    print(f"   ✅ Procesados: {success_count}")
    print(f"   ⏩ Omitidos: {skipped_count}")
    print(f"   ❌ Errores: {error_count}")

def split_text(text, max_length=4000):
    parts = []
    current = ""
    for paragraph in text.split(". "):
        if len(current) + len(paragraph) < max_length:
            current += paragraph + ". "
        else:
            parts.append(current.strip())
            current = paragraph + ". "
    if current:
        parts.append(current.strip())
    return parts

if __name__ == "__main__":
    process_all_videos()