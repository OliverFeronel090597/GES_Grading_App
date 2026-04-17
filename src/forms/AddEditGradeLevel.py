from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton,
    QFormLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt
from layouts.DatabaseConnector import DatabaseConnector
from layouts.LineEditTitleMode import TitleCaseLineEdit


class AddEditGradeLevel(QDialog):
    def __init__(self, db: DatabaseConnector = None, data:list=None, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Edit Grade Level" if data else "Add Grade Level")
        self.setObjectName("form")
        self.setFixedSize(300, 100)

        # Proper dialog flags
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.WindowCloseButtonHint |
            Qt.WindowType.MSWindowsFixedSizeDialogHint
        )

        self.setModal(True)
        self.db = db
        self.data = data

        # Widgets
        self.add_level_lbl = QLabel("Level:")
        self.add_level_lbl.setObjectName("form")

        self.level_text = TitleCaseLineEdit()
        self.level_text.setObjectName("form")
        if self.data:
            self.level_text.setText(self.data[1])

        self.btn_submit = QPushButton("Submit")
        self.btn_submit.setObjectName("form")

        # Signals
        self.btn_submit.clicked.connect(self.submit)
        self.level_text.returnPressed.connect(self.submit)

        # Layout
        form = QFormLayout()
        form.addRow(self.add_level_lbl, self.level_text)

        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(self.btn_submit)

        form.addRow(button_row)
        self.setLayout(form)

    def submit(self):
        level = self.level_text.text().strip()
        if self.data:
            '''It means we are in edit mode'''
            self.db.update_level(self.data[0], level)
        else:
            '''Add mode'''
            self.db.add_level(level)
        # if not name:
        #     print("No level entered!")
        #     return

        # try:
        #     if self.data:
        #         # EDIT mode
        #         level_data = self.db.get_level(self.data)
        #         if level_data:
        #             level_id = level_data["ID"]
        #             self.db.edit_level(level_id, name)  # call the correct method
        #             print(f"Updated Level: {self.data} → {name}")
        #         else:
        #             print(f"Original level '{self.data}' not found.")
        #     else:
        #         # ADD mode
        #         if self.db.get_level_id(name):
        #             print(f"Level '{name}' already exists!")
        #             return
        #         self.db.add_level(name)
        #         print(f"Added Level: {name}")

        #     self.accept()

        # except Exception as e:
        #     print(f"Database error: {e}")

        self.accept()  # close dialog with success