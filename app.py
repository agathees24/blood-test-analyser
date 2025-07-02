import streamlit as st
import pandas as pd
import time
import requests
import os
from PDF_generator.generate_pdf import generate_pdf
from database.supabase_client import supabase

st.set_page_config(page_title="Blood Test Analyzer", page_icon="🧪", layout="wide")
st.title("🧪 Blood Test Report Analysis Dashboard")

# -------------------------------
# Upload & Run Analysis Section
# -------------------------------
st.subheader("📄 Upload Report (optional preview)")
uploaded_file = st.file_uploader("Upload a blood test report (PDF or TXT)", type=["pdf", "txt"])
query = st.text_input("📝 Enter your query", "Summarize my blood test report")

if uploaded_file is not None:
    st.success("✅ File uploaded successfully.")
    st.write("**Filename:**", uploaded_file.name)
    st.write("**Size:**", f"{uploaded_file.size / 1024:.2f} KB")

    if st.button("🚀 Run Analysis"):
        with st.spinner("⏳ Sending file for analysis..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.read())}
                data = {"query": query}
                response = requests.post("http://localhost:8000/analyze", files=files, data=data)

                if response.status_code == 200:
                    result = response.json()
                    task_id = result.get("task_id")
                    if task_id:
                        st.session_state["task_id"] = task_id
                        st.session_state["start_time"] = time.time()
                        st.session_state["query_type"] = query
                        st.session_state["submitted"] = True
                        st.rerun()
                    else:
                        st.error("❌ No task ID returned.")
                else:
                    st.error(f"❌ Server error: {response.status_code}")
                    st.text(response.text)

            except Exception as e:
                st.error(f"❌ Request failed: {e}")
else:
    st.warning("⚠️ No file uploaded yet.")

# ----------------------------------------
# ⏳ Show Live Task Progress if running
# ----------------------------------------
if st.session_state.get("submitted", False):
    task_id = st.session_state.get("task_id")
    start_time = st.session_state.get("start_time", time.time())
    status_url = f"http://localhost:8000/status/{task_id}"

    st.subheader("🔄 Live Report Status")
    with st.status("⏳ Analyzing report... wait ~2 mins", expanded=False) as status_box:
        progress_bar = st.empty()
        while True:
            try:
                response = requests.get(status_url)
                result = response.json()
                state = result.get("status")

                elapsed = int(time.time() - start_time)
                if state in ["PENDING", "Processing"]:
                    progress = min(99, int(elapsed * 1))  # Adjustable speed
                    progress_bar.progress(progress, text=f"Processing... {progress}%")
                    time.sleep(2)
                elif state == "Completed":
                    progress_bar.progress(100, text="✅ Completed!")
                    #st.success("🎉 Analysis complete. Click refresh to view results below.")
                    st.session_state["submitted"] = False
                    break
                elif state == "Failed":
                    st.error(f"❌ Analysis failed: {result.get('error')}")
                    st.session_state["submitted"] = False
                    break
                else:
                    st.warning(f"🔄 Unknown status: {state}")
                    time.sleep(2)
            except Exception as e:
                st.error(f"❌ Failed to fetch task status: {e}")
                break

    st.button("🔁 Refresh to Load Results", on_click=st.rerun)
    st.success("🎉 Analysis complete. Click refresh to view results below.")

# -------------------------------
# 📊 Report Viewer Section
# -------------------------------
st.divider()
st.header("📊 Analyzed Reports")

if st.button("🔄 Manual Refresh"):
    st.rerun()

# 🟡 Fetch data from Supabase
try:
    data = supabase.table("blood_reports").select("*").execute()
    df = pd.DataFrame(data.data)
    df = df.sort_values(by="id", ascending=False)  # Show newest on top
except Exception as e:
    st.error(f"❌ Failed to load reports: {e}")
    st.stop()

if df.empty:
    st.info("No reports found in Supabase yet.")
    st.stop()

# Filter by Query Type
query_filter = st.selectbox("🔍 Filter by Query Type", df["query"].unique())
filtered_df = df[df["query"] == query_filter]

# ✅ Render each report
if filtered_df.empty:
    st.info("No reports found for the selected query.")
else:
    for idx, row in filtered_df.iterrows():
        st.markdown(f"### 🧾 Report: `{row['filename']}`")

        col1, col2 = st.columns(2)
        with col1:
            st.write("📥 **Query Asked:**", row.get("query", "-"))
        with col2:
            st.write("🆔 **Record ID:**", row.get("id", "N/A"))

        # ✅ Completion %
        task_keys = ["medical_result", "nutrition_result", "exercise_result", "verification_result"]
        completed = sum(1 for key in task_keys if row.get(key))
        progress = int((completed / len(task_keys)) * 100)
        st.progress(progress, text=f"📊 Task Completion: {progress}%")

        # ✅ Expanders for each result
        with st.expander("🩺 Medical Result"):
            st.markdown(row.get("medical_result", "❌ No medical result yet."), unsafe_allow_html=True)

        with st.expander("🥦 Nutrition Result"):
            st.markdown(row.get("nutrition_result", "❌ No nutrition result yet."), unsafe_allow_html=True)

        with st.expander("🏃 Exercise Result"):
            st.markdown(row.get("exercise_result", "❌ No exercise result yet."), unsafe_allow_html=True)

        with st.expander("📄 Verification Result"):
            st.markdown(row.get("verification_result", "❌ No verification result yet."), unsafe_allow_html=True)

        # ✅ Download full PDF
        pdf_path = generate_pdf(row)
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download Full PDF Report",
                    data=f.read(),
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf"
                )

        st.divider()

# Footer
st.markdown("Powered by **OpenAI**, **CrewAI**, **Celery**, and **Supabase** 🚀")
