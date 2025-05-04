from openai import AsyncOpenAI
import os
import requests
from app.utils.prompt_templates import get_keywords_prompt, get_image_prompt

openai = AsyncOpenAI()
# You should already set your OpenAI API key via env
openai.api_key = os.getenv("OPENAI_API_KEY")

IMG_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "images")
os.makedirs(IMG_DIR, exist_ok=True)

async def generate_image(request, response):

    #filename = f"{request.user_id}_{uuid.uuid4().hex}.png"
    filename = f"{request.user_id}_response.png"
    keywords = get_keywords_prompt(request.scenario, request.role, request.place, request.language, response)

    keywords_gen = await openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": keywords}
        ]
    )
    keywords_response = keywords_gen.choices[0].message.content

    prompt = get_image_prompt(request.scenario, request.role, request.place, request.language, response, keywords_response)

    prompt_gen = await openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    prompt_response = prompt_gen.choices[0].message.content

    #response = openai.images.create_variation()

    response = await openai.images.generate(
        model="dall-e-3",
        prompt=prompt_response,
        size="1024x1024",
        quality="standard",
        n=1
    )

    image_url = response.data[0].url
    image_path = os.path.join(IMG_DIR, filename)

    # Download and save locally
    img_data = requests.get(image_url).content
    with open(image_path, "wb") as f:
        f.write(img_data)

    # return {"image_path": image_path}
    return filename