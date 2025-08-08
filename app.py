from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

AUDIO_DIR = "audios"
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.post("/generate-voice")
async def generate_voice(text: str = Form(...)):
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)
    try:
        tts = gTTS(text=text, lang='fr')
        tts.save(filepath)
        return JSONResponse({"status": "success", "file": f"/download/{filename}"})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)})

@app.get("/download/{filename}")
async def download(filename: str):
    filepath = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type="audio/mpeg", filename=filename)
    return JSONResponse({"status": "error", "message": "Fichier introuvable"})
