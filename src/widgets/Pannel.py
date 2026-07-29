from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QPushButton, QLabel, QFrame)
from PyQt6.QtCore import Qt

class SidePanel(QFrame):
    """Side panel with buttons only"""
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        
        # Header
        header = QLabel("📋 MENU")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Buttons only
        self.btn_dashboard = QPushButton("📊 Dashboard")
        self.btn_dashboard.setProperty("active", True)
        self.btn_dashboard.clicked.connect(lambda: self.button_clicked("Dashboard"))
        
        self.btn_students = QPushButton("👨‍🎓 Students")
        self.btn_students.clicked.connect(lambda: self.button_clicked("Students"))
        
        self.btn_grades = QPushButton("📝 Grades")
        self.btn_grades.clicked.connect(lambda: self.button_clicked("Grades"))
        
        self.btn_reports = QPushButton("📊 Reports")
        self.btn_reports.clicked.connect(lambda: self.button_clicked("Reports"))
        
        self.btn_settings = QPushButton("⚙️ Settings")
        self.btn_settings.clicked.connect(lambda: self.button_clicked("Settings"))
        
        self.btn_help = QPushButton("❓ Help")
        self.btn_help.clicked.connect(lambda: self.button_clicked("Help"))
        
        # Add buttons
        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_students)
        layout.addWidget(self.btn_grades)
        layout.addWidget(self.btn_reports)
        layout.addWidget(self.btn_settings)
        layout.addWidget(self.btn_help)
        layout.addStretch()
        
        # Footer
        footer = QLabel("v1.0.0")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setObjectName("version_label")
        layout.addWidget(footer)
        
        self.buttons = [self.btn_dashboard, self.btn_students, self.btn_grades, 
                       self.btn_reports, self.btn_settings, self.btn_help]

        self.parent_window = parent

        
    def button_clicked(self, name):
        """Handle button clicks and update active state"""
        # Reset all buttons
        for btn in self.buttons:
            btn.setProperty("active", False)
            btn.setStyleSheet("")
        
        # Set active for clicked button
        sender = self.sender()
        sender.setProperty("active", True)
        
        # Notify parent to switch page
        if self.parent_window:
            self.parent_window.switch_page(name)
