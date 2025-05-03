from fastapi import APIRouter, Form
import redis

router = APIRouter()
r = redis.Redis()

@router.post("/reset")
async def reset_session(user_id: str = Form(...)):
    r.delete(f"session:{user_id}")
    r.delete(f"chat:{user_id}")
    r.delete(f"audio:{user_id}")
    r.delete(f"image:{user_id}")
    return {"message": "Session reset successful."}