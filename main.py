# main.py
from tkinter import *
from login import Login
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Hides the oneDNN warning
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'   # Hides other TensorFlow info logs
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Forces CPU mode to prevent GPU freezing

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