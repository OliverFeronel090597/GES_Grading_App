from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                            QLabel, QGroupBox, QTableWidget, QTableWidgetItem,
                            QHeaderView, QFrame, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from src.Database.Database import Database

class DashboardPage(QWidget):
    """Dashboard page content with grid layout"""
    def __init__(self, parent="", db:Database=""):
        super().__init__(parent)
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.main_layout)

        self.db = db

        self.root_parent = parent
        # Header GroupBox
        header_group = QGroupBox()
        header_group.setObjectName("header_group")
        header_group.setStyleSheet("""
            QGroupBox#header_group {
                background-color: #001eff;
                border-radius: 10px;
                border: none;
                padding: 10px;
                margin-bottom: 10px;
            }
        """)
        
        header_layout = QVBoxLayout()
        header_group.setLayout(header_layout)
        
        # School name
        self.school_name = QLabel("Guintas Elementary School")
        self.school_name.setObjectName("school_name")
        self.school_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.school_name.setStyleSheet("""
            QLabel#school_name {
                color: #ffffff;
                font-size: 50px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        header_layout.addWidget(self.school_name)

        # School location
        self.school_location = QLabel("Guintas, Leganes, Iloilo")
        self.school_location.setObjectName("school_location")
        self.school_location.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.school_location.setStyleSheet("""
            QLabel#school_location {
                color: #ffffff;
                font-size: 25px;
                background-color: transparent;
            }
        """)
        header_layout.addWidget(self.school_location)
        
        self.main_layout.addWidget(header_group)

        # Grid for tables
        grid = QGridLayout()
        self.main_layout.addLayout(grid)

        tables = self.db.get_all_tables()
        for i, table in enumerate(tables):
            lbl = QLabel(table)
            lbl.setObjectName("table_label")
            lbl.setStyleSheet("""
                QLabel#table_label {
                    color: #333333;
                    background-color: #e3f2fd;
                    padding: 10px 20px;
                    border-radius: 6px;
                    border: 1px solid #90caf9;
                    font-weight: bold;
                    font-size: 14px;
                }
                QLabel#table_label:hover {
                    background-color: #bbdefb;
                    border-color: #42a5f5;
                }
            """)
            grid.addWidget(lbl, 0, i)