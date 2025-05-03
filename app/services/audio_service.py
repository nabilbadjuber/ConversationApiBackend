import tempfile
import whisper
import imageio_ffmpeg
import os
from app.services.chat_service import handle_chat
from app.services.image_service import generate_image
from app.utils.tts import text_to_speech
import subprocess
import numpy as np
from gtts import gTTS

model = whisper.load_model("base")

# Get ffmpeg path and directory
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
ffmpeg_dir = os.path.dirname(ffmpeg_path)
print(f"[INFO] Using ffmpeg from: {ffmpeg_path}")

# Patch whisper to use full ffmpeg path

def load_audio_with_custom_ffmpeg(path, sr=16000):
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        command = [
            ffmpeg_path,
            "-nostdin",
            "-threads", "0",
            "-i", path,
            "-f", "wav",
            "-ac", "1",
            "-ar", str(sr),
            "-loglevel", "quiet",
            "-"
        ]
        out = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if out.returncode != 0:
            raise RuntimeError(f"ffmpeg failed: {out.stderr.decode()}")

        audio = np.frombuffer(out.stdout, np.int16).flatten().astype(np.float32) / 32768.0
        return audio  # ✅ Return np.ndarray, not tensor

whisper.audio.load_audio = load_audio_with_custom_ffmpeg

# Define audio output directory inside app
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

# Generate TTS and save inside app/audio/
def text_to_speech(text, filename="response.mp3", lang='en', slow=False, tld='com'):
    tts = gTTS(text, lang=lang, slow=slow, tld=tld)
    audio_path = os.path.join(AUDIO_DIR, filename)
    tts.save(audio_path)
    return audio_path

# Main audio processing function
def transcribe_audio(file_path):
    file_path = os.path.abspath(file_path).replace("\\", "/")
    result = model.transcribe(file_path)
    return result["text"]

async def process_audio(file, user_id, scenario, language, role, place):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp_path = tmp.name
    tmp.close()

    with open(tmp_path, "wb") as f:
        f.write(await file.read())

    if not os.path.exists(tmp_path):
        raise FileNotFoundError(f"Temp file not found: {tmp_path}")

    text = transcribe_audio(tmp_path)
    os.remove(tmp_path)

    chat_request = type("ChatRequest", (object,), {
        "user_id": user_id,
        "scenario": scenario,
        "message": text,
        "language": language,
        "role": role,
        "place": place
    })
    chat_response = await handle_chat(chat_request)

    # Generate Audio Response
    audio_response_path = text_to_speech(chat_response["response"], filename=f"{user_id}_response.mp3", lang=language, slow=False, tld=language)

    # Generate Image Response
    img_response_path = await generate_image(chat_request, chat_response["response"])

    # Generate Text hint


    return {
        # "transcription": text,
        # "response": chat_response["response"],
        # "audio_url": audio_response_path,
        "audio_file": f"/api/audio/{user_id}_response.mp3",
        "image_file": f"/api/image/{img_response_path}"
    }
