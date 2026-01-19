import fastapi, io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
import pandas as pd
from generate_report import generate_report

app = FastAPI(title="SaaS Analytics Report Generator")

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files supported")

    contents = await file.read()

    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV format")

    html_report = generate_report(df)

    return HTMLResponse(content=html_report)
