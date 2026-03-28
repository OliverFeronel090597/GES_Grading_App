from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QApplication
from PyQt6.QtCore import Qt
from libs.DatabaseConnector import DatabaseConnector
from libs.CustomQtable import SmartTable
import sys


class GradeSubject(QWidget):
    """
    Academic Master Data UI for Subjects with a SmartTable that supports:
        - Add / Edit / Delete context menu
        - Double-click row callback
    """

    def __init__(self, db: DatabaseConnector, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Academic Master Data")
        self.db = db

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.init_ui()

    def init_ui(self):
        self.init_subject_table()

    def init_subject_table(self):
        """
        Sets up the subjects table with sample data.
        """
        table_layout = QVBoxLayout()
        self.main_layout.addLayout(table_layout)

        title_label = QLabel("Subjects")
        title_label.setObjectName("MasterTitle")
        table_layout.addWidget(title_label)

        # Create SmartTable for subjects
        self.subject_table = SmartTable(
            parent=self,
            enable_context_menu=True,
            enable_double_click=False
        )
        self.subject_table.setObjectName("MasterTable")  # for consistent QSS styling
        table_layout.addWidget(self.subject_table)

        # Set menu actions and double-click callback
        self.subject_table.set_actions(
            add=self.add_subject,
            edit=self.edit_subject,
            delete=self.delete_subject,
            double_click=self.on_subject_double_click
        )

        # Sample subject data
        subject_data = [
            ["Mathematics", "Mr. Cruz", "Grade 1"],
            ["English", "Ms. Santos", "Grade 1"],
            ["Science", "Mr. Lim", "Grade 2"],
            ["Filipino", "Ms. Reyes", "Grade 2"],
            ["Arts", "Ms. Navarro", "Grade 3"],
            ["Music", "Mr. Gomez", "Grade 3"],
            ["Physical Education", "Mr. Dela Cruz", "Grade 4"],
            ["Mathematics", "Mr. Cruz", "Grade 4"],
            ["English", "Ms. Santos", "Grade 5"],
            ["Science", "Mr. Lim", "Grade 5"],
            ["Filipino", "Ms. Reyes", "Grade 6"],
            ["Arts", "Ms. Navarro", "Grade 6"],
        ]
        subject_headers = ["Subject", "Advisor", "GradeLevel"]

        self.subject_table.update_data(subject_data, subject_headers)

    # -----------------------------
    # Context menu callbacks
    # -----------------------------
    def add_subject(self):
        print("Add subject clicked")

    def edit_subject(self, row_index):
        row_index = int(row_index)
        cols = self.subject_table.columnCount()
        values = [self.subject_table.item(row_index, c).text()
                  if self.subject_table.item(row_index, c) else None
                  for c in range(cols)]
        print("Edit subject values:", values)

    def delete_subject(self, row_index):
        row_index = int(row_index)
        cols = self.subject_table.columnCount()
        values = [self.subject_table.item(row_index, c).text()
                  if self.subject_table.item(row_index, c) else None
                  for c in range(cols)]
        print("Delete subject values:", values)

    # -----------------------------
    # Double-click callback
    # -----------------------------
    def on_subject_double_click(self, row_index):
        """
        Handle double-click on a table row.

        Args:
            row_index (int): Index of the row double-clicked.
        """
        cols = self.subject_table.columnCount()
        values = [self.subject_table.item(row_index, c).text()
                  if self.subject_table.item(row_index, c) else None
                  for c in range(cols)]
        print("Double-clicked subject values:", values)


if __name__ == "__main__":
    db = DatabaseConnector()
    app = QApplication(sys.argv)
    window = GradeSubject(db)
    window.show()
    sys.exit(app.exec())