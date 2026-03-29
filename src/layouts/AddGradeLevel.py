import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QLineEdit, QPushButton, QFormLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt


class AddGradeLevel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Sample Form")
        self.setFixedSize(300, 180)

        # Widgets
        self.lbl_name = QLabel("Name:")
        self.txt_name = QLineEdit()

        self.lbl_age = QLabel("Age:")
        self.txt_age = QLineEdit()

        self.btn_submit = QPushButton("Submit")
        self.btn_cancel = QPushButton("Cancel")

        # Signals
        self.btn_submit.clicked.connect(self.submit)
        self.btn_cancel.clicked.connect(self.close)

        # Layout
        form = QFormLayout()
        form.addRow(self.lbl_name, self.txt_name)
        form.addRow(self.lbl_age, self.txt_age)

        button_row = QHBoxLayout()
        button_row.addWidget(self.btn_submit)
        button_row.addWidget(self.btn_cancel)

        form.addRow(button_row)
        self.setLayout(form)

    def submit(self):
        name = self.txt_name.text()
        age = self.txt_age.text()
        print(f"Name: {name}, Age: {age}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AddGradeLevel()
    win.show()
    sys.exit(app.exec())