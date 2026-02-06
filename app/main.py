from fastapi import FastAPI, UploadFile, File
from app.worker import celery_app, extract_ingredients_task, match_recipes_task
from celery import chain

app = FastAPI()

@app.post("/upload-fridge")
async def upload_fridge(file: UploadFile = File(...)):
    # 1. Receive the file
    content = await file.read()
    
    # 2. This creates a pipeline: Extract -> Match
    # The output of Task 1 (ingredients) is automatically passed to Task 2
    workflow = chain(
        extract_ingredients_task.s(content.hex()),
        match_recipes_task.s()
    )

    task = workflow.apply_async()
    return {"task_id": task.id, "status": "Analyzing photo and finding recipes..."}