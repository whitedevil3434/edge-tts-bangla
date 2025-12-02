import edge_tts
from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Rizik TTS Service")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "Rizik TTS Service is Running", "voice": "bn-BD-PradeepNeural"}

@app.get("/speak")
async def speak(text: str):
    """
    Converts text to speech using Microsoft Edge TTS (bn-BD-PradeepNeural).
    Returns an audio stream (audio/mpeg).
    """
    try:
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")

        # Use the high-quality Bangladeshi Bengali Voice
        communicate = edge_tts.Communicate(text, "bn-BD-PradeepNeural")
        
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        return Response(content=audio_data, media_type="audio/mpeg")
    
    except Exception as e:
        print(f"Error generating TTS: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
