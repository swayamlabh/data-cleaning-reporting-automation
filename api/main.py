from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from src.automation import run_pipeline
from src.models import CleaningOptions

app = FastAPI(title="Data Cleaning & Reporting Automation", version="0.1.0")
UPLOAD_DIR = Path("data/raw")
RESULTS: dict[str, dict] = {}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if Path(file.filename or "").suffix.lower() not in {".csv", ".xlsx", ".xls", ".json", ".parquet"}:
        raise HTTPException(400, "Unsupported file type")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True); target = UPLOAD_DIR / f"{uuid4()}_{file.filename}"
    target.write_bytes(await file.read())
    return {"file_id": str(target), "filename": file.filename}


@app.post("/clean")
def clean(file_id: str, options: CleaningOptions = CleaningOptions()):
    try:
        result=run_pipeline(file_id, options); key=str(uuid4()); RESULTS[key]=result.model_dump(); return {"job_id": key, **RESULTS[key]}
    except (FileNotFoundError, ValueError) as exc: raise HTTPException(400, str(exc)) from exc


@app.post("/analyze")
def analyze(file_id: str): return run_pipeline(file_id).model_dump()


@app.post("/report")
def report(file_id: str): return run_pipeline(file_id).model_dump()


@app.get("/download/{job_id}/{format_name}")
def download(job_id: str, format_name: str):
    if job_id not in RESULTS or format_name not in RESULTS[job_id]["report_paths"]: raise HTTPException(404, "Report not found")
    return FileResponse(RESULTS[job_id]["report_paths"][format_name])
