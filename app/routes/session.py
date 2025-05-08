from fastapi import APIRouter, Form
import redis

router = APIRouter()
r = redis.Redis()

@router.post("/reset")
async def reset_session(user_id: str = Form(...)):
    await r.delete(f"session:{user_id}")
    await r.delete(f"chat:{user_id}")
    await r.delete(f"audio:{user_id}")
    await r.delete(f"image:{user_id}")
    return {"message": "Session reset successful."}

@router.post("/resetscenario")
async def reset_session(user_id: str = Form(...)):
    await r.delete(f"chat:{user_id}")
    await r.delete(f"audio:{user_id}")
    await r.delete(f"image:{user_id}")
    return {"message": "Session scenario reset successfully."}