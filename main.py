from datetime import datetime
from fastapi import FastAPI, Depends, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from database import engine, get_db, Base
from models import Task
from schemas import TaskCreate

# Создание таблиц при старте (для демо-целей)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Инициализация БД при старте приложения
@app.on_event("startup")
async def on_startup():
    await init_db()

# --- ROUTES ---

# READ (Чтение списка и отображение страницы)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: AsyncSession = Depends(get_db)):
    # Запрос к БД через ORM
    result = await db.execute(select(Task).order_by(Task.id.desc()))
    tasks = result.scalars().all()
    
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

# CREATE (Создание)
@app.post("/add")
async def add_task(
    title: str = Form(...),
    description: str = Form(None),
    db: AsyncSession = Depends(get_db)
):
    new_task = Task(title=title, description=description)
    db.add(new_task)
    await db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# UPDATE (Обновление статуса - пример частичного обновления)
@app.post("/toggle/{task_id}")
async def toggle_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.is_completed = not task.is_completed
    await db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# DELETE (Удаление)
@app.post("/delete/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    await db.execute(delete(Task).where(Task.id == task_id))
    await db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# app/main.py (добавьте после импортов)

@app.get("/health", include_in_schema=False)
async def health_check():
    """
    Эндпоинт для проверки работоспособности приложения.
    Используется Docker healthcheck и оркестраторами.
    """
    return {
        "status": "healthy",
        "service": "fastapi-app",
        "timestamp": datetime.utcnow().isoformat()
    }