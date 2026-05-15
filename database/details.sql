-- 1. credentials schema (details.sql)
CREATE DATABASE IF NOT EXISTS credentials;
USE credentials;

CREATE TABLE IF NOT EXISTS details (
  Email varchar(50) NOT NULL,
  First_Name varchar(40) DEFAULT NULL,
  Last_Name varchar(40) DEFAULT NULL,
  Mobile varchar(15) DEFAULT NULL,
  Password varchar(100) DEFAULT NULL,
  PRIMARY KEY (Email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 2. frs schema (students.sql and logs)
CREATE DATABASE IF NOT EXISTS frs;
USE frs;

CREATE TABLE IF NOT EXISTS student (
  StudentID varchar(20) DEFAULT NULL,
  Name varchar(50) DEFAULT NULL,
  Department varchar(50) DEFAULT NULL,
  Course varchar(50) DEFAULT NULL,
  Semester varchar(50) DEFAULT NULL,
  Year year DEFAULT NULL,
  Mobile varchar(50) DEFAULT NULL,
  Email varchar(50) DEFAULT NULL,
  School varchar(50) DEFAULT NULL,
  Parent_Name varchar(50) DEFAULT NULL,
  DOB date DEFAULT NULL,
  Address varchar(100) DEFAULT NULL,
  PRIMARY KEY (StudentID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS attendance_logs (
  LogID int NOT NULL AUTO_INCREMENT,
  StudentID varchar(20) NOT NULL,
  Name varchar(50) DEFAULT NULL,
  Date date DEFAULT NULL,
  Time time DEFAULT NULL,
  Status varchar(20) DEFAULT 'Present',
  PRIMARY KEY (LogID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;