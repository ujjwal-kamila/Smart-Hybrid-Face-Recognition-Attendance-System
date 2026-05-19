# login.py
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from database import get_credentials_db

class Login:
    def __init__(self, window):
        self.window = window 

        def sign_up():
            from register import Register
            self.new_window = Toplevel(self.window)
            Register(self.new_window)

        frame = Frame(self.window, background="#ffdab9")
        # relx=0.5 and rely=0.5 tell it to go exactly to the 50% mark (the center) of the screen!
        frame.place(relx=0.5, rely=0.5, width=700, height=700, anchor=CENTER)

        try:
            # This opens your image and dynamically resizes it to 150x150 pixels
            raw_image = Image.open("Images\\Makaut_logo.png") # Make sure this matches your exact filename
            resized_image = raw_image.resize((150, 150))
            self.logo = ImageTk.PhotoImage(resized_image)
        except Exception as e:
            print("Logo Error:", e)
            self.logo = None
        
        if self.logo:
            Label(frame, image=self.logo, background="#ffdab9").place(x=30, y=30)
            
        # --- NEW TITLE NEXT TO LOGO ---
        Label(frame, text="Face Recognition Based", background="#ffdab9", font=("Arial", 25, "bold"), fg="black").place(x=190, y=60)
        Label(frame, text="Attendance System", background="#ffdab9", font=("Arial", 22, "bold"), fg="#008080").place(x=190, y=110)
            
        Label(frame, text="Username", background="#ffdab9", font=("aerial", 30, "bold")).place(x=30, y=210)
        Label(frame, text="Password", background="#ffdab9", font=("aerial", 30, "bold")).place(x=30, y=345)

        self.username = Entry(frame, font=("aerial", 30, "bold"), background="#008080", foreground="white")
        self.username.place(x=35, y=270, height=50, width=500)

        self.password = Entry(frame, font=("aerial", 30, "bold"), background="#008080", foreground="white", show="*")
        self.password.place(x=35, y=405, height=50, width=500)

        Button(frame, text="Sign Up", font=("aerial", 15, "bold"), command=sign_up, background="#ffdab9", borderwidth=0, activebackground="#ffdab9", foreground="black").place(x=30, y=540)
        
        login_btn = Button(frame, text="Login", width=7, font=("aerial", 20, "bold"), command=self.login, background="#008080", activebackground="#ffdab9", foreground="white", relief=RAISED, bd=10)
        login_btn.place(x=210, y=475)

        # --- BIND ENTER KEY TO LOGIN ---
        self.window.bind('<Return>', self.trigger_login)

    # Helper function to catch the Enter key event
    def trigger_login(self, event):
        self.login()

    def login(self):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "Please enter Username and Password")
            return
            
        conn = get_credentials_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM details WHERE Email = %s AND Password = %s", (self.username.get(), self.password.get()))
                row = cursor.fetchone()

                if row is not None:
                    self.new_window = Toplevel(self.window)
                    from dashboard import Dashboard  # Lazy import for fast UI
                    self.new = Dashboard(self.new_window)
                    
                    # FIX: When dashboard is closed via standard window close button (X), kill the hidden login window completely
                    self.new_window.protocol("WM_DELETE_WINDOW", self.window.destroy)
                    
                    self.window.withdraw()
                else:
                    messagebox.showerror("Error", "Invalid Username and Password.")
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                conn.close()