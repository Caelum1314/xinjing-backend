import whisper
import tempfile
import os

whisper_model = whisper.load_model("base")


def speech_to_text(audio_bytes):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp.write(audio_bytes)
    temp.close()

    result = whisper_model.transcribe(temp.name, language="zh")

    os.unlink(temp.name)

    return result["text"].strip()