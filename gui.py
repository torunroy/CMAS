import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
import threading
import os
import pandas as pd

import capture_faces
import edit_student
import delete_student
import train_model
import attendance_system

def run_in_thread(target, *args, **kwargs):
    t = threading.Thread(target=target, args=args, kwargs=kwargs)
    t.daemon = True
    t.start()


#Add Student
def add_student_gui():
    form = tk.Toplevel()
    form.title("Add / Register Student")
    form.geometry("430x360")
    form.resizable(False, False)

    frame = tk.Frame(form, padx=15, pady=15)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Student ID *").grid(row=0, column=0, sticky="w", pady=3)
    entry_id = tk.Entry(frame, width=30)
    entry_id.grid(row=0, column=1, pady=3)

    tk.Label(frame, text="Roll").grid(row=1, column=0, sticky="w", pady=3)
    entry_roll = tk.Entry(frame, width=30)
    entry_roll.grid(row=1, column=1, pady=3)

    tk.Label(frame, text="Registration No").grid(row=2, column=0, sticky="w", pady=3)
    entry_reg = tk.Entry(frame, width=30)
    entry_reg.grid(row=2, column=1, pady=3)

    tk.Label(frame, text="Name").grid(row=3, column=0, sticky="w", pady=3)
    entry_name = tk.Entry(frame, width=30)
    entry_name.grid(row=3, column=1, pady=3)

    tk.Label(frame, text="Email").grid(row=4, column=0, sticky="w", pady=3)
    entry_email = tk.Entry(frame, width=30)
    entry_email.grid(row=4, column=1, pady=3)

    tk.Label(frame, text="Choose one option: Webcam or Upload Photos").grid(
        row=5, column=0, columnspan=2, pady=10
    )

    def get_fields():
        student_id = entry_id.get().strip()
        roll = entry_roll.get().strip()
        reg_no = entry_reg.get().strip()
        name = entry_name.get().strip()
        email = entry_email.get().strip()

        if not student_id:
            messagebox.showerror("Error", "Student ID is required.")
            return None
        return student_id, roll, reg_no, name, email

    def start_webcam():
        fields = get_fields()
        if not fields:
            return
        student_id, roll, reg_no, name, email = fields
        form.destroy()

        def _run():
            try:
                capture_faces.register_student_webcam(
                    student_id,
                    roll,
                    reg_no,
                    name,
                    email,
                    gui_confirm=lambda t, m: messagebox.askyesno(t, m),
                )
                messagebox.showinfo("Done", f"Student {student_id} registered (webcam).")
            except Exception as e:
                messagebox.showerror("Error", f"Error (webcam):\n{e}")

        run_in_thread(_run)

    def start_upload():
        fields = get_fields()
        if not fields:
            return
        student_id, roll, reg_no, name, email = fields

        image_paths = filedialog.askopenfilenames(
            title="Select face images",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")],
        )
        if not image_paths:
            return

        form.destroy()

        def _run():
            try:
                capture_faces.register_student_from_files(
                    student_id, roll, reg_no, name, email, list(image_paths)
                )
                messagebox.showinfo("Done", f"Student {student_id} registered (upload).")
            except Exception as e:
                messagebox.showerror("Error", f"Error (upload):\n{e}")

        run_in_thread(_run)

    tk.Button(frame, text="📷 Use Webcam", width=20, command=start_webcam).grid(
        row=6, column=0, pady=10
    )
    tk.Button(frame, text="🖼 Upload Photos", width=20, command=start_upload).grid(
        row=6, column=1, pady=10
    )

    tk.Button(frame, text="⬅ Back", width=20, command=form.destroy).grid(
        row=7, column=0, columnspan=2, pady=(5, 0)
    )


#Delete Student
def delete_student_gui():
    student_id = simpledialog.askstring("Delete Student", "Enter Student ID to delete:")
    if not student_id:
        return

    def _delete():
        try:
            delete_student.delete_student(student_id.strip())
            messagebox.showinfo(
                "Done",
                f"Student {student_id} deleted (if existed).\n"
                "Don't forget to Train Face Model again.",
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error while deleting:\n{e}")

    run_in_thread(_delete)


#Edit Student GUI
def edit_student_gui(student_id=None):
    if student_id is None:
        student_id = simpledialog.askstring("Edit Student", "Enter Student ID to edit:")

    if not student_id:
        return

    if not os.path.exists("students.csv"):
        messagebox.showerror("Error", "students.csv not found!")
        return

    df = pd.read_csv("students.csv", dtype=str)

    if student_id not in df["student_id"].values:
        messagebox.showerror("Error", "Student ID not found!")
        return

    data = df[df["student_id"] == student_id].iloc[0]

    form = tk.Toplevel()
    form.title(f"Edit Student - {student_id}")
    form.geometry("400x320")
    form.resizable(False, False)

    frame = tk.Frame(form, padx=15, pady=15)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Name").grid(row=0, column=0, sticky="w", pady=3)
    entry_name = tk.Entry(frame, width=30)
    entry_name.insert(0, data.get("name", ""))
    entry_name.grid(row=0, column=1, pady=3)

    tk.Label(frame, text="Roll").grid(row=1, column=0, sticky="w", pady=3)
    entry_roll = tk.Entry(frame, width=30)
    entry_roll.insert(0, data.get("roll", ""))
    entry_roll.grid(row=1, column=1, pady=3)

    tk.Label(frame, text="Registration No").grid(row=2, column=0, sticky="w", pady=3)
    entry_reg = tk.Entry(frame, width=30)
    entry_reg.insert(0, data.get("registration_no", ""))
    entry_reg.grid(row=2, column=1, pady=3)

    tk.Label(frame, text="Email").grid(row=3, column=0, sticky="w", pady=3)
    entry_email = tk.Entry(frame, width=30)
    entry_email.insert(0, data.get("email", ""))
    entry_email.grid(row=3, column=1, pady=3)

    def save_changes():
        new_name = entry_name.get().strip() or None
        new_roll = entry_roll.get().strip() or None
        new_reg = entry_reg.get().strip() or None
        new_email = entry_email.get().strip() or None

        try:
            edit_student.edit_student(
                student_id, new_name, new_roll, new_reg, new_email
            )
            messagebox.showinfo("Success", "Student details updated.")
            form.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Update failed:\n{e}")

    tk.Button(frame, text="Save Changes", width=25, command=save_changes).grid(
        row=4, column=0, columnspan=2, pady=15
    )

    tk.Button(frame, text="⬅ Back", width=25, command=form.destroy).grid(
        row=5, column=0, columnspan=2, pady=(0, 5)
    )


#View Students
def view_students_gui():
    if not os.path.exists("students.csv"):
        messagebox.showerror("Error", "students.csv not found!")
        return

    df = pd.read_csv("students.csv", dtype=str)
    original_df = df.copy()

    win = tk.Toplevel()
    win.title("Students List")
    win.geometry("750x480")

    top_frame = tk.Frame(win, padx=10, pady=5)
    top_frame.pack(fill="x")

    tk.Label(top_frame, text="Search:").pack(side="left")

    search_var = tk.StringVar()
    entry_search = tk.Entry(top_frame, textvariable=search_var, width=25)
    entry_search.pack(side="left", padx=5)

    tk.Label(top_frame, text="By:").pack(side="left", padx=(15, 0))

    search_by_var = tk.StringVar(value="student_id")
    combo = ttk.Combobox(
        top_frame,
        textvariable=search_by_var,
        values=["student_id", "name"],
        state="readonly",
        width=12,
    )
    combo.pack(side="left", padx=5)

    list_frame = tk.Frame(win)
    list_frame.pack(fill="both", expand=True, padx=10, pady=5)

    columns = list(df.columns)

    tree = ttk.Treeview(list_frame, columns=columns, show="headings")
    vsb = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    list_frame.rowconfigure(0, weight=1)
    list_frame.columnconfigure(0, weight=1)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, stretch=True)

    def load_rows(dataframe):
        tree.delete(*tree.get_children())
        for _, row in dataframe.iterrows():
            tree.insert("", "end", values=list(row.values))

    load_rows(df)

    def apply_search(*args):
        text = search_var.get().strip().lower()
        by = search_by_var.get()

        if text == "":
            load_rows(original_df)
            return

        mask = original_df[by].astype(str).str.lower().str.contains(text)
        load_rows(original_df[mask])

    search_var.trace_add("write", apply_search)

    def on_row_double_click(event):
        selected = tree.selection()
        if not selected:
            return
        values = tree.item(selected[0], "values")
        sid = values[0]  
        edit_student_gui(sid)

    tree.bind("<Double-1>", on_row_double_click)

    bottom = tk.Frame(win, padx=10, pady=5)
    bottom.pack(fill="x")
    tk.Button(bottom, text="⬅ Back", width=15, command=win.destroy).pack(anchor="e")


#CSV View
def csv_viewer_gui():
    file_path = filedialog.askopenfilename(
        title="Open CSV file", filetypes=[("CSV files", "*.csv")]
    )
    if not file_path:
        return

    try:
        df = pd.read_csv(file_path, dtype=str)
    except Exception as e:
        messagebox.showerror("Error", f"Could not read CSV:\n{e}")
        return

    view = tk.Toplevel()
    view.title(f"CSV Viewer - {os.path.basename(file_path)}")
    view.geometry("800x480")

    frame = tk.Frame(view)
    frame.pack(fill="both", expand=True)

    columns = list(df.columns)

    tree = ttk.Treeview(frame, columns=columns, show="headings")
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130)

    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row.values))

    bottom = tk.Frame(view, padx=10, pady=5)
    bottom.pack(fill="x")
    tk.Button(bottom, text="⬅ Back", width=15, command=view.destroy).pack(anchor="e")


#Replace Student Photos
def edit_student_photos_gui():
    student_id = simpledialog.askstring("Edit Photos", "Enter Student ID:")
    if not student_id:
        return

    files = filedialog.askopenfilenames(
        title="Select NEW photos",
        filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")]
    )
    if not files:
        return

    confirm = messagebox.askyesno(
        "Confirm",
        f"Replace ALL existing photos of {student_id}?"
    )
    if not confirm:
        return

    def _run():
        try:
            capture_faces.replace_photos_for_student(student_id, list(files))
            messagebox.showinfo("Success", "Photos replaced successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    run_in_thread(_run)


#Add Photos to Existing Student
def add_photos_existing_student_gui():
    student_id = simpledialog.askstring("Add Photos", "Enter Student ID:")
    if not student_id:
        return

    files = filedialog.askopenfilenames(
        title="Select photos to ADD",
        filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")]
    )
    if not files:
        return

    def _run():
        try:
            capture_faces.add_photos_to_student(student_id, list(files))
            messagebox.showinfo("Success", "Photos added successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    run_in_thread(_run)


#View Attendance
def view_attendance_gui():
    file_path = filedialog.askopenfilename(
        title="Open Attendance File",
        filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
    )
    if not file_path:
        return

    try:
        df = pd.read_excel(file_path, dtype=str)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file:\n{e}")
        return

    original_df = df.copy()

    win = tk.Toplevel()
    win.title(f"Attendance - {os.path.basename(file_path)}")
    win.geometry("850x520")

    top_frame = tk.Frame(win, padx=10, pady=5)
    top_frame.pack(fill="x")

    tk.Label(top_frame, text="Search:").pack(side="left")

    search_var = tk.StringVar()
    entry_search = tk.Entry(top_frame, textvariable=search_var, width=25)
    entry_search.pack(side="left", padx=5)

    possible_cols = ["Student ID", "Name"]
    available_cols = [c for c in possible_cols if c in df.columns]
    if not available_cols:
        available_cols = list(df.columns[:3])

    tk.Label(top_frame, text="By:").pack(side="left", padx=(15, 0))

    search_by_var = tk.StringVar(value=available_cols[0])
    combo = ttk.Combobox(
        top_frame,
        textvariable=search_by_var,
        values=available_cols,
        width=15,
        state="readonly"
    )
    combo.pack(side="left", padx=5)

    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True)

    columns = list(df.columns)

    tree = ttk.Treeview(frame, columns=columns, show="headings")
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130)

    def load_rows(dataframe):
        tree.delete(*tree.get_children())
        for _, row in dataframe.iterrows():
            tree.insert("", "end", values=list(row.values))

    load_rows(df)

    def apply_search(*args):
        text = search_var.get().lower().strip()
        col = search_by_var.get()

        if text == "":
            load_rows(original_df)
            return

        mask = original_df[col].astype(str).str.lower().str.contains(text)
        load_rows(original_df[mask])

    search_var.trace_add("write", apply_search)

    bottom = tk.Frame(win, padx=10, pady=5)
    bottom.pack(fill="x")
    tk.Button(bottom, text="⬅ Back", width=15, command=win.destroy).pack(anchor="e")


#Train Model
def train_model_gui():
    def _run():
        try:
            train_model.main()
            messagebox.showinfo("Success", "Model training completed.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    run_in_thread(_run)


#Take Attendance
def take_attendance_gui():
    confirm = messagebox.askyesno(
        "Start Attendance",
        "This will open webcam for attendance.\nPress 'q' to stop.\nContinue?"
    )
    if not confirm:
        return

    def _run():
        try:
            attendance_system.main()
            messagebox.showinfo("Done", "Attendance completed. Check Excel file.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    run_in_thread(_run)


#Student MENU
def student_menu_gui():
    win = tk.Toplevel()
    win.title("Student Management")
    win.geometry("380x360")
    win.resizable(False, False)

    frame = tk.Frame(win, padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Student Management", font=("Segoe UI", 14, "bold")).pack(pady=(0, 15))

    tk.Button(frame, text="Add / Register Student", width=30, command=add_student_gui).pack(pady=4)
    tk.Button(frame, text="Edit Student Details", width=30, command=edit_student_gui).pack(pady=4)
    tk.Button(frame, text="Delete Student", width=30, command=delete_student_gui).pack(pady=4)
    tk.Button(frame, text="Replace Student Photos", width=30, command=edit_student_photos_gui).pack(pady=4)
    tk.Button(frame, text="Add Photos to Student", width=30, command=add_photos_existing_student_gui).pack(pady=4)

    tk.Button(frame, text="⬅ Back", width=30, command=win.destroy).pack(pady=(10, 0))


#View MENU
def view_menu_gui():
    win = tk.Toplevel()
    win.title("View Data")
    win.geometry("380x300")
    win.resizable(False, False)

    frame = tk.Frame(win, padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="View Data", font=("Segoe UI", 14, "bold")).pack(pady=(0, 15))

    tk.Button(frame, text="Attendance File", width=30, command=view_attendance_gui).pack(pady=4)
    tk.Button(frame, text="CSV File", width=30, command=csv_viewer_gui).pack(pady=4)
    tk.Button(frame, text="Students List", width=30, command=view_students_gui).pack(pady=4)

    tk.Button(frame, text="⬅ Back", width=30, command=win.destroy).pack(pady=(10, 0))


#MAIN WINDOW
def main():
    root = tk.Tk()
    root.title("UI")
    root.geometry("420x420")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame, text="CMAS", font=("Segoe UI", 17, "bold")
    ).pack(pady=(0, 5))

    tk.Label(
        frame, text="AI Based Class Monitoring & Attendence System", font=("Segoe UI", 9)
    ).pack(pady=(0, 20))

    tk.Button(
        frame,
        text="Student",
        width=30,
        height=2,
        command=student_menu_gui
    ).pack(pady=8)

    tk.Button(
        frame,
        text="View",
        width=30,
        height=2,
        command=view_menu_gui
    ).pack(pady=8)

    tk.Label(frame, text="", pady=5).pack()  # spacer

    tk.Button(
        frame, text=" Train Model", width=30, command=train_model_gui
    ).pack(pady=4)

    tk.Button(
        frame, text="Take Attendance", width=30, command=take_attendance_gui
    ).pack(pady=4)

    tk.Button(
        frame, text="Exit", width=30, command=root.destroy
    ).pack(pady=12)

    root.mainloop()


if __name__ == "__main__":
    main()
