from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QApplication
from PyQt6.QtCore import Qt
from libs.DatabaseConnector import DatabaseConnector
from libs.CustomQtable import SmartTable
import sys


class GradeLevelMaster(QWidget):
    """
    Academic Master Data UI for Grades with a SmartTable that supports:
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
        self.init_grade_table()

    def init_grade_table(self):
        """
        Sets up the grade-level table with sample data.
        """
        table_layout = QVBoxLayout()
        self.main_layout.addLayout(table_layout)

        title_label = QLabel("Grades")
        title_label.setObjectName("MasterTitle")
        table_layout.addWidget(title_label)

        # Create SmartTable for grades
        self.grade_table = SmartTable(
            parent=self,
            enable_context_menu=True,
            enable_double_click=False
        )
        self.grade_table.setObjectName("MasterTable")  # for consistent QSS styling
        table_layout.addWidget(self.grade_table)

        # Set callbacks
        self.grade_table.set_actions(
            add=self.add_grade,
            edit=self.edit_grade,
            delete=self.delete_grade,
            double_click=self.on_grade_double_click
        )

        # Sample grade-level data
        grade_data = [
            ["Kinder 1", "A", "Ms. Navarro"],
            ["Kinder 1", "B", "Mr. Dela Cruz"],
            ["Kinder 2", "A", "Ms. Santos"],
            ["Kinder 2", "B", "Mr. Lim"],
            ["Grade 1", "A", "Ms. Reyes"],
            ["Grade 1", "B", "Mr. Gomez"],
            ["Grade 2", "A", "Ms. Cruz"],
            ["Grade 2", "B", "Ms. Martinez"],
            ["Grade 3", "A", "Mr. Santos"],
            ["Grade 3", "B", "Ms. Navarro"],
            ["Grade 4", "A", "Mr. Lim"],
            ["Grade 4", "B", "Ms. Reyes"],
            ["Grade 5", "A", "Mr. Gomez"],
            ["Grade 5", "B", "Ms. Cruz"],
            ["Grade 6", "A", "Ms. Martinez"],
            ["Grade 6", "B", "Mr. Dela Cruz"],
        ]
        headers = ["GradeLevel", "Section", "Advisor"]

        self.grade_table.update_data(grade_data, headers)

    # -----------------------------
    # Context menu callbacks
    # -----------------------------
    def add_grade(self):
        print("Add grade clicked")

    def edit_grade(self, row_index):
        row_index = int(row_index)
        cols = self.grade_table.columnCount()
        values = [self.grade_table.item(row_index, c).text()
                  if self.grade_table.item(row_index, c) else None
                  for c in range(cols)]
        print("Edit grade values:", values)

    def delete_grade(self, row_index):
        row_index = int(row_index)
        cols = self.grade_table.columnCount()
        values = [self.grade_table.item(row_index, c).text()
                  if self.grade_table.item(row_index, c) else None
                  for c in range(cols)]
        print("Delete grade values:", values)

    # -----------------------------
    # Double-click callback
    # -----------------------------
    def on_grade_double_click(self, row_index):
        """
        Handle double-click on a grade table row.

        Args:
            row_index (int): Index of the row double-clicked.
        """
        cols = self.grade_table.columnCount()
        values = [self.grade_table.item(row_index, c).text()
                  if self.grade_table.item(row_index, c) else None
                  for c in range(cols)]
        print("Double-clicked grade values:", values)


if __name__ == "__main__":
    db = DatabaseConnector()
    app = QApplication(sys.argv)
    window = GradeLevelMaster(db)
    window.show()
    sys.exit(app.exec())