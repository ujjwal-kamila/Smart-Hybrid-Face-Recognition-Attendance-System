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
- ✅ Manual attendance management

---

## ✨ Features

### 🔐 Authentication & Login
- Email-based login system (login.py)
- Password recovery via email with automatic sending
- Admin and User authentication
- All new users sign up as regular users by default
- Credentials stored securely in MySQL
- Forgot Password functionality with email integration

### 👤 Student Management (student.py)
- Register new students with details:
  - Student ID, Name, Department, Course
  - Semester, Year, Mobile, Email
  - School, Parent Name, DOB, Address
- Real-time dataset capture (100+ face samples)
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
- Spoofing detection (anti-fake face presentation)

### 📊 Attendance Management (attendance.py)
- Auto-detection and marking via face recognition
- Manual attendance management (Admin only)
- Admin can update attendance status: Present ↔ Absent
- Prevents duplicate attendance (same day auto-detection)
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
- Manual update capability

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
source venv/bin/activate
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
│   ├── login.py                     # Login interface (Admin & User)
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
│   │   ├── Makaut_logo.png
│   │   └── Screenshots/             # Application screenshots
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

![Login Screen](Images/Screenshots/login_screen.png)

```
1. Run: python main.py
2. Enter Email & Password
3. Select Role: Admin or User
4. Click "Login" button
5. Use "Forgot Password?" for password recovery
```

**Login Options:**
- **Admin Login**: Access full system including manual attendance management
- **User Login**: Limited access to system features
- **Password Recovery**: Automatic email sending

---

### 2️⃣ Sign Up / Register (register.py)

![Sign Up Screen](Images/Screenshots/register_screen.png)

```
From Login Screen → Click "Sign Up"

Fill Details:
- Email (Username)
- First Name
- Last Name
- Mobile Number
- Password
- Confirm Password

Note: All new registrations are signed up as "User" role
      Users can later be promoted to Admin in database
```

---

### 3️⃣ Dashboard Navigation

![Dashboard](Images/Screenshots/dashboard.png)

```
Main Dashboard Features:
- 👤 Student Details - Register and manage students
- 📋 Attendance Records - View/manage attendance
- 📸 Face Recognition - Real-time attendance marking
- 🧠 Train Model - Train hybrid ML model
- 👥 Manage Face Samples - Capture face images
- ❌ Exit - Close application
```

---

### 4️⃣ Register New Student (student.py)

![Student Details Page](Images/Screenshots/student_details_page.png)

```
From Dashboard → Student Details

Fill Student Information:
- Student ID (1001, 1234, etc.)
- Name
- Department (CS, IT, etc.)
- Course (AI, ML, Web Dev, etc.)
- Semester, Year
- Mobile, Email
- School Name, Parent Name
- Date of Birth, Address

Operations:
- Save: Add new student
- Update: Modify existing student
- Delete: Remove student record
- Take Photo Sample: Capture 100 face images

Buttons:
- Save → Save student details
- Update → Update after modifications
- Delete → Remove from database
- Take Photo Sample → Capture face dataset
- Reset → Clear all fields
- Back → Return to dashboard
```

---

### 5️⃣ Train the Hybrid Model (train.py)

![Training Started](Images/Screenshots/training_start.png)
![Training Completed](Images/Screenshots/trained_successfully.png)

```
From Dashboard → Train Model

Process:
1. System reads all face images from Faces/StudentID/ folders
2. Extracts FaceNet embeddings (128-dimensional vectors)
3. Encodes student IDs using LabelEncoder
4. Trains SVM classifier with RBF kernel
5. Saves two model files:
   - label_encoder.pkl (Student ID mappings)
   - svm_facenet_model.pkl (Trained classifier)
6. Shows completion message

Status Messages:
- "Training Started. Click OK to watch the training progress..."
- "Hybrid Model Training completed successfully! Saved as svm_facenet_model.pkl"

Training Time: 2-5 minutes depending on:
- Number of students
- Number of samples per student
- System specifications
```

---

### 6️⃣ Real-time Face Recognition (face_recognition.py)

![Face Recognition - Scanning](Images/Screenshots/check_liveness_using_fake_phone_photo.png)
![Face Recognition - Detected](Images/Screenshots/check_using_fake_phone_photo.png)
![Liveness Check Failed](Images/Screenshots/failed_detect_using_fake_phone_photo.png)

```
From Dashboard → Face Recognition

Real-time Attendance Process:
1. Webcam activates automatically
2. Frame capture starts (30 FPS)
3. Real-time face detection
4. Face region extracted and resized (160x160)
5. FaceNet embedding generated
6. Compared against trained SVM model
7. Liveness check: "Please Blink!" verification
8. If match found & alive:
   - Mark attendance in database
   - Send email confirmation
   - Display success message

Status Indicators:
🟠 Orange: "Scanning..." (searching for face)
🔵 Cyan: "Please Blink!" (liveness verification)
🟡 Yellow: "Please Blink! (1/2/3)" (blink attempt counter)
🔴 Red: "Spoofing Detected or No Blink" (anti-spoofing alert)
🟢 Green: Attendance marked successfully ✓
```

**Anti-Spoofing Features:**
- Blink detection required
- Fake phone photo detection
- 3D face verification
- Real-time face presentation detection

---

### 7️⃣ Manual Attendance Management (attendance.py)

**ADMIN ONLY FEATURE**

![Manual Attendance Management](Images/Screenshots/manual_attendance_managamnet_system.png)

```
From Dashboard → Attendance Records (Admin Access)

Manual Management Features:
1. View all attendance records in table format
   - Columns: ID, StudentID, Name, Date, Time, Status
   
2. Manual Update Capability (Admin Only):
   - Student ID: 1234
   - Name: ujjwal
   - Date: 25/05/2026
   - Time: 12:02:38
   - Status: Change Present ↔ Absent
   
3. Update Attendance Status:
   - Select a record from the table
   - Click status dropdown (Present/Absent)
   - Click "Update" button
   - Change is saved to database

4. Admin Operations:
   - Update: Modify attendance (Present/Absent toggle)
   - Reset: Clear all fields
   - Import File: Load attendance from CSV
   - Export File: Save attendance to CSV
   - Back: Return to dashboard

5. Search & Filter:
   - Filter by date range
   - Search by Student ID or Name
   - View all records or specific date

Benefits:
✅ Correct erroneous entries
✅ Add manual entries for absences
✅ Update late markings
✅ Manage special cases
✅ Maintain accurate records
```

---

### 8️⃣ Email Notifications

![Attendance Email](Images/Screenshots/attendance_recorded_mail_to_the_student.png)
![Password Recovery Email](Images/Screenshots/password_recovery_email.jpg)
![Email Sent Notification](Images/Screenshots/email_sent_notification.jpg)
![Password Sent Notification](Images/Screenshots/forget_pass_send_in_mail.png)

```
Automated Email System:

1. Attendance Confirmation Email (Auto-sent):
   Subject: "Attendance Successfully Marked"
   Body: 
   - Student name
   - Date and time marked
   - Confirmation via Face Recognition System
   
2. Password Recovery Email (On Request):
   Subject: "Password Recovery"
   Body:
   - Registered password
   - Security reminder
   
3. Email Notifications:
   Popup confirmations:
   - "Attendance confirmation email sent to: ujjwal@gmail.com"
   - "Password successfully sent to your respected email id."

Email Configuration:
- Sender: ujjwalkamila86@gmail.com
- App Password: bdrj vxxz jlha bwyj
- SMTP: smtp.gmail.com
- Port: 587
```

---

### 9️⃣ Attendance Success Messages

![Success Message](Images/Screenshots/save attendece pop up.png)

```
Confirmation Popups:

1. Attendance Saved Successfully:
   "Attendance successfully saved for ujjwal"
   
2. Record Updated:
   Shows when manual attendance is updated
   
3. Email Confirmation:
   "Attendance confirmation email sent to: ujjwal@gmail.com"
   
4. System Messages:
   Displays during all operations with status updates
```

---

### 🔟 Admin Update Student Data

![Admin Update](Images/Screenshots/admin update studnet data.png)

```
Admin Panel Features:

Admin can:
1. Update Student Information
   - All student fields editable
   - Save changes to database
   - Track modifications

2. Manual Attendance Corrections
   - Change Present → Absent
   - Change Absent → Present
   - Update date/time if needed
   - Correct system errors

3. Attendance Management
   - Override auto-marked records
   - Add manual entries
   - Remove erroneous entries
   - Generate accurate reports

Admin Restrictions:
- Only admin accounts can access these features
- User accounts have limited visibility
- Actions are logged for audit trail
```

---

## 🏗️ System Architecture

![System Architecture](Images/Screenshots/system arch.png)

```
Complete Application Flow:

User Input Layer:
├── Login/Register (login.py, register.py)
├── Student Management (student.py)
├── Attendance Management (attendance.py)
└── Face Recognition (face_recognition.py)

Processing Layer:
├── FaceNet Embeddings (keras-facenet)
├── SVM Classifier (scikit-learn)
├── Face Detection (OpenCV)
└── Liveness Detection (blink verification)

Database Layer:
├── Credentials DB (admin/user accounts)
└── FRS DB (students & attendance)

Output Layer:
├── Email Notifications (SMTP)
├── CSV Reports (attendance.py)
└── Real-time Display (Tkinter GUI)

Flow:
main.py → Login → Dashboard → Modules → Database/Email
```

---

## 🗄️ Database Schema

### Credentials Database (`credentials`)

#### Table: `details`

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

**Sample Data:**
```
Email: admin@example.com | admin123 | Admin
Email: user@example.com | user123 | User
```

### FRS Database (`frs`)

#### Table: `student`

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

#### Table: `attendance`

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

---

## 📸 Screenshots Overview

### Application Screens
- **login_screen.png** - Initial login interface
- **register_screen.png** - User registration form
- **dashboard.png** - Main dashboard with all modules
- **student_details_page.png** - Student management interface
- **admin_update_student_data.png** - Admin panel for updates

### Face Recognition Screens
- **check_liveness_using_fake_phone_photo.png** - Anti-spoofing detection
- **check_using_fake_phone_photo.png** - Fake face detection
- **failed_detect_using_fake_phone_photo.png** - Detection failure alert

### Attendance Management
- **manual_attendance_managamnet_system.png** - Admin attendance control
- **save_attendece_popup.png** - Success confirmation

### Training & Processing
- **training_start.png** - Training initiation
- **trained_successfully.png** - Training completion

### Email & Notifications
- **attendance_recorded_mail_to_the_student.png** - Attendance email
- **password_recovery_email.jpg** - Password recovery email
- **email_sent_notification.jpg** - Email sent confirmation
- **forget_pass_send_in_mail.png** - Password sent notification

### System Diagrams
- **system_arch.png** - Complete system architecture

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
| **Fake face detected** | Spoofing attempt | Use real face, improve lighting |
| **Blink not detected** | Lighting issue | Improve camera lighting conditions |
| **Manual update fails** | Not admin account | Login as admin to update attendance |
| **Cannot change status** | Permission denied | Admin access required for updates |
| **Attendance CSV export fails** | Permission denied | Check folder write permissions |
| **Login fails** | Wrong credentials | Verify email/password in credentials DB |

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

---

## 🎓 How It Works - Technical Details

### Face Recognition Pipeline

#### Training Phase (train.py)
```
1. Load 100+ images per student from Faces/StudentID/
2. For each image:
   a) Detect face using OpenCV Cascade Classifier
   b) Extract face region (crop & resize to 160x160)
   c) Generate 128-D embedding using FaceNet
3. Encode Student IDs: 0, 1, 2, ... using LabelEncoder
4. Train SVM classifier:
   - Input: Face embeddings (128 dimensions)
   - Output: Student ID
   - Kernel: RBF (Radial Basis Function)
5. Save models:
   - label_encoder.pkl
   - svm_facenet_model.pkl
```

#### Recognition Phase (face_recognition.py)
```
1. Capture webcam frames (30 FPS)
2. Detect faces using Cascade Classifier
3. Extract face region & generate embedding
4. Pass to SVM classifier
5. If confidence > 0.6:
   a) Get student ID from LabelEncoder
   b) Verify liveness (blink detection)
   c) Mark attendance if all checks pass
   d) Send email confirmation
   e) Prevent duplicate (same-day check)
```

#### Manual Update Phase (attendance.py - Admin Only)
```
1. Admin selects record from table
2. Changes status: Present ↔ Absent
3. Clicks "Update" button
4. System updates database
5. Changes reflected immediately
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/YourFeature`
3. Make changes and test thoroughly
4. Commit: `git commit -m 'Add YourFeature'`
5. Push: `git push origin feature/YourFeature`
6. Create Pull Request

---

## 📄 License

MIT License © 2026 Ujjwal Kamila

---

## 👨‍💻 Author & Contact

**Ujjwal Kamila**
- **Email**: ujjwalkamila86@gmail.com
- **Project**: Smart Hybrid Face Recognition Attendance System
- **Version**: 1.0
- **Last Updated**: June 4, 2026

---

## 📞 Support & FAQs

### FAQ

**Q: Can I manually update attendance?**
A: Yes, but only admin accounts can update attendance status from Present to Absent or vice versa

**Q: How do I fix erroneous attendance?**
A: Login as admin, go to Attendance section, select record, change status, click Update

**Q: What happens if face recognition fails?**
A: Admin can manually mark attendance using the Manual Attendance Management system

**Q: Can I export attendance records?**
A: Yes, click "Export File" button in Attendance section to save as CSV

**Q: How accurate is the face recognition?**
A: 95%+ with good lighting and 100+ training samples per student

---

**For issues or contributions, contact ujjwalkamila86@gmail.com**

Last Updated: June 4, 2026 | Version: 1.0