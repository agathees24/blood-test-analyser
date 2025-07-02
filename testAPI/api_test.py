from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

# Load your .env file
load_dotenv()

# Fetch API key and model name from .env
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")

if not api_key:
    print("❌ OPENAI_API_KEY not found in .env")
    exit()

# Initialize the model
llm = OpenAI(
    temperature=0.5,
    model=model_name,
    openai_api_key=api_key
)

# Ask a basic medical question
prompt = "Explain what hemoglobin does in the blood."

try:
    response = llm.invoke(prompt)
    print("✅ LLM Response:\n")
    print(response)
except Exception as e:
    print("❌ LLM failed with error:")
    print(e)
