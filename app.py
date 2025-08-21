from fastapi import FastAPI
import uvicorn
from bot import get_application

app = FastAPI()
bot_app = get_application()

# FastAPI endpoint (Render free Web Service এর জন্য)
@app.get("/")
def root():
    return {"status": "Bot is running!"}

if __name__ == "__main__":
    # Polling bot আর HTTP server একসাথে চলবে
    import asyncio

    loop = asyncio.get_event_loop()
    loop.create_task(bot_app.run_polling())
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
