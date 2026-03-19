import sys
import os
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QApplication, QTableView
from PyQt6.QtCore import Qt

DB_NAME = "db/school_qt.db"

# ==========================
# DATABASE INITIALIZATION
# ==========================
def init_db():
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(DB_NAME)

    if not db.open():
        raise RuntimeError("Cannot open database")

    query = QSqlQuery()

    # Create Students
    query.exec("""
    CREATE TABLE IF NOT EXISTS Students (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Guardian TEXT NOT NULL,
        SchoolYear TEXT NOT NULL,
        GradeLevel TEXT NOT NULL
    )
    """)

    # Create Subjects
    query.exec("""
    CREATE TABLE IF NOT EXISTS Subjects (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Subject TEXT NOT NULL,
        Advisor TEXT NOT NULL,
        GradeLevel TEXT NOT NULL
    )
    """)

    # Create Grades
    query.exec("""
    CREATE TABLE IF NOT EXISTS Grades (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentID INTEGER NOT NULL,
        SubjectID INTEGER NOT NULL,
        SchoolYear TEXT NOT NULL,
        Section TEXT NOT NULL,
        Grade TEXT NOT NULL,
        FOREIGN KEY(StudentID) REFERENCES Students(ID) ON DELETE CASCADE,
        FOREIGN KEY(SubjectID) REFERENCES Subjects(ID) ON DELETE CASCADE
    )
    """)

    # Indexes for speed
    query.exec("CREATE INDEX IF NOT EXISTS idx_grades_student ON Grades(StudentID)")
    query.exec("CREATE INDEX IF NOT EXISTS idx_grades_subject ON Grades(SubjectID)")

    return db

# ==========================
# CRUD FUNCTIONS
# ==========================
def add_student(name, guardian, year, grade_level):
    query = QSqlQuery()
    query.prepare("INSERT INTO Students (Name, Guardian, SchoolYear, GradeLevel) VALUES (?, ?, ?, ?)")
    query.addBindValue(name)
    query.addBindValue(guardian)
    query.addBindValue(year)
    query.addBindValue(grade_level)
    return query.exec()

def add_subject(subject, advisor, grade_level):
    query = QSqlQuery()
    query.prepare("INSERT INTO Subjects (Subject, Advisor, GradeLevel) VALUES (?, ?, ?)")
    query.addBindValue(subject)
    query.addBindValue(advisor)
    query.addBindValue(grade_level)
    return query.exec()

def add_grade(student_id, subject_id, school_year, section, grade):
    query = QSqlQuery()
    query.prepare("""
        INSERT INTO Grades (StudentID, SubjectID, SchoolYear, Section, Grade)
        VALUES (?, ?, ?, ?, ?)
    """)
    query.addBindValue(student_id)
    query.addBindValue(subject_id)
    query.addBindValue(school_year)
    query.addBindValue(section)
    query.addBindValue(grade)
    return query.exec()

# ==========================
# SAMPLE DATA INSERTION
# ==========================
def insert_sample_data():
    query = QSqlQuery()

    # Check if Students already exist
    query.exec("SELECT COUNT(*) FROM Students")
    if query.next() and query.value(0) > 0:
        return  # Already populated

    # Students
    students = [
        ("Alice Cruz", "Maria Cruz", "2026-2027", "3"),
        ("Bob Santos", "Juan Santos", "2026-2027", "4"),
        ("Charlie Reyes", "Ana Reyes", "2026-2027", "5"),
    ]
    for s in students:
        add_student(*s)

    # Subjects
    subjects = [
        ("Mathematics", "Mr. Dela Cruz", "3"),
        ("English", "Ms. Garcia", "3"),
        ("Science", "Mr. Ramos", "4"),
        ("Filipino", "Ms. Santos", "5"),
    ]
    for s in subjects:
        add_subject(*s)

    # Grades
    grades = [
        (1, 1, "2026-2027", "3-A", "92"),
        (1, 2, "2026-2027", "3-A", "88"),
        (2, 3, "2026-2027", "4-B", "90"),
        (3, 4, "2026-2027", "5-C", "95"),
    ]
    for g in grades:
        add_grade(*g)

# ==========================
# FETCH FUNCTIONS (for demo)
# ==========================
def fetch_student_grades(student_id):
    query = QSqlQuery()
    query.prepare("""
        SELECT 
            Students.Name AS StudentName,
            Subjects.Subject AS Subject,
            Subjects.Advisor AS Advisor,
            Grades.Grade AS Grade,
            Grades.Section AS Section,
            Grades.SchoolYear AS SY
        FROM Grades
        LEFT JOIN Students ON Students.ID = Grades.StudentID
        LEFT JOIN Subjects ON Subjects.ID = Grades.SubjectID
        WHERE Students.ID = ?
    """)
    query.addBindValue(student_id)
    query.exec()
    results = []
    while query.next():
        results.append({
            "StudentName": query.value("StudentName"),
            "Subject": query.value("Subject"),
            "Advisor": query.value("Advisor"),
            "Grade": query.value("Grade"),
            "Section": query.value("Section"),
            "SY": query.value("SY")
        })
    return results

# ==========================
# DEMO DISPLAY IN QTableView
# ==========================
def show_demo_table():
    from PyQt6.QtSql import QSqlTableModel
    app = QApplication(sys.argv)
    db = QSqlDatabase.database()

    model = QSqlTableModel()
    model.setTable("Grades")
    model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
    model.select()

    view = QTableView()
    view.setModel(model)
    view.setWindowTitle("Grades Table - QtSql Demo")
    view.resize(800, 400)
    view.show()

    sys.exit(app.exec())

# ==========================
# MAIN EXECUTION
# ==========================
if __name__ == "__main__":
    db = init_db()
    insert_sample_data()
    print("=== Alice's Grades ===")
    print(fetch_student_grades(1))

    # Optional: Launch Qt Table Demo
    show_demo_table()
