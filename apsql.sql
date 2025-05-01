CREATE DATABASE IF NOT EXISTS attendance_syste;
USE attendance_syste;

-- Students Table
CREATE TABLE IF NOT EXISTS Students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    urn VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    class VARCHAR(50)
);

-- Subjects Table
CREATE TABLE IF NOT EXISTS Subjects (
    subject_id INT PRIMARY KEY AUTO_INCREMENT,
    subject_name VARCHAR(100) NOT NULL
);

-- Attendance Table
CREATE TABLE IF NOT EXISTS Attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    urn VARCHAR(20),
    subject_id INT,
    date DATE NOT NULL,
    status ENUM('Present', 'Absent') DEFAULT 'Absent',
    FOREIGN KEY (urn) REFERENCES Students(urn),
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id),
    UNIQUE KEY (urn, subject_id, date)
);

-- Enhanced Attendance Summary View (with correct ROUND syntax)
CREATE OR REPLACE VIEW Attendance_Summary AS
SELECT 
    s.urn,
    s.name,
    s.class,
    COUNT(a.status) AS total_days,
    SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS present_days,
    CASE 
        WHEN COUNT(a.status) = 0 THEN 0
        ELSE ROUND(
            SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) * 100.0 / COUNT(a.status),
        2)
    END AS attendance_percentage
FROM Students s
LEFT JOIN Attendance a ON s.urn = a.urn
GROUP BY s.urn, s.name, s.class;
