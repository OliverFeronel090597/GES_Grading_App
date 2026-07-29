import sqlite3
import os
from typing import Optional, List, Dict, Any
from datetime import datetime

class Database:
    def __init__(self):
        self.base_path = "DB"
        self.db_path = os.path.join(self.base_path, "PersonalGrading.db")
        self._ensure_directory()
        self._create_tables()
        #self.populate_sample_data()

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
        """
        Execute a SQL query with optional rollback support.
        
        Args:
            query: SQL query string
            params: Query parameters (tuple or dict)
            fetch_one: Return one row as dict
            fetch_all: Return all rows as list of dicts
            
        Returns:
            - For SELECT: dict or list of dicts
            - For INSERT/UPDATE/DELETE: True on success, None on failure
        """
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
            conn.rollback()  # Rollback on error
            return None

        finally:
            conn.close()

    def execute_transaction(self, queries: List[tuple]) -> bool:
        """
        Execute multiple queries as a single transaction.
        
        Args:
            queries: List of (query, params) tuples
            
        Returns:
            True if all queries succeed, False otherwise (rolls back on failure)
        """
        conn = self.connect()
        if conn is None:
            return False

        cur = conn.cursor()
        try:
            for query, params in queries:
                cur.execute(query, params)
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"[TRANSACTION ERROR] {e}")
            conn.rollback()
            return False
            
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
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                level_section TEXT NOT NULL UNIQUE
            );
            """,

            # -----------------------------------------------------
            # SUBJECTS TABLE
            # -----------------------------------------------------
            """
            CREATE TABLE IF NOT EXISTS Subjects (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_group TEXT NOT NULL,
                subject TEXT NOT NULL
            );
            """,

            # -----------------------------------------------------
            # STUDENTS TABLE
            # -----------------------------------------------------
            """
            CREATE TABLE IF NOT EXISTS Students (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                level_id INTEGER,
                section TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (level_id) REFERENCES Levels(ID)
            );
            """,

            # -----------------------------------------------------
            # GRADES TABLE
            # -----------------------------------------------------
            """
            CREATE TABLE IF NOT EXISTS Grades (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                subject_id INTEGER NOT NULL,
                grade REAL,
                semester INTEGER DEFAULT 1,
                school_year TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES Students(student_id),
                FOREIGN KEY (subject_id) REFERENCES Subjects(ID),
                UNIQUE(student_id, subject_id, semester, school_year)
            );
            """,

            # -----------------------------------------------------
            # ATTENDANCE TABLE
            # -----------------------------------------------------
            """
            CREATE TABLE IF NOT EXISTS Attendance (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                date DATE NOT NULL,
                status TEXT CHECK(status IN ('Present', 'Absent', 'Late', 'Excused')),
                remarks TEXT,
                FOREIGN KEY (student_id) REFERENCES Students(student_id),
                UNIQUE(student_id, date)
            );
            """,

            # -----------------------------------------------------
            # ACTIVITY LOG TABLE (Your specific version)
            # -----------------------------------------------------
            """
            CREATE TABLE IF NOT EXISTS ActivityLog (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                activity TEXT NOT NULL,
                changes TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    
    # ---------- TABLE UTILITIES ----------
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database."""
        result = self.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,), fetch_one=True
        )
        return result is not None

    def get_table_info(self, table_name: str) -> Optional[List[Dict]]:
        """Get column information for a table."""
        return self.execute(
            f"PRAGMA table_info({table_name})",
            fetch_all=True
        )

    def get_all_tables(self) -> List[str]:
        """Get list of all tables in the database."""
        result = self.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name",
            fetch_all=True
        )
        return [r['name'] for r in result] if result else []

    def get_table_row_count(self, table_name: str) -> int:
        """Get the number of rows in a table."""
        result = self.execute(
            f"SELECT COUNT(*) as count FROM {table_name}",
            fetch_one=True
        )
        return result['count'] if result else 0

    # ---------- QUERY BUILDERS ----------
    def build_insert_query(self, table: str, data: Dict) -> tuple:
        """
        Build an INSERT query from a dictionary.
        
        Args:
            table: Table name
            data: Dictionary of column: value pairs
            
        Returns:
            Tuple of (query, params)
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return query, tuple(data.values())

    def build_update_query(self, table: str, data: Dict, where: Dict) -> tuple:
        """
        Build an UPDATE query from dictionaries.
        
        Args:
            table: Table name
            data: Dictionary of column: value pairs to update
            where: Dictionary of condition column: value pairs
            
        Returns:
            Tuple of (query, params)
        """
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = ?" for k in where.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        params = tuple(list(data.values()) + list(where.values()))
        return query, params

    def build_delete_query(self, table: str, where: Dict) -> tuple:
        """
        Build a DELETE query from a dictionary.
        
        Args:
            table: Table name
            where: Dictionary of condition column: value pairs
            
        Returns:
            Tuple of (query, params)
        """
        where_clause = ' AND '.join([f"{k} = ?" for k in where.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        return query, tuple(where.values())

    # ---------- CRUD OPERATIONS ----------
    def insert(self, table: str, data: Dict) -> Optional[int]:
        """
        Insert a record into a table.
        
        Args:
            table: Table name
            data: Dictionary of column: value pairs
            
        Returns:
            Last row ID if successful, None otherwise
        """
        query, params = self.build_insert_query(table, data)
        conn = self.connect()
        if conn is None:
            return None
            
        cur = conn.cursor()
        try:
            cur.execute(query, params)
            conn.commit()
            return cur.lastrowid
        except sqlite3.Error as e:
            print(f"[INSERT ERROR] {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    def update(self, table: str, data: Dict, where: Dict) -> bool:
        """
        Update records in a table.
        
        Args:
            table: Table name
            data: Dictionary of column: value pairs to update
            where: Dictionary of condition column: value pairs
            
        Returns:
            True if successful, False otherwise
        """
        query, params = self.build_update_query(table, data, where)
        return self.execute(query, params) is not False

    def delete(self, table: str, where: Dict) -> bool:
        """
        Delete records from a table.
        
        Args:
            table: Table name
            where: Dictionary of condition column: value pairs
            
        Returns:
            True if successful, False otherwise
        """
        query, params = self.build_delete_query(table, where)
        return self.execute(query, params) is not False

    def select(self, table: str, columns: List[str] = None, 
               where: Dict = None, order_by: str = None, 
               limit: int = None) -> Optional[List[Dict]]:
        """
        Select records from a table.
        
        Args:
            table: Table name
            columns: List of columns to select (default: *)
            where: Dictionary of condition column: value pairs
            order_by: ORDER BY clause (e.g., "name ASC")
            limit: LIMIT clause
            
        Returns:
            List of dictionaries or None if error
        """
        col_str = ', '.join(columns) if columns else '*'
        query = f"SELECT {col_str} FROM {table}"
        params = []
        
        if where:
            conditions = ' AND '.join([f"{k} = ?" for k in where.keys()])
            query += f" WHERE {conditions}"
            params.extend(where.values())
            
        if order_by:
            query += f" ORDER BY {order_by}"
            
        if limit:
            query += f" LIMIT {limit}"
            
        return self.execute(query, tuple(params), fetch_all=True)

    # ---------- TRANSACTION UTILITIES ----------
    def begin_transaction(self):
        """Begin a transaction."""
        conn = self.connect()
        if conn:
            conn.execute("BEGIN TRANSACTION")
        return conn

    def commit_transaction(self, conn):
        """Commit a transaction."""
        if conn:
            conn.commit()
            conn.close()

    def rollback_transaction(self, conn):
        """Rollback a transaction."""
        if conn:
            conn.rollback()
            conn.close()

    # ---------- BACKUP & MAINTENANCE ----------
    def vacuum(self) -> bool:
        """Vacuum the database to reclaim space."""
        conn = self.connect()
        if conn:
            conn.execute("VACUUM")
            conn.close()
            return True
        return False

    def backup_database(self, backup_path: str) -> bool:
        """Create a backup of the database."""
        conn = self.connect()
        if conn:
            try:
                backup_conn = sqlite3.connect(backup_path)
                conn.backup(backup_conn)
                backup_conn.close()
                conn.close()
                return True
            except sqlite3.Error as e:
                print(f"[BACKUP ERROR] {e}")
                return False
        return False

    def restore_database(self, backup_path: str) -> bool:
        """Restore database from backup."""
        if not os.path.exists(backup_path):
            print(f"[RESTORE ERROR] Backup file not found: {backup_path}")
            return False
            
        # Close any open connections
        try:
            # Create a backup of current db first
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_backup = f"{self.db_path}.pre_restore_{timestamp}"
            self.backup_database(temp_backup)
            
            # Restore from backup
            backup_conn = sqlite3.connect(backup_path)
            conn = sqlite3.connect(self.db_path)
            backup_conn.backup(conn)
            conn.close()
            backup_conn.close()
            return True
        except sqlite3.Error as e:
            print(f"[RESTORE ERROR] {e}")
            return False

    # ---------- ACTIVITY LOG FUNCTIONS ----------
    def log_activity(self, location: str, activity: str, changes: str) -> bool:
        """
        Log an activity to the activity log.
        
        Args:
            location: Where the activity occurred (e.g., "Dashboard", "Grades Page")
            activity: What action was performed (e.g., "Insert", "Update", "Delete")
            changes: Details of what changed
        
        Returns:
            True if successful, False otherwise
        """
        query = """
            INSERT INTO ActivityLog (location, activity, changes) 
            VALUES (?, ?, ?)
        """
        return self.execute(query, (location, activity, changes)) is not False

    def get_activity_log(self, limit: int = 100) -> Optional[List[Dict]]:
        """
        Get recent activity log entries.
        
        Args:
            limit: Number of records to return (default: 100)
        
        Returns:
            List of activity log entries or None if error
        """
        query = """
            SELECT ID, location, activity, changes, timestamp 
            FROM ActivityLog 
            ORDER BY timestamp DESC 
            LIMIT ?
        """
        return self.execute(query, (limit,), fetch_all=True)

    def get_activity_log_by_location(self, location: str, limit: int = 50) -> Optional[List[Dict]]:
        """
        Get activity log entries for a specific location.
        
        Args:
            location: Location name to filter by
            limit: Number of records to return (default: 50)
        
        Returns:
            List of activity log entries or None if error
        """
        query = """
            SELECT ID, location, activity, changes, timestamp 
            FROM ActivityLog 
            WHERE location = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """
        return self.execute(query, (location, limit), fetch_all=True)

    def get_activity_log_by_activity(self, activity: str, limit: int = 50) -> Optional[List[Dict]]:
        """
        Get activity log entries for a specific activity type.
        
        Args:
            activity: Activity type to filter by (e.g., "Update", "Delete")
            limit: Number of records to return (default: 50)
        
        Returns:
            List of activity log entries or None if error
        """
        query = """
            SELECT ID, location, activity, changes, timestamp 
            FROM ActivityLog 
            WHERE activity = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """
        return self.execute(query, (activity, limit), fetch_all=True)

    def clear_activity_log(self, older_than_days: int = 30) -> bool:
        """
        Clear activity log entries older than specified days.
        
        Args:
            older_than_days: Delete entries older than this many days (default: 30)
        
        Returns:
            True if successful, False otherwise
        """
        query = """
            DELETE FROM ActivityLog 
            WHERE DATE(timestamp) < DATE('now', ?)
        """
        return self.execute(query, (f'-{older_than_days} days',)) is not False

    # ---------- DATA VALIDATION ----------
    def validate_foreign_key(self, table: str, column: str, value: Any) -> bool:
        """
        Validate if a foreign key value exists in the referenced table.
        
        Args:
            table: Table containing the foreign key
            column: Foreign key column name
            value: Value to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Get foreign key info
        fk_info = self.execute(f"PRAGMA foreign_key_list({table})", fetch_all=True)
        if not fk_info:
            return True
            
        for fk in fk_info:
            if fk['from'] == column:
                ref_table = fk['table']
                ref_column = fk['to']
                result = self.execute(
                    f"SELECT 1 FROM {ref_table} WHERE {ref_column} = ?",
                    (value,), fetch_one=True
                )
                return result is not None
        return True

    # ---------- DATABASE INFO ----------
    def get_database_size(self) -> int:
        """Get database size in bytes."""
        if os.path.exists(self.db_path):
            return os.path.getsize(self.db_path)
        return 0

    def get_database_info(self) -> Dict:
        """Get database information."""
        info = {
            'path': self.db_path,
            'size': self.get_database_size(),
            'tables': []
        }
        
        tables = self.get_all_tables()
        for table in tables:
            info['tables'].append({
                'name': table,
                'rows': self.get_table_row_count(table),
                'columns': len(self.get_table_info(table) or [])
            })
            
        return info

    # ============================================================
    # SAMPLE DATA POPULATION
    # ============================================================
    def populate_sample_data(self):
        """Populate the database with sample data for all tables."""
        print("[INFO] Populating sample data...")
        
        # Get existing counts
        level_count = self.get_table_row_count('Levels')
        subject_count = self.get_table_row_count('Subjects')
        student_count = self.get_table_row_count('Students')
        
        if level_count > 0 and subject_count > 0 and student_count > 0:
            print("[INFO] Sample data already exists. Skipping...")
            return
        
        # Sample data in transaction
        queries = []
        
        # ---------- LEVELS ----------
        if level_count == 0:
            levels = [
                ("Grade 7", "Grade 7 - Jade"),
                ("Grade 7", "Grade 7 - Ruby"),
                ("Grade 7", "Grade 7 - Sapphire"),
                ("Grade 8", "Grade 8 - Jade"),
                ("Grade 8", "Grade 8 - Ruby"),
                ("Grade 8", "Grade 8 - Sapphire"),
                ("Grade 9", "Grade 9 - Jade"),
                ("Grade 9", "Grade 9 - Ruby"),
                ("Grade 9", "Grade 9 - Sapphire"),
                ("Grade 10", "Grade 10 - Jade"),
                ("Grade 10", "Grade 10 - Ruby"),
                ("Grade 10", "Grade 10 - Sapphire"),
            ]
            for level, section in levels:
                queries.append((
                    "INSERT INTO Levels (level, level_section) VALUES (?, ?)",
                    (level, section)
                ))
        
        # ---------- SUBJECTS ----------
        if subject_count == 0:
            subjects = [
                ("English", "English 1"),
                ("English", "English 2"),
                ("English", "English 3"),
                ("English", "English 4"),
                ("Math", "Math 1"),
                ("Math", "Math 2"),
                ("Math", "Math 3"),
                ("Math", "Math 4"),
                ("Science", "Science 1"),
                ("Science", "Science 2"),
                ("Science", "Science 3"),
                ("Science", "Science 4"),
                ("History", "History 1"),
                ("History", "History 2"),
                ("History", "History 3"),
                ("History", "History 4"),
                ("Filipino", "Filipino 1"),
                ("Filipino", "Filipino 2"),
                ("Filipino", "Filipino 3"),
                ("Filipino", "Filipino 4"),
                ("PE", "PE 1"),
                ("PE", "PE 2"),
                ("PE", "PE 3"),
                ("PE", "PE 4"),
            ]
            for group, subject in subjects:
                queries.append((
                    "INSERT INTO Subjects (subject_group, subject) VALUES (?, ?)",
                    (group, subject)
                ))
        
        # ---------- STUDENTS ----------
        if student_count == 0:
            students = [
                ("S001", "Juan", "Dela Cruz", 1, "A"),
                ("S002", "Maria", "Santos", 1, "A"),
                ("S003", "Jose", "Rizal", 2, "B"),
                ("S004", "Andres", "Bonifacio", 2, "B"),
                ("S005", "Emilio", "Aguinaldo", 3, "A"),
                ("S006", "Gabriela", "Silang", 3, "B"),
                ("S007", "Lapu", "Lapu", 4, "A"),
                ("S008", "Ferdinand", "Magellan", 4, "B"),
                ("S009", "Jose", "Mercado", 5, "A"),
                ("S010", "Teodora", "Alonzo", 5, "B"),
                ("S011", "Andres", "Novales", 6, "A"),
                ("S012", "Teresa", "Magbanua", 6, "B"),
                ("S013", "Gregorio", "Del Pilar", 7, "A"),
                ("S014", "Mariano", "Gomez", 7, "B"),
                ("S015", "Jose", "Burgos", 8, "A"),
                ("S016", "Jacinto", "Zamora", 8, "B"),
                ("S017", "Melchora", "Aquino", 9, "A"),
                ("S018", "Apolinario", "Mabini", 9, "B"),
                ("S019", "Antonio", "Luna", 10, "A"),
                ("S020", "Emilio", "Jacinto", 10, "B"),
            ]
            for sid, first, last, level_id, section in students:
                queries.append((
                    """INSERT INTO Students (student_id, first_name, last_name, level_id, section) 
                       VALUES (?, ?, ?, ?, ?)""",
                    (sid, first, last, level_id, section)
                ))
        
        # ---------- GRADES ----------
        # Get subject IDs
        subject_ids = self.execute("SELECT ID, subject FROM Subjects", fetch_all=True)
        subject_map = {s['subject']: s['ID'] for s in subject_ids}
        
        # Generate grades for students
        import random
        random.seed(42)  # For reproducible results
        
        for student in students:
            sid = student[0]
            # Assign random grades for each subject
            for subject_name, subject_id in subject_map.items():
                grade = random.randint(70, 98)  # Random grade between 70-98
                queries.append((
                    """INSERT INTO Grades (student_id, subject_id, grade, semester, school_year) 
                       VALUES (?, ?, ?, ?, ?)""",
                    (sid, subject_id, grade, 1, "2024-2025")
                ))
        
        # ---------- ATTENDANCE ----------
        # Generate attendance records for the last 30 days
        from datetime import timedelta
        today = datetime.now().date()
        statuses = ['Present', 'Present', 'Present', 'Present', 'Absent', 'Late', 'Excused']
        
        for student in students:
            sid = student[0]
            for i in range(30, 0, -1):  # Last 30 days
                date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
                status = random.choice(statuses)
                remarks = "" if status == "Present" else f"Student was {status.lower()}"
                queries.append((
                    """INSERT INTO Attendance (student_id, date, status, remarks) 
                       VALUES (?, ?, ?, ?)""",
                    (sid, date, status, remarks)
                ))
        
        # ---------- ACTIVITY LOG ----------
        queries.append((
            """INSERT INTO ActivityLog (location, activity, changes) 
               VALUES (?, ?, ?)""",
            ("Database", "Initialize", "Sample data populated successfully")
        ))
        
        # Execute all queries in a single transaction
        if queries:
            print(f"[INFO] Executing {len(queries)} sample data queries...")
            success = self.execute_transaction(queries)
            if success:
                print("[INFO] Sample data populated successfully!")
                # Log the activity
                self.log_activity("System", "Populate Sample Data", 
                                 f"Inserted {len(queries)} records across all tables")
            else:
                print("[ERROR] Failed to populate sample data!")
        else:
            print("[INFO] No sample data to populate.")

# ============================================================
# USAGE EXAMPLES
# ============================================================
if __name__ == "__main__":
    # Initialize database
    db = Database()
    
    # Populate sample data
    db.populate_sample_data()
    
    # Example queries
    print("\n" + "="*50)
    print("SAMPLE DATA QUERIES")
    print("="*50)
    
    # Get all students
    students = db.select('Students', order_by='last_name ASC')
    print(f"\nTotal Students: {len(students) if students else 0}")
    
    # Get all levels
    levels = db.select('Levels', order_by='level ASC')
    print(f"Total Levels: {len(levels) if levels else 0}")
    
    # Get all subjects
    subjects = db.select('Subjects', order_by='subject_group ASC')
    print(f"Total Subjects: {len(subjects) if subjects else 0}")
    
    # Get grades summary
    grades_summary = db.execute("""
        SELECT 
            s.first_name || ' ' || s.last_name as student_name,
            COUNT(g.ID) as total_grades,
            ROUND(AVG(g.grade), 2) as average_grade
        FROM Students s
        LEFT JOIN Grades g ON s.student_id = g.student_id
        GROUP BY s.ID
        ORDER BY average_grade DESC
        LIMIT 5
    """, fetch_all=True)
    
    print("\nTop 5 Students by Average Grade:")
    for i, student in enumerate(grades_summary or [], 1):
        print(f"  {i}. {student['student_name']}: {student['average_grade']}%")
    
    # Get activity log
    activities = db.get_activity_log(limit=5)
    print(f"\nRecent Activities ({len(activities) if activities else 0}):")
    for activity in activities or []:
        print(f"  [{activity['timestamp']}] {activity['location']}: {activity['activity']}")
    
    # Get database info
    info = db.get_database_info()
    print(f"\nDatabase Info:")
    print(f"  Path: {info['path']}")
    print(f"  Size: {info['size'] / 1024:.2f} KB")
    print(f"  Tables: {len(info['tables'])}")
    for table in info['tables']:
        print(f"    - {table['name']}: {table['rows']} rows, {table['columns']} columns")