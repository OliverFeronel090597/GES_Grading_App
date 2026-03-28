import sqlite3
import os
import random

DB_PATH = "db/school.db"

# ==========================
# DB CONNECTION
# ==========================

def get_db():
    os.makedirs("db", exist_ok=True)
    return sqlite3.connect(DB_PATH)

# ==========================
# INITIALIZE DB STRUCTURE
# ==========================

def init_db():
    con = get_db()
    cur = con.cursor()

    cur.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS Levels (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        LevelName TEXT NOT NULL UNIQUE,
        Category TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Sections (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        SectionName TEXT NOT NULL,
        LevelID INTEGER NOT NULL,
        FOREIGN KEY(LevelID) REFERENCES Levels(ID) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Students (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Guardian TEXT NOT NULL,
        LevelID INTEGER NOT NULL,
        SectionID INTEGER NOT NULL,
        SchoolYear TEXT NOT NULL,
        FOREIGN KEY(LevelID) REFERENCES Levels(ID),
        FOREIGN KEY(SectionID) REFERENCES Sections(ID)
    );

    CREATE TABLE IF NOT EXISTS Subjects (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Subject TEXT NOT NULL,
        Advisor TEXT NOT NULL,
        LevelID INTEGER NOT NULL,
        FOREIGN KEY(LevelID) REFERENCES Levels(ID)
    );

    CREATE TABLE IF NOT EXISTS Grades (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        StudentID INTEGER NOT NULL,
        SubjectID INTEGER NOT NULL,
        Grade TEXT NOT NULL,
        SchoolYear TEXT NOT NULL,
        FOREIGN KEY(StudentID) REFERENCES Students(ID) ON DELETE CASCADE,
        FOREIGN KEY(SubjectID) REFERENCES Subjects(ID) ON DELETE CASCADE
    );
    """)

    con.commit()
    con.close()


# ==========================
# INSERT BASE DATA
# ==========================

def insert_levels(cur):
    levels = [
        ("Kinder", "Preschool"),
        ("Grade 1", "Elementary"),
        ("Grade 2", "Elementary"),
        ("Grade 3", "Elementary"),
        ("Grade 4", "Elementary"),
        ("Grade 5", "Elementary"),
        ("Grade 6", "Elementary"),
    ]

    cur.executemany("INSERT INTO Levels (LevelName, Category) VALUES (?, ?)", levels)


def insert_sections(cur):
    # 7 levels * 3 sections each = 21 sections
    sections = []
    for level_id in range(1, 8):
        level = ["Kinder", "1", "2", "3", "4", "5", "6"][level_id - 1]
        for sec in ["A", "B", "C"]:
            if level == "Kinder":
                sec_name = f"Kinder-{sec}"
            else:
                sec_name = f"{level}-{sec}"
            sections.append((sec_name, level_id))

    cur.executemany("INSERT INTO Sections (SectionName, LevelID) VALUES (?, ?)", sections)


def insert_subjects(cur):
    subjects_by_level = {
        1: ["Math", "English", "Reading"],
        2: ["Math", "English", "Science"],
        3: ["Math", "English", "Science", "Filipino"],
        4: ["Math", "English", "Science", "Filipino", "Araling Panlipunan"],
        5: ["Math", "English", "Science", "Filipino", "AP", "TLE"],
        6: ["Math", "English", "Science", "Filipino", "AP", "TLE", "MAPEH"],
        7: ["Math", "English", "Science", "Filipino", "AP", "TLE", "MAPEH"],
    }

    advisors = ["Mr. Cruz", "Ms. Santos", "Mr. Reyes", "Mr. Ramos", "Ms. Garcia"]

    for level_id, subjects in subjects_by_level.items():
        for subj in subjects:
            advisor = random.choice(advisors)
            cur.execute(
                "INSERT INTO Subjects (Subject, Advisor, LevelID) VALUES (?, ?, ?)",
                (subj, advisor, level_id)
            )


# ==========================
# GENERATE 50 STUDENTS
# ==========================

def insert_students(cur):
    first = ["Alice", "Bob", "Charlie", "Diana", "Evan", "Fiona", "George", "Hannah", "Ivan", "Julia",
             "Kevin", "Lara", "Marco", "Nina", "Oliver", "Paula", "Quinn", "Rico", "Sara", "Tim"]

    last = ["Cruz", "Santos", "Reyes", "Garcia", "Lopez", "Torres", "Ramos", "Dela Cruz"]

    students = []

    for _ in range(50):
        name = f"{random.choice(first)} {random.choice(last)}"
        guardian = f"{random.choice(first)} {random.choice(last)}"

        # Levels 1..7
        level_id = random.randint(1, 7)

        # Each level has 3 sections → (level−1)*3 + 1..3
        section_id = (level_id - 1) * 3 + random.randint(1, 3)

        students.append((name, guardian, level_id, section_id, "2026-2027"))

    cur.executemany("""
        INSERT INTO Students (Name, Guardian, LevelID, SectionID, SchoolYear)
        VALUES (?, ?, ?, ?, ?)
    """, students)


# ==========================
# INSERT GRADES PER STUDENT
# ==========================

def insert_grades(cur):
    cur.execute("SELECT ID, LevelID FROM Students")
    students = cur.fetchall()

    for student_id, level_id in students:
        # Get subjects for this student's level
        cur.execute("SELECT ID FROM Subjects WHERE LevelID = ?", (level_id,))
        subjects = [s[0] for s in cur.fetchall()]

        for subj_id in subjects:
            grade = random.randint(80, 98)
            cur.execute("""
                INSERT INTO Grades (StudentID, SubjectID, Grade, SchoolYear)
                VALUES (?, ?, ?, ?)
            """, (student_id, subj_id, str(grade), "2026-2027"))


# ==========================
# MAIN POPULATION FUNCTION
# ==========================

def populate_all():
    con = get_db()
    cur = con.cursor()

    # Skip if already populated
    cur.execute("SELECT COUNT(*) FROM Students")
    if cur.fetchone()[0] > 0:
        print("Database already populated.")
        con.close()
        return

    insert_levels(cur)
    insert_sections(cur)
    insert_subjects(cur)
    insert_students(cur)
    insert_grades(cur)

    con.commit()
    con.close()
    print("Database fully populated with sample data.")


# ==========================
# RUN
# ==========================

if __name__ == "__main__":
    init_db()
    populate_all()
