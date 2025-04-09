import logging
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends, Request, status, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import inspect

import models
import schemas
import crud
from database import get_db, engine
from utils import perform_translation

# models.Base.metadata.create_all(bind=engine)#it will make sure if certain db exist, otherwise create one.

inspector = inspect(engine)
table_names = inspector.get_table_names()

if not table_names:
    models.Base.metadata.create_all(bind=engine)
    print("Database created successfully")
else:
    print("Database already exists")

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)



@app.get('/index', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.post('/translate/', response_model=schemas.TaskResponse)
def translate(
    request: schemas.TranslationRequest, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    task = crud.create_translation_task(db, request.text, request.language)
    background_tasks.add_task(perform_translation, task.id, request.text, request.language, db)
    return {"task_id": task.id}


@app.post('/translate/{task_id}', response_model=schemas.TranslationStatus)
def get_translate(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return {
        "task_id": task.id, 
        "status": task.status, 
        "translation": task.translation     
    }

@app.post('/translate/content/{task_id}', response_model=schemas.TranslationStatus)
def get_translate_content(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return {task}