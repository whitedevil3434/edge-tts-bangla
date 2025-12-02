# Rizik TTS Service (Microservice)

This is a Python FastAPI service that uses `edge-tts` to generate high-quality Bengali voice (Banglish optimized) for the Rizik Super App.

## 🚀 Deployment Guide (Render.com)

1.  **Push to GitHub:**
    *   Initialize a git repo in this folder or push this folder to your existing repo.
    *   `git init`
    *   `git add .`
    *   `git commit -m "Initial commit"`
    *   `git push ...`

2.  **Create Service on Render:**
    *   Go to [dashboard.render.com](https://dashboard.render.com).
    *   Click **New +** -> **Web Service**.
    *   Connect your GitHub repo.
    *   **Settings:**
        *   **Runtime:** Python 3
        *   **Build Command:** `pip install -r requirements.txt`
        *   **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
    *   Click **Deploy**.

3.  **Get URL:**
    *   Once deployed, copy the URL (e.g., `https://rizik-tts.onrender.com`).
    *   Update `TTS_SERVICE_URL` in `backend/src/ai/AIOrchestrator.ts` if it's different.

## ⚠️ Important: Prevent Sleeping
Render Free Tier spins down after 15 mins of inactivity. To keep it hot:
1.  Go to [uptimerobot.com](https://uptimerobot.com).
2.  Create a new Monitor (HTTP(s)).
3.  URL: `https://your-app-name.onrender.com/`
4.  Interval: 5 minutes.

## API Usage
**GET /speak?text=Hello**
Returns: Audio Stream (MP3)
