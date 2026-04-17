import sqlite3
import os
from typing import Optional, List, Dict, Any


class DatabaseConnector:
    def __init__(self):
        self.base_path = "db"
        self.db_path = os.path.join(self.base_path, "PersonalGrading.db")
        self._ensure_directory()
        self._create_tables()

    # ============================================================
    # INTERNAL
    # ============================================================
    def _ensure_directory(self):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def connect(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return None

    def execute(self, query: str, params=(), fetch_one=False, fetch_all=False):
        conn = self.connect()
        if conn is None:
            return None

        cur = conn.cursor()
        try:
            cur.execute(query, params)

            if fetch_one:
                row = cur.fetchone()
                return dict(row) if row else None

            if fetch_all:
                return [dict(r) for r in cur.fetchall()]

            conn.commit()
            return True

        except sqlite3.Error as e:
            print(f"[SQL ERROR] {e}")
            return None

        finally:
            conn.close()

    # ============================================================
    # TABLE CREATION
    # ============================================================
    def _create_tables(self):
        schema = [

            # -----------------------------------------------------
            # LEVELS TABLE
            # -----------------------------------------------------
            """
            CREATE TABLE IF NOT EXISTS Levels (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,   -- Unique level ID
                LevelName TEXT NOT NULL UNIQUE         -- Name of the level (ex: Grade 1)
            );
            """,

            # -----------------------------------------------------
            # SECTIONS TABLE
            # -----------------------------------------------------
            """
            CREATE TABLE IF NOT EXISTS Sections (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,   -- Unique section ID
                SectionName TEXT NOT NULL,              -- Section name (ex: A, St. John)
                LevelID INTEGER NOT NULL                -- Links to Levels.ID (no FK enforcement)
            );
            """,

            # -----------------------------------------------------
            # STUDENTS TABLE
            # -----------------------------------------------------
            """
            CREATE TABLE IF NOT EXISTS Students (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,   -- Student unique ID
                Name TEXT NOT NULL,                     -- Full name of student
                Guardian TEXT NOT NULL,                 -- Parent/guardian full name
                LevelID INTEGER NOT NULL,               -- Assigned level (Grade)
                SectionID INTEGER NOT NULL,             -- Assigned section
                SchoolYear TEXT NOT NULL                -- Ex: '2024-2025'
            );
            """,

            # -----------------------------------------------------
            # SUBJECTS TABLE
            # -----------------------------------------------------
            """
            CREATE TABLE IF NOT EXISTS Subjects (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,   -- Subject unique ID
                Subject TEXT NOT NULL,                  -- Subject name (Math, Science)
                Advisor TEXT NOT NULL,                  -- Teacher in charge of subject
                LevelID INTEGER NOT NULL                -- Level this subject belongs to
            );
            """,

            # -----------------------------------------------------
            # GRADES TABLE
            # -----------------------------------------------------
            """
            CREATE TABLE IF NOT EXISTS Grades (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,   -- Grade unique ID
                StudentID INTEGER NOT NULL,             -- Student receiving the grade
                SubjectID INTEGER NOT NULL,             -- Subject the grade belongs to
                Grade TEXT NOT NULL,                    -- Grade (number, letter, etc.)
                SchoolYear TEXT NOT NULL                -- Year the grade applies to
            );
            """
        ]
        conn = self.connect()
        if conn:
            cur = conn.cursor()
            for q in schema:
                cur.execute(q)
            conn.commit()
            conn.close()

    # ============================================================
    # UTILITY FUNCTIONS
    # ============================================================
    def table_exists(self, table_name):
        result = self.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,), fetch_one=True
        )
        return result is not None

    def get_table_info(self, table_name):
        return self.execute(
            f"PRAGMA table_info({table_name})",
            fetch_all=True
        )

    def vacuum(self):
        conn = self.connect()
        if conn:
            conn.execute("VACUUM")
            conn.close()
            return True
        return False

    def backup_database(self, backup_path):
        conn = self.connect()
        if conn:
            backup_conn = sqlite3.connect(backup_path)
            conn.backup(backup_conn)
            backup_conn.close()
            conn.close()
            return True
        return False

    # ============================================================
    # LEVELS CRUD
    # ============================================================
    def add_level(self, level_name: str, ) -> bool:
        return self.execute(
            "INSERT INTO Levels (LevelName) VALUES (?)",
            (level_name,)
        )

    def get_level(self, level_id: int) -> Optional[Dict]:
        return self.execute(
            "SELECT * FROM Levels WHERE ID = ?",
            (level_id,),
            fetch_one=True
        )

    def get_all_levels(self) -> List[Dict]:
        return self.execute(
            "SELECT * FROM Levels ORDER BY ID",
            fetch_all=True
        ) or []

    def update_level(self, level_id: int, level_name: str) -> bool:
        return self.execute(
            "UPDATE Levels SET LevelName = ? WHERE ID = ?",
            (level_name, level_id)
        )
    
    def delete_level(self, level_id: int) -> bool:
        return self.execute(
            "DELETE FROM Levels WHERE ID = ?",
            (level_id,)
        )

    # ============================================================
    # SECTIONS CRUD
    # ============================================================
    def add_section(self, section_name: str, level_id: int) -> bool:
        return self.execute(
            "INSERT INTO Sections (SectionName, LevelID) VALUES (?, ?)",
            (section_name, level_id)
        )

    def get_section(self, section_id: int) -> Optional[Dict]:
        return self.execute(
            "SELECT * FROM Sections WHERE ID = ?",
            (section_id,),
            fetch_one=True
        )

    def get_sections_by_level(self, level_id: int) -> List[Dict]:
        return self.execute(
            "SELECT * FROM Sections WHERE LevelID = ? ORDER BY ID",
            (level_id,),
            fetch_all=True
        ) or []

    def get_all_sections(self) -> List[Dict]:
        return self.execute(
            "SELECT * FROM Sections ORDER BY ID",
            fetch_all=True
        ) or []

    def update_section(self, section_id: int, section_name: str, level_id: int) -> bool:
        return self.execute(
            "UPDATE Sections SET SectionName = ?, LevelID = ? WHERE ID = ?",
            (section_name, level_id, section_id)
        )

    def delete_section(self, section_id: int) -> bool:
        return self.execute(
            "DELETE FROM Sections WHERE ID = ?",
            (section_id,)
        )

    # ============================================================
    # STUDENTS CRUD
    # ============================================================
    def add_student(self, name: str, guardian: str, level_id: int, section_id: int, school_year: str) -> bool:
        return self.execute(
            "INSERT INTO Students (Name, Guardian, LevelID, SectionID, SchoolYear) VALUES (?, ?, ?, ?, ?)",
            (name, guardian, level_id, section_id, school_year)
        )

    def get_student(self, student_id: int) -> Optional[Dict]:
        return self.execute(
            "SELECT * FROM Students WHERE ID = ?",
            (student_id,),
            fetch_one=True
        )

    def get_students_by_section(self, section_id: int) -> List[Dict]:
        return self.execute(
            "SELECT * FROM Students WHERE SectionID = ? ORDER BY Name",
            (section_id,),
            fetch_all=True
        ) or []

    def get_students_by_level(self, level_id: int) -> List[Dict]:
        return self.execute(
            "SELECT * FROM Students WHERE LevelID = ? ORDER BY Name",
            (level_id,),
            fetch_all=True
        ) or []

    def get_all_students(self) -> List[Dict]:
        return self.execute(
            "SELECT * FROM Students ORDER BY Name",
            fetch_all=True
        ) or []

    def update_student(self, student_id: int, name: str, guardian: str, level_id: int, section_id: int, school_year: str) -> bool:
        return self.execute(
            "UPDATE Students SET Name = ?, Guardian = ?, LevelID = ?, SectionID = ?, SchoolYear = ? WHERE ID = ?",
            (name, guardian, level_id, section_id, school_year, student_id)
        )

    def delete_student(self, student_id: int) -> bool:
        return self.execute(
            "DELETE FROM Students WHERE ID = ?",
            (student_id,)
        )

    # ============================================================
    # SUBJECTS CRUD
    # ============================================================
    def add_subject(self, subject: str, advisor: str, level_id: int) -> bool:
        return self.execute(
            "INSERT INTO Subjects (Subject, Advisor, LevelID) VALUES (?, ?, ?)",
            (subject, advisor, level_id)
        )

    def get_subject(self, subject_id: int) -> Optional[Dict]:
        return self.execute(
            "SELECT * FROM Subjects WHERE ID = ?",
            (subject_id,),
            fetch_one=True
        )

    def get_subjects_by_level(self, level_id: int) -> List[Dict]:
        return self.execute(
            "SELECT * FROM Subjects WHERE LevelID = ? ORDER BY Subject",
            (level_id,),
            fetch_all=True
        ) or []

    def get_all_subjects(self) -> List[Dict]:
        return self.execute(
            "SELECT * FROM Subjects ORDER BY Subject",
            fetch_all=True
        ) or []

    def update_subject(self, subject_id: int, subject: str, advisor: str, level_id: int) -> bool:
        return self.execute(
            "UPDATE Subjects SET Subject = ?, Advisor = ?, LevelID = ? WHERE ID = ?",
            (subject, advisor, level_id, subject_id)
        )

    def delete_subject(self, subject_id: int) -> bool:
        return self.execute(
            "DELETE FROM Subjects WHERE ID = ?",
            (subject_id,)
        )

    # ============================================================
    # GRADES CRUD
    # ============================================================
    def add_grade(self, student_id: int, subject_id: int, grade: str, school_year: str) -> bool:
        return self.execute(
            "INSERT INTO Grades (StudentID, SubjectID, Grade, SchoolYear) VALUES (?, ?, ?, ?)",
            (student_id, subject_id, grade, school_year)
        )

    def get_grade(self, grade_id: int) -> Optional[Dict]:
        return self.execute(
            "SELECT * FROM Grades WHERE ID = ?",
            (grade_id,),
            fetch_one=True
        )

    def get_student_grades(self, student_id: int, school_year: Optional[str] = None) -> List[Dict]:
        if school_year:
            return self.execute(
                "SELECT * FROM Grades WHERE StudentID = ? AND SchoolYear = ? ORDER BY SubjectID",
                (student_id, school_year),
                fetch_all=True
            ) or []
        return self.execute(
            "SELECT * FROM Grades WHERE StudentID = ? ORDER BY SubjectID",
            (student_id,),
            fetch_all=True
        ) or []

    def get_subject_grades(self, subject_id: int, school_year: Optional[str] = None) -> List[Dict]:
        if school_year:
            return self.execute(
                "SELECT * FROM Grades WHERE SubjectID = ? AND SchoolYear = ? ORDER BY StudentID",
                (subject_id, school_year),
                fetch_all=True
            ) or []
        return self.execute(
            "SELECT * FROM Grades WHERE SubjectID = ? ORDER BY StudentID",
            (subject_id,),
            fetch_all=True
        ) or []

    def get_all_grades(self) -> List[Dict]:
        return self.execute(
            "SELECT * FROM Grades ORDER BY StudentID, SubjectID",
            fetch_all=True
        ) or []

    def update_grade(self, grade_id: int, student_id: int, subject_id: int, grade: str, school_year: str) -> bool:
        return self.execute(
            "UPDATE Grades SET StudentID = ?, SubjectID = ?, Grade = ?, SchoolYear = ? WHERE ID = ?",
            (student_id, subject_id, grade, school_year, grade_id)
        )

    def delete_grade(self, grade_id: int) -> bool:
        return self.execute(
            "DELETE FROM Grades WHERE ID = ?",
            (grade_id,)
        )
