import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        self.root.geometry("1200x800")
        
        # Database Connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Blackshadow8080800821",
            database="attendance_syste"
        )
        self.cursor = self.db.cursor(buffered=True)
        
        # Track changes
        self.attendance_changes = {}
        
        # Create GUI
        self.create_gui()
        
    def create_gui(self):
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        # Create Tabs
        self.create_student_tab()
        self.create_subject_tab()
        self.create_attendance_tab()
        self.create_reports_tab()
    
    def create_student_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Student Management")
        
        # Student Form
        tk.Label(tab, text="URN:").grid(row=0, column=0, padx=10, pady=5)
        self.urn_entry = tk.Entry(tab)
        self.urn_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(tab, text="Name:").grid(row=1, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(tab)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(tab, text="Email:").grid(row=2, column=0, padx=10, pady=5)
        self.email_entry = tk.Entry(tab)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(tab, text="Phone:").grid(row=3, column=0, padx=10, pady=5)
        self.phone_entry = tk.Entry(tab)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(tab, text="Class:").grid(row=4, column=0, padx=10, pady=5)
        self.class_entry = tk.Entry(tab)
        self.class_entry.grid(row=4, column=1, padx=10, pady=5)
        
        tk.Button(tab, text="Add Student", command=self.add_student).grid(row=5, column=0, columnspan=2, pady=10)
        
        # Student List
        self.student_tree = ttk.Treeview(tab, columns=("URN", "Name", "Email", "Phone", "Class"), show="headings")
        self.student_tree.heading("URN", text="URN")
        self.student_tree.heading("Name", text="Name")
        self.student_tree.heading("Email", text="Email")
        self.student_tree.heading("Phone", text="Phone")
        self.student_tree.heading("Class", text="Class")
        self.student_tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.student_tree.yview)
        scrollbar.grid(row=6, column=2, sticky="ns")
        self.student_tree.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        tab.grid_rowconfigure(6, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        
        self.load_students()
    
    def create_subject_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Subject Management")
        
        # Subject Form
        tk.Label(tab, text="Subject Name:").grid(row=0, column=0, padx=10, pady=5)
        self.subject_entry = tk.Entry(tab)
        self.subject_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Button(tab, text="Add Subject", command=self.add_subject).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Subject List
        self.subject_tree = ttk.Treeview(tab, columns=("ID", "Name"), show="headings")
        self.subject_tree.heading("ID", text="ID")
        self.subject_tree.heading("Name", text="Name")
        self.subject_tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.subject_tree.yview)
        scrollbar.grid(row=2, column=2, sticky="ns")
        self.subject_tree.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        tab.grid_rowconfigure(2, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        
        self.load_subjects()
    
    def create_attendance_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Mark Attendance")
        
        # Date Selection
        tk.Label(tab, text="Date:").grid(row=0, column=0, padx=10, pady=5)
        self.attendance_date = tk.Entry(tab)
        self.attendance_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.attendance_date.grid(row=0, column=1, padx=10, pady=5)
        
        # Subject Selection
        tk.Label(tab, text="Subject:").grid(row=0, column=2, padx=10, pady=5)
        self.attendance_subject = ttk.Combobox(tab)
        self.attendance_subject.grid(row=0, column=3, padx=10, pady=5)
        
        # Load Button
        tk.Button(tab, text="Load Students", command=self.load_attendance_sheet).grid(row=0, column=4, padx=10, pady=5)
        
        # Attendance Sheet Frame
        self.sheet_frame = ttk.Frame(tab)
        self.sheet_frame.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
        
        # Action Buttons Frame
        action_frame = ttk.Frame(tab)
        action_frame.grid(row=2, column=0, columnspan=5, pady=10)
        
        # Save Button
        tk.Button(action_frame, text="Save Changes", command=self.save_attendance, 
                 bg="#4CAF50", fg="white").pack(side="left", padx=5)
        
        # Discard Button
        tk.Button(action_frame, text="Discard Changes", command=self.discard_changes,
                 bg="#f44336", fg="white").pack(side="left", padx=5)
        
        # Configure grid weights
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        
        # Load subjects
        self.load_subject_combo()
    
    def create_reports_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Reports")
        
        # Report Type
        tk.Label(tab, text="Report Type:").grid(row=0, column=0, padx=10, pady=5)
        self.report_type = ttk.Combobox(tab, values=["Daily Attendance", "Student Summary"])
        self.report_type.grid(row=0, column=1, padx=10, pady=5)
        self.report_type.bind("<<ComboboxSelected>>", self.load_report)
        
        # Report Table
        self.report_tree = ttk.Treeview(tab)
        self.report_tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.report_tree.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.report_tree.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
    
    # Database Methods
    def add_student(self):
        try:
            self.cursor.execute(
                "INSERT INTO Students (urn, name, email, phone, class) VALUES (%s, %s, %s, %s, %s)",
                (
                    self.urn_entry.get(),
                    self.name_entry.get(),
                    self.email_entry.get(),
                    self.phone_entry.get(),
                    self.class_entry.get()
                )
            )
            self.db.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            self.load_students()
            # Clear form
            self.urn_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.class_entry.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add student: {err}")
    
    def add_subject(self):
        try:
            self.cursor.execute(
                "INSERT INTO Subjects (subject_name) VALUES (%s)",
                (self.subject_entry.get(),)
            )
            self.db.commit()
            messagebox.showinfo("Success", "Subject added successfully!")
            self.load_subjects()
            self.load_subject_combo()
            # Clear form
            self.subject_entry.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add subject: {err}")
    
    def load_subject_combo(self):
        self.cursor.execute("SELECT subject_id, subject_name FROM Subjects")
        self.attendance_subject["values"] = [f"{id} - {name}" for (id, name) in self.cursor]
    
    def load_attendance_sheet(self):
        # Clear existing sheet and reset changes
        for widget in self.sheet_frame.winfo_children():
            widget.destroy()
        self.attendance_changes = {}
        
        # Get selected subject and date
        subject_id = self.attendance_subject.get().split(" - ")[0] if self.attendance_subject.get() else None
        date = self.attendance_date.get()
        
        if not subject_id or not date:
            messagebox.showwarning("Warning", "Please select a subject and date")
            return
        
        # Store current subject and date
        self.current_subject_id = subject_id
        self.current_date = date
        
        # Create headers
        headers = ["URN", "Name", "Class", "Status", "Action"]
        for col, header in enumerate(headers):
            tk.Label(self.sheet_frame, text=header, relief="ridge", font=('Arial', 10, 'bold'), 
                   width=15, bg="#f0f0f0").grid(row=0, column=col, sticky="nsew")
        
        # Get all students
        self.cursor.execute("SELECT urn, name, class FROM Students ORDER BY urn")
        students = self.cursor.fetchall()
        
        # Create attendance sheet rows
        for row, (urn, name, class_) in enumerate(students, start=1):
            # Student info
            tk.Label(self.sheet_frame, text=urn, relief="ridge", width=15).grid(
                row=row, column=0, sticky="nsew")
            tk.Label(self.sheet_frame, text=name, relief="ridge", width=15).grid(
                row=row, column=1, sticky="nsew")
            tk.Label(self.sheet_frame, text=class_, relief="ridge", width=15).grid(
                row=row, column=2, sticky="nsew")
            
            # Check current attendance status
            self.cursor.execute(
                "SELECT status FROM Attendance WHERE urn=%s AND subject_id=%s AND date=%s",
                (urn, subject_id, date))
            existing = self.cursor.fetchone()
            current_status = existing[0] if existing else "Not Marked"
            
            # Status display with color coding
            status_var = tk.StringVar(value=current_status)
            status_label = tk.Label(self.sheet_frame, textvariable=status_var, 
                                  relief="ridge", width=15)
            status_label.grid(row=row, column=3, sticky="nsew")
            
            # Set initial color
            self.update_status_color(status_var, status_label)
            
            # Action buttons
            btn_frame = tk.Frame(self.sheet_frame)
            btn_frame.grid(row=row, column=4, sticky="nsew")
            
            present_btn = tk.Button(btn_frame, text="Present", width=7,
                                  command=lambda v=status_var, l=status_label: self.set_status(v, l, "Present"))
            present_btn.pack(side="left", padx=2)
            
            absent_btn = tk.Button(btn_frame, text="Absent", width=7,
                                  command=lambda v=status_var, l=status_label: self.set_status(v, l, "Absent"))
            absent_btn.pack(side="left", padx=2)
            
            # Store the status for saving
            self.attendance_changes[urn] = {
                'status_var': status_var,
                'status_label': status_label,
                'original_status': current_status
            }
        
        # Configure grid weights
        for i in range(len(headers)):
            self.sheet_frame.grid_columnconfigure(i, weight=1)

    def set_status(self, status_var, status_label, status):
        # Confirm change for existing records
        current_value = status_var.get()
        if current_value != "Not Marked":
            if not messagebox.askyesno("Confirm", "Change existing attendance record?"):
                return
        
        status_var.set(status)
        self.update_status_color(status_var, status_label)

    def update_status_color(self, status_var, status_label):
        status = status_var.get()
        if status == "Present":
            status_label.config(bg="#d4edda")  # Light green
        elif status == "Absent":
            status_label.config(bg="#f8d7da")  # Light red
        else:
            status_label.config(bg="#fff3cd")  # Light yellow for not marked

    def save_attendance(self):
        if not hasattr(self, 'current_subject_id') or not hasattr(self, 'current_date'):
            messagebox.showwarning("Warning", "Please load attendance sheet first")
            return
        
        try:
            changes_made = False
            for urn, data in self.attendance_changes.items():
                original_status = data['original_status']
                current_status = data['status_var'].get()
                
                # Only update if status changed
                if original_status != current_status:
                    changes_made = True
                    
                    if original_status == "Not Marked":
                        # Insert new record
                        self.cursor.execute(
                            "INSERT INTO Attendance (urn, subject_id, date, status) VALUES (%s, %s, %s, %s)",
                            (urn, self.current_subject_id, self.current_date, current_status))
                    else:
                        # Update existing record
                        self.cursor.execute(
                            "UPDATE Attendance SET status=%s WHERE urn=%s AND subject_id=%s AND date=%s",
                            (current_status, urn, self.current_subject_id, self.current_date))
            
            if changes_made:
                self.db.commit()
                messagebox.showinfo("Success", "Attendance changes saved successfully!")
                # Reload to show updated original status
                self.load_attendance_sheet()
            else:
                messagebox.showinfo("Info", "No changes to save")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to save attendance: {err}")
            self.db.rollback()
    
    def discard_changes(self):
        if hasattr(self, 'current_subject_id') and hasattr(self, 'current_date'):
            self.load_attendance_sheet()
        else:
            messagebox.showwarning("Warning", "No attendance sheet loaded to discard")

    def load_report(self, event=None):
        for row in self.report_tree.get_children():
            self.report_tree.delete(row)
        
        report_type = self.report_type.get()
        
        if report_type == "Daily Attendance":
            self.report_tree["columns"] = ("URN", "Name", "Subject", "Date", "Status")
            for col in self.report_tree["columns"]:
                self.report_tree.heading(col, text=col)
                self.report_tree.column(col, width=150, anchor='center')
            
            self.cursor.execute("""
                SELECT s.urn, s.name, sub.subject_name, a.date, a.status 
                FROM Attendance a
                JOIN Students s ON a.urn = s.urn
                JOIN Subjects sub ON a.subject_id = sub.subject_id
                ORDER BY a.date DESC, s.urn
            """)
            for row in self.cursor:
                self.report_tree.insert("", "end", values=row)
        
        elif report_type == "Student Summary":
            self.report_tree["columns"] = ("URN", "Name", "Class", "Total Days", "Present Days", "Percentage")
            for col in self.report_tree["columns"]:
                self.report_tree.heading(col, text=col)
                self.report_tree.column(col, width=120, anchor='center')
            
            self.cursor.execute("""
                SELECT 
                    urn, 
                    name, 
                    class, 
                    total_days, 
                    present_days,
                    CASE 
                        WHEN total_days = 0 THEN '0.00%'
                        ELSE CONCAT(FORMAT(attendance_percentage, 2), '%')
                    END AS percentage
                FROM Attendance_Summary 
                ORDER BY urn
            """)
            
            for row in self.cursor:
                self.report_tree.insert("", "end", values=row)
    
    def load_students(self):
        for row in self.student_tree.get_children():
            self.student_tree.delete(row)
        
        self.cursor.execute("SELECT urn, name, email, phone, class FROM Students ORDER BY urn")
        for row in self.cursor:
            self.student_tree.insert("", "end", values=row)
    
    def load_subjects(self):
        for row in self.subject_tree.get_children():
            self.subject_tree.delete(row)
        
        self.cursor.execute("SELECT subject_id, subject_name FROM Subjects ORDER BY subject_name")
        for row in self.cursor:
            self.subject_tree.insert("", "end", values=row)
    
    def __del__(self):
        if hasattr(self, 'db') and self.db.is_connected():
            self.cursor.close()
            self.db.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop()