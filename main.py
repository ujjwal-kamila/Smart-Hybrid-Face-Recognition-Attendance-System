# main.py
from tkinter import *
from login import Login

if __name__ == "__main__":
    window = Tk()
    app = Login(window)
    window.title("Smart Hybrid Face Recognition Attendance System")
    window.geometry("1530x800+-5+0")
    window.config(background="#008080")
    
    try:
        icon = PhotoImage(file="Images\\Makaut_logo.png")
        window.iconphoto(True, icon)
    except:
        pass
        
    window.mainloop()