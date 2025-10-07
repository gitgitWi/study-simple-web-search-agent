from fastapi import FastAPI
from datetime import datetime
from routes.chat import router as chat_router


app = FastAPI()

app.include_router(chat_router, prefix="/api/v1/chat")


@app.get("/")
def root():
    return {"message": "hello", "now": datetime.now().isoformat()}
