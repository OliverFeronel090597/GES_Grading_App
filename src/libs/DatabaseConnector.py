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
            # PRAGMA foreign_keys = ON - must be executed immediately after connection
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
            # Execute the query - pragma is already set in connect()
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
        # Each table has its own CREATE statement (no foreign keys)
        schema = [
            """
            CREATE TABLE IF NOT EXISTS Levels (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Level TEXT NOT NULL UNIQUE
            );
            """,
            # """
            # CREATE TABLE IF NOT EXISTS Sections (
            #     ID INTEGER PRIMARY KEY AUTOINCREMENT,
            #     SectionName TEXT NOT NULL,
            #     LevelID INTEGER NOT NULL
            # );
            # """,
            # """
            # CREATE TABLE IF NOT EXISTS Students (
            #     ID INTEGER PRIMARY KEY AUTOINCREMENT,
            #     Name TEXT NOT NULL,
            #     Guardian TEXT NOT NULL,
            #     LevelID INTEGER NOT NULL,
            #     SectionID INTEGER NOT NULL,
            #     SchoolYear TEXT NOT NULL
            # );
            # """,
            # """
            # CREATE TABLE IF NOT EXISTS Subjects (
            #     ID INTEGER PRIMARY KEY AUTOINCREMENT,
            #     Subject TEXT NOT NULL,
            #     Advisor TEXT NOT NULL,
            #     LevelID INTEGER NOT NULL
            # );
            # """,
            # """
            # CREATE TABLE IF NOT EXISTS Grades (
            #     ID INTEGER PRIMARY KEY AUTOINCREMENT,
            #     StudentID INTEGER NOT NULL,
            #     SubjectID INTEGER NOT NULL,
            #     Grade TEXT NOT NULL,
            #     SchoolYear TEXT NOT NULL
            # );
            # """
        ]

        conn = self.connect()
        if conn:
            cur = conn.cursor()
            for q in schema:
                cur.execute(q)
            conn.commit()
            conn.close()

    # ============================================================
    # LEVELS CRUD + EXTRA QUERIES
    # ============================================================
    def add_level(self, level_name):
        return self.execute(
            "INSERT INTO Levels (Level) VALUES (?)",
            (level_name,)
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

if __name__=="__main__":
    db = DatabaseConnector()
    db.add_level("Kinder")
    # rslt = db.get_all_students()
    # for r in rslt:
    #     print(r)