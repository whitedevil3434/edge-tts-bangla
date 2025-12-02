from fastapi import FastAPI, Response
import edge_tts
from gtts import gTTS
import uvicorn
import io

app = FastAPI()

# World Class Bangla Voice
EDGE_VOICE = "bn-BD-PradeepNeural"

@app.get("/")
def home():
    return {"status": "Rizik TTS Service (Patched) 🚀"}

@app.get("/speak")
async def speak(text: str):
    """
    Rizik Smart TTS Engine
    1. Tries Edge TTS (PradeepNeural) with Latest Security Patch
    2. Falls back to Google TTS if anything goes wrong
    """
    
    # ——— PLAN A: EDGE TTS (The Best) ———
    try:
        print(f"🎤 Trying Edge TTS for: {text[:15]}...")
        
        # New pattern to avoid 403 errors
        communicate = edge_tts.Communicate(text, EDGE_VOICE)
        audio_data = b""
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        if len(audio_data) > 0:
            print("✅ Edge TTS Success")
            return Response(content=audio_data, media_type="audio/mp3", headers={"X-TTS-Provider": "Edge-Neural"})
            
    except Exception as e:
        print(f"⚠️ Edge Failed: {e}")

    # ——— PLAN B: GOOGLE TTS (The Savior) ———
    print("🔄 Falling back to Google TTS...")
    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang='bn', slow=False)
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        
        return Response(content=mp3_fp.read(), media_type="audio/mp3", headers={"X-TTS-Provider": "Google-Standard"})
        
    except Exception as e:
        return {"error": "All systems failed", "details": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
