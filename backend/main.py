
from fastapi import FastAPI
from models import MessageRequest
# from database import save_to_db
from database import save_to_db, get_all_messages

app = FastAPI()

@app.post("/message")
def store_message(msg: MessageRequest):

    save_to_db(msg.text)

    return {
        "status": "ok",
        "message": msg.text
    }



@app.get("/messages")
def list_messages():

    data = get_all_messages()

    return {
        "count": len(data),
        "items": data
    }

