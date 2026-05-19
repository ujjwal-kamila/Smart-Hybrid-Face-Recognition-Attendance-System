# register.py
from tkinter import *
from tkinter import messagebox
from database import get_credentials_db
from PIL import Image, ImageTk
import re 

class Register: 
    def __init__(self, window):  
        self.window = window
        self.window.title("Register")
        self.window.geometry("1540x800+-10+0")
        self.window.config(background="#008080")

        # Main Centered Frame
        frame = Frame(self.window, background="#ffdab9", padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, width=950, height=650, anchor=CENTER)

        # Title
        Label(frame, text="Create a new account", background="#ffdab9", font=("Times New Roman", 40, "bold")).pack(pady=(0, 30))
        
        # Font settings
        label_font = ("Times New Roman", 24, "bold")
        entry_font = ("Times New Roman", 24, "bold")

        # Input Grid Frame
        input_frame = Frame(frame, background="#ffdab9")
        input_frame.pack()

        # Labels and Entry Widgets
        labels = ["First Name", "Last Name", "Mobile No.", "Email", "Password", "Confirm Password"]
        entries = []

        for i in range(0, 6, 2):
            row_frame = Frame(input_frame, background="#ffdab9")
            row_frame.pack(fill=X, pady=10)
            
            # Left Column
            col1 = Frame(row_frame, background="#ffdab9")
            col1.pack(side=LEFT, padx=20)
            Label(col1, text=labels[i], font=label_font, background="#ffdab9").pack(anchor=W)
            e1 = Entry(col1, font=entry_font, background="#008080", foreground="white")
            e1.pack(fill=X, ipady=5, ipadx=5)
            entries.append(e1)

            # Right Column
            col2 = Frame(row_frame, background="#ffdab9")
            col2.pack(side=LEFT, padx=20)
            Label(col2, text=labels[i+1], font=label_font, background="#ffdab9").pack(anchor=W)
            e2 = Entry(col2, font=entry_font, background="#008080", foreground="white")
            e2.pack(fill=X, ipady=5, ipadx=5)
            entries.append(e2)

        self.first_name, self.last_name = entries[0], entries[1]
        self.mobile, self.email = entries[2], entries[3]
        self.password, self.conf_password = entries[4], entries[5]
        
        self.password.config(show="*")
        self.conf_password.config(show="*")

        # Register Button (Shifted down for layout)
        Button(frame, text="Register", command=self.register, background="#008080", foreground="white", 
               font=("Times New Roman", 25, "bold"), relief=RAISED, bd=5, width=15).pack(pady=30)

        # Back Button
        try:
            arrow = Image.open("Images\\Left_Arrow.png").resize((50, 40))
            self.arrow = ImageTk.PhotoImage(arrow)
            Button(self.window, image=self.arrow, background="#008080", borderwidth=0, command=self.back).place(x=20, y=20)
        except:
            Button(self.window, text="← Back", font=("Times New Roman", 20, "bold"), command=self.back).place(x=20, y=20)

    def register(self):
        # Validation Logic
        mobile = self.mobile.get()
        if not (mobile.isdigit() and len(mobile) == 10):
            messagebox.showerror("Error", "Mobile number must be exactly 10 digits.")
            return

        email = self.email.get()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Please enter a valid email (e.g., xyz@gmail.com).")
            return

        password = self.password.get()
        # Regex: 12 chars, 1 lower, 1 upper, 4 numbers, 1 special
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d{4})(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12}$"
        if not re.match(pattern, password):
            messagebox.showerror("Error", "Password must be 12 chars: Uppercase, Lowercase, 4 Numbers, 1 Special character.")
            return

        if password != self.conf_password.get():
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Database Registration
        conn = get_credentials_db()
        if conn:
            try:
                my_cursor = conn.cursor()
                my_cursor.execute("SELECT * FROM details WHERE Email=%s", (email,))
                if my_cursor.fetchone():
                    messagebox.showerror("Error", "User already exists. Try another email.")
                else:
                    my_cursor.execute(
                        "INSERT INTO details (Email, FirstName, LastName, Mobile, Password) VALUES (%s,%s,%s,%s,%s)",
                        (email, self.first_name.get(), self.last_name.get(), mobile, password)
                    )
                    conn.commit()
                    messagebox.showinfo("Success", "User registered successfully.")
                    self.back()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                conn.close()

    def back(self):
        self.window.destroy()