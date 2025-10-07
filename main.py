from fastapi import FastAPI
from datetime import datetime

app = FastAPI()


@app.get("/")
def root():
    return {"message": "hello", "now": datetime.now().isoformat()}
