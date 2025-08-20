import sys
import cv2
import mediapipe as mp
import numpy as np
import os

# -----------------------------
# Get input video path from command line
# -----------------------------
if len(sys.argv) < 2:
    print("Usage: python process_video.py <input_video_path>")
    sys.exit(1)

video_path = sys.argv[1]
print(f"Processing video: {video_path}")

# -----------------------------
# Setup Mediapipe
# -----------------------------
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# -----------------------------
# Open input video
# -----------------------------
cap = cv2.VideoCapture(video_path)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# -----------------------------
# Output video path & writer (H.264 codec for browser)
# -----------------------------
output_path = 'public/output_pushups.mp4'
fourcc = cv2.VideoWriter_fourcc(*'avc1')  # H.264 codec
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# -----------------------------
# Push-up counter variables
# -----------------------------
counter = 0
stage = None

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to RGB for Mediapipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        frame = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Overlay rectangle for text
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, 100), (50, 50, 50), -1)
        frame = cv2.addWeighted(overlay, 0.4, frame, 0.6, 0)

        try:
            landmarks = results.pose_landmarks.landmark

            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * width,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * height]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * width,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * height]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * width,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * height]

            angle = calculate_angle(shoulder, elbow, wrist)

            cv2.putText(frame, f'Elbow Angle: {int(angle)}°', (30, 70),
                        cv2.FONT_HERSHEY_DUPLEX, 1.2, (255, 255, 0), 2)

            if angle > 160:
                stage = "up"
            if angle < 90 and stage == 'up':
                stage = "down"
                counter += 1

            cv2.putText(frame, f'Push-ups: {counter}', (width//2 - 150, 70),
                        cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)

            bar_fill = np.interp(angle, (90, 160), (350, 0))

            for i in range(int(350 - bar_fill), 350):
                color = (0, int(255 * (i - (350 - bar_fill)) / bar_fill),
                         255 - int(255 * (i - (350 - bar_fill)) / bar_fill))
                cv2.line(frame, (100, i + 150), (150, i + 150), color, 1)
                cv2.line(frame, (width - 150, i + 150), (width - 100, i + 150), color, 1)

            cv2.rectangle(frame, (100, 150), (150, 500), (255, 255, 255), 2)
            cv2.rectangle(frame, (width - 150, 150), (width - 100, 500), (255, 255, 255), 2)

            cv2.circle(frame, (125, 150), 10, (255, 0, 255), -1)
            cv2.circle(frame, (width - 125, 150), 10, (255, 0, 255), -1)

            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=6, circle_radius=8),
                mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=4, circle_radius=6)
            )

        except:
            pass

        # Write frame to output video
        out.write(frame)

# Release resources
cap.release()
out.release()

print(f"✅ Output video saved as: {output_path} (encoded in H.264 for browser playback)")
