from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = []

class Task(BaseModel):
  title: str

@app.post("/add")
def add(task: Task):
  tasks.append(task.title)
  return {"message": "追加しました", "task": task.title}

@app.get("/list")
def get_tasks():
  return {"tasks": tasks}

@app.delete("/delete/{task_id}")
def delete_task(task_id: int):
  if 0 <= task_id < len(tasks):
    removed = tasks.pop(task_id)
    return {"message": "削除しました", "removed": removed}
raise HTTPException(status_code=404, detail="タスクが見つかりません")
