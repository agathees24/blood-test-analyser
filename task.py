from crewai import Task, Crew
from agents import doctor, verifier, nutritionist, exercise_specialist
from tools import BloodTestReaderTool

# Initialize tool
reader_tool = BloodTestReaderTool()

# Task 1: Doctor reviews and interprets blood report
analyze_blood_report_task = Task(
    description=(
        "Interpret the blood test report found at {path}. The user has asked: {query}.\n"
        "Extract key values such as Hemoglobin, RBC, WBC, Platelet count, MCV, MCH.\n"
        "Provide medical insight, identify abnormalities, and suggest next steps."
    ),
    expected_output=(
        "Return a detailed medical summary including:\n"
        "- Key values with normal ranges\n"
        "- Flags on abnormal results\n"
        "- Health risks (if any)\n"
        "- Medical advice or follow-up recommendation"
    ),
    agent=doctor,
    tools=[reader_tool],
    async_execution=False,
    output_file="output/medical_summary.txt"
)

# Task 2: Nutritionist gives diet suggestions based on report
nutrition_task = Task(
    description=(
        "Based on the blood report at {path}, provide diet recommendations.\n"
        "Identify possible nutritional deficiencies or needs (e.g., iron, B12, vitamin D).\n"
        "Recommend food items, hydration tips, and general wellness practices."
    ),
    expected_output=(
        "Provide:\n"
        "- A personalized diet chart\n"
        "- Suggestions for supplements (if needed)\n"
        "- Tips on meal timing, hydration, and food groups"
    ),
    agent=nutritionist,
    tools=[reader_tool],
    async_execution=False,
    output_file="output/nutrition_advice.txt"
)

# Task 3: Fitness coach builds a custom plan
exercise_task = Task(
    description=(
        "Read the blood report at {path} and recommend a customized workout plan.\n"
        "Avoid intense training for patients with low hemoglobin or abnormal results.\n"
        "Suggest safe exercises and explain how they support better health."
    ),
    expected_output=(
        "Return:\n"
        "- Weekly exercise schedule (3-5 days/week)\n"
        "- Activity types: walking, yoga, strength, etc.\n"
        "- Safety notes for patients with health concerns"
    ),
    agent=exercise_specialist,
    tools=[reader_tool],
    async_execution=False,
    output_file="output/fitness_plan.txt"
)

# Task 4: Verifier checks if uploaded file is a blood report
verification_task = Task(
    description=(
        "Check the uploaded file at {path} to verify whether it's a valid blood test report.\n"
        "If it doesn't match expected structure, flag it."
    ),
    expected_output=(
        "Return:\n"
        "- Confirmation if file is a blood test report\n"
        "- Reason for rejection if not\n"
        "- File type and document title if available"
    ),
    agent=verifier,
    tools=[reader_tool],
    async_execution=False,
    output_file="output/verification_result.txt"
)

# 🧠 Assemble full Crew with all tasks
help_patients = Crew(
    agents=[doctor, nutritionist, exercise_specialist, verifier],
    tasks=[
        verification_task,
        analyze_blood_report_task,
        nutrition_task,
        exercise_task
    ],
    verbose=True,
    return_intermediate_steps=True  # ✅ Important for getting separate outputs
)

