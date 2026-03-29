from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QPushButton
from PyQt6.QtCore import Qt
from layouts.DatabaseConnector import DatabaseConnector
from layouts.CustomQtable import SmartTable
from layouts.MessageTypes import MessageBox

from forms.AddGradeLevel import AddGradeLevel

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

        self.init_ui()

    def init_ui(self):
        self.init_grade_table()

    def init_grade_table(self):
        table_layout = QVBoxLayout()
        self.main_layout.addLayout(table_layout)

        title_label = QLabel("Academic Levels")
        title_label.setObjectName("MasterTitle")
        table_layout.addWidget(title_label)

        self.grade_table = SmartTable(
            parent=self,
            enable_context_menu=True,
            enable_double_click=False
        )
        self.grade_table.setObjectName("MasterTable")
        table_layout.addWidget(self.grade_table)

        self.grade_table.set_actions(
            add=self.add_grade,
            edit=self.edit_grade,
            delete=self.delete_grade,
            double_click=self.on_grade_double_click
        )

        self.update_table_data()


    def update_table_data(self):
        # -----------------------------
        # LOAD HEADERS + VALUES FROM DB
        # -----------------------------
        # table_info = self.db.get_table_info("Levels")
        # headers = [col["name"] for col in table_info]   # ['ID','LevelName','Category']

        raw_rows = self.db.get_levels_no_id()                 # list of dicts
        values = [[row[h] for h in ["Level"]] for row in raw_rows]
        

        self.grade_table.update_data(values, ["Level"])


    # -----------------------------
    # Context menu callbacks
    # -----------------------------
    def add_grade(self):
        dlg = AddGradeLevel(db=self.db, parent=self)
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
        dlg = AddGradeLevel(db=self.db, data=values[0], parent=self)
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