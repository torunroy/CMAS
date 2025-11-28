# CMAS
A complete AI-based Face Recognition  Classs Monitoring & Attendance System with Tkinter GUI, OpenCV, Face Dataset Handling, Student Management, and Excel Attendance Export.
This project is designed for schools, colleges, coaching centers, or any classroom where automated attendance and student data management is needed.

###Features###

##Student Management System

-Add/Register new student

-Webcam face capture

-Upload photos instead of webcam

-Edit student details

-Delete student

-Add new face images to an existing student

-Replace all photos of a student

-All student data stored in students.csv

---------------------------------------------------------------------------------------------------------
##View Section

-View Students List

-Search by ID / Name

-Double-click to edit student

-View CSV files

-View Attendance Excel files

-Search by ID / Name
---------------------------------------------------------------------------------------------------------
##Attendance System

-Real-time Face Recognition

-Press ‘q’ to stop taking attendance

-Automatically generates Excel file:

-Attendance_YYYY-MM-DD_HH-MM-SS.xlsx

->Includes:

-Student ID

-Roll

-Reg. No

-Name

-Email

-Status (Present/Absent)
------------------------------------------------------------------------------------------------------

##Model Training

-Comprehensive face dataset training

-LBPH Face Recognizer (OpenCV)

-Re-train model anytime after adding/removing students

-------------------------------------------------------------------------------------------------------

##Graphical User Interface (GUI)

->Built with Tkinter featuring:


-Student menu

-View menu

-Back buttons in all sub-pages

-Non-freezing threading system

Clean, modern, easy-to-use layout

-------------------------------------------------------------------------------------------------------

📁 CMAS

│
├── gui.py                                # Main Tkinter GUI

├── capture_faces.py                 # Registration (webcam / upload)

├── attendance_system.py             # Attendance + Attentiveness detection

├── train_model.py                   # Train face recognition model (LBPH)

├── delete_student.py                # Remove student & dataset folder

├── edit_student.py                  # Edit student info


├── students.csv                     # Student info database (auto created)

├── face_model.yml                   # Trained LBPH face recognizer (auto)

├── haarcascade_frontalface_default.xml   # Haar Cascade for face detection



📁 dataset/  

  └── <student_id>/
  
   └── 1.jpg, 2.jpg, ...
  

📁 attendance/                      

  └── Attendance_2025-02-14_10-30.xlsx

----------------------------------------------------------------------------------------------------------
## Requirements
Install dependencies:
pip install opencv-python
pip install numpy
pip install pandas
pip install pillow
pip install tk
pip install openpyxl
----------------------------------------------------------------------------------------------------------
##How to Run


(create virtual enviroment used python version 3.12 > nedded)

-python -m venv  (v_e name)

-(v_e name)\Scripts\activated

1. Start the GUI
   
->python gui.py

3. Add Students
   
Use webcam or Upload multiple face photos

5. Train Model
   
Click "Train Model" after adding students.

7. Take Attendance

Click "Take Attendance"
Press ‘q’ to stop.

5. View Attendance

Open attendance Excel from GUI.
