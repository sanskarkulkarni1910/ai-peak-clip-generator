import os
import librosa
import numpy as np
import cv2

def detect_peak_segments(video_path, num_clips=4, clip_len=35, min_gap=40):
    audio_path = os.path.join(os.path.dirname(video_path), "audio.wav")
    os.system(
        f'ffmpeg -loglevel quiet -i "{video_path}" -vn -ac 1 -ar 16000 -y "{audio_path}"'
    )

    # ---------- AUDIO ENERGY ----------
    try:
        y, sr = librosa.load(audio_path, sr=None)
        energy = librosa.feature.rms(y=y)[0]
        if np.max(energy) > 0:
            energy = energy / np.max(energy)
    except:
        energy = np.zeros(1000)

    # ---------- MOTION ----------
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    motion = []
    ret, prev = cap.read()
    if not ret:
        return {"clips": [{"start": 0}], "peak_count": 1, "message": "Fallback clip"}

    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, gray)
        motion.append(np.mean(diff))
        prev_gray = gray

    cap.release()

    motion = np.array(motion)
    if np.max(motion) > 0:
        motion = motion / np.max(motion)

    # ---------- COMBINE AUDIO + MOTION ----------
    length = min(len(energy), len(motion))
    combined = (energy[:length] * 0.6) + (motion[:length] * 0.4)

    threshold = np.mean(combined) + np.std(combined)
    peak_indices = np.where(combined > threshold)[0]

    peaks = []
    for idx in peak_indices:
        peaks.append({
            "start": idx / fps,
            "score": combined[idx]
        })

    peaks = sorted(peaks, key=lambda x: x["score"], reverse=True)

    # ---------- SELECT FINAL CLIPS ----------
    selected = []
    for p in peaks:
        start_time = round(max(0, p["start"] - clip_len / 2), 2)

        if all(abs(start_time - s["start"]) > min_gap for s in selected):
            selected.append({"start": start_time})

        if len(selected) == num_clips:
            break

    # ---------- FALLBACK ----------
    if not selected:
        selected = [{"start": 0}]

    if os.path.exists(audio_path):
        os.remove(audio_path)

    peak_count = len(selected)

    message = (
        f"Only {peak_count} peak moments found."
        if peak_count < num_clips
        else "4 peak moments detected."
    )

    print("\n--- PEAK MOMENTS ---")
    for c in selected:
        print("Clip at:", c["start"], "sec")
    print("Message:", message)
    print("-------------------\n")

    return {
        "clips": selected,
        "peak_count": peak_count,
        "message": message
    }
