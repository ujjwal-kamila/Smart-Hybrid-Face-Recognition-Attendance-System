# student.py
from tkinter import *
from tkinter import ttk, messagebox
import cv2
import os
import threading
from PIL import Image, ImageTk
from database import get_frs_db

class Student:  
    def __init__(self, window):
        self.window = window
        self.window.title("Student Details")
        self.window.geometry("1540x800+-5+0")
        self.window.configure(background="#008080")

        self.dep, self.course, self.semester, self.year = StringVar(), StringVar(), StringVar(), StringVar()
        self.student_id, self.dob, self.student_name, self.mobile = StringVar(), StringVar(), StringVar(), StringVar()
        self.parent_name, self.email, self.school, self.address = StringVar(), StringVar(), StringVar(), StringVar()

        self.dob.set("YYYY-MM-DD")
        self.email.set("xyz@gmail.com")

        Label(self.window, text="Student Management System", font=("aerial",35,"bold"), bg="#ffdab9", width=1530).place(x=0, y=0, width=1550, height=70)

        frame = Frame(self.window, background="#008080")
        frame.place(x=0, y=71, width=1550, height=650)

        left_frame = LabelFrame(frame, background="#fffaf0", font=("aerial",20,"bold"))
        left_frame.place(x=20, y=50, height=600, width=730)

        course = LabelFrame(left_frame, background="#fffaf0")
        course.place(x=0, y=0, height=180, width=728)

        Label(course, text="Course Information", font=("Aerial",20,"bold"), background="#fffaf0").place(x=0,y=0)
        Label(course, text="Department", font=("Aerial",18,"bold"), background="#fffaf0").place(x=25, y=50)
        Label(course, text="Course", font=("Aerial",18,"bold"), background="#fffaf0").place(x=400, y=50)
        Label(course, text="Semester", font=("Aerial",18,"bold"), background="#fffaf0").place(x=25, y=110)
        Label(course, text="Year", font=("Aerial",18,"bold"), background="#fffaf0").place(x=402, y=110)

        col_bg, col_fg = "#008080", "WHITE"
        
        
        
        self.dep.set("Select Department")
        # Updated Branches
        OptionMenu(course, self.dep, *["CS", "IT", "CIVIL", "EE", "ME", "ECE"]).place(x=185, y=50, height=39, width=190)
        
        self.course.set("Select Course")
        # Updated Courses
        OptionMenu(course, self.course, *["DSA", "OOPS", "AI","Machine Learning", "OS", "DBMS", "CN", "COA", "Python","Web Developer"]).place(x=508, y=50, height=39, width=190)
        
        self.semester.set("Select Semester")
        OptionMenu(course, self.semester, *['1st', '2nd', '3rd', '4th', '5th', "6th", "7th", "8th"]).place(x=185, y=110, height=39, width=190)
        
        self.year.set("Select Year")
        # Updated Years
        OptionMenu(course, self.year, *["2022", "2023", "2024", "2025", "2026", "2027", "2028","2029","2030"]).place(x=508, y=110, height=39, width=190)

        # self.dep.set("Select Department")
        # OptionMenu(course, self.dep, *["IT","Civil","CS","Electrical"]).place(x=185, y=50, height=39, width=190)
        # self.course.set("Select Course")
        # OptionMenu(course, self.course, *["Data Structures","Web Developer","AI","Machine Learning"]).place(x=508, y=50, height=39, width=190)
        # self.semester.set("Select Semester")
        # OptionMenu(course, self.semester, *['1st', '2nd', '3rd', '4th', '5th', "6th", "7th", "8th"]).place(x=185, y=110, height=39, width=190)
        # self.year.set("Select Year")
        # OptionMenu(course, self.year, *[2024, 2023, 2022, 2021, 2020]).place(x=508, y=110, height=39, width=190)

        info = LabelFrame(left_frame, background="#fffaf0")
        info.place(x=0, y=179, height=300, width=728)
        Label(info, text="Student Information", font=("aerial",20,"bold"), bg="#fffaf0").place(x=0, y=0)

        Label(info, text="Student ID", font=("Aerial",18,"bold"), background="#fffaf0").place(x=20, y=50)
        Label(info, text="Student Name", font=("Aerial",17,"bold"), background="#fffaf0").place(x=20, y=100)
        Label(info, text="Parent Name", font=("Aerial",18,"bold"), background="#fffaf0").place(x=20, y=150)
        Label(info, text="School Name", font=("Aerial",18,"bold"), background="#fffaf0").place(x=20, y=200)
        Label(info, text="D.O.B", font=("Aerial",18,"bold"), background="#fffaf0").place(x=400, y=50)
        Label(info, text="Mobile", font=("Aerial",18,"bold"), background="#fffaf0").place(x=400, y=100)
        Label(info, text="Email", font=("Aerial",18,"bold"), background="#fffaf0").place(x=400, y=150)
        Label(info, text="Address", font=("Aerial",18,"bold"), background="#fffaf0").place(x=400, y=200)

        Entry(info, font=("Aerial",18,"bold"), background="#008080", fg="white", textvariable=self.student_id).place(x=185, y=50, height=33, width=189)
        Entry(info, font=("Aerial",18,"bold"), background="#008080", fg="white", textvariable=self.student_name).place(x=185, y=100, height=33, width=189)
        Entry(info, font=("Aerial",18,"bold"), background="#008080", fg="white", textvariable=self.parent_name).place(x=185, y=150, height=33, width=189)
        Entry(info, font=("Aerial",18,"bold"), background="#008080", fg="white", textvariable=self.school).place(x=185, y=200, height=33, width=189)
        Entry(info, font=("Aerial",18,"bold"), background="#008080", fg="white", textvariable=self.dob).place(x=508, y=50, height=33, width=189)
        Entry(info, font=("Aerial",18,"bold"), background="#008080", fg="white", textvariable=self.mobile).place(x=508, y=100, height=33, width=189)
        Entry(info, font=("Aerial",18,"bold"), background="#008080", fg="white", textvariable=self.email).place(x=508, y=150, height=33, width=189)
        Entry(info, font=("Aerial",18,"bold"), background="#008080", fg="white", textvariable=self.address).place(x=508, y=200, height=33, width=189)

        buttons = LabelFrame(left_frame, background="black")
        buttons.place(x=0, y=470, height=180, width=728)

        Button(buttons, text="Save", command=self.add_data, background="#008080", fg="white", font=("aerial",15,"bold"), relief=RAISED, bd=10, width=18).grid(row=0, column=0, pady=3)
        Button(buttons, text="Update", command=self.update_data, background="#008080", fg="white", font=("aerial",15,"bold"), relief=RAISED, bd=10, width=18).grid(row=0, column=1)
        Button(buttons, text="Delete", command=self.delete_data, background="#008080", fg="white", font=("aerial",15,"bold"), relief=RAISED, bd=10, width=18).grid(row=0, column=2)
        Button(buttons, text="Reset", command=self.reset_data, background="#008080", fg="white", font=("aerial",15,"bold"), relief=RAISED, bd=10, width=18).grid(row=1, column=0)
        Button(buttons, text="Take Photo Sample", command=self.start_dataset_thread, background="#008080", fg="white", font=("aerial",15,"bold"), relief=RAISED, bd=10, width=18).grid(row=1, column=1)
        Button(buttons, text="Back", command=self.window.destroy, background="#008080", fg="white", font=("aerial",15,"bold"), relief=RAISED, bd=10, width=18).grid(row=1, column=2)

        right_frame = LabelFrame(frame, background="#fffaf0", font=("aerial",10,"bold"))
        right_frame.place(x=780, y=50, height=600, width=730)

        search_frame = LabelFrame(right_frame, background="#fffaf0")
        search_frame.place(x=0, y=0, width=728, height=115)
        Label(search_frame, text="Search System", font=("aerial",20,"bold"), background="#fffaf0").place(x=0, y=0)
        Label(search_frame, text="Search By", font=("aerial",18,"bold"), background="#fffaf0").place(x=13, y=52)

        self.category = StringVar()
        self.category.set("Category")
        OptionMenu(search_frame, self.category, *["StudentID","Name","Department", "Semester"]).place(x=146, y=50, height=39, width=160)

        self.variable5 = StringVar()
        Entry(search_frame, font=("Aerial",15,"bold"), textvariable=self.variable5, background="#008080", fg="white").place(x=327, y=53, height=33, width=160)
        Button(search_frame, text="Search", font=("Aerial", 15, "bold"), command=self.search, background="#008080", fg="white", relief=RAISED, bd=7).place(x=508, y=53, height=33, width=93)
        Button(search_frame, text="Show All", font=("Aerial", 15, "bold"), command=self.fetch_data, background="#008080", fg="white", relief=RAISED, bd=5).place(x=620, y=53, height=33, width=98)

        table = LabelFrame(right_frame, background="#fffaf0")
        table.place(x=0, y=114, width=728, height=483)
        scroll_x = ttk.Scrollbar(table, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table, orient=VERTICAL)
        self.student_table = ttk.Treeview(table, columns=("id","name","dep","course","sem","year","mobile","email","school","parent","dob", "address"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        for col in self.student_table["columns"]:
            self.student_table.heading(col, text=col.capitalize())
        self.student_table["show"] = "headings"
        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)

        self.fetch_data()

    def add_data(self):
        if self.student_id.get() == "" or self.student_name.get() == "":
            messagebox.showerror("Error", "All fields are required.", parent=self.window)
            return
        conn = get_frs_db()
        if conn:
            try:
                my_cursor = conn.cursor()
                my_cursor.execute("insert into student values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                    self.student_id.get(), self.student_name.get(), self.dep.get(), self.course.get(),
                    self.semester.get(), self.year.get(), self.mobile.get(), self.email.get(),
                    self.school.get(), self.parent_name.get(), self.dob.get(), self.address.get()
                ))
                conn.commit()
                self.fetch_data()
                messagebox.showinfo("Success", "Student details registered.")
            except Exception as es:
                messagebox.showerror("Error", f"Due to {str(es)}")
            finally:
                conn.close()

    def fetch_data(self):
        conn = get_frs_db()
        if conn:
            try:
                my_cursor = conn.cursor()
                my_cursor.execute("select * from student")
                data = my_cursor.fetchall()
                self.student_table.delete(*self.student_table.get_children())
                for row in data:
                    self.student_table.insert("", END, values=row)
            except Exception as es:
                pass
            finally:
                conn.close()

    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]
        if data:
            self.student_id.set(data[0])
            self.student_name.set(data[1])
            self.dep.set(data[2])
            self.course.set(data[3])
            self.semester.set(data[4])
            self.year.set(data[5])
            self.mobile.set(data[6])
            self.email.set(data[7])
            self.school.set(data[8])
            self.parent_name.set(data[9])
            self.dob.set(data[10])
            self.address.set(data[11])

    def update_data(self):
        Update = messagebox.askyesno("Update", "Do you want to update details?", parent=self.window)
        if Update:
            conn = get_frs_db()
            if conn:
                try:
                    mycursor = conn.cursor()
                    sql = """UPDATE student SET Name=%s, Department=%s, Course=%s, Semester=%s, Year=%s, Mobile=%s, Email=%s, School=%s, Parent_Name=%s, DOB=%s, Address=%s WHERE StudentID=%s"""
                    mycursor.execute(sql, (self.student_name.get(), self.dep.get(), self.course.get(), self.semester.get(), self.year.get(), self.mobile.get(), self.email.get(), self.school.get(), self.parent_name.get(), self.dob.get(), self.address.get(), self.student_id.get()))
                    conn.commit()
                    self.fetch_data()
                except Exception as es:
                    messagebox.showerror("Error", f"Due to {str(es)}")
                finally:
                    conn.close()

    def delete_data(self):
        if self.student_id.get() == "":
            return
        delete = messagebox.askyesno("Delete", "Delete this student?", parent=self.window)
        if delete:
            conn = get_frs_db()
            if conn:
                try:
                    my_cursor = conn.cursor()
                    my_cursor.execute("delete from student where StudentID = %s", (self.student_id.get(),))
                    conn.commit()
                    self.fetch_data()
                    self.reset_data()
                except Exception as es:
                    messagebox.showerror("Error", f"Due to {str(es)}")
                finally:
                    conn.close()

    def reset_data(self):
        self.dep.set("Select Department")
        self.course.set("Select Course")
        self.semester.set("Select Semester")
        self.year.set("Select Year")
        self.student_id.set("")
        self.student_name.set("")
        self.mobile.set("")
        self.email.set("xyz@gmail.com")

    def start_dataset_thread(self):
        threading.Thread(target=self.generate_dataset, daemon=True).start()

    def generate_dataset(self):
        if self.student_id.get() == "" or self.student_name.get() == "":
            messagebox.showerror("Error", "Select a student first.", parent=self.window)
            return

        try:
            os.makedirs("Faces", exist_ok=True)
            face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

            def face_cropped(img):
                grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(grey, 1.3, 5)
                for (x, y, w, h) in faces:
                    return img[y:y + h, x:x + w]
                return None

            cap = cv2.VideoCapture(0)
            img_id = 0
            student_id = self.student_id.get()

            while True:
                ret, my_frame = cap.read()
                if not ret: break
                
                cropped = face_cropped(my_frame)
                if cropped is not None:
                    img_id += 1
                    face = cv2.resize(cropped, (160, 160)) 
                    file_path = f"Faces/user.{student_id}.{img_id}.jpg"
                    cv2.imwrite(file_path, face)

                    cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow("Cropping Faces - Press ESC to stop", face)

                if cv2.waitKey(1) == 27 or img_id == 100:  
                    break

            cap.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Result", f"Photo samples saved for Student ID {student_id}!")
        except Exception as es:
            messagebox.showerror("Error", f"Due to {str(es)}", parent=self.window)

    def search(self):
        if self.variable5.get() == "":
            return
        conn = get_frs_db()
        if conn:
            try:
                my_cursor = conn.cursor()
                query = f"select * from student where {self.category.get()} LIKE '%{self.variable5.get()}%'"
                my_cursor.execute(query)
                data = my_cursor.fetchall()
                self.student_table.delete(*self.student_table.get_children())
                for i in data:
                    self.student_table.insert("", END, values=i)
            except Exception as es:
                messagebox.showerror("Error", f"Due to {str(es)}")
            finally:
                conn.close()