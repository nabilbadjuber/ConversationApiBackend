from app.services.chat_service import handle_chat, textToAudio, audioToText
from app.services.image_service import generate_image

async def process_audio(file, user_id, scenario, language, role, place):

    # Transacribe Audio
    text = await audioToText(filename=f"{user_id}_response.mp3", lang=language)

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
    await textToAudio(input_text=chat_response["response"], filename=f"{user_id}_response.mp3")

    # Generate Image Response
    img_response_path = await generate_image(chat_request, chat_response["response"])

    return {
        "audio_file": f"/api/audio/{user_id}_response.mp3",
        "image_file": f"/api/image/{img_response_path}"
    }


