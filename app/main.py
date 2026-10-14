from fastapi import FastAPI

# FastAPI создаёт объект приложения c настройками.
app = FastAPI(
    title="Task API",
    description="Семинар по FastAPI",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"message": "Привет, Мир!"}


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "task-api"}

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return {"task_id": task_id, "title": f"Задача #{task_id}"}