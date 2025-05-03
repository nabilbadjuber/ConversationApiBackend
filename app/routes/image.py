import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/{filename}")
async def get_image(filename: str):
    image_path = os.path.join(os.path.dirname(__file__), "..", "static", "images", filename)

    if not os.path.exists(image_path):
        return {"error": "Image not found"}

    return FileResponse(image_path, media_type="image/png")