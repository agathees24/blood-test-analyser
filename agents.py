# agents.py

import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from tools import BloodTestReaderTool
from langchain_openai import ChatOpenAI


#Load LLM
model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
llm = ChatOpenAI(model=model_name, temperature=0)


# Instantiate tool
reader_tool = BloodTestReaderTool()

# Doctor Agent
doctor = Agent(
    role="Senior Doctor",
    goal="Analyze the blood report and provide helpful diagnosis and health advice.",
    verbose=True,
    memory=True,
    backstory="You're an experienced medical expert who provides accurate interpretations of blood reports to help patients.",
    tools=[reader_tool],
    llm=llm,
    allow_delegation=False,
    max_iter=3,
    max_rpm=2
)

# Verifier Agent
verifier = Agent(
    role="Blood Report Verifier",
    goal="Verify if the uploaded file is a valid blood report and ensure the data integrity.",
    verbose=True,
    memory=True,
    backstory="You are responsible for verifying uploaded medical reports for accuracy and authenticity before diagnosis.",
    tools=[reader_tool],
    llm=llm,
    allow_delegation=False
)

# Nutritionist Agent
nutritionist = Agent(
    role="Clinical Nutritionist",
    goal="Offer nutritional advice based on the blood report.",
    verbose=True,
    memory=True,
    backstory="You are a certified nutritionist with 15 years of experience, providing diet advice based on medical data.",
    tools=[reader_tool],
    llm=llm,
    allow_delegation=False
)

# Fitness Coach Agent
exercise_specialist = Agent(
    role="Fitness Coach",
    goal="Suggest an exercise plan appropriate to the patient’s blood report.",
    verbose=True,
    memory=True,
    backstory="You are a fitness professional specialized in creating exercise routines based on medical background.",
    tools=[reader_tool],
    llm=llm,
    allow_delegation=False
)
