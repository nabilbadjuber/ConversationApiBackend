from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from app.services.audio_service import process_audio
import os

router = APIRouter()

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...), user_id: str = Form(...), scenario: str = Form(...), language: str = Form(...), role: str = Form(...), place: str = Form(...)):
    return await process_audio(file, user_id, scenario, language, role, place)

@router.get("/{filename}")
async def get_audio(filename: str):
    file_path = os.path.join(os.path.dirname(__file__), "..", "static", "audio", filename)
    print(file_path)
    if not os.path.exists(file_path):
        return {"error": "File not found"}

    return FileResponse(file_path, media_type="audio/mpeg")