import whisper
import tempfile
import os

# Whisper 权重较大，改为首次调用语音接口时才加载，之后全局复用，
# 这样不使用语音功能时不会拖慢服务启动。
_whisper_model = None


def _get_model():
    global _whisper_model
    if _whisper_model is None:
        print("正在加载语音识别模型（首次调用，请稍候）...")
        _whisper_model = whisper.load_model("base")
    return _whisper_model


def speech_to_text(audio_bytes):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp.write(audio_bytes)
    temp.close()

    result = _get_model().transcribe(temp.name, language="zh")

    os.unlink(temp.name)

    return result["text"].strip()