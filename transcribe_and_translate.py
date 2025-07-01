import whisper
from deep_translator import GoogleTranslator
import sys

def transcribe_and_translate(mp4_file_path):
    model = whisper.load_model("base")  # pueden ser "small", "medium" o "large"
    print(f"Transcribiendo: {mp4_file_path}")
    result = model.transcribe(mp4_file_path, language="en")

    print("\n🔊 Transcripción en inglés:")
    print(result["text"])

    translated = GoogleTranslator(source='en', target='es').translate(result["text"])

    print("\n🌍 Traducción al castellano:")
    print(translated)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python transcribe_and_translate.py videos/test.mp4")
        sys.exit(1)

    transcribe_and_translate(sys.argv[1])