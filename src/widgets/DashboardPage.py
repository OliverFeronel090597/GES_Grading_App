from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                            QLabel, QGroupBox, QTableWidget, QTableWidgetItem,
                            QHeaderView, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

class DashboardPage(QWidget):
    """Dashboard page content with grid layout"""
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Title
        title = QLabel("📊 Dashboard")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #1a237e; padding: 10px 0 20px 0;")
        main_layout.addWidget(title)
  