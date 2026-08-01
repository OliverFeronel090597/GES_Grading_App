from PyQt6.QtWidgets            import (QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                                        QPushButton, QLabel, QFrame, QStackedWidget, QTextEdit,
                                        QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox)
from PyQt6.QtCore               import (Qt, QTimer)
from PyQt6.QtGui                import (QFont, QColor)
import sys

from src.widgets.Pannel         import SidePanel
from src.widgets.DashboardPage  import DashboardPage
from src.widgets.StudentsPage   import StudentsPage
from src.widgets.GradesPage     import GradesPage
from src.widgets.ReportsPage    import ReportsPage
from src.widgets.SettingsPage   import SettingsPage
from src.widgets.HelpPage       import HelpPage
from src.Database.Database      import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 1100, 700)

        self.db = Database()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        
        # Side panel
        self.side_panel = SidePanel(self)
        main_layout.addWidget(self.side_panel)
        
        # Content area with stacked widget
        self.content_area = QWidget()
        self.content_area.setStyleSheet("background-color: white;")
        content_layout = QVBoxLayout()
        self.content_area.setLayout(content_layout)
        content_layout.setContentsMargins(25, 25, 25, 25)
        
        # Stacked widget
        self.stacked_widget = QStackedWidget()
        
        # Add pages
        self.stacked_widget.addWidget(DashboardPage(parent=self, db=self.db))   # Index 0
        self.stacked_widget.addWidget(StudentsPage())    # Index 1
        self.stacked_widget.addWidget(GradesPage())      # Index 2
        self.stacked_widget.addWidget(ReportsPage())     # Index 3
        self.stacked_widget.addWidget(SettingsPage())    # Index 4
        self.stacked_widget.addWidget(HelpPage())        # Index 5
        
        content_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(self.content_area)
        
        self.apply_style()

        self.timer = QTimer()
        self.timer.timeout.connect(self.apply_style)
        self.timer.start(100)  # Interval in milliseconds

    def apply_style(self):
        with open("styles/Styles.qss", "r") as f:
            self.setStyleSheet(f.read())

    def switch_page(self, page_name):
        """Switch to the selected page"""
        page_map = {
            "Dashboard": 0,
            "Students": 1,
            "Grades": 2,
            "Reports": 3,
            "Settings": 4,
            "Help": 5
        }
        
        if page_name in page_map:
            index = page_map[page_name]
            self.stacked_widget.setCurrentIndex(index)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())