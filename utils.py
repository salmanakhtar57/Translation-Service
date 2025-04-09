import openai
from sqlalchemy.orm import Session
from crud import update_translation_task
from dotenv import load_dotenv

import os
# from models import TranslationRequest, TranslationResult, IndividualTranslations
# from datetime import datetime
from database import get_db
from typing import List
#from my_secrets import api_key


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def perform_translation(text: str, languages: list, db: Session,  task_id:int):
    translation = {}
    for language in languages:
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a helpful assistance who translate the following text to {language}:"},
                    {"role": "user", "content": text},
                ],
                max_tokens=1000
            )
            translate_text = response['choices'][0]['message']['content'].strip()
            translation[language] = translate_text
        except Exception as e:
            print(f"Error translating to {language}")
            translation[language] = f"Error: {e}"
        except Exception as e:
            print(f"Unexpected error {e}")
            translation[language] = f"Unexpected error: {e}"
            update_translation_task(db, task_id, translation)

# async def perform_translation(task: int, text: str, languages: List):
#     translation = {}
#     for language in languages:
#         try:
#             translated_text = await translate_text(text, language)
#             translation_result = TranslationResult(
#                 request_id=request_id, language=language, translated_text=translated_text
#             )
#             individual_translation = IndividualTranslations(
#                 request_id=request_id, translated_text=translated_text
#             )
#             session.add(translation_result)
#             session.add(individual_translation)
#             session.commit()
#         request = session.query(TranslationRequest).filter(TranslationRequest.id == request_id).first()
#         request.status = "completed"
#         request.updated_at = datetime.utcnow()
#         session.add(request)
#         session.commit()