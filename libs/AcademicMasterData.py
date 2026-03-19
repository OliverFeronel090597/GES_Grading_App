from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QApplication
from PyQt6.QtCore import Qt
from libs.DatabaseConnector import DatabaseConnector
from libs.AddStudents import StudentMasterData
from libs.AddSubject import GradeSubject
from libs.AddGradeLevel import GradeLevelMaster
import sys


class AcademicMasterData(QWidget):
    """
    Academic Master Data UI with a SmartTable that supports:
        - Add / Edit / Delete context menu
        - Double-click row callback
    """

    def __init__(self, db: DatabaseConnector, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Academic Master Data")
        self.db = db

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.initUI()

    def initUI(self):
        add_students = StudentMasterData(
            self.db
        )
        grade_subject = GradeSubject(
            self.db
        )
        grade_level = GradeLevelMaster(
            self.db
        )

        self.main_layout.addWidget(add_students)
        self.main_layout.addWidget(grade_subject)
        self.main_layout.addWidget(grade_level)


if __name__ == "__main__":
    db = DatabaseConnector()
    app = QApplication(sys.argv)
    win = AcademicMasterData(db)
    win.show()
    sys.exit(app.exec())

    