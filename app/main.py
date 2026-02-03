from fastapi import FastAPI, UploadFile, File
from app.worker import extract_ingredients_task

app = FastAPI()

@app.post("/upload-fridge")
async def upload_fridge(file: UploadFile = File(...)):
    # 1. Receive the file
    content = await file.read()
    
    # 2. Hand it off to the background worker
    task = extract_ingredients_task.delay(content.hex())
    
    return {"task_id": task.id, "status": "Processing in background"}