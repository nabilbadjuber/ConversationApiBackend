from app.utils.prompt_templates import get_conversation_prompt, get_context_prompt, get_hint_conversation_prompt
from app.utils.redis_client import get_redis_client
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # Only needs to be called once somewhere near startup

openai = AsyncOpenAI()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

# Define audio output directory inside app
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

async def handle_chat(request):
    redis = get_redis_client()
    session_key = f"chat:{request.user_id}"

    # Type of scenarios:
    # 1. Ordering food at a restaurant
    # 2. Job interview
    # 3. Visiting a doctor
    # 4. Booking a hotel room
    # 5. Shopping for clothes

    previous_messages = await redis.get(session_key) or ""
    context = get_context_prompt(request.scenario, request.role, request.place, request.language)
    prompt = get_conversation_prompt(request.scenario, previous_messages, request.message, request.language)
    completion = await openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )

    response = completion.choices[0].message.content

    await redis.set(session_key, previous_messages + f"\n User: {request.message} \n Bot: {response}")

    return {"response": response}

async def handle_hint(user_id, scenario, language):
    redis = get_redis_client()
    session_key = f"chat:{user_id}"

    previous_messages = await redis.get(session_key) or ""
    prompt = get_hint_conversation_prompt(scenario, previous_messages, language)

    completion = await openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response = completion.choices[0].message.content

    return response

async def audioToText(filename: str, lang: str):
    file_path = os.path.join(AUDIO_DIR, filename)
    input_audio = open(file_path, "rb")
    text = await openai.audio.transcriptions.create(
      model="whisper-1",
      file=input_audio,
      language=lang
    )

    return text.text

async def textToAudio(input_text: str, filename: str):
    speech_file_path = os.path.join(AUDIO_DIR, filename)
    response = await openai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=input_text
    )

    with open(speech_file_path, "wb") as f:
        f.write(await response.aread())

    return True