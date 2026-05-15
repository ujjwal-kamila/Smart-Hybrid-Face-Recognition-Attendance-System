# train.py
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import cv2
import numpy as np
import pickle
from tkinter import messagebox

def train_hybrid_model():
    from sklearn.svm import SVC
    from sklearn.preprocessing import LabelEncoder
    from keras_facenet import FaceNet

    faces_dir = "Faces"
    if not os.path.exists(faces_dir) or len(os.listdir(faces_dir)) == 0:
        messagebox.showerror("Error", "No training images found in 'images' folder.")
        return

    messagebox.showinfo("Info", "Training Started.\nClick OK to watch the training progress...")
    
    embedder = FaceNet()
    embeddings = []
    labels = []

    files = [f for f in os.listdir(faces_dir) if f.endswith((".jpg", ".png"))]
    total_files = len(files)

    for i, file in enumerate(files):
        path = os.path.join(faces_dir, file)
        parts = file.split('.')
        if len(parts) >= 3:
            student_id = parts[1] 
            
            img = cv2.imread(path)
            if img is None: continue
            
            display_img = img.copy()
            cv2.putText(display_img, f"Training: {i+1}/{total_files}", (20, 40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow("Training Hybrid Model", display_img)
            cv2.waitKey(1)

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_resized = cv2.resize(img_rgb, (160, 160)) 
            img_expanded = np.expand_dims(img_resized, axis=0)
            
            emb = embedder.embeddings(img_expanded)[0]
            embeddings.append(emb)
            labels.append(student_id)

    cv2.destroyAllWindows()

    if len(labels) == 0:
        messagebox.showerror("Error", "No valid images processed.")
        return

    unique_classes = set(labels)
    if len(unique_classes) < 2:
        messagebox.showerror("AI Data Error", "The SVM AI requires at least TWO different students to draw a boundary.\n\nPlease go to Student Details, register a second student, capture their photo samples, and try again.")
        return

    le = LabelEncoder()
    labels_encoded = le.fit_transform(labels)

    clf = SVC(kernel='linear', probability=True)
    clf.fit(embeddings, labels_encoded)

    os.makedirs("models", exist_ok=True)
    with open("models/svm_facenet_model.pkl", "wb") as f:
        pickle.dump(clf, f)
    with open("models/label_encoder.pkl", "wb") as f:
        pickle.dump(le, f)

    messagebox.showinfo("Result", "Hybrid Model Training completed successfully!\nSaved as svm_facenet_model.pkl")