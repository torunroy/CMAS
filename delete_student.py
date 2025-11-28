import pandas as pd
import os
import shutil

STUDENTS_FILE = "students.csv"
DATASET_DIR = "dataset"

def delete_student(student_id):
    if not os.path.exists(STUDENTS_FILE):
        print("[ERROR] students.csv not found!")
        return

    df = pd.read_csv(STUDENTS_FILE, dtype=str)

    if student_id not in df["student_id"].values:
        print("[ERROR] Student not found!")
        return

    # Remove row
    df = df[df["student_id"] != student_id]
    df.to_csv(STUDENTS_FILE, index=False)
    print("[INFO] Student info removed from students.csv")

    # Delete dataset folder (face images)
    folder_path = os.path.join(DATASET_DIR, student_id)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print("[INFO] Deleted face images folder:", folder_path)
    else:
        print("[INFO] No image folder found to delete.")

    print("\n[NOTE] After deleting a student, run:")
    print("      Train Face Model (option 3 in main menu).")

def main():
    student_id = input("Enter Student ID to delete: ").strip()
    delete_student(student_id)

if __name__ == "__main__":
    main()
