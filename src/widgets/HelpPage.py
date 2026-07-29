from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel)

class HelpPage(QWidget):
    """Help page content"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)