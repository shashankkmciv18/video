from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()


# uvicorn cron.JobScheduler:app --reload --port 8001 To run this command.
def upload_video_task():
    print("Running video upload task...")  # Replace this with your actual upload logic


# Add job: run every 20 minutes
trigger = CronTrigger(minute='*/1')  # Every 20 minutes
scheduler.add_job(upload_video_task, trigger, id="upload_task", replace_existing=True)


# FastAPI route for testing
@app.get("/")
def read_root():
    return {"message": "FastAPI is running with a scheduled job every 20 minutes."}
