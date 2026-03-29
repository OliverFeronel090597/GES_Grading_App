from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QApplication, QSizePolicy
from layouts.DatabaseConnector import DatabaseConnector
from layouts.AddStudents import StudentMasterData
from layouts.AddSubject import GradeSubject
from layouts.GradeLevel import GradeLevelMaster
import sys


class AcademicMasterData(QWidget):
    """
    Academic Master Data UI with adjustable layout:
        - Add / Edit / Delete context menu in submodules
        - Resizable columns/widgets
    """

    def __init__(self, db: DatabaseConnector, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Academic Master Data")
        self.db = db

        # Main horizontal layout
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.initUI()

    def initUI(self):
        # Initialize modules
        self.grade_level = GradeLevelMaster(self.db)
        self.grade_subject = GradeSubject(self.db)
        self.add_students = StudentMasterData(self.db)

        # Make widgets expandable
        for widget in (self.grade_level, self.grade_subject, self.add_students):
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Add widgets with stretch factors (optional: control relative widths)
        self.main_layout.addWidget(self.grade_level, 1)     # stretch factor 1
        self.main_layout.addWidget(self.grade_subject, 2)   # stretch factor 2
        self.main_layout.addWidget(self.add_students, 3)    # stretch factor 3

        # Optional: spacing and margins
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)


if __name__ == "__main__":
    db = DatabaseConnector()
    app = QApplication(sys.argv)
    win = AcademicMasterData(db)
    win.resize(1200, 600)  # default window size
    win.show()
    sys.exit(app.exec())