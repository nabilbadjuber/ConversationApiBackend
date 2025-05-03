from fastapi import WebSocket, APIRouter, WebSocketDisconnect
import asyncio
import json
from app.utils.redis_client import get_redis_client

router = APIRouter()

@router.websocket("/ws/conversation/{user_id}")
async def websocket_conversation(websocket: WebSocket, user_id: str):
    await websocket.accept()
    try:
        while True:
            # You can await a redis pubsub event or just refresh every 2s

            redis = get_redis_client()
            session_key = f"chat:{user_id}"
            conversation = await redis.get(session_key) or ""
            conversation = conversation[2:]
            conversation = conversation.replace("\n", "|")
            conversation = conversation.replace(":", "~")
            conversation = conversation.replace('User', '"role": "user"')
            conversation = conversation.replace('Bot', '"role": "bot"')

            conv_array = []
            conv_list = conversation.split("|")
            for conv in conv_list:
                conv = '{' + conv + '"}'
                conv = conv.replace('~','~"content":"')
                conv = conv.replace('~',',')

                if(conv != '{"}'):
                    data = json.loads(conv)
                    data["content"] = data["content"].strip()

                    if(data["role"] == "user"):
                        data["isSentByUser"] = True
                    else:
                        data["isSentByUser"] = False

                    data["datetime"] = ""
                    conv_array.append(data)

            if conv_array:
                try:
                    # Try to load conversation if already JSON
                    conversation_list = conv_array
                except json.JSONDecodeError:
                    # fallback: turn it into single entry if it's still plain text
                    conversation_list = [{"role": "bot", "content": conversation}]
                    #conversation_list = conv_array
            else:
                conversation_list = []

            await websocket.send_json(conversation_list)
            await asyncio.sleep(2)  # polling every 2 seconds inside websocket

    except WebSocketDisconnect:
        print(f"WebSocket disconnected: user_id={user_id}")
    except Exception as e:
        print(f"Other WebSocket error: {e}")