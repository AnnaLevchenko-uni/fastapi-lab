from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models import Task
from app.schemas import TaskCreate, TaskOut, TaskUpdate, StudentCreate

# FastAPI объект с настройками
app = FastAPI(
    title="Task API",
    description="API для работы с задачами, написанное с FastAPI",
    version="0.2.0"
)

# Создаём таблицы при старте (для лабораторной; в реальном проекте — Alembic)
Base.metadata.create_all(bind=engine)

STUDENTS: list[dict] = []

@app.get("/")
def root():
    return {"message": "Hello, WORLD!"}

@app.get("/tasks")
def list_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@app.get("/tasks/search", response_model=list[TaskOut])
def search_tasks(
    q: str = Query(min_length=1, max_length=100),
    db: Session = Depends(get_db),
):
    return db.query(Task).filter(Task.title.ilike(f"%{q}%")).order_by(Task.id).all()

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

@app.post("/tasks", status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, patch: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    updates = patch.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_by_id(task_id, db)
    db.delete(task)
    db.commit()
    return db.query(Task).all()

# Со следующей строки добавляйте эндпоинты для students
@app.post("/create_kalinichenko_i_v" , status_code=201)
def create_kalinichenko_i_v():
    new_student = {
        "id": len(STUDENTS) + 1,
        "first_name": "Irina",
        "second_name": "Kalinichenko",
        "group": 1,
        "course": 4,
        }
    STUDENTS.append(new_student)
    return new_student


@app.get("/get_kalinichenko_i_v")
def get_kalinichenko_i_v():
    for student in STUDENTS:
        if student["second_name"] == "Kalinichenko":
            return student
    raise HTTPException(status_code=404, detail="Студент не найден")


@app.post("/create_sumarokova_e_b", status_code=201)
def create_sumarokova_e_b():
    new_student = {
        "id": len(STUDENTS) + 1,
        "first_name": "Elizaveta",
        "second_name": "Sumarokova",
        "group": "640-01",
        "course": 4,
    }
    STUDENTS.append(new_student)
    return new_student


@app.get("/get_sumarokova_e_b")
def get_sumarokova_e_b():
    for student in STUDENTS:
        if student.get("second_name", "").lower() == "sumarokova":
            return student
    raise HTTPException(status_code=404, detail="Студент не найден")

@app.post("/create_kim_y_v", status_code=201)
def create_kim_y_v(student: StudentCreate):
    new = {
        "id": 1 if not STUDENTS else max(s["id"] for s in STUDENTS) + 1,
        **student.model_dump()  
    }
    
    STUDENTS.append(new)
    return {"message": "Добавлен", "student": new}


@app.get("/get_kim_y_v")
def get_kim_y_v():

    for student in STUDENTS:
        if student["second_name"].lower() == "ким":  
            return student
            
    raise HTTPException(status_code=404, detail="Нет в списке")
