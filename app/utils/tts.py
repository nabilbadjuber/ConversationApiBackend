from gtts import gTTS
import os

def text_to_speech(text: str, user_id: str) -> str:
    output_dir = "static/audio"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{user_id}_response.mp3")

    tts = gTTS(text)
    tts.save(filepath)
    return filepath