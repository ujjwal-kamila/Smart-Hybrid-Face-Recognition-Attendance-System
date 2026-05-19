# face_recognition.py
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import cv2
import numpy as np
import pickle
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from tkinter import messagebox
from database import get_frs_db

def send_email_alert(student_email, student_name, time_marked):
    # CHANGE THESE TWO LINES TO YOUR GMAIL DETAILS
    sender_email = "ujjwalkamila86@gmail.com" 
    sender_password = "bdrj vxxz jlha bwyj" 

    subject = "Attendance Successfully Marked"
    body = f"Hello {student_name},\n\nYour attendance for today has been successfully recorded at {time_marked} via the Face Recognition System.\n\nThank you!"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = student_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {student_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def mark_attendance(student_id, name):
    now = datetime.now()
    d1 = now.strftime("%d/%m/%Y")
    t1 = now.strftime("%H:%M:%S")
    
    newly_marked = False
    
    conn = get_frs_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM attendance WHERE StudentID=%s AND Date=%s", (student_id, d1))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO attendance (StudentID, Name, Date, Time, Status) VALUES(%s,%s,%s,%s,%s)",
                               (student_id, name, d1, t1, "Present"))
                conn.commit()
                newly_marked = True
            else:
                newly_marked = False 
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save attendance to MySQL!\nError: {str(e)}")
            newly_marked = False
        finally:
            conn.close()
    else:
        messagebox.showerror("Database Error", "Could not connect to the database.")

    if newly_marked:
        try:
            os.makedirs("Attendance", exist_ok=True)
            file_path = "Attendance/face_recognised_attendance.csv"
            file_exists = os.path.isfile(file_path)
            
            with open(file_path, "a+", newline="") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["StudentID", "Name", "Date", "Time", "Status"])
                writer.writerow([student_id, name, d1, t1, "Present"])
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to save to Excel/CSV!\nError: {str(e)}")

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
    
    # Built-in OpenCV Eye Tracking for Liveness Detection
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Cache student details locally
    student_cache = {}
    conn = get_frs_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT StudentID, Name, Email FROM student")
            for row in cursor.fetchall():
                student_cache[str(row[0])] = {"name": row[1], "email": row[2]}
        except Exception as e:
            print(f"Error compiling student cache: {e}")
        finally:
            conn.close()

    cap = cv2.VideoCapture(0)
    frame_count = 0
    last_faces = []
    last_identities = []
    
    # Tracking dictionary to include strict Timeout for Liveness
    student_states = {} 
    MAX_DETECTIONS = 12 
    MAX_TIMEOUT = 50 # How long they have to blink before being declined (approx 3-4 seconds)

    while True:
        ret, frame = cap.read()
        if not ret: break

        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # --- RECOGNITION (Runs every 3 frames to save CPU) ---
        if frame_count % 3 == 0:
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

            last_faces = faces
            last_identities = []

            for (x, y, w, h) in faces:
                face_crop = frame[y:y+h, x:x+w]
                face_crop_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
                face_crop_resized = cv2.resize(face_crop_rgb, (160, 160))
                face_crop_expanded = np.expand_dims(face_crop_resized, axis=0)

                emb = embedder.embeddings(face_crop_expanded)[0]
                emb = np.expand_dims(emb, axis=0)
                
                preds = clf.predict_proba(emb)[0]
                max_idx = np.argmax(preds)
                prob = preds[max_idx]

                if prob > 0.65: 
                    student_id = str(le.inverse_transform([max_idx])[0])
                    
                    student_info = student_cache.get(student_id, {"name": "Unknown", "email": None})
                    name = student_info["name"]
                    student_email = student_info["email"]

                    # Initialize state for new faces
                    if student_id not in student_states:
                        student_states[student_id] = {
                            "count": 0, 
                            "eyes_closed_frames": 0, 
                            "has_blinked": False, 
                            "marked": False,
                            "timeout": 0 # NEW: Tracks how long they've been asked to blink
                        }
                    
                    if student_states[student_id]["marked"]:
                        progress_text = "Attendance: Saved"
                        color = (255, 255, 0) # Cyan/Yellow
                    else:
                        # Stop counting once we reach the max
                        if student_states[student_id]["count"] < MAX_DETECTIONS:
                            student_states[student_id]["count"] += 1
                            
                        current_count = student_states[student_id]["count"]
                        progress_pct = int((current_count / MAX_DETECTIONS) * 100)
                        
                        if progress_pct >= 100:
                            # --- STRICT LIVENESS GATE ---
                            if not student_states[student_id]["has_blinked"]:
                                student_states[student_id]["timeout"] += 1
                                time_left = MAX_TIMEOUT - student_states[student_id]["timeout"]
                                
                                progress_text = f"Please Blink! ({time_left})"
                                color = (0, 165, 255) # Orange (Warning)
                                
                                # Analyze only the top half of the face for eyes
                                roi_gray = gray[y:y+int(h/2), x:x+w]
                                eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=6, minSize=(15, 15))
                                
                                if len(eyes) == 0:
                                    student_states[student_id]["eyes_closed_frames"] += 1
                                else:
                                    # If eyes were closed previously, it's a blink!
                                    if student_states[student_id]["eyes_closed_frames"] >= 1:
                                        student_states[student_id]["has_blinked"] = True
                                    
                                    # Reset the closed frame counter
                                    student_states[student_id]["eyes_closed_frames"] = 0
                                
                                # --- DECLINE CONDITION ---
                                # If the timeout reaches 0 and they still haven't blinked (e.g. holding a photo)
                                if student_states[student_id]["timeout"] > MAX_TIMEOUT:
                                    messagebox.showerror("Liveness Failed", f"Spoofing Detected!\nNo blink registered for {name}.\nAttendance Declined.")
                                    
                                    # Completely reset their progress so they have to start over
                                    student_states[student_id]["count"] = 0
                                    student_states[student_id]["timeout"] = 0
                                    student_states[student_id]["eyes_closed_frames"] = 0
                            else:
                                progress_text = "Saving..."
                                color = (0, 255, 0)
                                
                                is_newly_marked = mark_attendance(student_id, name)
                                student_states[student_id]["marked"] = True
                                
                                if is_newly_marked:
                                    if student_email:
                                        current_time = datetime.now().strftime("%H:%M:%S")
                                        send_email_alert(student_email, name, current_time)

                                    messagebox.showinfo("Success", f"Attendance Saved for {name}\n(ID: {student_id})")
                                else:
                                    messagebox.showinfo("Info", f"Attendance was already marked for {name} today!")
                        else:
                            progress_text = f"Scanning: {progress_pct}%"
                            color = (0, 255, 0)

                    last_identities.append((student_id, name, progress_text, color)) 
                else:
                    last_identities.append(("Unknown", "Unknown", "Scanning: 0%", (0, 0, 255))) 

        # --- DRAW BOUNDING BOXES ---
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