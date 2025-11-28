import cv2
import os
import pandas as pd
from datetime import datetime

CASCADE_PATH = "haarcascade_frontalface_default.xml"
MODEL_PATH = "face_model.yml"
LABELS_PATH = "labels.txt"
STUDENTS_FILE = "students.csv"

ATTENDANCE_DIR = "attendance"
CONFIDENCE_THRESHOLD = 80  

def load_labels(labels_path):
    labels = {}
    if not os.path.exists(labels_path):
        return labels
    with open(labels_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            label_id, student_id = line.split(",", 1)
            labels[int(label_id)] = student_id
    return labels

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    make_dir(ATTENDANCE_DIR)

    if not os.path.exists(MODEL_PATH):
        print("[ERROR] Model not found. Train the model first.")
        return

    labels = load_labels(LABELS_PATH)
    if not labels:
        print("[ERROR] Labels not found.")
        return

    if not os.path.exists(STUDENTS_FILE):
        print("[ERROR] students.csv not found. Register students first.")
        return

    # Load student details
    students_df = pd.read_csv(STUDENTS_FILE, dtype=str)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    cap = cv2.VideoCapture(0)

    attendance = {}      # student_id time_in
    seen_frames = {}     # student_id how many frames seen
    total_frames = 0

    print("[INFO] Press 'q' to end class and save attendance.")
    print("[INFO] System is analyzing attentiveness...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Camera not found.")
            break

        total_frames += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100)
        )

        detected_ids_this_frame = set()

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            label_id, confidence = recognizer.predict(roi_gray)

            if confidence < CONFIDENCE_THRESHOLD:
                student_id = labels.get(label_id, None)

                if student_id:
                    if student_id not in attendance:
                        attendance[student_id] = datetime.now().strftime("%H:%M:%S")

                    detected_ids_this_frame.add(student_id)

                    display_name = f"ID: {student_id}"
                    color = (0, 255, 0)
                else:
                    display_name = "Unknown"
                    color = (0, 0, 255)
            else:
                display_name = "Unknown"
                color = (0, 0, 255)

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, display_name, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Add frame count for those seen
        for sid in detected_ids_this_frame:
            if sid not in seen_frames:
                seen_frames[sid] = 0
            seen_frames[sid] += 1

        cv2.imshow("Attendance & Attentiveness - Press q to finish", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if attendance:
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_name = f"Attendance_{date_str}.xlsx"
        file_path = os.path.join(ATTENDANCE_DIR, file_name)

        rows = []

        for student_id, time_in in attendance.items():
            info = students_df[students_df["student_id"] == student_id]

            if info.empty:
                name = roll = reg_no = email = ""
            else:
                info = info.iloc[0]
                name = info.get("name", "")
                roll = info.get("roll", "")
                reg_no = info.get("registration_no", "")
                email = info.get("email", "")

            seen = seen_frames.get(student_id, 0)
            ratio = seen / total_frames if total_frames > 0 else 0

            attentive_status = "Attentive" if ratio >= 0.5 else "Not attentive"

            rows.append({
                "Date": date_str,
                "Student ID": student_id,
                "Roll": roll,
                "Registration No": reg_no,
                "Name": name,
                "Email": email,
                "Time In": time_in,
                "Seen Frames": seen,
                "Total Frames": total_frames,
                "Attentive Ratio": round(ratio, 2),
                "Attentive Status": attentive_status,
                "Status": "Present"
            })

        df = pd.DataFrame(rows)
        df.to_excel(file_path, index=False)
        print("[INFO] Attendance & attentiveness saved to", file_path)

        # Auto-open Excel file
        try:
            os.startfile(file_path)    
        except:
            try:
                os.system(f'xdg-open \"{file_path}\"') 
            except:
                pass

    else:
        print("[INFO] No attendance recorded.")


if __name__ == "__main__":
    main()
