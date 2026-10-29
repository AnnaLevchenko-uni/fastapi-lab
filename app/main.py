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

from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    age: int = 20


@app.post("/students", status_code=201)
def create_liza(payload: StudentCreate):
    student = {
        "id": len(STUDENTS) + 1,
        "name": payload.name,
        "age": payload.age
    }
# Со следующей строки добавляйте эндпоинты для students
from app.schemas import StudentCreate
from fastapi import HTTPException

@app.post("/students", status_code=201)
def create_student(payload: StudentCreate):
    student_data = payload.model_dump()
    student_data["id"] = len(STUDENTS) + 1  
    STUDENTS.append(student_data)
    return {"message": "Студент добавлен", "student": student_data}

@app.get("/students/{student_name}")
def get_student(student_name: str):

@app.post("/students/create_{student_name}", status_code=201, tags=["students"])
def create_student(student_name: str):
    if any(student["name"] == student_name for student in STUDENTS):
        raise HTTPException(status_code=409, detail="Студент уже существует")

    student = {"name": student_name}
    STUDENTS.append(student)
    return student


@app.get("/students/{student_id}")
def get_liza(student_id: int):
    for student in STUDENTS:
        if student["id"] == student_id:
@app.get("/students/get__{student_name}", tags=["students"])
def get_student(student_name: str):
    for student in STUDENTS:
        if student["name"] == student_name:
            return student

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
        if (student.get("first_name", "").lower() == student_name.lower() or
                student.get("second_name", "").lower() == student_name.lower()):
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


@app.post("/create_sendirev_t_s", status_code=201)
def create_sendirev_t_s(student: StudentCreate):
    new = {
        "id": 1 if not STUDENTS else max(s["id"] for s in STUDENTS) + 1,
        **student.model_dump()
    }

    STUDENTS.append(new)
    return {"message": "Добавлен", "student": new}


@app.get("/get_sendirev_t_s")
def get_sendirev_t_s():
    for student in STUDENTS:
        if student["second_name"].lower() == "tsendirev":
            return student

    raise HTTPException(status_code=404, detail="Нет в списке")
@app.post("/create_drachuk_u_p", status_code=201)
def create_drachuk_u_p():
    new_student = {
        "id": 1 if not STUDENTS else max(s["id"] for s in STUDENTS) + 1,
        "first_name": "Uliana",
        "second_name": "Drachuk",
        "group": 1,
        "course": 4,
    }
@app.post("/create_krutko_anastasia", status_code=201)
def create_krutko_anastasia(student: StudentCreate):
    new_student = {
        "id": len(STUDENTS) + 1,
        **student.model_dump(),
    }

@app.post("/create_kuznetsova_d_o", status_code=201)
def create_kuznetsova_d_o(student: StudentCreate):
    new_student = {
            "id": len(STUDENTS) + 1,
            "first_name": "Diana",
            "second_name": "Kuznetsova",
            "group": 1,
            "course": 4,
            }
    STUDENTS.append(new_student)
    return new_student


@app.get("/get_drachuk_u_p")
def get_drachuk_u_p():
    for student in STUDENTS:
        if student["second_name"] == "Drachuk":
@app.get("/get__krutko_anastasia")
def get__krutko_anastasia():
    for student in STUDENTS:
        if (
            student["first_name"].strip().lower() == "анастасия"
            and student["second_name"].strip().lower() == "крутко"
        ):
            return student

    raise HTTPException(
        status_code=404,
        detail="Студент не найден",
    )
@app.get("/get_kuznetsova_d_o")
def get_kuznetsova_d_o():
    for student in STUDENTS:
        if student["second_name"].lower() == "Kuznetsova":
            return student
    raise HTTPException(status_code=404, detail="Студент не найден")
@app.post("/create_airapetyan_v", status_code=201)
def create_airapetyan_v(student: StudentCreate):
    new_student = {
        "id": 1 if not STUDENTS else max(s["id"] for s in STUDENTS) + 1,
        **student.model_dump(),
    }
    STUDENTS.append(new_student)
    return new_student

@app.get("/get_airapetyan_v")
def get_airapetyan_v():
    for student in STUDENTS:
        if student["second_name"].lower() == "airapetyan":
            return student
    raise HTTPException(status_code=404, detail="Студент не найден")
