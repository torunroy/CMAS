import cv2
import os
import numpy as np

DATASET_DIR = "dataset"
MODEL_PATH = "face_model.yml"
CASCADE_PATH = "haarcascade_frontalface_default.xml"
LABELS_PATH = "labels.txt"

def get_images_and_labels(dataset_dir):
    face_samples = []
    ids = []
    labels_map = {}
    current_id = 0

    #student_id
    for folder in os.listdir(dataset_dir):
        folder_path = os.path.join(dataset_dir, folder)
        if not os.path.isdir(folder_path):
            continue

        
        label_id = current_id
        labels_map[label_id] = folder 
        current_id += 1

        for img_name in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue

            face_samples.append(img)
            ids.append(label_id)

    return face_samples, np.array(ids), labels_map

def main():
    print("[INFO] Training model...")
    faces, ids, labels_map = get_images_and_labels(DATASET_DIR)

    if len(faces) == 0:
        print("[ERROR] No face images found. Capture faces first.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, ids)
    recognizer.write(MODEL_PATH)

    # labels map
    with open(LABELS_PATH, "w", encoding="utf-8") as f:
        for label_id, student_id in labels_map.items():
            f.write(f"{label_id},{student_id}\n")

    print("[INFO] Model trained and saved to", MODEL_PATH)

if __name__ == "__main__":
    main()
