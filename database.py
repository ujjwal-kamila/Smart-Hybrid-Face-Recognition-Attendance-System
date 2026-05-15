# database.py
import mysql.connector
from tkinter import messagebox

DB_PASSWORD = "Ujjwal@81"  # Update with your MySQL password

def get_credentials_db():
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password=DB_PASSWORD,
            database="credentials", port=3306, auth_plugin='caching_sha2_password'
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Error", f"Credentials DB Error: {str(e)}")
        return None

def get_frs_db():
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password=DB_PASSWORD,
            database="frs", port=3306, auth_plugin='caching_sha2_password'
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Error", f"FRS DB Error: {str(e)}")
        return None