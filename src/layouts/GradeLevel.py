from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QPushButton
from PyQt6.QtCore import Qt
from layouts.DatabaseConnector import DatabaseConnector
from layouts.CustomQtable import SmartTable
from layouts.MessageTypes import MessageBox

from forms.AddEditGradeLevel import AddEditGradeLevel

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

        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowCloseButtonHint
        )

        self.add_grade_level = None
        self.db = db
        self.msg = MessageBox(self)

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.init_grade_table()

    def init_grade_table(self):
        table_layout = QVBoxLayout()
        self.main_layout.addLayout(table_layout)

        title_label = QLabel("Levels")
        title_label.setObjectName("MasterTitle")
        table_layout.addWidget(title_label)

        self.grade_table = SmartTable(
            parent=self,
            enable_context_menu=True,
            enable_double_click=False,
            enable_vertical_header=False
        )
        self.grade_table.setObjectName("MasterTable")
        table_layout.addWidget(self.grade_table)

        self.grade_table.set_actions(
            add=self.add_grade_level,
            edit=self.edit_grade,
            delete=self.delete_grade,
            double_click=self.on_grade_double_click
        )

        self.update_table_data()

    def update_table_data(self):
        """
        Load grade levels from DB and update the table widget
        """
        raw_rows = self.db.get_all_levels()  # list of dicts

        # fallback if DB returns empty
        if not raw_rows:
            raw_rows = [{"ID": 1, "LevelName": "Sample Only", "Category": "Default"}]

        # extract true column names
        col_info = self.db.get_table_info("Levels")
        print(col_info)
        headers = [c["name"] for c in col_info]

        # build table rows
        values = [[row.get(h) for h in headers] for row in raw_rows]

        self.grade_table.update_data(values, headers)

    # Context menu callbacks
    # -----------------------------
    def add_grade_level(self):
        dlg = AddEditGradeLevel(db=self.db, parent=self)
        if dlg.exec():
            self.update_table_data()
        else:
            print("Cancelled")

    def edit_grade(self, row_index):
        row_index = int(row_index)
        cols = self.grade_table.columnCount()
        values = [self.grade_table.item(row_index, c).text()
                  if self.grade_table.item(row_index, c) else None
                  for c in range(cols)]
        dlg = AddEditGradeLevel(db=self.db, data=values, parent=self)
        if dlg.exec():
            self.update_table_data()
        else:
            print("Cancelled")

    def delete_grade(self, row_index):
        row_index = int(row_index)
        cols = self.grade_table.columnCount()
        values = [self.grade_table.item(row_index, c).text()
                  if self.grade_table.item(row_index, c) else None
                  for c in range(cols)]
        print(values)
        if self.msg.question("Confirm", f"Do you want to delete grade level {values}?"):
            self.db.delete_level(values[0])
            self.update_table_data()
        else:
            print("User clicked No")

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