import cv2
from datetime import datetime
import time
import os

os.makedirs("screenshots", exist_ok=True)

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

face_missing_start = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Sedikit peningkatan sensitivitas dengan minNeighbors dan scaleFactor
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.08, minNeighbors=4)

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    filename_time = datetime.now().strftime('%H%M%S')

    if len(faces) > 1:
        msg = f"[{now}] Lebih dari 1 wajah terdeteksi"
        print(msg)
        with open("cheating_log.txt", "a") as log:
            log.write(msg + "\n")
        cv2.imwrite(f"screenshots/terdeteksi curang_{filename_time}.jpg", frame)

    elif len(faces) == 0:
        if face_missing_start is None:
            face_missing_start = time.time()
        elif time.time() - face_missing_start > 3:
            msg = f"[{now}] Wajah tidak terlihat lebih dari 3 detik (diduga curang)"
            print(msg)
            with open("cheating_log.txt", "a") as log:
                log.write(msg + "\n")
            cv2.imwrite(f"screenshots/terseteksi curang_{filename_time}.jpg", frame)
            face_missing_start = None
    else:
        # Jika 1 wajah terdeteksi
        cv2.imwrite(f"screenshots/terdeteksi aman_{filename_time}.jpg", frame)
        face_missing_start = None

    # Gambar kotak di sekitar wajah
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Tambahkan teks jumlah wajah
    cv2.putText(frame, f"Wajah Terdeteksi: {len(faces)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # Tampilkan frame
    cv2.imshow("Ujian Online - Deteksi Kecurangan", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
