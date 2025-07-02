from worker import analyze_blood_report_task
from database.supabase_client import supabase
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import shutil
from task import help_patients

app = FastAPI(title="Blood Test Report Analyzer")

# Optional: Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Blood Test Report Analyzer API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarize my blood test report")
):
    """Analyze blood test report and return diagnosis"""

    try:
        # Extract original file extension
        ext = file.filename.split(".")[-1].lower()
        if ext not in ["pdf", "txt"]:
            raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")

        # Generate a unique filename with correct extension
        unique_filename = f"blood_report_{uuid.uuid4()}.{ext}"
        file_path = os.path.join(DATA_DIR, unique_filename)

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Queue background task
        task = analyze_blood_report_task.delay(file_path, query, unique_filename)

        return {
            "status": "queued",
            "task_id": task.id,
            "message": "Your report is being processed in the background."
        }

    
       
        # Run the task (your logic)
        result = help_patients.kickoff(inputs=inputs)
        # ✅ Save to Supabase
        try:
            supabase.table("blood_reports").insert({
                "filename": file.filename,
                "query": query,
                "result": str(result)
            }).execute()
            print("✅ Saved to Supabase successfully")
        except Exception as e:
            print("❌ Supabase save error:", e)
        return JSONResponse(content={
            "status": "success",
            "message": "Analysis complete.",
            "analysis": str(result),
            "file_uploaded": file.filename
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    '''finally:
        # Clean up uploaded file
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass  # Ignore cleanup failure'''
        
@app.get("/status/{task_id}")
def get_status(task_id: str):
    task_result = analyze_blood_report_task.AsyncResult(task_id)

    if task_result.state == "PENDING":
        return {"status": "Processing"}
    elif task_result.state == "SUCCESS":
        return {"status": "Completed", "result": task_result.result}
    elif task_result.state == "FAILURE":
        return {"status": "Failed", "error": str(task_result.info)}
    else:
        return {"status": task_result.state}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
