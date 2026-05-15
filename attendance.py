# attendance.py
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import os
import csv
from database import get_frs_db

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
        messagebox.showerror("Error", "You can't alter the attendance via UI.")