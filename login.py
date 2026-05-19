# login.py
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from database import get_credentials_db
import smtplib
from email.mime.text import MIMEText

class Login:
    def __init__(self, window):
        self.window = window 

        # Main Centered Frame
        frame = Frame(self.window, background="#ffdab9", padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, width=600, height=700, anchor=CENTER)

        # Logo Section
        try:
            raw_image = Image.open("Images\\Makaut_logo.png")
            resized_image = raw_image.resize((120, 120))
            self.logo = ImageTk.PhotoImage(resized_image)
            Label(frame, image=self.logo, background="#ffdab9").pack(pady=(0, 20))
        except:
            pass
            
        # Title
        Label(frame, text="Face Recognition Based", background="#ffdab9", font=("Times New Roman", 24, "bold"), fg="black").pack()
        Label(frame, text="Attendance System", background="#ffdab9", font=("Times New Roman", 22, "bold"), fg="#008080").pack(pady=(0, 30))
            
        # Input Fields
        font_style = ("Times New Roman", 18, "bold")
        
        Label(frame, text="Username", background="#ffdab9", font=font_style).pack(anchor=W)
        self.username = Entry(frame, font=font_style, background="#008080", foreground="white")
        self.username.pack(fill=X, pady=(5, 20), ipady=5)

        Label(frame, text="Password", background="#ffdab9", font=font_style).pack(anchor=W)
        self.password = Entry(frame, font=font_style, background="#008080", foreground="white", show="*")
        self.password.pack(fill=X, pady=(5, 5), ipady=5)

        # Forgot Password Link
        Button(frame, text="Forgot Password?", font=("Times New Roman", 12, "bold", "underline"), command=self.forgot_password, 
               background="#ffdab9", borderwidth=0, activebackground="#ffdab9", fg="blue", cursor="hand2").pack(anchor=E, pady=(20, 20))

        # --- MOVED BUTTONS DOWN ---
        # Added a spacer frame to push buttons further down
        Spacer = Frame(frame, height=20, background="#ffdab9").pack()
        
        btn_frame = Frame(frame, background="#ffdab9")
        btn_frame.pack(fill=X, pady=20) # Increased pady to move them down
        
        Button(btn_frame, text="Login", font=("Times New Roman", 18, "bold"), command=self.login, 
               background="#008080", foreground="white", relief=RAISED, bd=3, width=15).pack(side=LEFT, padx=10)
        
        Button(btn_frame, text="Sign Up", font=("Times New Roman", 18, "bold"), command=self.sign_up, 
               background="#ffdab9", relief=RAISED, bd=3, width=15).pack(side=LEFT, padx=10)

        self.window.bind('<Return>', self.trigger_login)

    # Moved sign_up out of __init__ to be a class method
    def sign_up(self):
        from register import Register
        self.new_window = Toplevel(self.window)
        Register(self.new_window)

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
                    from dashboard import Dashboard
                    self.new = Dashboard(self.new_window)
                    self.new_window.protocol("WM_DELETE_WINDOW", self.window.destroy)
                    self.window.withdraw()
                else:
                    messagebox.showerror("Error", "Invalid Username and Password.")
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                conn.close()

    def forgot_password(self):
        # Increased window size
        self.win_fp = Toplevel(self.window)
        self.win_fp.title("Recover Password")
        self.win_fp.geometry("500x300")
        self.win_fp.config(bg="#ffdab9")
        
        Label(self.win_fp, text="Enter your registered Email:", font=("Times New Roman", 16, "bold"), bg="#ffdab9").pack(pady=30)
        
        # Bigger Entry box
        self.email_entry = Entry(self.win_fp, width=30, font=("Times New Roman", 16))
        self.email_entry.pack(pady=10, ipady=5)
        
        # Bigger Button
        Button(self.win_fp, text="Send Password", command=self.send_reset_email, 
               bg="#008080", fg="white", font=("Times New Roman", 14, "bold"), width=15, height=2).pack(pady=30)

    def send_reset_email(self):
        email = self.email_entry.get()
        if not email:
            messagebox.showerror("Error", "Please enter an email address!")
            return

        conn = get_credentials_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT Password FROM details WHERE Email=%s", (email,))
                row = cursor.fetchone()
                
                if row:
                    password = row[0]
                    # Using your existing email credentials
                    sender_email = "ujjwalkamila86@gmail.com"
                    sender_password = "bdrj vxxz jlha bwyj"
                    
                    msg = MIMEText(f"Hello,\n\nYour registered password is: {password}\n\nPlease keep it safe.")
                    msg['Subject'] = "Password Recovery"
                    msg['From'] = sender_email
                    msg['To'] = email
                    
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.send_message(msg)
                    server.quit()
                    
                    # Success Message
                    messagebox.showinfo("Success", "Password successfully sent to your respected email id.")
                    self.win_fp.destroy()
                else:
                    # Error Message for unregistered email
                    messagebox.showerror("Error", "Email id is not registered, please enter correct email id!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send email: {str(e)}")
            finally:
                conn.close()