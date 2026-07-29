from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel)

class ReportsPage(QWidget):
    """Reports page content"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
   