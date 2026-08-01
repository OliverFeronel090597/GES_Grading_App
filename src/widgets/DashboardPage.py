from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                            QLabel, QGroupBox, QTableWidget, QTableWidgetItem,
                            QHeaderView, QFrame, QGridLayout, QSizePolicy)
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWebEngineWidgets import QWebEngineView

from src.Database.Database import Database

class DashboardPage(QWidget):
    """Dashboard page content with grid layout"""
    def __init__(self, parent="", db:Database=""):
        super().__init__(parent)
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for full size
        self.setLayout(self.main_layout)

        self.db = db
        self.root_parent = parent

        # Create QWebEngineView
        self.header_new = QWebEngineView()
        self.header_new.load(QUrl.fromLocalFile(r"C:\Users\O.Feronel\OneDrive - ams OSRAM\Documents\PYTHON_EXTERN_PROJ\GUINTAS_ELEM_GRADING_SYSTEM\html\Header.html"))
        
        # Make it expand to fill available space
        self.header_new.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )
        
        # Add to layout - it will automatically resize with the parent
        self.main_layout.addWidget(self.header_new)

        # Optional: Timer to refresh the HTML (if needed)
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_html)
        self.timer.start(5000)  # Interval in milliseconds
    
    def refresh_html(self):
        """Refresh the HTML content"""
        self.header_new.load(QUrl.fromLocalFile(r"C:\Users\O.Feronel\OneDrive - ams OSRAM\Documents\PYTHON_EXTERN_PROJ\GUINTAS_ELEM_GRADING_SYSTEM\html\Header.html"))
    
    def resizeEvent(self, event):
        """Handle resize events to ensure webview fills the space"""
        super().resizeEvent(event)
        # The webview will automatically resize due to the layout
        # No manual resizing needed
    
    def set_html_file(self, html_path):
        """Change the HTML file to display"""
        if html_path:
            self.header_new.load(QUrl.fromLocalFile(html_path))