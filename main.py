from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/", StaticFiles(directory="./home", html=True), name="static")

def roll_dice():
    return [random.randint(1, 6) for _ in range(3)]

def judge_dice(dice):
    dice.sort()
    a, b, c = dice
    if a == b == c:
        if a == 1:
            return "ピンゾロ！"
        return "ゾロ目！"
    elif a == 1 and b == 2 and c == 3:
        return "ヒフミ"
    elif a == 4 and b == 5 and c == 6:
        return "シゴロ"
    elif a == b:
        return f"出目: {c}"
    elif b == c:    
        return f"出目: {a}"
    elif a == c:
        return f"出目: {b}"
    else:
        return "役なし"

@app.get("/chinchiro", response_class=HTMLResponse)
async def chinchiro(request: Request):
    dice = roll_dice()
    result_dice = judge_dice(dice)
    return templates.TemplateResponse("dice.html", {
        "request": request,
        "dice": dice,
        "result": result_dice
    })

marks = ['♠', '♥', '♦', '♣']
numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
cords = [s + r for s in marks for r in numbers]

def draw_poker():
    random.shuffle(cords)
    poker = cords[:5]
    return poker

@app.get("/poker", response_class=HTMLResponse)
async def poker(request: Request):
    poker = draw_poker()
    return templates.TemplateResponse("poker.html", {
        "request": request,
        "poker": poker,
    })
