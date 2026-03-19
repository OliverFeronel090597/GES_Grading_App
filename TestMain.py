from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QApplication
from PyQt6.QtCore import Qt
from libs.DatabaseConnector import DatabaseConnector
from libs.CustomQtable import SmartTable
import sys


class AcademicMasterData(QWidget):
    """
    Academic Master Data UI with a SmartTable that supports:
        - Add / Edit / Delete context menu
        - Double-click row callback
    """

    def __init__(self, db: DatabaseConnector, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Academic Master Data")
        self.db = db

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.initUI()

    def initUI(self):
        self.add_grade_level()

    def add_grade_level(self):
        """
        Sets up the grade-level table with sample data.
        """
        gl_layout = QVBoxLayout()
        self.main_layout.addLayout(gl_layout)

        title = QLabel("Add Students")
        gl_layout.addWidget(title)

        # Enable context menu and double-click
        self.gl_table = SmartTable(enable_context_menu=True, enable_double_click=False)
        gl_layout.addWidget(self.gl_table)

        # Set menu actions and double-click callback
        self.gl_table.set_actions(
            add=self.add_row,
            edit=self.edit_row,
            delete=self.delete_row,
            double_click=self.on_row_double_click
        )

        # Sample data
        data = [
            [1, "Math", "Mr. Cruz"],
            [2, "English", "Ms. Santos"],
            [3, "Science", "Mr. Lim"],
        ]
        headers = ["ID", "Subject", "Teacher"]

        self.gl_table.update_data(data, headers)

    # -----------------------------
    # Context menu callbacks
    # -----------------------------
    def add_row(self):
        print("Add row clicked")

    def edit_row(self, row):
        row = int(row)
        cols = self.gl_table.columnCount()
        values = [self.gl_table.item(row, c).text() if self.gl_table.item(row, c) else None
                  for c in range(cols)]
        print("Edit row values:", values)

    def delete_row(self, row):
        row = int(row)
        cols = self.gl_table.columnCount()
        values = [self.gl_table.item(row, c).text() if self.gl_table.item(row, c) else None
                  for c in range(cols)]
        print("Delete row values:", values)

    # -----------------------------
    # Double-click callback
    # -----------------------------
    def on_row_double_click(self, row):
        """
        Handle double-click on a table row.

        Args:
            row (int): Index of the row double-clicked.
        """
        cols = self.gl_table.columnCount()
        values = [self.gl_table.item(row, c).text() if self.gl_table.item(row, c) else None
                  for c in range(cols)]
        print("Double-clicked row values:", values)


if __name__ == "__main__":
    db = DatabaseConnector()
    app = QApplication(sys.argv)
    win = AcademicMasterData(db)
    win.show()
    sys.exit(app.exec())

    