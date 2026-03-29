from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem
)
import sys
from ..layouts.CustomQtable import SmartTable

class ListSample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Table Demo")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table = SmartTable()
        layout.addWidget(self.table)

        self.table.set_actions(
            add=self.add_row,
            edit=self.edit_row,
            delete=self.delete_row
        )

        # Sample data
        data = [
            [1, "Math", "Mr. Cruz"],
            [2, "English", "Ms. Santos"],
            [3, "Science", "Mr. Lim"],
        ]
        headers = ["ID", "Subject", "Teacher"]

        self.table.update_data(data, headers)

    def add_row(self):
        print("Add row clicked")

    def edit_row(self, row):
        print("Edit row:", row)

    def delete_row(self, row):
        print("Delete row:", row)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ListSample()
    win.show()
    sys.exit(app.exec())