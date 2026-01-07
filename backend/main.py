import os
import uuid
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.downloader import download_video
from backend.chunker import detect_peak_segments
from backend.video_utils import crop_vertical

from backend.ai_pipeline import get_captions_for_video
from backend.video_utils import burn_caption
from backend import video_utils as vu





# ---------- APP ----------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- PATHS ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Serve generated clips
app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")


# ---------- REQUEST MODEL ----------
class VideoRequest(BaseModel):
    url: str


# ---------- API ----------
@app.post("/process")
def process_video(req: VideoRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())

    # 🔥 DELETE OLD OUTPUT CLIPS (IMPORTANT FIX)
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith(".mp4"):
            os.remove(os.path.join(OUTPUT_DIR, f))

    background_tasks.add_task(run_job, req.url, job_id)
    return {"job_id": job_id}



def run_job(url: str, job_id: str):
    video_path = download_video(url)
    result = detect_peak_segments(video_path)

    result["clips"] = get_captions_for_video(video_path, result["clips"])

    for i, p in enumerate(result["clips"]):
        temp_out = os.path.join(OUTPUT_DIR, f"temp_{job_id}_{i}.mp4")
        final_out = os.path.join(OUTPUT_DIR, f"{job_id}_{i}.mp4")

        crop_vertical(video_path, temp_out, p["start"], 12)
        print("CAPTION TEXT:", p["caption"])


        vu.burn_caption(
            temp_out,
            final_out,
            p["caption"]
        )


        os.remove(temp_out)




@app.get("/status/{job_id}")
def status(job_id: str):
    files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith(job_id)]
    count = len(files)

    message = (
        f"Only {count} major peak moment found in this video."
        if count < 3
        else "Multiple peak moments detected."
    )

    return {
        "clips": files,
        "count": count,
        "message": message
    }
