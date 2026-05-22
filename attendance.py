# attendance.py
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os
import csv
from database import get_frs_db
from database import get_credentials_db

my_data = []

class Attendance:
    def __init__(self, window):
        self.window = window
        self.window.title("Attendance Management")
        self.window.geometry("1540x800+-5+0")
        self.window.configure(background="#008080")

        Label(self.window, text="Attendance Management System",font=("aerial",35,"bold"), bg="#ffdab9", width=1530).place(x=0, y=0, width=1550, height=70)

        frame = Frame(self.window, background="black", bg="#008080")
        frame.place(x=0,y=70, height=650, width=1540)

        left_frame = LabelFrame(frame, background="#fffaf0" , font=("aerial",20,"bold"))
        left_frame.place(x=20, y=50, height=600, width=730)

        Label(left_frame, text="Student Attendance Details", font=("Aerial",20,"bold"), background="#ffdab9", width=42, padx=15, pady=6).place(x=0,y=0)

        Label(left_frame, text="StudentID", font=("Aerial",18,"bold"), background="#fffaf0").place(x=25, y=75)
        Label(left_frame, text="Date", font=("Aerial",18,"bold"), background="#fffaf0").place(x=412, y=75)
        Label(left_frame, text="Name", font=("Aerial",18,"bold"), background="#fffaf0").place(x=25, y=135)
        Label(left_frame, text="Time", font=("Aerial",18,"bold"), background="#fffaf0").place(x=412, y=135)
        Label(left_frame, text="Attendance Status", font=("Aerial",18,"bold"), background="#fffaf0").place(x=25, y=195)

        self.student_id, self.date, self.time, self.name = StringVar(), StringVar(), StringVar(), StringVar()
        
        Entry(left_frame, font=("Aerial",18,"bold"), background="#008080", fg="white", textvariable=self.student_id).place(x=185, y=77, height=33, width=189)
        Entry(left_frame, font=("Aerial",18,"bold"), background="#008080", fg="white", textvariable=self.date).place(x=508, y=77, height=33, width=189)
        Entry(left_frame, font=("Aerial",18,"bold"), background="#008080", fg="white", textvariable=self.time).place(x=508, y=137, height=33, width=189)
        Entry(left_frame, font=("Aerial", 18, "bold"), background="#008080", fg="white", textvariable=self.name).place(x=185, y=137, height=33, width=189)

        Button(left_frame, text="Update", font=("Aerial", 25, "bold"), command=self.update, background="#008080", fg="white", relief=RAISED, bd=15).place(x=-1, y=448, height=75, width=365)
        Button(left_frame, text="Reset", font=("Aerial", 25, "bold"), command=self.reset, background="#008080", fg="white", relief=RAISED, bd=15).place(x=364, y=448, height=75, width=365)
        Button(left_frame, text="Import File", command=self.importCsv, font=("Aerial", 25, "bold"), background="#008080", fg="white", relief=RAISED, bd=15).place(x=-1, y=523, height=75, width=365)
        Button(left_frame, text="Export File", command=self.export_csv, font=("Aerial", 25, "bold"), background="#008080", fg="white", relief=RAISED, bd=15).place(x=364, y=523, height=75, width=365)

        Button(self.window, text="Back", font=("aerial", 15, "bold"), command=self.window.destroy).place(x=10, y=10)

        self.attendance = StringVar()
        self.attendance.set("Present")
        OptionMenu(left_frame, self.attendance, *["Present","Absent"]).place(x=260, y=195, height=39, width=190)

        right_frame = LabelFrame(frame, background="#fffaf0")
        right_frame.place(x=780, y=50, height=600, width=730)

        table = LabelFrame(right_frame, background="#fffaf0")
        table.place(x=0, y=10, width=728, height=580)

        scroll_x = ttk.Scrollbar(table, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table, orient=VERTICAL)

        self.attendance_table = ttk.Treeview(table, columns=("id","name","date","time","status"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)

        for col in self.attendance_table["columns"]:
            self.attendance_table.heading(col, text=col.capitalize())
        self.attendance_table["show"] = "headings"
        self.attendance_table.pack(fill=BOTH, expand=1)
        self.attendance_table.bind("<ButtonRelease>", self.get_cursor)

        self.load_from_db()

    def load_from_db(self):
        conn = get_frs_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT StudentID, Name, Date, Time, Status FROM attendance")
                rows = cursor.fetchall()
                self.fetch_data(rows)
            except Exception as e:
                pass
            finally:
                conn.close()

    def fetch_data(self, rows):
        self.attendance_table.delete(*self.attendance_table.get_children())
        for i in rows:
            self.attendance_table.insert("",END, values=i)

    def importCsv(self):
        global my_data
        my_data.clear()
        file_name = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(("CSV File","*.csv"),("ALL Files","*.*")))
        if file_name:
            with open(file_name) as myfile:
                read = csv.reader(myfile, delimiter=",")
                for r in read:
                    my_data.append(r)
                self.fetch_data(my_data)

    def export_csv(self):
        if len(self.attendance_table.get_children()) < 1:
            messagebox.showerror("No Data", "No Data found to export")
            return False
        file_name = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV", defaultextension=".csv")
        if file_name:
            with open(file_name, "w", newline="") as myfile:
                write_new_file = csv.writer(myfile, delimiter=",")
                for row_id in self.attendance_table.get_children():
                    row = self.attendance_table.item(row_id)['values']
                    write_new_file.writerow(row)
            messagebox.showinfo("Success", "Data exported successfully")

    def get_cursor(self, event=""):
        cursor_row = self.attendance_table.focus()
        content = self.attendance_table.item(cursor_row)
        rows = content['values']
        if rows:
            self.student_id.set(rows[0])
            self.name.set(rows[1])
            self.date.set(rows[2])
            self.time.set(rows[3])
            self.attendance.set(rows[4])

    def reset(self):
        self.student_id.set("")
        self.name.set("")
        self.date.set("")
        self.time.set("")
        self.attendance.set("Present")

    def update(self):
        if self.student_id.get() == "":
            messagebox.showerror("Error", "Please select an entry")
            return
            
        # UI Styling to match your request
        self.auth_win = Toplevel(self.window)
        self.auth_win.title("Admin Panel")
        self.auth_win.geometry("500x400")
        self.auth_win.config(bg="#ffdab9")
        
        Label(self.auth_win, text="ADMIN PANEL", font=("Times New Roman", 25, "bold"), bg="#ffdab9", fg="red").pack(pady=20)
        
        Label(self.auth_win, text="Admin Email:", font=("Times New Roman", 15, "bold"), bg="#ffdab9").pack(anchor=W, padx=50)
        self.admin_user = Entry(self.auth_win, font=("Times New Roman", 15), bg="#008080", fg="white")
        self.admin_user.pack(fill=X, padx=50, ipady=5)
        
        Label(self.auth_win, text="Admin Password:", font=("Times New Roman", 15, "bold"), bg="#ffdab9").pack(anchor=W, padx=50, pady=(10,0))
        self.admin_pass = Entry(self.auth_win, font=("Times New Roman", 15), bg="#008080", fg="white", show="*")
        self.admin_pass.pack(fill=X, padx=50, ipady=5)
        
        # Forgot Password link within the popup
        Button(self.auth_win, text="Forgot Password?", font=("Times New Roman", 12, "bold", "underline"), 
               command=self.open_forgot_password, bg="#ffdab9", borderwidth=0, fg="blue").pack(pady=10)
        
        # Styled Verify Button
        Button(self.auth_win, text="Verify & Update", font=("Times New Roman", 15, "bold"), 
               command=self.verify_admin, bg="#008080", fg="white", bd=3, relief=RAISED).pack(pady=20)

    def verify_admin(self):
        conn = get_credentials_db()
        if not conn: return
        try:
            cursor = conn.cursor()
            # Verify Email, Password, AND Role
            cursor.execute("SELECT Role FROM details WHERE Email=%s AND Password=%s AND Role='Admin'", 
                           (self.admin_user.get(), self.admin_pass.get()))
            
            if cursor.fetchone():
                self.execute_update() 
                self.auth_win.destroy()
            else:
                messagebox.showerror("Error", "Access Denied: Admin privileges required!")
        finally:
            conn.close()

    def execute_update(self):
        # This performs the actual database update
        conn = get_frs_db()
        try:
            cursor = conn.cursor()
            sql = "UPDATE attendance SET Status=%s WHERE StudentID=%s AND Date=%s"
            val = (self.attendance.get(), self.student_id.get(), self.date.get())
            cursor.execute(sql, val)
            conn.commit()
            self.load_from_db() # Refresh table
            messagebox.showinfo("Success", "Attendance updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {str(e)}")
        finally:
            conn.close()
            
    def open_forgot_password(self):
        # Create the recovery window directly here
        self.win_fp = Toplevel(self.window)
        self.win_fp.title("Recover Password")
        self.win_fp.geometry("500x300")
        self.win_fp.config(bg="#ffdab9")
        
        Label(self.win_fp, text="Enter your registered Email:", font=("Times New Roman", 16, "bold"), bg="#ffdab9").pack(pady=30)
        
        self.email_entry = Entry(self.win_fp, width=30, font=("Times New Roman", 16))
        self.email_entry.pack(pady=10, ipady=5)
        
        # Use your existing send_reset_email method
        Button(self.win_fp, text="Send Password", command=self.send_reset_email, 
               bg="#008080", fg="white", font=("Times New Roman", 14, "bold"), width=15, height=2).pack(pady=30)

    # Make sure you also have send_reset_email inside attendance.py or import it
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
                    # Same logic used in your login.py
                    import smtplib
                    from email.mime.text import MIMEText
                    sender_email = "ujjwalkamila86@gmail.com"
                    sender_password = "bdrj vxxz jlha bwyj"
                    msg = MIMEText(f"Hello,\n\nYour registered password is: {password}")
                    msg['Subject'] = "Password Recovery"
                    msg['From'] = sender_email
                    msg['To'] = email
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.send_message(msg)
                    server.quit()
                    messagebox.showinfo("Success", "Password successfully sent!")
                    self.win_fp.destroy()
                else:
                    messagebox.showerror("Error", "Email not found!")
            finally:
                conn.close()