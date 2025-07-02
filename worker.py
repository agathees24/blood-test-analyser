# worker.py

import os
from celery import Celery
from task import help_patients
from database.supabase_client import supabase

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task(name="analyze_blood_report_task")
def analyze_blood_report_task(file_path: str, query: str, filename: str):
    try:
        print("🚀 Running CrewAI...")
        inputs = {"path": file_path, "query": query}
        result = help_patients.kickoff(inputs=inputs)
        print("✅ CrewAI processing complete.")

        # Read each output file if exists
        def read_output(file):
            full_path = os.path.join("output", file)
            if os.path.exists(full_path):
                with open(full_path, "r", encoding="utf-8") as f:
                    return f.read()
            return None

        medical_result = read_output("medical_summary.txt")
        nutrition_result = read_output("nutrition_advice.txt")
        exercise_result = read_output("fitness_plan.txt")
        verification_result = read_output("verification_result.txt")

        # ✅ Save structured results to Supabase
        supabase.table("blood_reports").insert({
            "filename": filename,
            "query": query,
            "medical_result": medical_result,
            "nutrition_result": nutrition_result,
            "exercise_result": exercise_result,
            "verification_result": verification_result
        }).execute()
        print("✅ Saved to Supabase successfully.")

        return str(result)

    except Exception as e:
        print(f"❌ Worker error: {e}")
        return f"❌ Error: {str(e)}"

    finally:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"🧹 Deleted file: {file_path}")
        except Exception as cleanup_error:
            print(f"⚠️ Error deleting file: {cleanup_error}")
