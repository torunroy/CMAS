import os
import pandas as pd

STUDENTS_FILE = "students.csv"


def edit_student(student_id: str,
                 new_name: str | None = None,
                 new_roll: str | None = None,
                 new_reg: str | None = None,
                 new_email: str | None = None) -> bool:

    if not os.path.exists(STUDENTS_FILE):
        print("[ERROR] students.csv not found!")
        return False

    # Load CSV
    df = pd.read_csv(STUDENTS_FILE, dtype=str)

    if "student_id" not in df.columns:
        print("[ERROR] 'student_id' column not found in students.csv!")
        return False

    if student_id not in df["student_id"].values:
        print(f"[ERROR] Student ID '{student_id}' not found!")
        return False

    # Find row index
    idx = df.index[df["student_id"] == student_id][0]

    # Update fields if provided
    if new_name is not None:
        df.at[idx, "name"] = new_name

    if new_roll is not None:
        if "roll" in df.columns:
            df.at[idx, "roll"] = new_roll
        else:
            print("[WARN] 'roll' column not found, skipping roll update.")

    if new_reg is not None:
        if "registration_no" in df.columns:
            df.at[idx, "registration_no"] = new_reg
        else:
            print("[WARN] 'registration_no' column not found, skipping reg update.")

    if new_email is not None:
        if "email" in df.columns:
            df.at[idx, "email"] = new_email
        else:
            print("[WARN] 'email' column not found, skipping email update.")

    # Save back to CSV
    df.to_csv(STUDENTS_FILE, index=False, encoding="utf-8")
    print(f"[INFO] Student '{student_id}' updated successfully.")
    return True


def main():
    print("=== Edit Student (Console Mode) ===")
    student_id = input("Student ID to edit: ").strip()
    if not student_id:
        print("[ERROR] Student ID is required.")
        return

    name = input("New Name (blank = no change): ").strip() or None
    roll = input("New Roll (blank = no change): ").strip() or None
    reg = input("New Registration No (blank = no change): ").strip() or None
    email = input("New Email (blank = no change): ").strip() or None

    ok = edit_student(student_id, name, roll, reg, email)
    if ok:
        print("[INFO] Done.")
    else:
        print("[ERROR] Failed to update.")


if __name__ == "__main__":
    main()
