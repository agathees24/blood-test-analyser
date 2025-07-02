# 🧪 AI-Powered Blood Test Report Analyzer

Blood Test Report Analyzer is an AI-powered medical assistant designed to analyze uploaded blood test reports and provide comprehensive insights, personalized recommendations, and health summaries using CrewAI, LangChain, and OpenAI models. This system transforms traditionally manual, time-consuming interpretation of lab results into an instant, intelligent experience powered by large language models.

The system allows users (patients, doctors, or labs) to upload .pdf or .txt reports, submit a query (e.g., "Summarize my blood test"), and receive structured results across 4 domains:  


🩺 Medical Diagnosis – Highlights abnormal values, flags risks, and provides follow-up advice.  
🥦 Nutritional Guidance – Suggests diet improvements based on nutrient deficiencies.  
🏋️ Fitness Plan – Offers personalized exercise plans adjusted to blood parameters.  
📄 Report Verification – Confirms if the uploaded file is a valid blood test report.

---

What i do:  
✅ Intelligent report interpretation using multiple AI agents (Doctor, Nutritionist, Fitness Coach, Verifier)  
✅ FastAPI backend for secure file uploads and task orchestration  
✅ Streamlit dashboard for interactive UI and real-time result visualization      
✅ Celery-based asynchronous task processing using Redis queue  
✅ Supabase integration for storing analysis results and query history  
✅ PDF report generation with full summaries for user download  
✅ 📦 Now Supports Both **PDF and TXT** Inputs with Live AI Analysis
✅ ✨ Uses **OpenAI GPT-4o-mini** for reliable and context-aware report generation (💡 replaces Serper used in original company code) 



---

## 🛠️ Bugs Found and How I Fixed Them (Company Code vs Fixed Code)


| 🔍 Issue                                                                         | 📁 File(s)             | 🛠️ Fix Applied                                                                                                  |
| -------------------------------------------------------------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------- |
| ❌ **No LLM Initialized** (`llm = llm` without defining `llm`)                    | `agents.py`            | Properly imported and initialized `ChatOpenAI` LLM from `langchain_openai`, using `.env` keys                    |
| ❌ **Fictional, joke-based agent prompts** (Dr. House style, selling supplements) | `agents.py`, `task.py` | Rewrote all agents (Doctor, Verifier, Nutritionist, Fitness Coach) with **professional medical roles and tasks** |
| ❌ **All tasks run inside `/analyze` API blocking request**                       | `main.py`              | Moved long tasks to **Celery background workers** to support **asynchronous processing**                         |
| ❌ **No task progress shown in UI**                                               | Not present            | Added `GET /status/{task_id}` API and used **live % progress bar in Streamlit**                                  |
| ❌ **No structured output or file-based results**                                 | `main.py`, `task.py`   | Used `Crew.return_intermediate_steps=True`, saved output to `output/` as `.txt` files                            |
| ❌ **No Supabase integration** (data lost after restart)                          | Not present            | Integrated **Supabase** to store: filename, query, all 4 AI-generated results                                    |
| ❌ **No PDF export**                                                              | Not present            | Added `generate_pdf.py` using `FPDF`, with emoji/Unicode fixes                                                   |
| ❌ **No CORS enabled for API**                                                    | `main.py`              | Added `CORSMiddleware` so frontend (Streamlit) can call backend (FastAPI)                                        |
| ❌ **Only 1 hardcoded query type (medical)**                                      | `task.py`              | Added 3 more realistic task flows: **Nutrition**, **Fitness**, **Verification**                                  |
| ❌ **No task cleanup** (files left undeleted)                                     | `main.py`, `task.py`   | Added file cleanup logic in `worker.py → finally:` block                                                         |
| ❌ **No file support check**                                                      | `main.py`              | Now checks file extension is `.pdf` or `.txt`                                                                    |
| ❌ **Broken PDF reader tool (not async)**                                         | `tools.py`             | Refactored into class-based `BloodTestReaderTool` using `PDFMinerLoader`                                         |
| ❌ **No unified launcher**                                                        | Not present            | Created `run_all.py` to launch: Redis, Celery, FastAPI, and Streamlit in correct order                           |
| ❌ **Missing error handling and validations**                                     | Multiple files         | Added try-except blocks around key logic (file save, Supabase insert, file read, Celery errors)                  |

---
## 🚀 Additional Features and Enhancements

| Feature                                  | Description                                                                 |
| ---------------------------------------- | --------------------------------------------------------------------------- |
| ✅ **Live Analysis Tracking**             | Progress % bar shown in real-time using `GET /status/{task_id}`             |
| ✅ **Celery Task Queue**                  | Enables multiple requests to be processed without blocking UI               |
| ✅ **Supabase Integration**               | Stores all uploaded filenames, queries, and generated results               |
| ✅ **Query Type Filtering**               | View results grouped by query type in Streamlit dashboard                   |
| ✅ **Streamlit UI Polished**              | Better sectioning, icons, progress bars, expanders, refresh button          |
| ✅ **PDF Download**                       | Generates and allows download of AI-generated full blood report summary     |
| ✅ **Unicode & Emoji Handling in PDF**    | Cleaned non-latin-1 characters before PDF export                            |
| ✅ **One-click Launch Script**            | `run_all.py` auto-starts Redis, Celery, FastAPI, Streamlit in correct order |
| ✅ **Docker Integration for Redis**       | Uses Docker to auto-run Redis server even on Windows                        |
| ✅ **Reusable File Tool**                 | `BloodTestReaderTool` handles `.pdf` and `.txt` input across all agents     |
| ✅ **CORS Support in FastAPI**            | Allows UI → API communication without browser errors                        |
| ✅ **Failure-safe Task Result Retrieval** | Status endpoint handles `PENDING`, `SUCCESS`, `FAILURE` states              |

---

## ⚙️ Setup Instructions

### ✅ 1. Clone the Repository

```bash
git clone https://github.com/yourusername/blood-test-analyzer.git
cd blood-test-analyzer
