# Attendance System (DBMS Project)

A simple **Attendance Management System** built using **Python** and **SQL (Database Management System)** for tracking student attendance.

---

## 📚 Table of Contents
- [Motivation & Goals](#motivation--goals)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technologies Used](#technologies-used)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [How to Contribute](#how-to-contribute)
- [License](#license)
- [Contact](#contact)

---

## 🎯 Motivation & Goals
The goal of this project is to create a streamlined system that:
- Enables instructors to mark and track attendance efficiently.
- Stores attendance data persistently in a database.
- Reduces manual errors and simplifies attendance reports.
- Demonstrates DBMS integration using Python and SQL.

---

## ⚙️ Features
- ➕ Add and manage student records.
- 🕒 Mark students as *present* or *absent* for any date.
- 📋 View attendance history by student or session.
- 📊 Generate attendance percentage reports.
- 💾 Persistent storage in a relational database.

---

## 🧩 System Architecture
1. **Database (SQL)**  
   - Schema defined in `apsql.sql`
   - Tables for students, sessions, and attendance.
   - Primary/foreign keys maintain relationships.

2. **Python Backend**  
   - `finalattendence.py` connects to the database.
   - Handles CRUD operations (Create, Read, Update, Delete).
   - Uses standard DB-API (e.g., `sqlite3`, `mysql.connector`).

3. **Workflow**
   - Initialize database → Run Python script → Interact via console → Save records.

---

## 💻 Technologies Used
- **Python** – application logic
- **SQL** – data management
- **SQLite / MySQL** – database
- *(Optional: Tkinter or CLI for UI)*

---

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/JagdeepKaur-09/Attendance-System-DBMS-project-.git
cd Attendance-System-DBMS-project-
2. Set up the database
If using SQLite:

bash
Copy code
sqlite3 attendance.db < apsql.sql
If using MySQL or PostgreSQL:

Create a new database.

Run the apsql.sql script.

Update DB connection details in finalattendence.py.

3. Install dependencies
bash
Copy code
pip install mysql-connector-python
# or other database driver as needed
4. Run the program
bash
Copy code
python finalattendence.py
🧠 Usage
Add new student records.

Mark attendance for a given date.

View attendance or generate summary reports.

Exit when done — all data remains saved in the database.

🗄️ Database Schema
Tables:

students — stores student info (id, name, class)

sessions — stores class sessions (session_id, date)

attendance — links students & sessions (student_id, session_id, status)
