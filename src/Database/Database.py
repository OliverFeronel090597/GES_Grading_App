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
            conn.rollback()
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
            # SCHOOL_YEARS TABLE (New)
            # -----------------------------------------------------
            """
            CREATE TABLE IF NOT EXISTS SchoolYears (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                school_year TEXT NOT NULL UNIQUE,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,

            # -----------------------------------------------------
            # LEVELS TABLE
            # -----------------------------------------------------
            """
            CREATE TABLE IF NOT EXISTS Levels (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                level_section TEXT NOT NULL UNIQUE,
                school_year_id INTEGER,
                FOREIGN KEY (school_year_id) REFERENCES SchoolYears(ID)
            );
            """,

            # -----------------------------------------------------
            # SUBJECTS TABLE
            # -----------------------------------------------------
            """
            CREATE TABLE IF NOT EXISTS Subjects (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_group TEXT NOT NULL,
                subject TEXT NOT NULL,
                school_year_id INTEGER,
                FOREIGN KEY (school_year_id) REFERENCES SchoolYears(ID)
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
                school_year_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (level_id) REFERENCES Levels(ID),
                FOREIGN KEY (school_year_id) REFERENCES SchoolYears(ID)
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
                school_year_id INTEGER,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES Students(student_id),
                FOREIGN KEY (subject_id) REFERENCES Subjects(ID),
                FOREIGN KEY (school_year_id) REFERENCES SchoolYears(ID),
                UNIQUE(student_id, subject_id, semester, school_year_id)
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
                school_year_id INTEGER,
                FOREIGN KEY (student_id) REFERENCES Students(student_id),
                FOREIGN KEY (school_year_id) REFERENCES SchoolYears(ID),
                UNIQUE(student_id, date, school_year_id)
            );
            """,

            # -----------------------------------------------------
            # ACTIVITY LOG TABLE
            # -----------------------------------------------------
            """
            CREATE TABLE IF NOT EXISTS ActivityLog (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                activity TEXT NOT NULL,
                changes TEXT NOT NULL,
                school_year_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (school_year_id) REFERENCES SchoolYears(ID)
            );
            """,
                        
            # -----------------------------------------------------
            # USER LOGIN
            # -----------------------------------------------------
            """
            CREATE TABLE IF NOT EXISTS Credentials (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                password TEXT NOT NULL
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
    # SCHOOL YEAR FUNCTIONS
    # ============================================================
    def get_current_school_year(self) -> Optional[Dict]:
        """Get the active school year."""
        return self.execute(
            "SELECT * FROM SchoolYears WHERE is_active = 1 LIMIT 1",
            fetch_one=True
        )

    def get_school_year_id(self, school_year: str) -> Optional[int]:
        """Get school year ID by year string."""
        result = self.execute(
            "SELECT ID FROM SchoolYears WHERE school_year = ?",
            (school_year,), fetch_one=True
        )
        return result['ID'] if result else None

    def add_school_year(self, school_year: str, is_active: bool = False) -> Optional[int]:
        """Add a new school year."""
        data = {
            'school_year': school_year,
            'is_active': 1 if is_active else 0
        }
        return self.insert('SchoolYears', data)

    def set_active_school_year(self, school_year_id: int) -> bool:
        """Set a school year as active (deactivate others)."""
        queries = [
            ("UPDATE SchoolYears SET is_active = 0 WHERE is_active = 1", ()),
            ("UPDATE SchoolYears SET is_active = 1 WHERE ID = ?", (school_year_id,))
        ]
        return self.execute_transaction(queries)

    def get_all_school_years(self) -> Optional[List[Dict]]:
        """Get all school years."""
        return self.select('SchoolYears', order_by='school_year DESC')

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
            
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_backup = f"{self.db_path}.pre_restore_{timestamp}"
            self.backup_database(temp_backup)
            
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
    def log_activity(self, location: str, activity: str, changes: str, school_year_id: int = None) -> bool:
        """
        Log an activity to the activity log.
        
        Args:
            location: Where the activity occurred
            activity: What action was performed
            changes: Details of what changed
            school_year_id: Optional school year ID
        
        Returns:
            True if successful, False otherwise
        """
        query = """
            INSERT INTO ActivityLog (location, activity, changes, school_year_id) 
            VALUES (?, ?, ?, ?)
        """
        return self.execute(query, (location, activity, changes, school_year_id)) is not False

    def get_activity_log(self, limit: int = 100, school_year_id: int = None) -> Optional[List[Dict]]:
        """
        Get recent activity log entries.
        
        Args:
            limit: Number of records to return
            school_year_id: Optional filter by school year
        
        Returns:
            List of activity log entries or None if error
        """
        if school_year_id:
            query = """
                SELECT ID, location, activity, changes, timestamp 
                FROM ActivityLog 
                WHERE school_year_id = ?
                ORDER BY timestamp DESC 
                LIMIT ?
            """
            return self.execute(query, (school_year_id, limit), fetch_all=True)
        else:
            query = """
                SELECT ID, location, activity, changes, timestamp 
                FROM ActivityLog 
                ORDER BY timestamp DESC 
                LIMIT ?
            """
            return self.execute(query, (limit,), fetch_all=True)

    # ---------- DATA VALIDATION ----------
    def validate_foreign_key(self, table: str, column: str, value: Any) -> bool:
        """Validate if a foreign key value exists in the referenced table."""
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
        
        queries = []
        students = []
        
        # ---------- SCHOOL YEARS ----------
        school_years = ["2023-2024", "2024-2025", "2025-2026"]
        school_year_ids = {}
        
        for i, year in enumerate(school_years):
            is_active = 1 if i == 1 else 0  # 2024-2025 as active
            queries.append((
                "INSERT INTO SchoolYears (school_year, is_active) VALUES (?, ?)",
                (year, is_active)
            ))
            # Store for later use (we'll get actual IDs after insert)
        
        # Execute school year inserts first to get IDs
        for year in school_years:
            result = self.execute(
                "SELECT ID FROM SchoolYears WHERE school_year = ?",
                (year,), fetch_one=True
            )
            if result:
                school_year_ids[year] = result['ID']
        
        # Get current active school year ID
        active_year = self.get_current_school_year()
        active_year_id = active_year['ID'] if active_year else 1
        
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
                    "INSERT INTO Levels (level, level_section, school_year_id) VALUES (?, ?, ?)",
                    (level, section, active_year_id)
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
                    "INSERT INTO Subjects (subject_group, subject, school_year_id) VALUES (?, ?, ?)",
                    (group, subject, active_year_id)
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
                    """INSERT INTO Students (student_id, first_name, last_name, level_id, section, school_year_id) 
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (sid, first, last, level_id, section, active_year_id)
                ))
        
        # ---------- GRADES ----------
        if students:
            subject_ids = self.execute(
                "SELECT ID, subject FROM Subjects WHERE school_year_id = ?",
                (active_year_id,), fetch_all=True
            )
            subject_map = {s['subject']: s['ID'] for s in subject_ids} if subject_ids else {}
            
            import random
            random.seed(42)
            
            for student in students:
                sid = student[0]
                for subject_name, subject_id in subject_map.items():
                    grade = random.randint(70, 98)
                    queries.append((
                        """INSERT INTO Grades (student_id, subject_id, grade, semester, school_year_id) 
                        VALUES (?, ?, ?, ?, ?)""",
                        (sid, subject_id, grade, 1, active_year_id)
                    ))
            
            # ---------- ATTENDANCE ----------
            from datetime import timedelta
            today = datetime.now().date()
            statuses = ['Present', 'Present', 'Present', 'Present', 'Absent', 'Late', 'Excused']
            
            for student in students:
                sid = student[0]
                for i in range(30, 0, -1):
                    date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
                    status = random.choice(statuses)
                    remarks = "" if status == "Present" else f"Student was {status.lower()}"
                    queries.append((
                        """INSERT INTO Attendance (student_id, date, status, remarks, school_year_id) 
                        VALUES (?, ?, ?, ?, ?)""",
                        (sid, date, status, remarks, active_year_id)
                    ))
        
        # ---------- ACTIVITY LOG ----------
        queries.append((
            """INSERT INTO ActivityLog (location, activity, changes, school_year_id) 
            VALUES (?, ?, ?, ?)""",
            ("Database", "Initialize", "Sample data populated successfully", active_year_id)
        ))
        
        # Execute all queries in a single transaction
        if queries:
            print(f"[INFO] Executing {len(queries)} sample data queries...")
            success = self.execute_transaction(queries)
            if success:
                print("[INFO] Sample data populated successfully!")
                self.log_activity("System", "Populate Sample Data", 
                                f"Inserted {len(queries)} records across all tables", active_year_id)
            else:
                print("[ERROR] Failed to populate sample data!")
        else:
            print("[INFO] No sample data to populate.")

# ============================================================
# SAMPLE DATA POPULATION - EXAMPLES FOR EACH TABLE
# ============================================================
if __name__ == "__main__":
    import random
    from datetime import datetime, timedelta


    db = Database()

    # ============================================================
    # 1. SCHOOL YEARS
    # ============================================================
    print("\n" + "="*50)
    print("1. SCHOOL YEARS")
    print("="*50)

    # Add school years
    school_years = ["2023-2024", "2024-2025", "2025-2026"]
    for i, year in enumerate(school_years):
        is_active = 1 if i == 1 else 0  # 2024-2025 as active
        result = db.add_school_year(year, is_active=bool(is_active))
        print(f"  Added: {year} (Active: {is_active}) - ID: {result}")

    # Get active school year
    active = db.get_current_school_year()
    print(f"\n  Active School Year: {active['school_year'] if active else 'None'}")

    # ============================================================
    # 2. LEVELS
    # ============================================================
    print("\n" + "="*50)
    print("2. LEVELS")
    print("="*50)

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
        data = {
            'level': level,
            'level_section': section,
            'school_year_id': active['ID']
        }
        result = db.insert('Levels', data)
        print(f"  Added: {level} - {section} (ID: {result})")

    # ============================================================
    # 3. SUBJECTS
    # ============================================================
    print("\n" + "="*50)
    print("3. SUBJECTS")
    print("="*50)

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
        data = {
            'subject_group': group,
            'subject': subject,
            'school_year_id': active['ID']
        }
        result = db.insert('Subjects', data)
        print(f"  Added: {group} - {subject} (ID: {result})")

    # ============================================================
    # 4. STUDENTS
    # ============================================================
    print("\n" + "="*50)
    print("4. STUDENTS")
    print("="*50)

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
        data = {
            'student_id': sid,
            'first_name': first,
            'last_name': last,
            'level_id': level_id,
            'section': section,
            'school_year_id': active['ID']
        }
        result = db.insert('Students', data)
        print(f"  Added: {first} {last} ({sid}) - ID: {result}")

    # ============================================================
    # 5. GRADES
    # ============================================================
    print("\n" + "="*50)
    print("5. GRADES")
    print("="*50)

    # Get all subjects for the active school year
    subject_list = db.select('Subjects', where={'school_year_id': active['ID']})
    subject_ids = [s['ID'] for s in subject_list]

    grade_count = 0
    for student in students:
        sid = student[0]
        for subject_id in subject_ids:
            grade = random.randint(70, 98)
            data = {
                'student_id': sid,
                'subject_id': subject_id,
                'grade': grade,
                'semester': 1,
                'school_year_id': active['ID']
            }
            result = db.insert('Grades', data)
            if result:
                grade_count += 1
                if grade_count <= 10:  # Show first 10 only
                    print(f"  Added: {student[1]} {student[2]} - Subject ID {subject_id}: {grade}%")

    print(f"\n  Total Grades Added: {grade_count}")

    # ============================================================
    # 6. ATTENDANCE
    # ============================================================
    print("\n" + "="*50)
    print("6. ATTENDANCE")
    print("="*50)

    statuses = ['Present', 'Present', 'Present', 'Present', 'Absent', 'Late', 'Excused']
    today = datetime.now().date()
    attendance_count = 0

    for student in students:
        sid = student[0]
        for i in range(10, 0, -1):  # Last 10 days
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            status = random.choice(statuses)
            remarks = "" if status == "Present" else f"Student was {status.lower()}"
            
            data = {
                'student_id': sid,
                'date': date,
                'status': status,
                'remarks': remarks,
                'school_year_id': active['ID']
            }
            result = db.insert('Attendance', data)
            if result:
                attendance_count += 1

    print(f"  Total Attendance Records Added: {attendance_count}")

    # ============================================================
    # 7. ACTIVITY LOG
    # ============================================================
    print("\n" + "="*50)
    print("7. ACTIVITY LOG")
    print("="*50)

    activities = [
        ("System", "Initialize", "Database initialized successfully"),
        ("Dashboard", "View", "User viewed dashboard"),
        ("Students", "Add", "New student enrolled: Pedro Reyes"),
        ("Grades", "Update", "Updated grades for Grade 7-A"),
        ("Reports", "Generate", "Generated class summary report"),
    ]

    for location, activity, changes in activities:
        data = {
            'location': location,
            'activity': activity,
            'changes': changes,
            'school_year_id': active['ID']
        }
        result = db.insert('ActivityLog', data)
        print(f"  Added: {location} - {activity} (ID: {result})")

    # ============================================================
    # SUMMARY
    # ============================================================
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)

    print(f"\n  School Years: {len(school_years)}")
    print(f"  Levels: {len(levels)}")
    print(f"  Subjects: {len(subjects)}")
    print(f"  Students: {len(students)}")
    print(f"  Grades: {grade_count}")
    print(f"  Attendance: {attendance_count}")
    print(f"  Activity Log: {len(activities)}")

    print("\n" + "="*50)
    print("✅ SAMPLE DATA POPULATION COMPLETE!")
    print("="*50)

    # Show some sample queries
    print("\n📊 SAMPLE QUERIES:")
    print("-" * 30)

    # Get top 5 students by average grade
    top_students = db.execute("""
        SELECT 
            s.first_name || ' ' || s.last_name as student_name,
            ROUND(AVG(g.grade), 2) as average_grade
        FROM Students s
        JOIN Grades g ON s.student_id = g.student_id
        WHERE s.school_year_id = ?
        GROUP BY s.ID
        ORDER BY average_grade DESC
        LIMIT 5
    """, (active['ID'],), fetch_all=True)

    print("\n  Top 5 Students:")
    for i, student in enumerate(top_students or [], 1):
        print(f"    {i}. {student['student_name']}: {student['average_grade']}%")

    # Show subject averages
    subject_averages = db.execute("""
        SELECT 
            sub.subject,
            ROUND(AVG(g.grade), 2) as avg_grade
        FROM Subjects sub
        JOIN Grades g ON sub.ID = g.subject_id
        WHERE sub.school_year_id = ?
        GROUP BY sub.ID
        ORDER BY avg_grade DESC
    """, (active['ID'],), fetch_all=True)

    print("\n  Subject Averages:")
    for subject in subject_averages or []:
        print(f"    {subject['subject']}: {subject['avg_grade']}%")