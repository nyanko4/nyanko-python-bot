from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/quiz")
async def getchat(request: Request):
  print(request.json())
