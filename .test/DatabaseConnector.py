import sqlite3
import os
from typing import Optional, List, Dict, Any


class DatabaseConnector:
    def __init__(self):
        self.base_path = "db"
        self.db_path = os.path.join(self.base_path, "school.db")
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

            # Levels
            """
            CREATE TABLE IF NOT EXISTS Levels (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                LevelName TEXT NOT NULL UNIQUE,
                Category TEXT NOT NULL
            );
            """,

            # Sections
            """
            CREATE TABLE IF NOT EXISTS Sections (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                SectionName TEXT NOT NULL,
                LevelID INTEGER NOT NULL,
                FOREIGN KEY(LevelID) REFERENCES Levels(ID) ON DELETE CASCADE
            );
            """,

            # Students
            """
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
            """,

            # Subjects
            """
            CREATE TABLE IF NOT EXISTS Subjects (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Subject TEXT NOT NULL,
                Advisor TEXT NOT NULL,
                LevelID INTEGER NOT NULL,
                FOREIGN KEY(LevelID) REFERENCES Levels(ID)
            );
            """,

            # Grades
            """
            CREATE TABLE IF NOT EXISTS Grades (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                StudentID INTEGER NOT NULL,
                SubjectID INTEGER NOT NULL,
                Grade TEXT NOT NULL,
                SchoolYear TEXT NOT NULL,
                FOREIGN KEY(StudentID) REFERENCES Students(ID) ON DELETE CASCADE,
                FOREIGN KEY(SubjectID) REFERENCES Subjects(ID) ON DELETE CASCADE
            );
            """
        ]

        conn = self.connect()
        if conn:
            for q in schema:
                conn.execute(q)
            conn.commit()
            conn.close()

    # ============================================================
    # LEVELS CRUD + EXTRA QUERIES
    # ============================================================
    def add_level(self, level_name, category):
        return self.execute(
            "INSERT INTO Levels (LevelName, Category) VALUES (?, ?)",
            (level_name, category)
        )

    def get_level(self, level_id):
        return self.execute(
            "SELECT * FROM Levels WHERE ID = ?",
            (level_id,), fetch_one=True
        )

    def get_levels(self):
        return self.execute("SELECT * FROM Levels ORDER BY ID ASC", fetch_all=True)

    def get_levels_by_category(self, category):
        return self.execute(
            "SELECT * FROM Levels WHERE Category = ? ORDER BY LevelName ASC",
            (category,), fetch_all=True
        )

    def get_level_with_details(self, level_id):
        return self.execute(
            """
            SELECT 
                l.*,
                COUNT(DISTINCT s.ID) as section_count,
                COUNT(DISTINCT stu.ID) as student_count,
                COUNT(DISTINCT sub.ID) as subject_count
            FROM Levels l
            LEFT JOIN Sections s ON l.ID = s.LevelID
            LEFT JOIN Students stu ON l.ID = stu.LevelID
            LEFT JOIN Subjects sub ON l.ID = sub.LevelID
            WHERE l.ID = ?
            GROUP BY l.ID
            """,
            (level_id,), fetch_one=True
        )

    def update_level(self, level_id, **fields):
        keys = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [level_id]
        return self.execute(f"UPDATE Levels SET {keys} WHERE ID = ?", values)

    def delete_level(self, level_id):
        return self.execute("DELETE FROM Levels WHERE ID = ?", (level_id,))

    def search_levels(self, search_term):
        return self.execute(
            """
            SELECT * FROM Levels 
            WHERE LevelName LIKE ? OR Category LIKE ?
            ORDER BY LevelName ASC
            """,
            (f'%{search_term}%', f'%{search_term}%'), fetch_all=True
        )

    def count_levels(self):
        return self.execute("SELECT COUNT(*) as count FROM Levels", fetch_one=True)

    # ============================================================
    # SECTIONS CRUD + EXTRA QUERIES
    # ============================================================
    def add_section(self, section_name, level_id):
        return self.execute(
            "INSERT INTO Sections (SectionName, LevelID) VALUES (?, ?)",
            (section_name, level_id)
        )

    def get_section(self, section_id):
        return self.execute(
            "SELECT * FROM Sections WHERE ID = ?",
            (section_id,), fetch_one=True
        )

    def get_sections(self, level_id=None):
        if level_id:
            return self.execute(
                "SELECT * FROM Sections WHERE LevelID = ? ORDER BY SectionName ASC",
                (level_id,), fetch_all=True
            )
        return self.execute("SELECT * FROM Sections ORDER BY SectionName ASC", fetch_all=True)

    def get_sections_with_details(self, level_id=None):
        query = """
            SELECT 
                s.*,
                l.LevelName,
                l.Category,
                COUNT(DISTINCT stu.ID) as student_count
            FROM Sections s
            JOIN Levels l ON s.LevelID = l.ID
            LEFT JOIN Students stu ON s.ID = stu.SectionID
        """
        
        if level_id:
            query += " WHERE s.LevelID = ?"
            query += " GROUP BY s.ID ORDER BY l.LevelName, s.SectionName"
            return self.execute(query, (level_id,), fetch_all=True)
        
        query += " GROUP BY s.ID ORDER BY l.LevelName, s.SectionName"
        return self.execute(query, fetch_all=True)

    def update_section(self, section_id, **fields):
        keys = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [section_id]
        return self.execute(f"UPDATE Sections SET {keys} WHERE ID = ?", values)

    def delete_section(self, section_id):
        return self.execute("DELETE FROM Sections WHERE ID = ?", (section_id,))

    def search_sections(self, search_term):
        return self.execute(
            """
            SELECT s.*, l.LevelName 
            FROM Sections s
            JOIN Levels l ON s.LevelID = l.ID
            WHERE s.SectionName LIKE ? OR l.LevelName LIKE ?
            ORDER BY l.LevelName, s.SectionName
            """,
            (f'%{search_term}%', f'%{search_term}%'), fetch_all=True
        )

    def count_sections_by_level(self, level_id):
        return self.execute(
            "SELECT COUNT(*) as count FROM Sections WHERE LevelID = ?",
            (level_id,), fetch_one=True
        )

    # ============================================================
    # STUDENTS CRUD + EXTRA QUERIES
    # ============================================================
    def add_student(self, name, guardian, level_id, section_id, school_year):
        return self.execute(
            """
            INSERT INTO Students (Name, Guardian, LevelID, SectionID, SchoolYear)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, guardian, level_id, section_id, school_year)
        )

    def get_student(self, student_id):
        return self.execute(
            """
            SELECT 
                stu.*,
                l.LevelName,
                s.SectionName
            FROM Students stu
            JOIN Levels l ON stu.LevelID = l.ID
            JOIN Sections s ON stu.SectionID = s.ID
            WHERE stu.ID = ?
            """,
            (student_id,), fetch_one=True
        )

    def get_all_students(self):
        return self.execute(
            """
            SELECT 
                stu.*,
                l.LevelName,
                s.SectionName
            FROM Students stu
            JOIN Levels l ON stu.LevelID = l.ID
            JOIN Sections s ON stu.SectionID = s.ID
            ORDER BY stu.Name ASC
            """, 
            fetch_all=True
        )

    def get_students_by_level(self, level_id):
        return self.execute(
            """
            SELECT 
                stu.*,
                s.SectionName
            FROM Students stu
            JOIN Sections s ON stu.SectionID = s.ID
            WHERE stu.LevelID = ?
            ORDER BY s.SectionName, stu.Name
            """,
            (level_id,), fetch_all=True
        )

    def get_students_by_section(self, section_id):
        return self.execute(
            """
            SELECT 
                stu.*,
                l.LevelName
            FROM Students stu
            JOIN Levels l ON stu.LevelID = l.ID
            WHERE stu.SectionID = ?
            ORDER BY stu.Name ASC
            """,
            (section_id,), fetch_all=True
        )

    def get_students_by_school_year(self, school_year):
        return self.execute(
            """
            SELECT 
                stu.*,
                l.LevelName,
                s.SectionName
            FROM Students stu
            JOIN Levels l ON stu.LevelID = l.ID
            JOIN Sections s ON stu.SectionID = s.ID
            WHERE stu.SchoolYear = ?
            ORDER BY l.LevelName, s.SectionName, stu.Name
            """,
            (school_year,), fetch_all=True
        )

    def get_students_with_grades_summary(self):
        return self.execute(
            """
            SELECT 
                stu.*,
                l.LevelName,
                s.SectionName,
                COUNT(DISTINCT g.ID) as grades_count,
                AVG(CAST(g.Grade AS FLOAT)) as average_grade
            FROM Students stu
            JOIN Levels l ON stu.LevelID = l.ID
            JOIN Sections s ON stu.SectionID = s.ID
            LEFT JOIN Grades g ON stu.ID = g.StudentID
            GROUP BY stu.ID
            ORDER BY stu.Name ASC
            """,
            fetch_all=True
        )

    def update_student(self, student_id, **fields):
        keys = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [student_id]
        return self.execute(f"UPDATE Students SET {keys} WHERE ID = ?", values)

    def delete_student(self, student_id):
        return self.execute("DELETE FROM Students WHERE ID = ?", (student_id,))

    def search_students(self, search_term):
        return self.execute(
            """
            SELECT 
                stu.*,
                l.LevelName,
                s.SectionName
            FROM Students stu
            JOIN Levels l ON stu.LevelID = l.ID
            JOIN Sections s ON stu.SectionID = s.ID
            WHERE stu.Name LIKE ? OR stu.Guardian LIKE ? OR l.LevelName LIKE ? OR s.SectionName LIKE ?
            ORDER BY stu.Name ASC
            """,
            (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'), 
            fetch_all=True
        )

    def count_students(self):
        return self.execute("SELECT COUNT(*) as count FROM Students", fetch_one=True)

    def count_students_by_level(self, level_id):
        return self.execute(
            "SELECT COUNT(*) as count FROM Students WHERE LevelID = ?",
            (level_id,), fetch_one=True
        )

    def count_students_by_section(self, section_id):
        return self.execute(
            "SELECT COUNT(*) as count FROM Students WHERE SectionID = ?",
            (section_id,), fetch_one=True
        )

    # ============================================================
    # SUBJECTS CRUD + EXTRA QUERIES
    # ============================================================
    def add_subject(self, subject, advisor, level_id):
        return self.execute(
            """
            INSERT INTO Subjects (Subject, Advisor, LevelID)
            VALUES (?, ?, ?)
            """,
            (subject, advisor, level_id)
        )

    def get_subject(self, subject_id):
        return self.execute(
            """
            SELECT 
                sub.*,
                l.LevelName
            FROM Subjects sub
            JOIN Levels l ON sub.LevelID = l.ID
            WHERE sub.ID = ?
            """,
            (subject_id,), fetch_one=True
        )

    def get_all_subjects(self):
        return self.execute(
            """
            SELECT 
                sub.*,
                l.LevelName
            FROM Subjects sub
            JOIN Levels l ON sub.LevelID = l.ID
            ORDER BY sub.Subject ASC
            """, 
            fetch_all=True
        )

    def get_subjects_by_level(self, level_id):
        return self.execute(
            "SELECT * FROM Subjects WHERE LevelID = ? ORDER BY Subject ASC",
            (level_id,), fetch_all=True
        )

    def get_subjects_with_grades_count(self):
        return self.execute(
            """
            SELECT 
                sub.*,
                l.LevelName,
                COUNT(DISTINCT g.ID) as grades_count,
                COUNT(DISTINCT g.StudentID) as students_count
            FROM Subjects sub
            JOIN Levels l ON sub.LevelID = l.ID
            LEFT JOIN Grades g ON sub.ID = g.SubjectID
            GROUP BY sub.ID
            ORDER BY sub.Subject ASC
            """,
            fetch_all=True
        )

    def update_subject(self, subject_id, **fields):
        keys = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [subject_id]
        return self.execute(f"UPDATE Subjects SET {keys} WHERE ID = ?", values)

    def delete_subject(self, subject_id):
        return self.execute("DELETE FROM Subjects WHERE ID = ?", (subject_id,))

    def search_subjects(self, search_term):
        return self.execute(
            """
            SELECT 
                sub.*,
                l.LevelName
            FROM Subjects sub
            JOIN Levels l ON sub.LevelID = l.ID
            WHERE sub.Subject LIKE ? OR sub.Advisor LIKE ? OR l.LevelName LIKE ?
            ORDER BY sub.Subject ASC
            """,
            (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'), 
            fetch_all=True
        )

    def count_subjects(self):
        return self.execute("SELECT COUNT(*) as count FROM Subjects", fetch_one=True)

    def count_subjects_by_level(self, level_id):
        return self.execute(
            "SELECT COUNT(*) as count FROM Subjects WHERE LevelID = ?",
            (level_id,), fetch_one=True
        )

    # ============================================================
    # GRADES CRUD + EXTRA QUERIES
    # ============================================================
    def add_grade(self, student_id, subject_id, grade, school_year):
        return self.execute(
            """
            INSERT INTO Grades (StudentID, SubjectID, Grade, SchoolYear)
            VALUES (?, ?, ?, ?)
            """,
            (student_id, subject_id, grade, school_year)
        )

    def get_grade(self, grade_id):
        return self.execute(
            """
            SELECT 
                g.*,
                stu.Name as StudentName,
                sub.Subject,
                sub.Advisor
            FROM Grades g
            JOIN Students stu ON g.StudentID = stu.ID
            JOIN Subjects sub ON g.SubjectID = sub.ID
            WHERE g.ID = ?
            """,
            (grade_id,), fetch_one=True
        )

    def get_all_grades(self):
        return self.execute(
            """
            SELECT 
                g.*,
                stu.Name as StudentName,
                sub.Subject,
                sub.Advisor
            FROM Grades g
            JOIN Students stu ON g.StudentID = stu.ID
            JOIN Subjects sub ON g.SubjectID = sub.ID
            ORDER BY stu.Name, sub.Subject
            """,
            fetch_all=True
        )

    def get_student_grades(self, student_id):
        return self.execute(
            """
            SELECT 
                g.*,
                sub.Subject,
                sub.Advisor,
                l.LevelName
            FROM Grades g
            JOIN Subjects sub ON g.SubjectID = sub.ID
            JOIN Levels l ON sub.LevelID = l.ID
            WHERE g.StudentID = ?
            ORDER BY sub.Subject ASC
            """,
            (student_id,), fetch_all=True
        )

    def get_student_grades_by_year(self, student_id, school_year):
        return self.execute(
            """
            SELECT 
                g.*,
                sub.Subject,
                sub.Advisor
            FROM Grades g
            JOIN Subjects sub ON g.SubjectID = sub.ID
            WHERE g.StudentID = ? AND g.SchoolYear = ?
            ORDER BY sub.Subject ASC
            """,
            (student_id, school_year), fetch_all=True
        )

    def get_subject_grades(self, subject_id):
        return self.execute(
            """
            SELECT 
                g.*,
                stu.Name as StudentName,
                stu.SchoolYear
            FROM Grades g
            JOIN Students stu ON g.StudentID = stu.ID
            WHERE g.SubjectID = ?
            ORDER BY stu.Name ASC
            """,
            (subject_id,), fetch_all=True
        )

    def get_grades_by_school_year(self, school_year):
        return self.execute(
            """
            SELECT 
                g.*,
                stu.Name as StudentName,
                sub.Subject,
                sub.Advisor
            FROM Grades g
            JOIN Students stu ON g.StudentID = stu.ID
            JOIN Subjects sub ON g.SubjectID = sub.ID
            WHERE g.SchoolYear = ?
            ORDER BY stu.Name, sub.Subject
            """,
            (school_year,), fetch_all=True
        )

    def get_grades_with_details(self):
        return self.execute(
            """
            SELECT 
                g.*,
                stu.Name as StudentName,
                stu.Guardian,
                l.LevelName,
                s.SectionName,
                sub.Subject,
                sub.Advisor
            FROM Grades g
            JOIN Students stu ON g.StudentID = stu.ID
            JOIN Levels l ON stu.LevelID = l.ID
            JOIN Sections s ON stu.SectionID = s.ID
            JOIN Subjects sub ON g.SubjectID = sub.ID
            ORDER BY l.LevelName, s.SectionName, stu.Name, sub.Subject
            """,
            fetch_all=True
        )

    def update_grade(self, grade_id, **fields):
        keys = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [grade_id]
        return self.execute(f"UPDATE Grades SET {keys} WHERE ID = ?", values)

    def delete_grade(self, grade_id):
        return self.execute("DELETE FROM Grades WHERE ID = ?", (grade_id,))

    def delete_student_grades(self, student_id):
        return self.execute("DELETE FROM Grades WHERE StudentID = ?", (student_id,))

    def delete_subject_grades(self, subject_id):
        return self.execute("DELETE FROM Grades WHERE SubjectID = ?", (subject_id,))

    def search_grades(self, search_term):
        return self.execute(
            """
            SELECT 
                g.*,
                stu.Name as StudentName,
                sub.Subject,
                sub.Advisor
            FROM Grades g
            JOIN Students stu ON g.StudentID = stu.ID
            JOIN Subjects sub ON g.SubjectID = sub.ID
            WHERE stu.Name LIKE ? OR sub.Subject LIKE ? OR g.Grade LIKE ?
            ORDER BY stu.Name, sub.Subject
            """,
            (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'), 
            fetch_all=True
        )

    def count_grades(self):
        return self.execute("SELECT COUNT(*) as count FROM Grades", fetch_one=True)

    def count_grades_by_student(self, student_id):
        return self.execute(
            "SELECT COUNT(*) as count FROM Grades WHERE StudentID = ?",
            (student_id,), fetch_one=True
        )

    def count_grades_by_subject(self, subject_id):
        return self.execute(
            "SELECT COUNT(*) as count FROM Grades WHERE SubjectID = ?",
            (subject_id,), fetch_one=True
        )

    def get_average_grade_by_student(self, student_id):
        return self.execute(
            "SELECT AVG(CAST(Grade AS FLOAT)) as average FROM Grades WHERE StudentID = ?",
            (student_id,), fetch_one=True
        )

    def get_average_grade_by_subject(self, subject_id):
        return self.execute(
            "SELECT AVG(CAST(Grade AS FLOAT)) as average FROM Grades WHERE SubjectID = ?",
            (subject_id,), fetch_one=True
        )

    def get_average_grade_by_level(self, level_id):
        return self.execute(
            """
            SELECT AVG(CAST(g.Grade AS FLOAT)) as average
            FROM Grades g
            JOIN Students stu ON g.StudentID = stu.ID
            WHERE stu.LevelID = ?
            """,
            (level_id,), fetch_one=True
        )

    def get_average_grade_by_section(self, section_id):
        return self.execute(
            """
            SELECT AVG(CAST(g.Grade AS FLOAT)) as average
            FROM Grades g
            JOIN Students stu ON g.StudentID = stu.ID
            WHERE stu.SectionID = ?
            """,
            (section_id,), fetch_one=True
        )

    def get_average_grade_by_school_year(self, school_year):
        return self.execute(
            "SELECT AVG(CAST(Grade AS FLOAT)) as average FROM Grades WHERE SchoolYear = ?",
            (school_year,), fetch_one=True
        )

    def get_grade_distribution(self):
        return self.execute(
            """
            SELECT 
                Grade,
                COUNT(*) as count,
                COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Grades) as percentage
            FROM Grades
            GROUP BY Grade
            ORDER BY Grade
            """,
            fetch_all=True
        )

    def get_top_students(self, limit=10):
        return self.execute(
            """
            SELECT 
                stu.ID,
                stu.Name,
                l.LevelName,
                s.SectionName,
                AVG(CAST(g.Grade AS FLOAT)) as average_grade,
                COUNT(g.ID) as grades_count
            FROM Students stu
            JOIN Levels l ON stu.LevelID = l.ID
            JOIN Sections s ON stu.SectionID = s.ID
            JOIN Grades g ON stu.ID = g.StudentID
            GROUP BY stu.ID
            HAVING grades_count > 0
            ORDER BY average_grade DESC
            LIMIT ?
            """,
            (limit,), fetch_all=True
        )

    # ============================================================
    # REPORTS AND ANALYTICS
    # ============================================================
    def get_school_statistics(self):
        return self.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM Levels) as total_levels,
                (SELECT COUNT(*) FROM Sections) as total_sections,
                (SELECT COUNT(*) FROM Students) as total_students,
                (SELECT COUNT(*) FROM Subjects) as total_subjects,
                (SELECT COUNT(*) FROM Grades) as total_grades,
                (SELECT AVG(CAST(Grade AS FLOAT)) FROM Grades) as overall_average,
                (SELECT COUNT(DISTINCT SchoolYear) FROM Students) as total_school_years
            """,
            fetch_one=True
        )

    def get_levels_summary(self):
        return self.execute(
            """
            SELECT 
                l.ID,
                l.LevelName,
                l.Category,
                COUNT(DISTINCT s.ID) as section_count,
                COUNT(DISTINCT stu.ID) as student_count,
                COUNT(DISTINCT sub.ID) as subject_count,
                COUNT(DISTINCT g.ID) as grades_count,
                AVG(CAST(g.Grade AS FLOAT)) as average_grade
            FROM Levels l
            LEFT JOIN Sections s ON l.ID = s.LevelID
            LEFT JOIN Students stu ON l.ID = stu.LevelID
            LEFT JOIN Subjects sub ON l.ID = sub.LevelID
            LEFT JOIN Grades g ON stu.ID = g.StudentID
            GROUP BY l.ID
            ORDER BY l.LevelName
            """,
            fetch_all=True
        )

    def get_sections_summary(self):
        return self.execute(
            """
            SELECT 
                s.ID,
                s.SectionName,
                l.LevelName,
                COUNT(DISTINCT stu.ID) as student_count,
                COUNT(DISTINCT g.ID) as grades_count,
                AVG(CAST(g.Grade AS FLOAT)) as average_grade
            FROM Sections s
            JOIN Levels l ON s.LevelID = l.ID
            LEFT JOIN Students stu ON s.ID = stu.SectionID
            LEFT JOIN Grades g ON stu.ID = g.StudentID
            GROUP BY s.ID
            ORDER BY l.LevelName, s.SectionName
            """,
            fetch_all=True
        )

    def get_subjects_summary(self):
        return self.execute(
            """
            SELECT 
                sub.ID,
                sub.Subject,
                sub.Advisor,
                l.LevelName,
                COUNT(DISTINCT g.ID) as grades_count,
                COUNT(DISTINCT g.StudentID) as students_count,
                AVG(CAST(g.Grade AS FLOAT)) as average_grade,
                MIN(CAST(g.Grade AS FLOAT)) as min_grade,
                MAX(CAST(g.Grade AS FLOAT)) as max_grade
            FROM Subjects sub
            JOIN Levels l ON sub.LevelID = l.ID
            LEFT JOIN Grades g ON sub.ID = g.SubjectID
            GROUP BY sub.ID
            ORDER BY sub.Subject
            """,
            fetch_all=True
        )

    def get_yearly_statistics(self):
        return self.execute(
            """
            SELECT 
                SchoolYear,
                COUNT(DISTINCT StudentID) as students_count,
                COUNT(ID) as grades_count,
                AVG(CAST(Grade AS FLOAT)) as average_grade
            FROM Grades
            GROUP BY SchoolYear
            ORDER BY SchoolYear DESC
            """,
            fetch_all=True
        )

    def get_student_performance_report(self, student_id):
        return self.execute(
            """
            SELECT 
                stu.Name as student_name,
                stu.Guardian,
                l.LevelName,
                s.SectionName,
                stu.SchoolYear,
                sub.Subject,
                sub.Advisor,
                g.Grade,
                g.SchoolYear as grade_year
            FROM Students stu
            JOIN Levels l ON stu.LevelID = l.ID
            JOIN Sections s ON stu.SectionID = s.ID
            LEFT JOIN Grades g ON stu.ID = g.StudentID
            LEFT JOIN Subjects sub ON g.SubjectID = sub.ID
            WHERE stu.ID = ?
            ORDER BY g.SchoolYear DESC, sub.Subject
            """,
            (student_id,), fetch_all=True
        )

    def get_grade_range_statistics(self, min_grade, max_grade):
        return self.execute(
            """
            SELECT 
                COUNT(*) as count,
                COUNT(DISTINCT StudentID) as students_count,
                COUNT(DISTINCT SubjectID) as subjects_count,
                AVG(CAST(Grade AS FLOAT)) as average
            FROM Grades
            WHERE CAST(Grade AS FLOAT) BETWEEN ? AND ?
            """,
            (min_grade, max_grade), fetch_one=True
        )

    # ============================================================
    # BULK OPERATIONS
    # ============================================================
    def bulk_insert_students(self, students_data):
        conn = self.connect()
        if conn is None:
            return False
        
        cur = conn.cursor()
        try:
            cur.executemany(
                """
                INSERT INTO Students (Name, Guardian, LevelID, SectionID, SchoolYear)
                VALUES (?, ?, ?, ?, ?)
                """,
                students_data
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[BULK INSERT ERROR] {e}")
            return False
        finally:
            conn.close()

    def bulk_insert_grades(self, grades_data):
        conn = self.connect()
        if conn is None:
            return False
        
        cur = conn.cursor()
        try:
            cur.executemany(
                """
                INSERT INTO Grades (StudentID, SubjectID, Grade, SchoolYear)
                VALUES (?, ?, ?, ?)
                """,
                grades_data
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[BULK INSERT ERROR] {e}")
            return False
        finally:
            conn.close()

    def delete_all_grades(self):
        return self.execute("DELETE FROM Grades")

    def delete_all_students(self):
        return self.execute("DELETE FROM Students")

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