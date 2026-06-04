# Smart Hybrid Face Recognition Attendance System

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage Guide](#usage-guide)
- [System Architecture](#system-architecture)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Screenshots](#screenshots)
- [License](#license)

---

## 🎯 Project Overview

**Smart Hybrid Face Recognition Attendance System** is an intelligent, automated attendance management solution built with Python and Tkinter GUI. It leverages **Keras FaceNet embeddings** combined with **SVM (Support Vector Machine)** classifier for accurate face recognition and real-time attendance marking.

**Key Highlights:**
- ✅ Real-time face detection and recognition
- ✅ Hybrid ML model (FaceNet + SVM)
- ✅ Email notifications for attendance confirmation
- ✅ Student profile management
- ✅ MySQL database integration
- ✅ Admin authentication system
- ✅ Attendance reports (CSV export)

---

## ✨ Features

### 🔐 Authentication & Login
- Email-based login system (login.py)
- Password recovery via email with automatic sending
- Admin role authentication
- All new users sign up as regular users by default
- Credentials stored securely in MySQL
- Forgot Password functionality with email integration

### 👤 Student Management (student.py)
- Register new students with details:
  - Student ID, Name, Department, Course
  - Semester, Year, Mobile, Email
  - School, Parent Name, DOB, Address
- Real-time dataset capture (50+ face samples)
- Update and delete student profiles
- Search functionality

### 🎭 Face Recognition (face_recognition.py)
- **Hybrid Model Architecture:**
  - FaceNet for face embedding extraction
  - SVM classifier for identification
  - Training with `label_encoder.pkl` and `svm_facenet_model.pkl`
- Real-time camera feed processing
- Face detection with bounding boxes
- Confidence scoring system
- Blinking verification for liveness detection

### 📊 Attendance Management (attendance.py)
- Auto-detection and marking
- Prevents duplicate attendance (same day)
- Email alerts with timestamp
- Attendance dashboard view
- CSV import/export functionality
- Detailed logs with Date, Time, Status

### 📧 Email Notifications (face_recognition.py)
- Attendance confirmation emails
- Password recovery emails (login.py)
- Admin notifications
- Duplicate attendance alerts
- Email configuration: ujjwalkamila86@gmail.com

### 📈 Reporting (attendance.py)
- View attendance logs (Date, Time, Status)
- CSV export for analysis
- Filter by date range
- Student-wise attendance tracking

---

## 📋 Prerequisites

```
✓ Python 3.8+
✓ MySQL Server (Local or Remote)
✓ Webcam/Camera device
✓ Windows 10/11 OS
✓ 8GB RAM minimum
✓ Internet connection (for email)
```

---

## 🚀 Installation

### Step 1: Clone/Download Project
```bash
cd d:\Laptop\Coding\Smart Hybrid Face Recognition Attendance System
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies:**
```
opencv-python              # Video capture & face detection
numpy                      # Numerical operations
Pillow                     # Image processing
mysql-connector-python     # MySQL database connection
scikit-learn              # SVM classifier & label encoding
keras-facenet             # FaceNet embeddings
tensorflow                # Deep learning backend
```

### Step 4: Setup MySQL Database

**Create Admin Account First (In MySQL Terminal):**

```sql
-- Database 1: Credentials
CREATE DATABASE credentials;
USE credentials;

CREATE TABLE details (
    Email VARCHAR(255) PRIMARY KEY,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Mobile VARCHAR(15),
    Password VARCHAR(100),
    Role ENUM('User', 'Admin') DEFAULT 'User'
);

-- Insert Admin Account
INSERT INTO details VALUES (
    'admin@example.com',
    'Admin',
    'User',
    '1234567890',
    'admin123',
    'Admin'
);

-- Database 2: Face Recognition System
CREATE DATABASE frs;
USE frs;

CREATE TABLE student (
    StudentID VARCHAR(50) PRIMARY KEY,
    Name VARCHAR(100),
    Department VARCHAR(50),
    Course VARCHAR(100),
    Semester INT,
    Year INT,
    Mobile VARCHAR(15),
    Email VARCHAR(255),
    School VARCHAR(100),
    Parent_Name VARCHAR(100),
    DOB DATE,
    Address VARCHAR(255)
);

CREATE TABLE attendance (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID VARCHAR(50),
    Name VARCHAR(100),
    Date DATE,
    Time TIME,
    Status ENUM('Present', 'Absent') DEFAULT 'Present',
    FOREIGN KEY (StudentID) REFERENCES student(StudentID)
);
```

### Step 5: Update Database Credentials
Edit `database.py`:
```python
DB_PASSWORD = "your_mysql_password"  # Update this with your MySQL password
```

### Step 6: Create Required Folders
```bash
mkdir Faces
mkdir Images
mkdir models
```

### Step 7: Add Logo Image
- Place all logos like `Makaut_logo.png` in `Images/` folder

### Step 8: Run Application
```bash
python main.py
```

---

## 📁 Project Structure

```
Smart Hybrid Face Recognition Attendance System/
│
├── Core Application Files
│   ├── main.py                      # Entry point
│   ├── login.py                     # Login interface (Admin only)
│   ├── register.py                  # User registration (Sign up as User)
│   ├── dashboard.py                 # Main dashboard
│   ├── database.py                  # Database connection handlers
│   └── newvxt.py                    # Additional config
│
├── Functional Modules
│   ├── student.py                   # Student management (CRUD)
│   ├── attendance.py                # Attendance tracking & reporting
│   ├── face_recognition.py          # Face recognition engine + email alerts
│   ├── train.py                     # Model training script
│   ├── face_recognition_ui.py       # Face recognition interface
│   ├── classifier.xml               # Face detection cascade file
│   └── harrcascade_frontalface_default.xml  # Get in Github OpenCv 
│
├── Data Directories
│   ├── Faces/                       # Face image dataset (per student)
│   │   ├── 1001/                    # Student ID folders
│   │   ├── 1234/
│   │   ├── 1234/
│   │   └── ...
│   │
│   ├── Images/                      # UI images & logos
│   │   └── Makaut_logo.png
│   │
│   ├── models/                      # ML models
│   │   ├── label_encoder.pkl        # LabelEncoder (student IDs)
│   │   └── svm_facenet_model.pkl    # Trained SVM classifier
│   │
│   └── Attendance/                  # Attendance logs (private)
│       ├── Attendance.csv
│       └── face_recognised_attendance.csv
│
├── Configuration
│   ├── requirements.txt             # Python dependencies
│   ├── .gitignore                   # Git ignore rules
│   ├── .gitattributes               # Git attributes
│   ├── LICENSE                      # MIT License
│   └── README.md                    # This file
└──
```

---

## 💻 Usage Guide

### 1️⃣ Login Screen (login.py)
```
1. Run: python main.py
2. Enter Admin Email & Password or Register 
3. Click "Login" button
4. Use "Forgot Password?" for password recovery
```

**Login Notes:**
- Admin credentials are created in MySQL terminal first
- Only Admin can access the system
- Regular users cannot login directly
- Password recovery sends to registered email

### 2️⃣ Sign Up / Register (register.py)
```
From Login Screen → Click "Sign Up"

Fill Details:
- Email (Username)
- First Name
- Last Name
- Mobile Number
- Password

Note: All new registrations are signed up as "User" role
      Users are managed through student database
```

### 3️⃣ Register New Student (student.py)
```
From Dashboard → Student Management → Add Student

Fill Details:
- Student ID (1001, 1234, etc.)
- Name
- Department (CS, IT, etc.)
- Course (AI, ML, etc.)
- Semester, Year
- Mobile, Email
- School, Parent Name, DOB, Address

Click "Take Samples" → Capture 100 face images
```

### 4️⃣ Train the Model (train.py)
```
From Dashboard → Train Model

Process:
1. Extracts FaceNet embeddings from all Faces/ folders
2. Encodes student IDs using LabelEncoder
3. Trains SVM classifier on embeddings
4. Saves: label_encoder.pkl & svm_facenet_model.pkl
5. Shows: "Hybrid Model Training completed successfully!"

Time: 2-5 minutes depending on dataset size
```

### 5️⃣ Mark Attendance (face_recognition.py)
```
From Dashboard → Face Recognition

Process:
1. Webcam activates automatically
2. Real-time face detection starts
3. Compares face with trained model
4. Auto-marks attendance if match found (confidence > threshold)
5. Shows: ID, Name, Confidence Score
6. Sends email confirmation to student
7. Prevents duplicate marking (same day)
```

**Status Indicators:**
```
🟢 Green: Scanning...
🔵 Cyan: "Please Blink!" (face verification - liveness detection)
🟡 Orange: "Please Blink! (X)" (multiple blink attempts)
🟢 Green: "Attendance: Saved" ✓
```

### 6️⃣ View Attendance Reports (attendance.py)
```
From Dashboard → Attendance

Features:
- View all attendance records in table format
- Columns: ID, StudentID, Name, Date, Time, Status
- Filter by date range
- Export to CSV file
- Search functionality
```

### 7️⃣ Manage Students (student.py)
```
From Dashboard → Student Management

Operations:
- ✏️ Update student info (click row, modify, update)
- 🗑️ Delete student record
- 🔍 Search by ID/Name
- View all registered students
```

### 8️⃣ Forgot Password (login.py)
```
From Login Screen → Click "Forgot Password?"

1. Enter registered admin email
2. System retrieves password from database
3. Sends password to email via SMTP
4. Email received with admin credentials
```

---

## 🏗️ System Architecture

![System Architecture](Screenshots/system_architecture.jpg)

---

## 🗄️ Database Schema

### Credentials Database (`credentials`)

#### Table: `details`

![Credentials Table](Screenshots/credentials_table.jpg)

```
Column      | Type         | Constraint  | Purpose
------------|--------------|-------------|------------------------
Email       | VARCHAR(255) | PRIMARY KEY | Unique user identifier
FirstName   | VARCHAR(100) | -           | User first name
LastName    | VARCHAR(100) | -           | User last name
Mobile      | VARCHAR(15)  | -           | Contact number
Password    | VARCHAR(100) | -           | Login password
Role        | ENUM         | -           | 'User' or 'Admin'
```

**Admin Sample Data:**
```
Email: admin@example.com
FirstName: Admin
LastName: User
Mobile: 1234567890
Password: admin123
Role: Admin
```

### FRS Database (`frs`)

#### Table: `student`

![Student Table](Screenshots/student_table.jpg)

```
Column      | Type         | Constraint  | Purpose
------------|--------------|-------------|------------------------
StudentID   | VARCHAR(50)  | PRIMARY KEY | Unique student ID
Name        | VARCHAR(100) | -           | Student name
Department  | VARCHAR(50)  | -           | CS, IT, etc.
Course      | VARCHAR(100) | -           | AI, ML, Web Dev, etc.
Semester    | INT          | -           | Current semester
Year        | INT          | -           | Graduation year
Mobile      | VARCHAR(15)  | -           | Contact number
Email       | VARCHAR(255) | -           | Email address
School      | VARCHAR(100) | -           | Institute name
Parent_Name | VARCHAR(100) | -           | Parent/Guardian name
DOB         | DATE         | -           | Date of birth
Address     | VARCHAR(255) | -           | Residential address
```

**Sample Data:**
```
StudentID: 1234
Name: ujjwal
Department: CS
Course: AI
Semester: 7
Year: 2022
Mobile: 9876543210
Email: ujjwal@gmail.com
School: makaut
Parent_Name: ujjwal kamila
DOB: 2000-12-11
Address: kalyani
```

#### Table: `attendance`

![Attendance Table](Screenshots/attendance_table.jpg)

```
Column      | Type         | Constraint  | Purpose
------------|--------------|-------------|------------------------
ID          | INT          | PRIMARY KEY | Auto-increment ID
StudentID   | VARCHAR(50)  | FOREIGN KEY | Reference to student
Name        | VARCHAR(100) | -           | Student name
Date        | DATE         | -           | Attendance date
Time        | TIME         | -           | Mark time
Status      | ENUM         | -           | 'Present' or 'Absent'
```

**Sample Data:**
```
ID: 1
StudentID: 1234
Name: ujjwal
Date: 2026-06-01
Time: 14:49:17
Status: Present

ID: 2
StudentID: 1001
Name: roni
Date: 2026-06-01
Time: 15:20:45
Status: Present
```

---

## 📸 Screenshots

### Login Screen
![Login Screen](Screenshots/login_screen.jpg)

### Dashboard
![Dashboard](Screenshots/dashboard.jpg)

### Student Registration
![Student Registration](Screenshots/student_registration.jpg)

### Face Recognition
![Face Recognition](Screenshots/face_recognition.jpg)

### Attendance Report
![Attendance Report](Screenshots/attendance_report.jpg)

### Model Training
![Model Training](Screenshots/model_training.jpg)

---

## ⚙️ Configuration

### `database.py` - Database Connection
```python
DB_PASSWORD = "Ujjwal@81"  # Update with your MySQL password
```

### `login.py` - Email Configuration
```python
sender_email = "ujjwalkamila86@gmail.com"
sender_password = "bdrj vxxz jlha bwyj"  # Gmail app password
```

### `face_recognition.py` - Model Parameters
```python
DETECTION_CONFIDENCE = 0.5       # Face detection sensitivity
RECOGNITION_THRESHOLD = 0.6      # Minimum confidence for match
MAX_ATTEMPTS = 3                 # Blink verification attempts
FRAME_RATE = 30                  # Camera FPS
```

### `main.py` - TensorFlow Optimization
```python
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'   # Disable oneDNN
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # Hide TF logs
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'   # Force CPU mode
```

---

## 🔧 Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| **Camera not detected** | Device not connected | Check camera connection, restart app |
| **Poor face recognition** | Bad lighting/angles | Capture samples in good light, retrain |
| **MySQL connection error** | Wrong credentials | Update DB_PASSWORD in database.py |
| **Email not sending** | SMTP auth failed | Use Gmail app password, enable 2FA |
| **Model training fails** | Empty Faces/ folder | Ensure Faces/StudentID/ has images |
| **Duplicate attendance** | Same-day marking | System prevents this automatically |
| **TensorFlow warnings** | Library logs | These are suppressed in main.py |
| **Blinking not detected** | Lighting issue | Improve camera lighting conditions |
| **"Please Blink!" stays on** | Liveness detection fails | Try different angles/lighting |
| **Attendance CSV export fails** | Permission denied | Check folder write permissions |
| **Login fails** | Not admin account | Only admin accounts can login |

---

## 📧 Email Setup Guide

### Using Gmail (Recommended)
1. Go to Google Account: myaccount.google.com
2. Enable 2-Step Verification
3. Generate App Password (16 characters)
4. Use in `login.py` and `face_recognition.py`

### Current Configuration
```
Sender: ujjwalkamila86@gmail.com
App Password: bdrj vxxz jlha bwyj
SMTP Server: smtp.gmail.com
Port: 587
```

### Email Templates

**Attendance Confirmation:**
```
Subject: Attendance Successfully Marked

Hello ujjwal,

Your attendance for today has been successfully recorded at 20:09:59 
via Face Recognition System.

Thank you!
```

**Password Recovery:**
```
Subject: Password Recovery

Hello,

Your registered password has been sent to your email.

Please keep it safe.
```

---

## 🎓 How It Works - Technical Details

### Face Recognition Pipeline

#### Training Phase (train.py)
```
1. Load images from Faces/StudentID/ directories
2. For each image:
   a) Detect face using OpenCV Cascade Classifier
   b) Extract face region (crop & resize to 160x160)
   c) Generate 128-D embedding using FaceNet
3. Encode Student IDs: 0, 1, 2, ... using LabelEncoder
4. Train SVM classifier:
   - Input: Face embeddings (128 dimensions)
   - Output: Student ID (0-n)
   - Kernel: RBF (Radial Basis Function)
5. Save models:
   - label_encoder.pkl (stores mapping)
   - svm_facenet_model.pkl (trained classifier)
```

#### Recognition Phase (face_recognition.py)
```
1. Capture frame from webcam (30 FPS)
2. Detect faces using Cascade Classifier
3. For each detected face:
   a) Extract face region (160x160)
   b) Generate FaceNet embedding
   c) Pass to SVM classifier
   d) Get prediction + confidence score
4. If confidence > threshold (0.6):
   a) Get student ID from LabelEncoder
   b) Mark attendance in database
   c) Send email notification
   d) Prevent duplicate (check same-day record)
5. Display: ID, Name, Confidence Score
```

### FaceNet Embeddings
- **Input**: Face image (160x160 pixels)
- **Process**: Deep CNN extracts features
- **Output**: 128-dimensional vector
- **Property**: Similar faces have close embeddings

### SVM Classifier
- **Training**: Learns decision boundaries between student embeddings
- **Kernel**: RBF for non-linear separation
- **Confidence**: Distance from decision boundary
- **Decision**: Max probability class

---

## 📊 Sample Outputs

### Console Training Output
```
Training Started...
Processing: 1234/ujjwal
Embedding 1 extracted: [0.23, -0.15, 0.89, ...]
Embedding 2 extracted: [0.22, -0.14, 0.88, ...]
Embedding 3 extracted: [0.24, -0.16, 0.87, ...]
...
Hybrid Model Training completed successfully!
Saved as svm_facenet_model.pkl
```

### Real-time Recognition Output
```
Frame 1: Scanning...
Frame 2: Scanning...
Frame 3: ID: 1234 | Name: ujjwal | Scanning: 59%
Frame 4: ID: 1234 | Name: ujjwal | Please Blink! (1)
Frame 5: ID: 1234 | Name: ujjwal | Scanning: 89%
Frame 6: ID: 1234 | Name: ujjwal | Attendance: Saved ✓
```

### Database Query Results
```sql
SELECT * FROM attendance 
WHERE Date = '2026-06-01' 
ORDER BY Time;

ID | StudentID | Name    | Date       | Time     | Status
1  | 1234      | ujjwal  | 2026-06-01 | 14:49:17 | Present
2  | 1001      | roni    | 2026-06-01 | 15:20:45 | Present
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/YourFeature`
3. Make changes and test thoroughly
4. Commit: `git commit -m 'Add YourFeature'`
5. Push: `git push origin feature/YourFeature`
6. Create Pull Request

**Guidelines:**
- Follow PEP 8 style guide
- Add comments for complex logic
- Test with multiple users
- Update README if adding features

---

## 📄 License

MIT License © 2026 Ujjwal Kamila

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

See `LICENSE` file for full details.

---

## 👨‍💻 Author & Contact

**Ujjwal Kamila**
- **Email**: ujjwalkamila86@gmail.com
- **Project**: Smart Hybrid Face Recognition Attendance System
- **Version**: 1.0
- **Last Updated**: June 4, 2026

---

## 🎯 Project Goals

✅ Eliminate manual attendance marking
✅ Provide real-time face recognition
✅ Maintain student privacy with encrypted passwords
✅ Generate accurate attendance reports
✅ Send instant email notifications
✅ Easy student profile management
✅ Scalable for institutional use

---

## 📞 Support & FAQs

### FAQ

**Q: Can I use a different email provider?**
A: Yes, update SMTP settings in `login.py` and `face_recognition.py`

**Q: How many students can be registered?**
A: Unlimited (depends on disk space for face images)

**Q: What's the accuracy rate?**
A: 95%+ with good lighting and 50+ samples per student

**Q: Can I modify the database schema?**
A: Yes, update database.py and adjust code accordingly

**Q: How do I backup attendance data?**
A: Export CSV from Attendance module or MySQL dump

**Q: Can I run this on Mac/Linux?**
A: Yes, update file paths and email credentials

**Q: How do I create an admin account?**
A: Create admin in MySQL terminal with Role='Admin' before running app

**Q: Can regular users login?**
A: No, only admin accounts can login. Regular users are managed through student database

---

**For issues, suggestions, or contributions, please contact ujjwalkamila86@gmail.com**

Last Updated: June 4, 2026 | Version: 1.0