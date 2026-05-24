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
        # --- ADJUSTED FOOTER ---
        # =========================================================================
        footer_bg = "#e7e1db" 
        
        # Increase height by adding a fixed height or more vertical padding
        footer_frame = Frame(self.window, bg=footer_bg, height=80) 
        footer_frame.pack(side=BOTTOM, fill=X)
        footer_frame.pack_propagate(False) # Prevents the frame from shrinking to fit content

        # Create a container inside the footer to center the items
        center_footer = Frame(footer_frame, bg=footer_bg)
        center_footer.place(relx=0.5, rely=0.5, anchor=CENTER)

        def add_icon(filename, url, label_text=None):
            img_path = os.path.join("Images", "logos", filename)
            try:
                img = Image.open(img_path).resize((25, 25), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Check if URL exists; if not, just use a Label or a non-command Button
                if url:
                    btn = Button(center_footer, image=photo, bg=footer_bg, bd=0, 
                                 activebackground=footer_bg, cursor="hand2",
                                 command=lambda: webbrowser.open_new(url))
                else:
                    btn = Label(center_footer, image=photo, bg=footer_bg)
                
                btn.image = photo
                btn.pack(side=LEFT, padx=(10, 2))
                
                if label_text:
                    Label(center_footer, text=label_text, font=("Times New Roman", 15, "bold"), 
                          bg=footer_bg).pack(side=LEFT, padx=(0, 10))
            except Exception as e:
                print(f"Error loading {filename}: {e}")

        # Adding elements
        add_icon("github.png", "https://github.com/ujjwal-kamila/Smart-Hybrid-Face-Recognition-Attendance-System", "GitHub |")
        # add_icon("linkedin.png", "https://www.linkedin.com/in/ujjwal-kamila/", "LinkedIn |")
        # # Replace the text label with this logic:
        # --- MADE WITH SECTION ---
        Label(center_footer, text="Made with", font=("Times New Roman", 15, "bold"), 
              bg=footer_bg).pack(side=LEFT, padx=(10, 5))
        
        # Add the heart icon (ensure heart.png is in your Images/logos folder)
        add_icon("love.png","") 
        
        # Text before the link
        Label(center_footer, text="by", font=("Times New Roman", 15, "bold"), 
              bg=footer_bg).pack(side=LEFT, padx=5)

        # CLICKABLE NAME: Replaces the static Label with a Button
        btn_name = Button(center_footer, text="Ujjwal Kamila", font=("Times New Roman", 15, "bold"),
                          bg=footer_bg, fg="black", activebackground=footer_bg,
                          bd=0, cursor="hand2",
                          command=lambda: webbrowser.open_new("https://ujjwal-kamila.vercel.app/"))
        btn_name.pack(side=LEFT)

        # Remaining part of the line
        Label(center_footer, text="| © 2026", font=("Times New Roman", 15, "bold"), 
              bg=footer_bg).pack(side=LEFT, padx=(5, 10))
        
        # add_icon("web.png", "https://ujjwal-kamila.vercel.app/")
        # add_icon("global.png", "https://leetcode.com/u/ujjwalkamila/")

    def close(self):
        self.window.destroy()

    def open_img(self):
        os.makedirs("Faces", exist_ok=True)
        os.startfile("Faces")