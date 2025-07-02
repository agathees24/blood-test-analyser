import subprocess
import time
import signal
import sys

# Helper to stop all subprocesses
def stop_all_processes(processes):
    print("\n🛑 Stopping all services...")
    for proc in processes:
        if proc.poll() is None:  # if still running
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
    print("✅ All services stopped.")

try:
    # Step 1: Start Redis
    print("🚀 Creating Redis container...")
    redis_create = subprocess.run([
        "docker", "run", "-d", "--name", "redis-server", "-p", "6379:6379", "redis"
    ], stderr=subprocess.DEVNULL)

    time.sleep(10)

    print("🔁 Restarting Redis container...")
    subprocess.run(["docker", "stop", "redis-server"])
    time.sleep(5)
    subprocess.run(["docker", "start", "redis-server"])
    time.sleep(10)

    # Step 2: Start Celery
    print("⚙️ Starting Celery worker (may take ~1 min)...")
    celery = subprocess.Popen([
        "celery", "-A", "worker.celery_app", "worker", "--loglevel=info", "--pool=solo"
    ])
    time.sleep(50)

    # Step 3: Start FastAPI
    print("🌐 Starting FastAPI (API)...")
    api = subprocess.Popen(["uvicorn", "main:app", "--reload"])

    # Step 4: Start Streamlit
    print("🧪 Launching Streamlit Dashboard...")
    streamlit = subprocess.Popen(["streamlit", "run", "app.py"])

    print("✅ All services launched and running! Press Ctrl+C to stop.")

    # Wait for exit signal
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    stop_all_processes([celery, api, streamlit])
    print("🛑 Exiting gracefully.")
    sys.exit(0)
