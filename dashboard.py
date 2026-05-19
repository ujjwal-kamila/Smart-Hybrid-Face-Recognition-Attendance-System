# dashboard.py
from tkinter import *
import os
import threading
import webbrowser
from PIL import Image, ImageTk

class Dashboard:
    def __init__(self, window):
        self.window = window
        self.window.title("Dashboard")
        self.window.geometry("1540x800+-10+0")
        self.window.configure(background="#008080")
        
        # Maximize the window automatically
        self.window.state('zoomed') 

        # =========================================================================
        # --- TITLE ADDED HERE (Now with White Bar and Black Text) ---
        # =========================================================================
        title_lbl = Label(self.window, text="FACE RECOGNITION ATTENDANCE SYSTEM", font=("Times New Roman", 35, "bold"), bg="#e7e1db", fg="black")
        title_lbl.pack(side=TOP, fill=X, pady=(0, 0))

        # --- MAIN CENTERED CONTAINER ---
        # This acts as an invisible box that holds all buttons in the exact center of the screen
        main_frame = Frame(self.window, bg="#008080")
        main_frame.place(relx=0.5, rely=0.48, anchor=CENTER) 

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

        def load_image(filename, width=210, height=200):
            try:
                img_path = os.path.join("Images", filename)
                img = Image.open(img_path)
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                return None 

        # --- LOAD ORIGINAL IMAGES --- 
        self.boy = load_image("12.png")
        self.atten = load_image("Attendance.png")
        self.face = load_image("Face2.png")
        self.trai = load_image("5.png")
        self.group = load_image("Group.png")
        self.exi = load_image("EXIT.png") 

        # --- BUTTONS IN A GRID ---
        btn_bg = "#ffdab9"
        btn_font = ("Times New Roman", 20, "bold")
        btn_border = 2 # Reduced the borders as requested to make it cleaner!
        
        # Row 0 (Top Row)
        btn_student = Button(main_frame, font=btn_font, text="Student Details", image=self.boy, background=btn_bg, compound=TOP, height=240, width=240, relief=RAISED, borderwidth=btn_border, activebackground="#fa8072", command=student)
        btn_student.grid(row=0, column=0, padx=40, pady=30)
        
        btn_attendance = Button(main_frame, font=btn_font, text="Attendance", image=self.atten, background=btn_bg, compound=TOP, height=240, width=240, relief=RAISED, borderwidth=btn_border, activebackground="#fa8072", command=attendance)
        btn_attendance.grid(row=0, column=1, padx=40, pady=30)
        
        btn_recognition = Button(main_frame, font=btn_font, text="Face Recognition", image=self.face, background=btn_bg, compound=TOP, height=240, width=240, relief=RAISED, borderwidth=btn_border, activebackground="#fa8072", command=run_recognition)
        btn_recognition.grid(row=0, column=2, padx=40, pady=30)

        # Row 1 (Bottom Row)
        btn_train = Button(main_frame, font=btn_font, text="Train Data", image=self.trai, background=btn_bg, compound=TOP, height=240, width=240, relief=RAISED, borderwidth=btn_border, activebackground="#fa8072", command=run_train)
        btn_train.grid(row=1, column=0, padx=40, pady=30)

        btn_samples = Button(main_frame, font=btn_font, text="Face Samples", image=self.group, background=btn_bg, compound=TOP, height=240, width=240, relief=RAISED, borderwidth=btn_border, activebackground="#fa8072", command=self.open_img)
        btn_samples.grid(row=1, column=1, padx=40, pady=30)

        btn_exit = Button(main_frame, font=btn_font, text="Exit", image=self.exi, background=btn_bg, compound=TOP, height=240, width=240, relief=RAISED, borderwidth=btn_border, activebackground="#fa8072", command=self.close)
        btn_exit.grid(row=1, column=2, padx=40, pady=30)

        # =========================================================================
        # --- SINGLE LINE FOOTER ---
        # =========================================================================
        footer_bg = "#e7e1db" 
        footer_font = ("Times New Roman", 15, "bold")
        
        footer_frame = Frame(self.window, bg=footer_bg)
        footer_frame.pack(side=BOTTOM, fill=X)

        # Center container for the single line
        center_footer = Frame(footer_frame, bg=footer_bg)
        center_footer.pack(pady=15) # Creates perfect vertical spacing

        # 1. GitHub (Changed fg to black)
        gh_lbl = Label(center_footer, text="github GitHub", font=footer_font, bg=footer_bg, fg="black", cursor="hand2")
        gh_lbl.pack(side=LEFT, padx=5)
        gh_lbl.bind("<Enter>", lambda e: gh_lbl.config(fg="#00ced1")) 
        gh_lbl.bind("<Leave>", lambda e: gh_lbl.config(fg="black")) # Changed leave color back to black
        gh_lbl.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/ujjwal-kamila"))

        # Separator (Changed fg to black)
        Label(center_footer, text=" | ", font=footer_font, bg=footer_bg, fg="black").pack(side=LEFT)

        # 2. Made with Love (Changed fg to black)
        Label(center_footer, text="Made with ❤️ by ", font=footer_font, bg=footer_bg, fg="black").pack(side=LEFT)
        
        # Clickable Name (Changed fg to black)
        name_lbl = Label(center_footer, text="Ujjwal Kamila", font=footer_font, bg=footer_bg, fg="black", cursor="hand2")
        name_lbl.pack(side=LEFT)
        name_lbl.bind("<Enter>", lambda e: name_lbl.config(fg="#00ced1")) # Added teal hover effect here too
        name_lbl.bind("<Leave>", lambda e: name_lbl.config(fg="black")) # Changed leave color back to black
        name_lbl.bind("<Button-1>", lambda e: webbrowser.open_new("https://ujjwal-kamila.vercel.app/"))
        
        # 3. Copyright (Changed fg to black)
        Label(center_footer, text=" | © 2026", font=footer_font, bg=footer_bg, fg="black").pack(side=LEFT)

    def close(self):
        self.window.destroy()

    def open_img(self):
        os.makedirs("Faces", exist_ok=True)
        os.startfile("Faces")