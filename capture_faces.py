import cv2
import os
import csv
import shutil

DATASET_DIR = "dataset"
CASCADE_PATH = "haarcascade_frontalface_default.xml"
SAMPLES_PER_STUDENT = 50
STUDENTS_FILE = "students.csv"


def make_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def save_student_info(student_id, roll, reg_no, name, email, folder_name):
    file_exists = os.path.isfile(STUDENTS_FILE)

    with open(STUDENTS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(
                ["student_id", "roll", "registration_no", "name", "email", "folder_name"]
            )
        writer.writerow([student_id, roll, reg_no, name, email, folder_name])


#Webcam capture
def register_student_webcam(student_id, roll, reg_no, name, email, gui_confirm=None):
    folder_name = student_id
    save_path = os.path.join(DATASET_DIR, folder_name)

    if os.path.isdir(save_path):
        shutil.rmtree(save_path)
    make_dir(save_path)

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    cap = cv2.VideoCapture(0)
    count = 0

    print("[INFO] Webcam Started")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Camera error.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]
            cv2.imwrite(os.path.join(save_path, f"{count}.jpg"), face_img)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, f"{count}", (x, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.imshow("Capture - Press q to stop", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        if count >= SAMPLES_PER_STUDENT:
            break

    cap.release()
    cv2.destroyAllWindows()

    if count == 0:
        print("[WARN] No images captured.")
        shutil.rmtree(save_path)
        return

    save_student_info(student_id, roll, reg_no, name, email, folder_name)
    print(f"[INFO] Saved {count} webcam images.")


#Register student by Upload
def register_student_from_files(student_id, roll, reg_no, name, email, image_paths):
    folder_name = student_id
    save_path = os.path.join(DATASET_DIR, folder_name)

    if os.path.isdir(save_path):
        shutil.rmtree(save_path)
    make_dir(save_path)

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    count = 0

    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            continue

        x, y, w, h = faces[0]
        face_img = gray[y:y+h, x:x+w]

        count += 1
        cv2.imwrite(os.path.join(save_path, f"{count}.jpg"), face_img)

    if count == 0:
        print("[WARN] No valid photos found")
        shutil.rmtree(save_path)
        return

    save_student_info(student_id, roll, reg_no, name, email, folder_name)
    print(f"[INFO] Saved {count} uploaded photos.")


#Add photos
def add_photos_to_student(student_id, image_paths):
    folder = os.path.join(DATASET_DIR, student_id)
    make_dir(folder)

    existing = len([f for f in os.listdir(folder) if f.endswith(".jpg")])
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

    count = existing

    for img_path in image_paths:
        img = cv2.imread(img_path)
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            continue

        x, y, w, h = faces[0]
        face = gray[y:y+h, x:x+w]

        count += 1
        cv2.imwrite(os.path.join(folder, f"{count}.jpg"), face)

    print("[INFO] New photos added.")


# Replace photos
def replace_photos_for_student(student_id, image_paths):
    folder = os.path.join(DATASET_DIR, student_id)

    if os.path.isdir(folder):
        shutil.rmtree(folder)
    make_dir(folder)

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    count = 0

    for img_path in image_paths:
        img = cv2.imread(img_path)
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            continue

        x, y, w, h = faces[0]
        face = gray[y:y+h, x:x+w]

        count += 1
        cv2.imwrite(os.path.join(folder, f"{count}.jpg"), face)

    print("[INFO] Photos replaced successfully.")
