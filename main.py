from fastapi import FastAPI, Response
import edge_tts
from gtts import gTTS
import uvicorn
import io

app = FastAPI()

# Best Bangla Voice
EDGE_VOICE = "bn-BD-PradeepNeural"

@app.get("/")
def home():
    return {"status": "Rizik Hybrid TTS is Running 🚀"}

@app.get("/speak")
async def speak(text: str):
    """
    ATTEMPT 1: Try High-Quality Edge TTS
    ATTEMPT 2: Fallback to Google TTS if blocked
    """
    try:
        # ——— PLAN A: EDGE TTS ———
        print(f"Trying Edge TTS for: {text[:20]}...")
        communicate = edge_tts.Communicate(text, EDGE_VOICE)
        audio_data = b""
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        print("✅ Edge TTS Success")
        return Response(content=audio_data, media_type="audio/mp3")

    except Exception as e:
        # ——— PLAN B: GOOGLE TTS (Backup) ———
        print(f"⚠️ Edge TTS Failed ({str(e)}). Switching to Google TTS...")
        
        try:
            # Create in-memory buffer
            mp3_fp = io.BytesIO()
            # Generate audio with Google (lang='bn' for Bangla)
            tts = gTTS(text=text, lang='bn', slow=False)
            tts.write_to_fp(mp3_fp)
            
            # Reset pointer to start
            mp3_fp.seek(0)
            print("✅ Google TTS Success (Fallback)")
            
            return Response(content=mp3_fp.read(), media_type="audio/mp3")
            
        except Exception as g_error:
            return {"error": "All TTS services failed", "details": str(g_error)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
