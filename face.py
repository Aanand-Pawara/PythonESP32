import face_recognition
import cv2
import os
import threading
import time

# ========== CONFIG ==========
FRAME_RESIZE_SCALE = 0.25  # for speed
PROCESS_EVERY_N_FRAMES = 2  # skip frames
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
# ============================

# ✅ Load known faces
known_face_encodings = []
known_face_names = []

print("🔍 Loading known faces...")
for filename in os.listdir("friends_faces"):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        path = os.path.join("friends_faces", filename)
        img = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(os.path.splitext(filename)[0])
            print(f"✅ Loaded: {filename}")
        else:
            print(f"❌ No face found in: {filename}")

# ✅ Threaded camera reader
class VideoStream:
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)
        self.ret, self.frame = self.capture.read()
        self.running = True
        thread = threading.Thread(target=self.update, daemon=True)
        thread.start()

    def update(self):
        while self.running:
            self.ret, self.frame = self.capture.read()

    def read(self):
        return self.ret, self.frame

    def release(self):
        self.running = False
        self.capture.release()

# ✅ Draw shadow text (always visible)
def draw_shadow_text(img, text, pos, font=cv2.FONT_HERSHEY_SIMPLEX, scale=0.8):
    x, y = pos
    # Black background rectangle
    (w, h), _ = cv2.getTextSize(text, font, scale, 1)
    cv2.rectangle(img, (x - 5, y - h - 5), (x + w + 5, y + 5), (0, 0, 0), -1)
    # White text
    cv2.putText(img, text, (x, y), font, scale, (255, 255, 255), 1, cv2.LINE_AA)

# ✅ Start webcam
stream = VideoStream()

frame_count = 0
print("📷 Camera started. Press Q to quit.")
while True:
    ret, frame = stream.read()
    if not ret:
        continue

    # Skip frames to speed up processing
    if frame_count % PROCESS_EVERY_N_FRAMES == 0:
        small = cv2.resize(frame, (0, 0), fx=FRAME_RESIZE_SCALE, fy=FRAME_RESIZE_SCALE)
        rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        locations = face_recognition.face_locations(rgb_small)
        encodings = face_recognition.face_encodings(rgb_small, locations)

        names = []
        for encoding in encodings:
            matches = face_recognition.compare_faces(known_face_encodings, encoding)
            name = "Unknown"
            if True in matches:
                name = known_face_names[matches.index(True)]
            names.append(name)

        face_locations = locations
        face_names = names

    # Draw results
    if 'face_locations' in locals():
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= int(1 / FRAME_RESIZE_SCALE)
            right *= int(1 / FRAME_RESIZE_SCALE)
            bottom *= int(1 / FRAME_RESIZE_SCALE)
            left *= int(1 / FRAME_RESIZE_SCALE)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 2)
            draw_shadow_text(frame, name, (left + 6, bottom - 6))

    # Top-left display
    draw_shadow_text(frame, "Press Q to quit", (10, 30))

    cv2.imshow("🧠 Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

# ✅ Clean up
stream.release()
cv2.destroyAllWindows()
print("🛑 Stopped.")
