from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
import requests

from models import Message
from database import get_db


load_dotenv()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")


from groq import Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama3-8b-8192"  

client = Groq(api_key=GROQ_API_KEY)


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(request: Request, db: Session = Depends(get_db)):
    try:
        
        data = await request.json()
        message = data.get("message")

        if not message:
            return JSONResponse(status_code=400, content={"error": "پیامی ارسال نشده است."})

        
        chat_completion = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": message}]
        )
        reply = chat_completion.choices[0].message.content

       
        db_message = Message(user_message=message, bot_reply=reply)
        db.add(db_message)
        db.commit()
        db.refresh(db_message)

        return {"reply": reply}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/messages/")
def create_message(user_message: str, db: Session = Depends(get_db)):
    db_message = Message(user_message=user_message)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return {"message": "پیام با موفقیت ذخیره شد.", "id": db_message.id}


@app.get("/messages/")
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).all()
    return {"messages": [{"id": m.id, "user_message": m.user_message, "bot_reply": m.bot_reply} for m in messages]}






























