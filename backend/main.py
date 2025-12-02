from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
from pathlib import Path
from converter import PDFConverter

app = FastAPI(title="PDF to DOCX Converter")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
UPLOAD_DIR = Path("../uploads")
PROCESSED_DIR = Path("../processed")
UPLOAD_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)

# Store task status (in-memory for simplicity)
tasks = {}

def process_pdf(task_id: str, file_path: Path, output_path: Path):
    converter = PDFConverter()
    tasks[task_id] = {"status": "processing", "message": "Converting..."}
    
    success, message = converter.convert(str(file_path), str(output_path))
    
    if success:
        tasks[task_id] = {"status": "completed", "file_id": task_id}
    else:
        tasks[task_id] = {"status": "failed", "message": message}

@app.post("/upload")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    task_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{task_id}.pdf"
    output_path = PROCESSED_DIR / f"{task_id}.docx"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    tasks[task_id] = {"status": "queued"}
    background_tasks.add_task(process_pdf, task_id, file_path, output_path)
    
    return {"task_id": task_id}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.get("/download/{task_id}")
async def download_file(task_id: str):
    file_path = PROCESSED_DIR / f"{task_id}.docx"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path, 
        filename=f"converted_{task_id}.docx",
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
