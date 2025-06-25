from fastapi import FastAPI, Request
from db._init_db import _init_db
from webhook.getchat import router as getchat

app = FastAPI()
    
@app.get("/")
def send():
    return {"status": "ok"}
    
@app.on_event("startup")
async def startup():
    await _init_db()
   
app.include_router(getchat)
