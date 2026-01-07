
from fastapi import FastAPI
from models import MessageRequest
from database import save_to_db

app = FastAPI()

@app.post("/message")
def store_message(msg: MessageRequest):

    save_to_db(msg.text)

    return {
        "status": "ok",
        "message": msg.text
    }
