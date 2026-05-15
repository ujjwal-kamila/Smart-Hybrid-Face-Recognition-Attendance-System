# face_recognition.py
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import cv2
import numpy as np
import pickle
import csv
from datetime import datetime
from tkinter import messagebox
from database import get_frs_db

def mark_attendance(student_id, name):
    now = datetime.now()
    d1 = now.strftime("%d/%m/%Y")
    t1 = now.strftime("%H:%M:%S")
    
    newly_marked = False
    
    # 1. SAVE TO MYSQL DATABASE
    conn = get_frs_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Check if student is already marked present for today
            cursor.execute("SELECT * FROM attendance WHERE StudentID=%s AND Date=%s", (student_id, d1))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO attendance (StudentID, Name, Date, Time, Status) VALUES(%s,%s,%s,%s,%s)",
                               (student_id, name, d1, t1, "Present"))
                conn.commit()
                newly_marked = True
            else:
                newly_marked = False # Already marked today
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save attendance to MySQL!\nError: {str(e)}")
            newly_marked = False
        finally:
            conn.close()
    else:
        messagebox.showerror("Database Error", "Could not connect to the database.")

    # 2. SAVE TO EXCEL/CSV FILE
    # We only write a new row to Excel if we successfully added a new row to the Database
    if newly_marked:
        try:
            os.makedirs("Attendance", exist_ok=True)
            file_path = "Attendance/face_recognised_attendance.csv"
            file_exists = os.path.isfile(file_path)
            
            with open(file_path, "a+", newline="") as f:
                writer = csv.writer(f)
                # If file is brand new, add Column Headers first
                if not file_exists:
                    writer.writerow(["StudentID", "Name", "Date", "Time", "Status"])
                
                # Add the student data
                writer.writerow([student_id, name, d1, t1, "Present"])
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to save to Excel/CSV!\n(Make sure the file isn't open in Excel)\nError: {str(e)}")

    return newly_marked

def start_recognition():
    from keras_facenet import FaceNet

    model_path = "models/svm_facenet_model.pkl"
    le_path = "models/label_encoder.pkl"
    
    if not os.path.exists(model_path) or not os.path.exists(le_path):
        messagebox.showwarning("Error", "Model not found. Please click 'Train Data' first.")
        return
        
    with open(model_path, "rb") as f:
        clf = pickle.load(f)
    with open(le_path, "rb") as f:
        le = pickle.load(f)

    embedder = FaceNet()
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)

    frame_count = 0
    last_faces = []
    last_identities = []
    verification_counts = {}
    MAX_DETECTIONS = 12 

    while True:
        ret, frame = cap.read()
        if not ret: break

        frame_count += 1

        if frame_count % 3 == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

            last_faces = faces
            last_identities = []

            for (x, y, w, h) in faces:
                face_crop = frame[y:y+h, x:x+w]
                face_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
                face_crop = cv2.resize(face_crop, (160, 160))
                face_crop = np.expand_dims(face_crop, axis=0)

                emb = embedder.embeddings(face_crop)[0]
                emb = np.expand_dims(emb, axis=0)
                
                preds = clf.predict_proba(emb)[0]
                max_idx = np.argmax(preds)
                prob = preds[max_idx]

                if prob > 0.65: 
                    student_id = le.inverse_transform([max_idx])[0]
                    
                    name = "Unknown"
                    conn = get_frs_db()
                    if conn:
                        try:
                            cursor = conn.cursor()
                            cursor.execute("SELECT Name FROM student WHERE StudentID=%s", (student_id,))
                            res = cursor.fetchone()
                            if res: name = res[0]
                        except:
                            pass
                        finally:
                            conn.close()

                    if verification_counts.get(student_id) == "MARKED":
                        progress_text = "Attendance: Saved"
                        color = (255, 255, 0)
                    else:
                        current_count = verification_counts.get(student_id, 0) + 1
                        verification_counts[student_id] = current_count
                        
                        progress_pct = int((current_count / MAX_DETECTIONS) * 100)
                        
                        if progress_pct >= 100:
                            progress_text = "Saving..."
                            color = (0, 255, 0)
                            
                            is_newly_marked = mark_attendance(student_id, name)
                            verification_counts[student_id] = "MARKED"
                            
                            if is_newly_marked:
                                messagebox.showinfo("Success", f"Attendance Saved for {name}\n(ID: {student_id})")
                            else:
                                messagebox.showinfo("Info", f"Attendance was already marked for {name} today!")
                        else:
                            progress_text = f"Scanning: {progress_pct}%"
                            color = (0, 255, 0)

                    last_identities.append((student_id, name, progress_text, color)) 
                else:
                    last_identities.append(("Unknown", "Unknown", "Scanning: 0%", (0, 0, 255))) 

        for i, (x, y, w, h) in enumerate(last_faces):
            if i < len(last_identities):
                student_id, name, progress_text, color = last_identities[i]
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, f"ID: {student_id}", (x, y-55), cv2.FONT_HERSHEY_DUPLEX, 0.8, color, 2)
                cv2.putText(frame, f"Name: {name}", (x, y-30), cv2.FONT_HERSHEY_DUPLEX, 0.8, color, 2)
                cv2.putText(frame, progress_text, (x, y-5), cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 2)

        cv2.imshow("Face Recognition - Press ESC to Exit", frame)
        
        if cv2.waitKey(1) == 27 or cv2.getWindowProperty("Face Recognition - Press ESC to Exit", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()