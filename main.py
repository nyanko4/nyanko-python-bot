from fastapi import FastAPI, Request
from webhook import getchat, mention

app = FastAPI()
    
@app.get("/")
def send():
    return {"status": "ok"}
   
app.include_router(getchat.router)
app.include_router(mention.router)
