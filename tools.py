from crewai.tools import BaseTool
from langchain_community.document_loaders import PDFMinerLoader
import os

# ✅ Main tool for reading blood reports (PDF or TXT)
class BloodTestReaderTool(BaseTool):
    name: str = "Read PDF Blood Report"
    description: str = "Reads a blood report from a PDF or TXT file and returns its content."

    def _run(self, path: str) -> str:
        try:
            if not os.path.exists(path):
                return f"❌ File not found: {path}"

            if path.lower().endswith(".pdf"):
                loader = PDFMinerLoader(file_path=path)
                docs = loader.load()
                full_text = "\n".join(doc.page_content.strip() for doc in docs)
            elif path.lower().endswith(".txt"):
                with open(path, "r", encoding="utf-8") as f:
                    full_text = f.read()
            else:
                return "❌ Unsupported file type. Only PDF and TXT are supported."

            # Truncate to first 2000 words to keep it LLM-friendly
            words = full_text.split()
            if len(words) > 2000:
                full_text = " ".join(words[:2000])
                full_text += "\n\n[Note: Text truncated to 2000 words for analysis.]"

            return full_text
        except Exception as e:
            return f"❌ Error reading file: {str(e)}"

# 🧪 Placeholder for Nutrition Tool (not used yet)
class NutritionTool:
    def analyze_nutrition(self, blood_report_data: str) -> str:
        # Add future logic here
        return "🧪 Nutrition analysis functionality not yet implemented."

# 🏋️‍♂️ Placeholder for Exercise Tool (not used yet)
class ExerciseTool:
    def create_plan(self, blood_report_data: str) -> str:
        # Add future logic here
        return "🏋️ Exercise planning functionality not yet implemented."
