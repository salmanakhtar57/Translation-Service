import openai
from sqlalchemy.orm import Session
from crud import update_translation_task
from dotenv import load_dotenv
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def perform_translation(task: int, text: str, languages: list, db: Session):
    translation = {}