# Pushup Counter with Pose Detection

This project is a **real-time push-up counter** built using **Python (OpenCV + MediaPipe)** and a **Node.js/Express server** for file uploads and video playback.  
It allows you to upload a workout video, process it, and get an annotated output video showing **pose landmarks**, **elbow angle**, and a **push-up counter**.

# Features
-  Upload workout videos through a web interface
-  Pose detection using **MediaPipe**
-  Calculates elbow angles for correct push-up form
-  Automatically counts push-ups
-  Visual overlay with:
  - Angle display
  - Push-up counter
  - Progress bars on both sides
-  Output video saved in `public/` and playable in the browser

# Tech Stack
- **Frontend**: HTML, CSS, EJS (for rendering pages)
- **Backend**: Node.js + Express
- **Video Processing**: Python (OpenCV, MediaPipe, NumPy)
- **File Uploads**: Multer (Node.js)

# Project Structure
pushup-counter/
│── public/ # Static files
│ ├── uploads/ # Uploaded videos
│ ├── output_pushups.mp4 # Processed video output
│── views/ # EJS templates
│── process_video.py # Python script for pose detection
│── server.js # Express server
│── package.json
│── README.md

## 🚀 Getting Started

### 1️⃣ Clone the repo
```bash
git clone https://github.com/rushilt912004/pushup-counter.git
cd pushup-counter

npm install

pip install opencv-python mediapipe numpy

node index.js


