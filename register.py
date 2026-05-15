# register.py
from tkinter import *
from tkinter import messagebox
from database import get_credentials_db
from PIL import Image, ImageTk

class Register: 
    def __init__(self, window):  
        self.window = window
        self.window.title("Register")
        self.window.geometry("1540x800+-10+0")
        self.window.config(background="#008080")

        frame = Frame(self.window, background="#ffdab9")
        frame.place(x=300, y=71, width=950, height=650)

        Label(frame, text="Create a new account", background="#ffdab9", font=("aerial",35,"bold"), width=33).place(x=0, y=0)
        Label(frame, text="First Name", font=("aerial",25,"bold"), background="#ffdab9").place(x=60, y=100)
        Label(frame, text="Mobile No.", font=("aerial", 25, "bold"), background="#ffdab9").place(x=60, y=240)
        Label(frame, text="Password", font=("aerial", 25, "bold"), background="#ffdab9").place(x=60, y=380)

        Label(frame, text="Last Name", font=("aerial",25,"bold"), background="#ffdab9").place(x=530, y=100)
        Label(frame, text="Email", font=("aerial", 25, "bold"), background="#ffdab9").place(x=530, y=240)
        Label(frame, text="Confirm Password", font=("aerial", 25, "bold"), background="#ffdab9").place(x=530, y=380)

        self.first_name = StringVar()
        Entry(frame, font=("aerial",25,"bold"), background="#008080", foreground="white", textvariable=self.first_name).place(x=60, y=160)

        self.mobile = StringVar()
        Entry(frame, font=("aerial",25,"bold"), background="#008080", foreground="white", textvariable=self.mobile).place(x=60, y=300)

        self.password = StringVar()
        Entry(frame, font=("aerial",25,"bold"), background="#008080", foreground="white", textvariable=self.password, show="*").place(x=60, y=440)

        self.last_name = StringVar()
        Entry(frame, font=("aerial", 25, "bold"), background="#008080", foreground="white", textvariable=self.last_name).place(x=530, y=160)

        self.email = StringVar()
        Entry(frame, font=("aerial",25,"bold"), background="#008080", foreground="white", textvariable=self.email).place(x=530, y=300)

        self.conf_password = StringVar()
        Entry(frame, font=("aerial",25,"bold"), background="#008080", foreground="white", textvariable=self.conf_password, show="*").place(x=530, y=440)

        Button(frame, text="Register", command=self.register, background="#008080", foreground="white", activebackground="#ffdab9", font=("aerial",20,"bold"), relief=RAISED, bd=10, activeforeground="black", width=15).place(x=335, y=530)

        try:
            arrow = Image.open("Images\\Left_Arrow.png").resize((100,80))
            self.arrow = ImageTk.PhotoImage(arrow)
            Button(self.window, image=self.arrow, background="#008080", borderwidth=0, activebackground="#008080", command=self.back).place(x=0, y=0)
        except:
            Button(self.window, text="Back", font=("aerial", 15, "bold"), command=self.back).place(x=10, y=10)

    def register(self):
        if self.password.get() != self.conf_password.get():
            messagebox.showerror("Error", "Passwords do not match.")
            return

        if (self.first_name.get() == "" or self.last_name.get() == "" or self.password.get() == ""):
            messagebox.showerror("Error", "All fields are mandatory.")
            return

        conn = get_credentials_db()
        if conn:
            try:
                my_cursor = conn.cursor()
                my_cursor.execute("SELECT * FROM details WHERE Email=%s", (self.email.get(),))
                if my_cursor.fetchone():
                    messagebox.showerror("Error", "User already exists. Try another email")
                else:
                    my_cursor.execute(
                        "INSERT INTO details (Email, FirstName, LastName, Mobile, Password) VALUES (%s,%s,%s,%s,%s)",
                        (self.email.get(), self.first_name.get(), self.last_name.get(), self.mobile.get(), self.password.get())
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