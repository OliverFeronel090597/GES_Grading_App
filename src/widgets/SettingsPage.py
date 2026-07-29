from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel)

class SettingsPage(QWidget):
    """Settings page content"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)