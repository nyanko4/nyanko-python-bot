from fastapi import FastAPI, request

app = FastAPI()

@app.post("/webhook")
async def webhook("Request": request):
    print(request)
