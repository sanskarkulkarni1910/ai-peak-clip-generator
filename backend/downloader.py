import yt_dlp
import os
import uuid

def download_video(url: str):
    video_id = str(uuid.uuid4())
    out = f"input_{video_id}.mp4"

    ydl_opts = {
        "outtmpl": out,
        "format": "mp4"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return os.path.abspath(out)
