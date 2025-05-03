from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# from app.routes import chat, ws, image, article, question, audio
from app.routes import chat, audio, image, session, ws

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(chat.router, prefix="/api/chat")
app.include_router(ws.router)
# app.include_router(article.router, prefix="/api/article")
# app.include_router(question.router, prefix="/api/question")
app.include_router(image.router, prefix="/api/image")
app.include_router(audio.router, prefix="/api/audio")
app.include_router(session.router, prefix="/api/session")