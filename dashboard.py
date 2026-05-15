# dashboard.py
from tkinter import *
import os
import threading

class Dashboard:
    def __init__(self, window):
        self.window = window
        self.window.title("Dashboard")
        self.window.geometry("1540x800+-10+0")
        self.window.configure(background="#008080")

        def student():
            from student import Student
            self.new_window = Toplevel(self.window)
            Student(self.new_window)

        def attendance():
            from attendance import Attendance
            self.new_window = Toplevel(self.window)
            Attendance(self.new_window)
            
        def run_train():
            from train import train_hybrid_model
            threading.Thread(target=train_hybrid_model, daemon=True).start()
            
        def run_recognition():
            from face_recognition import start_recognition
            threading.Thread(target=start_recognition, daemon=True).start()

        try:
            self.boy = PhotoImage(file=os.path.join("Images", "12.png"))
            self.face = PhotoImage(file=os.path.join("Images", "Face2.png"))
            self.atten = PhotoImage(file=os.path.join("Images", "Attendance.png"))
            self.group = PhotoImage(file=os.path.join("Images", "Group.png"))
            self.exi = PhotoImage(file=os.path.join("Images", "EXIT.png"))
            self.trai = PhotoImage(file=os.path.join("Images", "5.png"))
        except:
            self.boy = self.face = self.atten = self.group = self.exi = self.trai = None

        Button(self.window, font=("Arial", 20, "bold"), text="Student Details", image=self.boy, background="#ffdab9", compound=TOP, height=250, width=240, relief=RAISED, borderwidth=6, activebackground="#fa8072", command=student).place(x=220, y=100)
        Button(self.window, font=("aerial", 20, "bold"), text="Face Recognition", image=self.face, background="#ffdab9", compound=TOP, height=250, width=240, relief=RAISED, borderwidth=6, activebackground="#fa8072", command=run_recognition).place(x=1060, y=100)
        Button(self.window, font=("aerial", 20, "bold"), text="Attendance", image=self.atten, background="#ffdab9", compound=TOP, height=250, width=240, relief=RAISED, borderwidth=6, activebackground="#fa8072", command=attendance).place(x=640, y=100)
        Button(self.window, command=self.open_img, font=("aerial", 20, "bold"), text="Face Samples", image=self.group, background="#ffdab9", compound=TOP, height=250, width=240, relief=RAISED, borderwidth=6, activebackground="#fa8072").place(x=640, y=440)
        Button(self.window, font=("aerial", 20, "bold"), text="Exit", background="#ffdab9", image=self.exi, compound=TOP, height=250, width=240, relief=RAISED, borderwidth=6, command=self.close, activebackground="#fa8072").place(x=1060, y=440)
        Button(self.window, font=("aerial", 20, "bold"), text="Train Data", background="#ffdab9", image=self.trai, compound=TOP, height=250, width=240, relief=RAISED, borderwidth=6, command=run_train, activebackground="#fa8072").place(x=220, y=440)

    def close(self):
        self.window.destroy()

    def open_img(self):
        os.makedirs("Faces", exist_ok=True)
        os.startfile("Faces")