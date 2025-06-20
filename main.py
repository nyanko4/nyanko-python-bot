from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

templates = Jinja2Templates(directory="templates")

def roll_dice():
    return [random.randint(1, 6) for _ in range(3)]

def judge(dice):
    dice.sort()
    a, b, c = dice
    if a == b == c:
        return "ゾロ目！"
    elif a == 1 and b == 2 and c == 3:
        return "ヒフミ（負け）"
    elif a == 4 and b == 5 and c == 6:
        return "シゴロ（勝ち）"
    elif a == b:
        return f"出目: {c}"
    elif b == c:
        return f"出目: {a}"
    elif a == c:
        return f"出目: {b}"
    else:
        return "役なし"

@app.get("/", response_class=HTMLResponse)
async def chinchiro(request: Request):
    dice = roll_dice()
    result = judge(dice)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "dice": dice,
        "result": result
    })
