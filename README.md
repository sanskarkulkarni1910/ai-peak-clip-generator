# 🎬 AI Peak Clip Generator

An AI-based backend service that automatically detects peak moments in videos and generates short vertical clips suitable for Instagram Reels and YouTube Shorts.

This project is built using **FastAPI** and **FFmpeg** and focuses on automated short-form video content generation.

> 🚀 This is my **first AI-based tool**, developed as a learning and practical project.

---

## ✨ Features

- Automatically detects **peak moments** in videos  
- Generates **vertical (9:16) short clips**
- Optimized for **Reels / Shorts**
- FastAPI-based backend
- Uses FFmpeg for video processing
- Lightweight and deployable on Render

---

## 🧠 How It Works (Simple Explanation)

1. User provides a video URL  
2. The system analyzes the video to detect **important moments**
3. Peak moments are selected
4. Short vertical clips are generated automatically
5. Generated clips are served as downloadable outputs

---

## 🛠️ Tech Stack

- Python
- FastAPI
- FFmpeg
- Uvicorn
- Pydantic

---

## 📁 Project Structure

ai-peak-clip-generator/
│
├── backend/
│ ├── main.py
│ ├── video_utils.py
│ ├── ai_pipeline.py
│ ├── downloader.py
│ └── chunker.py
│
├── requirements.txt
└── README.md

---

## ▶️ How to Run Locally

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt

**Start Backend Server**
cd C:\Users\Armish\Desktop\ai-peak-clip-generator
uvicorn backend.main:app --reload


## 🖥️ Frontend Setup & Run Process

The frontend is a simple static web interface that allows users to submit a video URL and view the generated clips.

---

### 📁 Frontend Structure

frontend/
│
├── index.html
├── result.html
└── clips/


---

### ▶️ How to Run Frontend (Local)

#### Method 1️⃣: Using Live Server (Recommended)

1. Open the project folder in **VS Code**
2. Install the **Live Server** extension (if not already installed)
3. Right-click on `index.html`
4. Click **“Open with Live Server”**

The frontend will open in your browser at:



---

#### Method 2️⃣: Open Directly in Browser

1. Go to the `frontend` folder
2. Double-click `index.html`
3. It will open in your default browser

> ⚠️ Note: Some browsers may block API requests when opened directly.  
> Using **Live Server** is recommended.

---

### 🔗 Backend Connection

Make sure the backend server is running before using the frontend.

**Local Backend URL**
```js
http://127.0.0.1:8000

