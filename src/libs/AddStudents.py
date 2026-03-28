from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QApplication
from PyQt6.QtCore import Qt
from libs.DatabaseConnector import DatabaseConnector
from libs.CustomQtable import SmartTable
import sys


class StudentMasterData(QWidget):
    """
    Academic Master Data UI with a SmartTable that supports:
        - Add / Edit / Delete context menu
        - Optional double-click row callback
    """

    def __init__(self, db: DatabaseConnector, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Academic Master Data")
        self.db = db

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.init_ui()

    def init_ui(self):
        self.init_student_table()

    def init_student_table(self):
        """
        Sets up the students table with sample data.
        """
        table_layout = QVBoxLayout()
        self.main_layout.addLayout(table_layout)

        title_label = QLabel("Students")
        title_label.setObjectName("MasterTitle")
        table_layout.addWidget(title_label)

        # Create SmartTable for students
        self.student_table = SmartTable(
            parent=self,
            enable_context_menu=True,
            enable_double_click=False
        )
        self.student_table.setObjectName("MasterTable")
        table_layout.addWidget(self.student_table)

        # Set callbacks for context menu and double-click
        self.student_table.set_actions(
            add=self.add_student,
            edit=self.edit_student,
            delete=self.delete_student,
            double_click=self.on_student_double_click
        )

        # Sample student data
        student_data = [
            ["Juan Dela Cruz", "Maria Dela Cruz", "2026-2027", "Grade 1"],
            ["Ana Santos", "Jose Santos", "2026-2027", "Grade 2"],
            ["Miguel Reyes", "Lucia Reyes", "2026-2027", "Grade 3"],
            ["Liza Navarro", "Ramon Navarro", "2026-2027", "Kinder 1"],
            ["Carlos Gomez", "Elena Gomez", "2026-2027", "Grade 6"],
            ["Sofia Martinez", "Luis Martinez", "2026-2027", "Grade 4"],
            ["Marvin Cruz", "Sofia Cruz", "2026-2027", "Grade 1"],
            ["Isabella Flores", "Marco Flores", "2026-2027", "Grade 2"],
            ["Gabriel Reyes", "Lucia Reyes", "2026-2027", "Grade 3"],
            ["Lara Navarro", "Ramon Navarro", "2026-2027", "Kinder 1"],
            ["Carlos Santos", "Jose Santos", "2026-2027", "Grade 6"],
            ["Sofia Lim", "Miguel Lim", "2026-2027", "Grade 4"],
            ["Miguel Dela Cruz", "Juan Dela Cruz", "2026-2027", "Grade 1"],
            ["Ana Reyes", "Gabriel Reyes", "2026-2027", "Grade 2"],
            ["Liza Santos", "Carlos Santos", "2026-2027", "Grade 3"],
            ["Elena Martinez", "Sofia Martinez", "2026-2027", "Grade 5"],
            ["Ramon Gomez", "Carlos Gomez", "2026-2027", "Grade 6"],
            ["Luis Navarro", "Lara Navarro", "2026-2027", "Kinder 2"],
            ["Maria Lim", "Miguel Lim", "2026-2027", "Grade 2"],
            ["Sofia Cruz", "Marvin Cruz", "2026-2027", "Grade 1"],
        ]
        headers = ["Name", "Guardian", "SchoolYear", "GradeLevel"]

        self.student_table.update_data(student_data, headers, filter_text="Grade 1")

    # -----------------------------
    # Context menu callbacks
    # -----------------------------
    def add_student(self):
        print("Add student clicked")

    def edit_student(self, row_index):
        row_index = int(row_index)
        cols = self.student_table.columnCount()
        values = [self.student_table.item(row_index, c).text() 
                  if self.student_table.item(row_index, c) else None
                  for c in range(cols)]
        print("Edit student values:", values)

    def delete_student(self, row_index):
        row_index = int(row_index)
        cols = self.student_table.columnCount()
        values = [self.student_table.item(row_index, c).text() 
                  if self.student_table.item(row_index, c) else None
                  for c in range(cols)]
        print("Delete student values:", values)

    # -----------------------------
    # Double-click callback
    # -----------------------------
    def on_student_double_click(self, row_index):
        """
        Handle double-click on a student table row.

        Args:
            row_index (int): Index of the row double-clicked.
        """
        cols = self.student_table.columnCount()
        values = [self.student_table.item(row_index, c).text() 
                  if self.student_table.item(row_index, c) else None
                  for c in range(cols)]
        print("Double-clicked student values:", values)


if __name__ == "__main__":
    db = DatabaseConnector()
    app = QApplication(sys.argv)
    window = StudentMasterData(db)
    window.show()
    sys.exit(app.exec())