import os
from celery import Celery
import google.generativeai as genai

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task(name="extract_ingredients_task")
def extract_ingredients_task(image_bytes):
    # This is where your Phase 2 Gemini logic lives
    # It runs in the background so the user doesn't have to wait
    return ["eggs", "milk", "spinach"] # Placeholder for now