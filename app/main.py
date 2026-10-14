from fastapi import FastAPI, HTTPException
from app.schemas import TaskCreate

# FastAPI создаёт объект приложения c настройками.
app = FastAPI(
    title="Task API",
    description="Семинар по FastAPI",
    version="0.1.0",
)

# временное хранилище в памяти
TASKS: list[dict] = []

@app.get("/")
def read_root():
    return {"message": "Привет, Мир!"}


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "task-api"}

@app.get("/tasks")
def health_check():
    return TASKS

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in TASKS:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")

@app.get("/search")
def search(q: str = "", limit: int = 10):
    return {"query": q, "limit": limit}

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    new_task = {"id": len(TASKS) + 1, **task.model_dump()}
    TASKS.append(new_task)
    return new_task