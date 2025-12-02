from fastapi import FastAPI, Response
import azure.cognitiveservices.speech as speechsdk
import uvicorn
import os

app = FastAPI()

# ——— CONFIGURATION ———
# Code gets Key from Render Environment Variables
AZURE_SPEECH_KEY = os.environ.get("SPEECH_KEY") 
AZURE_SERVICE_REGION = os.environ.get("SPEECH_REGION")

# Best Bangla Voice (Official Azure)
VOICE_NAME = "bn-BD-PradeepNeural"

@app.get("/")
def home():
    return {"status": "Rizik Azure TTS (Official) is Running 💎"}

@app.get("/speak")
async def speak(text: str):
    try:
        # 1. Setup Configuration
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SERVICE_REGION)
        speech_config.speech_synthesis_voice_name = VOICE_NAME
        
        # We need audio bits, not speaker output
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

        # 2. Speak (Synthesize)
        print(f"🎤 Generating Azure Voice for: {text[:15]}...")
        result = speech_synthesizer.speak_text_async(text).get()

        # 3. Check Result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("✅ Azure Success!")
            return Response(content=result.audio_data, media_type="audio/mp3")
            
        elif result.reason == speechsdk.ResultReason.Canceled:
            details = result.cancellation_details
            print(f"❌ Azure Error: {details.error_details}")
            return {"error": "TTS Failed", "details": details.error_details}

    except Exception as e:
        print(f"🔥 System Error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
