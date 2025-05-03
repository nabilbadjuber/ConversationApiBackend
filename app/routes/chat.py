from fastapi import APIRouter, Request, Form
from pydantic import BaseModel
from app.services.chat_service import handle_chat, handle_hint

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
    scenario: str
    message: str
    language: str

@router.post("/converse")
async def chat_converse(request: ChatRequest):
    return await handle_chat(request)

@router.post("/hint")
async def chat_hint(user_id: str = Form(...), scenario: str = Form(...), language: str = Form(...)):
    return await handle_hint(user_id, scenario, language)