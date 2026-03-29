import sys
import os
from typing import Optional, List, Dict, Any

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTableWidget, QTableWidgetItem, QPushButton,
    QLineEdit, QLabel, QComboBox, QMessageBox, QGroupBox,
    QFormLayout, QSpinBox, QDoubleSpinBox, QHeaderView,
    QSplitter, QTextEdit, QDialog, QDialogButtonBox,
    QDateEdit, QCheckBox, QRadioButton, QButtonGroup,
    QMenuBar, QMenu, QStatusBar, QToolBar, QFileDialog
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal, QSize
from PyQt6.QtGui import QAction, QIcon, QFont, QColor, QPalette

# Import the DatabaseConnector
from layouts.DatabaseConnector import DatabaseConnector


# ============================================================
# STYLESHEET (QSS)
# ============================================================
DARK_STYLE = """
QMainWindow {
    background-color: #2b2b2b;
}

QTabWidget::pane {
    border: 1px solid #444444;
    background-color: #2b2b2b;
}

QTabBar::tab {
    background-color: #3c3c3c;
    color: #ffffff;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #4a4a4a;
    border-bottom: 2px solid #ff9800;
}

QTabBar::tab:hover {
    background-color: #4a4a4a;
}

QWidget {
    background-color: #2b2b2b;
    color: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
}

QGroupBox {
    border: 1px solid #444444;
    border-radius: 5px;
    margin-top: 1ex;
    padding-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
    color: #ff9800;
}

QPushButton {
    background-color: #4a4a4a;
    border: 1px solid #555555;
    border-radius: 3px;
    padding: 6px 12px;
    color: #ffffff;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #5a5a5a;
    border-color: #ff9800;
}

QPushButton:pressed {
    background-color: #3a3a3a;
}

QPushButton:disabled {
    background-color: #2d2d2d;
    color: #666666;
    border-color: #444444;
}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit, QTextEdit {
    background-color: #3c3c3c;
    border: 1px solid #555555;
    border-radius: 3px;
    padding: 5px;
    color: #ffffff;
    selection-background-color: #ff9800;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus, QTextEdit:focus {
    border-color: #ff9800;
}

QComboBox::drop-down {
    border: none;
    background-color: #4a4a4a;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #ffffff;
    margin-right: 5px;
}

QComboBox QAbstractItemView {
    background-color: #3c3c3c;
    border: 1px solid #555555;
    selection-background-color: #ff9800;
    selection-color: #ffffff;
}

QTableWidget {
    background-color: #2b2b2b;
    alternate-background-color: #333333;
    gridline-color: #444444;
    border: 1px solid #444444;
}

QTableWidget::item {
    padding: 5px;
    border-bottom: 1px solid #3c3c3c;
}

QTableWidget::item:selected {
    background-color: #ff9800;
    color: #000000;
}

QHeaderView::section {
    background-color: #3c3c3c;
    padding: 5px;
    border: 1px solid #555555;
    font-weight: bold;
    color: #ff9800;
}

QStatusBar {
    background-color: #1e1e1e;
    color: #888888;
}

QMenuBar {
    background-color: #1e1e1e;
    color: #ffffff;
    border-bottom: 1px solid #444444;
}

QMenuBar::item:selected {
    background-color: #ff9800;
    color: #000000;
}

QMenu {
    background-color: #2b2b2b;
    border: 1px solid #444444;
}

QMenu::item:selected {
    background-color: #ff9800;
    color: #000000;
}

QToolBar {
    background-color: #1e1e1e;
    border-bottom: 1px solid #444444;
    spacing: 5px;
}

QLabel {
    color: #cccccc;
}

QLabel[header="true"] {
    color: #ff9800;
    font-size: 16px;
    font-weight: bold;
    padding: 10px;
}

QScrollBar:vertical {
    background-color: #2b2b2b;
    width: 12px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #555555;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #666666;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QDialog {
    background-color: #2b2b2b;
    border: 1px solid #444444;
}

QDialogButtonBox QPushButton {
    min-width: 80px;
}
"""


# ============================================================
# CUSTOM WIDGETS
# ============================================================

class DataTable(QTableWidget):
    """Custom table widget for displaying data"""
    
    itemSelected = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.setSortingEnabled(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        
    def setData(self, data: List[Dict], headers: List[str]):
        """Populate table with data"""
        if not data:
            self.setRowCount(0)
            self.setColumnCount(0)
            return
            
        self.setRowCount(len(data))
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        for row, record in enumerate(data):
            for col, key in enumerate(record.keys()):
                value = str(record[key]) if record[key] is not None else ""
                item = QTableWidgetItem(value)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.setItem(row, col, item)
                
        self.resizeColumnsToContents()
        
    def getSelectedRowData(self) -> Optional[Dict]:
        """Get data from selected row"""
        current_row = self.currentRow()
        if current_row < 0:
            return None
            
        data = {}
        for col in range(self.columnCount()):
            header = self.horizontalHeaderItem(col).text()
            item = self.item(current_row, col)
            data[header] = item.text() if item else ""
            
        return data


class SearchWidget(QWidget):
    """Widget with search functionality"""
    
    searchPerformed = pyqtSignal(str)
    
    def __init__(self, placeholder="Search...", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(placeholder)
        self.search_input.textChanged.connect(self.onSearch)
        
        self.clear_button = QPushButton("✕")
        self.clear_button.setFixedSize(25, 25)
        self.clear_button.clicked.connect(self.clearSearch)
        
        layout.addWidget(self.search_input)
        layout.addWidget(self.clear_button)
        
        self.setLayout(layout)
        
    def onSearch(self, text):
        self.searchPerformed.emit(text)
        
    def clearSearch(self):
        self.search_input.clear()


class FilterComboBox(QComboBox):
    """Combo box with filter label"""
    
    def __init__(self, label_text="Filter:", parent=None):
        super().__init__(parent)
        self.label = QLabel(label_text)
        self.addItem("All")
        
    def getLayout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self)
        return layout


# ============================================================
# DIALOGS
# ============================================================

class StudentDialog(QDialog):
    """Dialog for adding/editing students"""
    
    def __init__(self, db: DatabaseConnector, student_id=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.student_id = student_id
        self.setWindowTitle("Add Student" if not student_id else "Edit Student")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout()
        
        # Form
        form_group = QGroupBox("Student Information")
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.guardian_input = QLineEdit()
        
        # Level combo
        self.level_combo = QComboBox()
        self.load_levels()
        self.level_combo.currentIndexChanged.connect(self.load_sections)
        
        # Section combo
        self.section_combo = QComboBox()
        
        # School year
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("e.g., 2024-2025")
        
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Guardian:", self.guardian_input)
        form_layout.addRow("Level:", self.level_combo)
        form_layout.addRow("Section:", self.section_combo)
        form_layout.addRow("School Year:", self.year_input)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
        # Load data if editing
        if student_id:
            self.load_student_data()
            
    def load_levels(self):
        levels = self.db.get_levels() or []
        self.level_combo.clear()
        for level in levels:
            self.level_combo.addItem(level['LevelName'], level['ID'])
            
    def load_sections(self):
        level_id = self.level_combo.currentData()
        if level_id:
            sections = self.db.get_sections(level_id) or []
            self.section_combo.clear()
            for section in sections:
                self.section_combo.addItem(section['SectionName'], section['ID'])
                
    def load_student_data(self):
        student = self.db.get_student(self.student_id)
        if student:
            self.name_input.setText(student['Name'])
            self.guardian_input.setText(student['Guardian'])
            self.year_input.setText(student['SchoolYear'])
            
            # Set level
            index = self.level_combo.findData(student['LevelID'])
            if index >= 0:
                self.level_combo.setCurrentIndex(index)
                self.load_sections()
                
                # Set section
                index = self.section_combo.findData(student['SectionID'])
                if index >= 0:
                    self.section_combo.setCurrentIndex(index)
                    
    def get_data(self):
        return {
            'name': self.name_input.text(),
            'guardian': self.guardian_input.text(),
            'level_id': self.level_combo.currentData(),
            'section_id': self.section_combo.currentData(),
            'school_year': self.year_input.text()
        }


class SubjectDialog(QDialog):
    """Dialog for adding/editing subjects"""
    
    def __init__(self, db: DatabaseConnector, subject_id=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.subject_id = subject_id
        self.setWindowTitle("Add Subject" if not subject_id else "Edit Subject")
        self.setModal(True)
        self.resize(400, 200)
        
        layout = QVBoxLayout()
        
        form_group = QGroupBox("Subject Information")
        form_layout = QFormLayout()
        
        self.subject_input = QLineEdit()
        self.advisor_input = QLineEdit()
        
        # Level combo
        self.level_combo = QComboBox()
        levels = self.db.get_levels() or []
        for level in levels:
            self.level_combo.addItem(level['LevelName'], level['ID'])
            
        form_layout.addRow("Subject:", self.subject_input)
        form_layout.addRow("Advisor:", self.advisor_input)
        form_layout.addRow("Level:", self.level_combo)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Load data if editing
        if subject_id:
            subject = self.db.get_subject(subject_id)
            if subject:
                self.subject_input.setText(subject['Subject'])
                self.advisor_input.setText(subject['Advisor'])
                index = self.level_combo.findData(subject['LevelID'])
                if index >= 0:
                    self.level_combo.setCurrentIndex(index)
                    
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
    def get_data(self):
        return {
            'subject': self.subject_input.text(),
            'advisor': self.advisor_input.text(),
            'level_id': self.level_combo.currentData()
        }


class GradeDialog(QDialog):
    """Dialog for adding/editing grades"""
    
    def __init__(self, db: DatabaseConnector, student_id=None, grade_id=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.student_id = student_id
        self.grade_id = grade_id
        self.setWindowTitle("Add Grade" if not grade_id else "Edit Grade")
        self.setModal(True)
        self.resize(400, 250)
        
        layout = QVBoxLayout()
        
        form_group = QGroupBox("Grade Information")
        form_layout = QFormLayout()
        
        # Student (if not pre-selected)
        if not student_id:
            self.student_combo = QComboBox()
            students = self.db.get_all_students() or []
            for student in students:
                self.student_combo.addItem(f"{student['Name']} ({student['SchoolYear']})", student['ID'])
            form_layout.addRow("Student:", self.student_combo)
        
        # Subject combo
        self.subject_combo = QComboBox()
        subjects = self.db.get_all_subjects() or []
        for subject in subjects:
            self.subject_combo.addItem(f"{subject['Subject']} - {subject['Advisor']}", subject['ID'])
        form_layout.addRow("Subject:", self.subject_combo)
        
        # Grade input
        self.grade_input = QLineEdit()
        self.grade_input.setPlaceholderText("e.g., 85.5 or A")
        form_layout.addRow("Grade:", self.grade_input)
        
        # School year
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("e.g., 2024-2025")
        form_layout.addRow("School Year:", self.year_input)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Load data if editing
        if grade_id:
            grade = self.db.get_grade(grade_id)
            if grade:
                self.grade_input.setText(grade['Grade'])
                self.year_input.setText(grade['SchoolYear'])
                index = self.subject_combo.findData(grade['SubjectID'])
                if index >= 0:
                    self.subject_combo.setCurrentIndex(index)
                    
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
    def get_data(self):
        data = {
            'subject_id': self.subject_combo.currentData(),
            'grade': self.grade_input.text(),
            'school_year': self.year_input.text()
        }
        
        if not hasattr(self, 'student_combo'):
            data['student_id'] = self.student_id
        else:
            data['student_id'] = self.student_combo.currentData()
            
        return data


# ============================================================
# MAIN WINDOW
# ============================================================

class SchoolManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnector()
        self.initUI()
        self.loadAllData()
        
    def initUI(self):
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 1200, 700)
        
        # Apply stylesheet
        self.setStyleSheet(DARK_STYLE)
        
        # Create menu bar
        self.createMenuBar()
        
        # Create toolbar
        self.createToolBar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Header
        header = QLabel("School Management System")
        header.setProperty("header", True)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)
        
        # Create tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Initialize tabs
        self.initStudentsTab()
        self.initSubjectsTab()
        self.initGradesTab()
        self.initLevelsTab()
        self.initSectionsTab()
        self.initReportsTab()
        
    def createMenuBar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        backup_action = QAction("Backup Database", self)
        backup_action.triggered.connect(self.backupDatabase)
        file_menu.addAction(backup_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        refresh_action = QAction("Refresh All", self)
        refresh_action.triggered.connect(self.loadAllData)
        edit_menu.addAction(refresh_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.showAbout)
        help_menu.addAction(about_action)
        
    def createToolBar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # Add actions
        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.loadAllData)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        backup_action = QAction("Backup", self)
        backup_action.triggered.connect(self.backupDatabase)
        toolbar.addAction(backup_action)
        
    # ============================================================
    # STUDENTS TAB
    # ============================================================
    
    def initStudentsTab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Search and filter section
        search_filter_widget = QWidget()
        search_filter_layout = QHBoxLayout()
        search_filter_layout.setContentsMargins(0, 0, 0, 0)
        
        # Search
        self.student_search = SearchWidget("Search students...")
        self.student_search.searchPerformed.connect(self.filterStudents)
        search_filter_layout.addWidget(self.student_search)
        
        # Level filter
        self.student_level_filter = QComboBox()
        self.student_level_filter.addItem("All Levels", None)
        self.student_level_filter.currentIndexChanged.connect(self.filterStudents)
        search_filter_layout.addWidget(QLabel("Level:"))
        search_filter_layout.addWidget(self.student_level_filter)
        
        # Year filter
        self.student_year_filter = QComboBox()
        self.student_year_filter.addItem("All Years", None)
        self.student_year_filter.currentIndexChanged.connect(self.filterStudents)
        search_filter_layout.addWidget(QLabel("Year:"))
        search_filter_layout.addWidget(self.student_year_filter)
        
        search_filter_widget.setLayout(search_filter_layout)
        layout.addWidget(search_filter_widget)
        
        # Buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        self.add_student_btn = QPushButton("Add Student")
        self.add_student_btn.clicked.connect(self.addStudent)
        
        self.edit_student_btn = QPushButton("Edit Student")
        self.edit_student_btn.clicked.connect(self.editStudent)
        self.edit_student_btn.setEnabled(False)
        
        self.delete_student_btn = QPushButton("Delete Student")
        self.delete_student_btn.clicked.connect(self.deleteStudent)
        self.delete_student_btn.setEnabled(False)
        
        self.view_grades_btn = QPushButton("View Grades")
        self.view_grades_btn.clicked.connect(self.viewStudentGrades)
        self.view_grades_btn.setEnabled(False)
        
        button_layout.addWidget(self.add_student_btn)
        button_layout.addWidget(self.edit_student_btn)
        button_layout.addWidget(self.delete_student_btn)
        button_layout.addWidget(self.view_grades_btn)
        button_layout.addStretch()
        
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)
        
        # Students table
        self.students_table = DataTable()
        self.students_table.itemSelectionChanged.connect(self.onStudentSelected)
        layout.addWidget(self.students_table)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Students")
        
    def loadStudents(self):
        students = self.db.get_all_students() or []
        
        # Update filters
        self.updateStudentFilters(students)
        
        # Set table data
        headers = ['ID', 'Name', 'Guardian', 'Level', 'Section', 'School Year']
        self.students_table.setData(students, headers)
        self.students_table.setColumnHidden(0, True)  # Hide ID column
        
    def updateStudentFilters(self, students):
        # Update level filter
        current_level = self.student_level_filter.currentData()
        self.student_level_filter.clear()
        self.student_level_filter.addItem("All Levels", None)
        
        levels = set()
        years = set()
        for student in students:
            levels.add(student['LevelName'])
            years.add(student['SchoolYear'])
            
        for level in sorted(levels):
            self.student_level_filter.addItem(level, level)
            
        if current_level in levels:
            index = self.student_level_filter.findData(current_level)
            if index >= 0:
                self.student_level_filter.setCurrentIndex(index)
                
        # Update year filter
        current_year = self.student_year_filter.currentData()
        self.student_year_filter.clear()
        self.student_year_filter.addItem("All Years", None)
        
        for year in sorted(years, reverse=True):
            self.student_year_filter.addItem(year, year)
            
        if current_year in years:
            index = self.student_year_filter.findData(current_year)
            if index >= 0:
                self.student_year_filter.setCurrentIndex(index)
                
    def filterStudents(self):
        search_text = self.student_search.search_input.text().lower()
        level_filter = self.student_level_filter.currentData()
        year_filter = self.student_year_filter.currentData()
        
        all_students = self.db.get_all_students() or []
        
        filtered = []
        for student in all_students:
            # Apply search filter
            if search_text:
                if (search_text not in student['Name'].lower() and 
                    search_text not in student['Guardian'].lower()):
                    continue
                    
            # Apply level filter
            if level_filter and student['LevelName'] != level_filter:
                continue
                
            # Apply year filter
            if year_filter and student['SchoolYear'] != year_filter:
                continue
                
            filtered.append(student)
            
        headers = ['ID', 'Name', 'Guardian', 'Level', 'Section', 'School Year']
        self.students_table.setData(filtered, headers)
        self.students_table.setColumnHidden(0, True)
        
    def onStudentSelected(self):
        enabled = self.students_table.currentRow() >= 0
        self.edit_student_btn.setEnabled(enabled)
        self.delete_student_btn.setEnabled(enabled)
        self.view_grades_btn.setEnabled(enabled)
        
    def addStudent(self):
        dialog = StudentDialog(self.db)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            result = self.db.add_student(
                data['name'],
                data['guardian'],
                data['level_id'],
                data['section_id'],
                data['school_year']
            )
            if result:
                self.status_bar.showMessage("Student added successfully")
                self.loadStudents()
            else:
                QMessageBox.critical(self, "Error", "Failed to add student")
                
    def editStudent(self):
        student_data = self.students_table.getSelectedRowData()
        if student_data:
            student_id = int(student_data['ID'])
            dialog = StudentDialog(self.db, student_id)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                result = self.db.update_student(
                    student_id,
                    Name=data['name'],
                    Guardian=data['guardian'],
                    LevelID=data['level_id'],
                    SectionID=data['section_id'],
                    SchoolYear=data['school_year']
                )
                if result:
                    self.status_bar.showMessage("Student updated successfully")
                    self.loadStudents()
                else:
                    QMessageBox.critical(self, "Error", "Failed to update student")
                    
    def deleteStudent(self):
        student_data = self.students_table.getSelectedRowData()
        if student_data:
            reply = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete {student_data['Name']}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                result = self.db.delete_student(int(student_data['ID']))
                if result:
                    self.status_bar.showMessage("Student deleted successfully")
                    self.loadStudents()
                    self.loadGrades()  # Refresh grades tab
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete student")
                    
    def viewStudentGrades(self):
        student_data = self.students_table.getSelectedRowData()
        if student_data:
            self.tabs.setCurrentIndex(2)  # Switch to grades tab
            self.grade_student_filter.setCurrentText(student_data['Name'])
            
    # ============================================================
    # SUBJECTS TAB
    # ============================================================
    
    def initSubjectsTab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Search
        self.subject_search = SearchWidget("Search subjects...")
        self.subject_search.searchPerformed.connect(self.filterSubjects)
        layout.addWidget(self.subject_search)
        
        # Buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        self.add_subject_btn = QPushButton("Add Subject")
        self.add_subject_btn.clicked.connect(self.addSubject)
        
        self.edit_subject_btn = QPushButton("Edit Subject")
        self.edit_subject_btn.clicked.connect(self.editSubject)
        self.edit_subject_btn.setEnabled(False)
        
        self.delete_subject_btn = QPushButton("Delete Subject")
        self.delete_subject_btn.clicked.connect(self.deleteSubject)
        self.delete_subject_btn.setEnabled(False)
        
        button_layout.addWidget(self.add_subject_btn)
        button_layout.addWidget(self.edit_subject_btn)
        button_layout.addWidget(self.delete_subject_btn)
        button_layout.addStretch()
        
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)
        
        # Subjects table
        self.subjects_table = DataTable()
        self.subjects_table.itemSelectionChanged.connect(self.onSubjectSelected)
        layout.addWidget(self.subjects_table)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Subjects")
        
    def loadSubjects(self):
        subjects = self.db.get_all_subjects() or []
        headers = ['ID', 'Subject', 'Advisor', 'Level']
        self.subjects_table.setData(subjects, headers)
        self.subjects_table.setColumnHidden(0, True)
        
    def filterSubjects(self, text):
        if not text:
            self.loadSubjects()
            return
            
        filtered = self.db.search_subjects(text) or []
        headers = ['ID', 'Subject', 'Advisor', 'Level']
        self.subjects_table.setData(filtered, headers)
        self.subjects_table.setColumnHidden(0, True)
        
    def onSubjectSelected(self):
        enabled = self.subjects_table.currentRow() >= 0
        self.edit_subject_btn.setEnabled(enabled)
        self.delete_subject_btn.setEnabled(enabled)
        
    def addSubject(self):
        dialog = SubjectDialog(self.db)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            result = self.db.add_subject(
                data['subject'],
                data['advisor'],
                data['level_id']
            )
            if result:
                self.status_bar.showMessage("Subject added successfully")
                self.loadSubjects()
            else:
                QMessageBox.critical(self, "Error", "Failed to add subject")
                
    def editSubject(self):
        subject_data = self.subjects_table.getSelectedRowData()
        if subject_data:
            subject_id = int(subject_data['ID'])
            dialog = SubjectDialog(self.db, subject_id)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                result = self.db.update_subject(
                    subject_id,
                    Subject=data['subject'],
                    Advisor=data['advisor'],
                    LevelID=data['level_id']
                )
                if result:
                    self.status_bar.showMessage("Subject updated successfully")
                    self.loadSubjects()
                else:
                    QMessageBox.critical(self, "Error", "Failed to update subject")
                    
    def deleteSubject(self):
        subject_data = self.subjects_table.getSelectedRowData()
        if subject_data:
            reply = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete {subject_data['Subject']}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                result = self.db.delete_subject(int(subject_data['ID']))
                if result:
                    self.status_bar.showMessage("Subject deleted successfully")
                    self.loadSubjects()
                    self.loadGrades()  # Refresh grades tab
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete subject")
                    
    # ============================================================
    # GRADES TAB
    # ============================================================
    
    def initGradesTab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Filters
        filter_widget = QWidget()
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(0, 0, 0, 0)
        
        # Student filter
        self.grade_student_filter = QComboBox()
        self.grade_student_filter.addItem("All Students", None)
        self.grade_student_filter.currentIndexChanged.connect(self.filterGrades)
        filter_layout.addWidget(QLabel("Student:"))
        filter_layout.addWidget(self.grade_student_filter)
        
        # Subject filter
        self.grade_subject_filter = QComboBox()
        self.grade_subject_filter.addItem("All Subjects", None)
        self.grade_subject_filter.currentIndexChanged.connect(self.filterGrades)
        filter_layout.addWidget(QLabel("Subject:"))
        filter_layout.addWidget(self.grade_subject_filter)
        
        # Year filter
        self.grade_year_filter = QComboBox()
        self.grade_year_filter.addItem("All Years", None)
        self.grade_year_filter.currentIndexChanged.connect(self.filterGrades)
        filter_layout.addWidget(QLabel("Year:"))
        filter_layout.addWidget(self.grade_year_filter)
        
        filter_layout.addStretch()
        filter_widget.setLayout(filter_layout)
        layout.addWidget(filter_widget)
        
        # Buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        self.add_grade_btn = QPushButton("Add Grade")
        self.add_grade_btn.clicked.connect(self.addGrade)
        
        self.edit_grade_btn = QPushButton("Edit Grade")
        self.edit_grade_btn.clicked.connect(self.editGrade)
        self.edit_grade_btn.setEnabled(False)
        
        self.delete_grade_btn = QPushButton("Delete Grade")
        self.delete_grade_btn.clicked.connect(self.deleteGrade)
        self.delete_grade_btn.setEnabled(False)
        
        button_layout.addWidget(self.add_grade_btn)
        button_layout.addWidget(self.edit_grade_btn)
        button_layout.addWidget(self.delete_grade_btn)
        button_layout.addStretch()
        
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)
        
        # Grades table
        self.grades_table = DataTable()
        self.grades_table.itemSelectionChanged.connect(self.onGradeSelected)
        layout.addWidget(self.grades_table)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Grades")
        
    def loadGrades(self):
        grades = self.db.get_grades_with_details() or []
        
        # Update filters
        self.updateGradeFilters(grades)
        
        # Set table data
        headers = ['ID', 'Student', 'Subject', 'Grade', 'Year', 'Level', 'Section']
        self.grades_table.setData(grades, headers)
        self.grades_table.setColumnHidden(0, True)
        self.grades_table.setColumnHidden(5, True)  # Hide Level
        self.grades_table.setColumnHidden(6, True)  # Hide Section
        
    def updateGradeFilters(self, grades):
        # Update student filter
        current_student = self.grade_student_filter.currentData()
        self.grade_student_filter.clear()
        self.grade_student_filter.addItem("All Students", None)
        
        students = set()
        subjects = set()
        years = set()
        
        for grade in grades:
            students.add(grade['StudentName'])
            subjects.add(grade['Subject'])
            years.add(grade['LevelName'])
            
        for student in sorted(students):
            self.grade_student_filter.addItem(student, student)
            
        if current_student in students:
            index = self.grade_student_filter.findData(current_student)
            if index >= 0:
                self.grade_student_filter.setCurrentIndex(index)
                
        # Update subject filter
        current_subject = self.grade_subject_filter.currentData()
        self.grade_subject_filter.clear()
        self.grade_subject_filter.addItem("All Subjects", None)
        
        for subject in sorted(subjects):
            self.grade_subject_filter.addItem(subject, subject)
            
        if current_subject in subjects:
            index = self.grade_subject_filter.findData(current_subject)
            if index >= 0:
                self.grade_subject_filter.setCurrentIndex(index)
                
        # Update year filter
        current_year = self.grade_year_filter.currentData()
        self.grade_year_filter.clear()
        self.grade_year_filter.addItem("All Years", None)
        
        for year in sorted(years, reverse=True):
            self.grade_year_filter.addItem(year, year)
            
        if current_year in years:
            index = self.grade_year_filter.findData(current_year)
            if index >= 0:
                self.grade_year_filter.setCurrentIndex(index)
                
    def filterGrades(self):
        student_filter = self.grade_student_filter.currentData()
        subject_filter = self.grade_subject_filter.currentData()
        year_filter = self.grade_year_filter.currentData()
        
        all_grades = self.db.get_grades_with_details() or []
        
        filtered = []
        for grade in all_grades:
            if student_filter and grade['StudentName'] != student_filter:
                continue
            if subject_filter and grade['Subject'] != subject_filter:
                continue
            if year_filter and grade['LevelName'] != year_filter:
                continue
            filtered.append(grade)
            
        headers = ['ID', 'Student', 'Subject', 'Grade', 'Level', 'Level', 'Section']
        self.grades_table.setData(filtered, headers)
        self.grades_table.setColumnHidden(0, True)
        self.grades_table.setColumnHidden(5, True)
        self.grades_table.setColumnHidden(6, True)
        
    def onGradeSelected(self):
        enabled = self.grades_table.currentRow() >= 0
        self.edit_grade_btn.setEnabled(enabled)
        self.delete_grade_btn.setEnabled(enabled)
        
    def addGrade(self):
        dialog = GradeDialog(self.db)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            result = self.db.add_grade(
                data['student_id'],
                data['subject_id'],
                data['grade'],
                data['school_year']
            )
            if result:
                self.status_bar.showMessage("Grade added successfully")
                self.loadGrades()
            else:
                QMessageBox.critical(self, "Error", "Failed to add grade")
                
    def editGrade(self):
        grade_data = self.grades_table.getSelectedRowData()
        if grade_data:
            grade_id = int(grade_data['ID'])
            dialog = GradeDialog(self.db, None, grade_id)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                result = self.db.update_grade(
                    grade_id,
                    Grade=data['grade'],
                    SchoolYear=data['school_year']
                )
                if result:
                    self.status_bar.showMessage("Grade updated successfully")
                    self.loadGrades()
                else:
                    QMessageBox.critical(self, "Error", "Failed to update grade")
                    
    def deleteGrade(self):
        grade_data = self.grades_table.getSelectedRowData()
        if grade_data:
            reply = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete this grade?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                result = self.db.delete_grade(int(grade_data['ID']))
                if result:
                    self.status_bar.showMessage("Grade deleted successfully")
                    self.loadGrades()
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete grade")
                    
    # ============================================================
    # LEVELS TAB
    # ============================================================
    
    def initLevelsTab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Search
        self.level_search = SearchWidget("Search levels...")
        self.level_search.searchPerformed.connect(self.filterLevels)
        layout.addWidget(self.level_search)
        
        # Buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        self.add_level_btn = QPushButton("Add Level")
        self.add_level_btn.clicked.connect(self.addLevel)
        
        self.edit_level_btn = QPushButton("Edit Level")
        self.edit_level_btn.clicked.connect(self.editLevel)
        self.edit_level_btn.setEnabled(False)
        
        self.delete_level_btn = QPushButton("Delete Level")
        self.delete_level_btn.clicked.connect(self.deleteLevel)
        self.delete_level_btn.setEnabled(False)
        
        button_layout.addWidget(self.add_level_btn)
        button_layout.addWidget(self.edit_level_btn)
        button_layout.addWidget(self.delete_level_btn)
        button_layout.addStretch()
        
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)
        
        # Levels table
        self.levels_table = DataTable()
        self.levels_table.itemSelectionChanged.connect(self.onLevelSelected)
        layout.addWidget(self.levels_table)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Levels")
        
    def loadLevels(self):
        levels = self.db.get_levels() or []
        headers = ['ID', 'Level Name', 'Category']
        self.levels_table.setData(levels, headers)
        self.levels_table.setColumnHidden(0, True)
        
    def filterLevels(self, text):
        if not text:
            self.loadLevels()
            return
            
        filtered = self.db.search_levels(text) or []
        headers = ['ID', 'Level Name', 'Category']
        self.levels_table.setData(filtered, headers)
        self.levels_table.setColumnHidden(0, True)
        
    def onLevelSelected(self):
        enabled = self.levels_table.currentRow() >= 0
        self.edit_level_btn.setEnabled(enabled)
        self.delete_level_btn.setEnabled(enabled)
        
    def addLevel(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Level")
        dialog.setModal(True)
        
        layout = QVBoxLayout()
        
        form_group = QGroupBox("Level Information")
        form_layout = QFormLayout()
        
        name_input = QLineEdit()
        category_input = QLineEdit()
        category_input.setPlaceholderText("e.g., Elementary, High School, etc.")
        
        form_layout.addRow("Level Name:", name_input)
        form_layout.addRow("Category:", category_input)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            result = self.db.add_level(name_input.text(), category_input.text())
            if result:
                self.status_bar.showMessage("Level added successfully")
                self.loadLevels()
            else:
                QMessageBox.critical(self, "Error", "Failed to add level")
                
    def editLevel(self):
        level_data = self.levels_table.getSelectedRowData()
        if level_data:
            dialog = QDialog(self)
            dialog.setWindowTitle("Edit Level")
            dialog.setModal(True)
            
            layout = QVBoxLayout()
            
            form_group = QGroupBox("Level Information")
            form_layout = QFormLayout()
            
            name_input = QLineEdit()
            name_input.setText(level_data['Level Name'])
            
            category_input = QLineEdit()
            category_input.setText(level_data['Category'])
            
            form_layout.addRow("Level Name:", name_input)
            form_layout.addRow("Category:", category_input)
            
            form_group.setLayout(form_layout)
            layout.addWidget(form_group)
            
            button_box = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Ok | 
                QDialogButtonBox.StandardButton.Cancel
            )
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)
            
            dialog.setLayout(layout)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                result = self.db.update_level(
                    int(level_data['ID']),
                    LevelName=name_input.text(),
                    Category=category_input.text()
                )
                if result:
                    self.status_bar.showMessage("Level updated successfully")
                    self.loadLevels()
                else:
                    QMessageBox.critical(self, "Error", "Failed to update level")
                    
    def deleteLevel(self):
        level_data = self.levels_table.getSelectedRowData()
        if level_data:
            reply = QMessageBox.question(
                self, "Confirm Delete",
                f"Are you sure you want to delete {level_data['Level Name']}?\nThis will also delete all related sections, students, and grades!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                result = self.db.delete_level(int(level_data['ID']))
                if result:
                    self.status_bar.showMessage("Level deleted successfully")
                    self.loadLevels()
                    self.loadSections()
                    self.loadStudents()
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete level")
                    
    # ============================================================
    # SECTIONS TAB
    # ============================================================
    
    def initSectionsTab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Level filter
        filter_widget = QWidget()
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(0, 0, 0, 0)
        
        self.section_level_filter = QComboBox()
        self.section_level_filter.addItem("All Levels", None)
        self.section_level_filter.currentIndexChanged.connect(self.filterSections)
        filter_layout.addWidget(QLabel("Level:"))
        filter_layout.addWidget(self.section_level_filter)
        filter_layout.addStretch()
        
        filter_widget.setLayout(filter_layout)
        layout.addWidget(filter_widget)
        
        # Buttons
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        self.add_section_btn = QPushButton("Add Section")
        self.add_section_btn.clicked.connect(self.addSection)
        
        self.edit_section_btn = QPushButton("Edit Section")
        self.edit_section_btn.clicked.connect(self.editSection)
        self.edit_section_btn.setEnabled(False)
        
        self.delete_section_btn = QPushButton("Delete Section")
        self.delete_section_btn.clicked.connect(self.deleteSection)
        self.delete_section_btn.setEnabled(False)
        
        button_layout.addWidget(self.add_section_btn)
        button_layout.addWidget(self.edit_section_btn)
        button_layout.addWidget(self.delete_section_btn)
        button_layout.addStretch()
        
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)
        
        # Sections table
        self.sections_table = DataTable()
        self.sections_table.itemSelectionChanged.connect(self.onSectionSelected)
        layout.addWidget(self.sections_table)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Sections")
        
    def loadSections(self):
        sections = self.db.get_sections_with_details() or []
        
        # Update level filter
        current_level = self.section_level_filter.currentData()
        self.section_level_filter.clear()
        self.section_level_filter.addItem("All Levels", None)
        
        levels = set()
        for section in sections:
            levels.add(section['LevelName'])
            
        for level in sorted(levels):
            self.section_level_filter.addItem(level, level)
            
        if current_level in levels:
            index = self.section_level_filter.findData(current_level)
            if index >= 0:
                self.section_level_filter.setCurrentIndex(index)
                
        # Set table data
        headers = ['ID', 'Section', 'Level', 'Students']
        self.sections_table.setData(sections, headers)
        self.sections_table.setColumnHidden(0, True)
        
    def filterSections(self):
        level_filter = self.section_level_filter.currentData()
        
        if level_filter:
            all_sections = self.db.get_sections_with_details() or []
            filtered = [s for s in all_sections if s['LevelName'] == level_filter]
        else:
            filtered = self.db.get_sections_with_details() or []
            
        headers = ['ID', 'Section', 'Level', 'Students']
        self.sections_table.setData(filtered, headers)
        self.sections_table.setColumnHidden(0, True)
        
    def onSectionSelected(self):
        enabled = self.sections_table.currentRow() >= 0
        self.edit_section_btn.setEnabled(enabled)
        self.delete_section_btn.setEnabled(enabled)
        
    def addSection(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Section")
        dialog.setModal(True)
        
        layout = QVBoxLayout()
        
        form_group = QGroupBox("Section Information")
        form_layout = QFormLayout()
        
        name_input = QLineEdit()
        
        level_combo = QComboBox()
        levels = self.db.get_levels() or []
        for level in levels:
            level_combo.addItem(level['LevelName'], level['ID'])
            
        form_layout.addRow("Section Name:", name_input)
        form_layout.addRow("Level:", level_combo)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            result = self.db.add_section(
                name_input.text(),
                level_combo.currentData()
            )
            if result:
                self.status_bar.showMessage("Section added successfully")
                self.loadSections()
            else:
                QMessageBox.critical(self, "Error", "Failed to add section")
                
    def editSection(self):
        section_data = self.sections_table.getSelectedRowData()
        if section_data:
            dialog = QDialog(self)
            dialog.setWindowTitle("Edit Section")
            dialog.setModal(True)
            
            layout = QVBoxLayout()
            
            form_group = QGroupBox("Section Information")
            form_layout = QFormLayout()
            
            name_input = QLineEdit()
            name_input.setText(section_data['Section'])
            
            # Get level ID from section data
            section_detail = self.db.get_section(int(section_data['ID']))
            
            level_combo = QComboBox()
            levels = self.db.get_levels() or []
            for level in levels:
                level_combo.addItem(level['LevelName'], level['ID'])
                
            if section_detail:
                index = level_combo.findData(section_detail['LevelID'])
                if index >= 0:
                    level_combo.setCurrentIndex(index)
                    
            form_layout.addRow("Section Name:", name_input)
            form_layout.addRow("Level:", level_combo)
            
            form_group.setLayout(form_layout)
            layout.addWidget(form_group)
            
            button_box = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Ok | 
                QDialogButtonBox.StandardButton.Cancel
            )
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)
            
            dialog.setLayout(layout)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                result = self.db.update_section(
                    int(section_data['ID']),
                    SectionName=name_input.text(),
                    LevelID=level_combo.currentData()
                )
                if result:
                    self.status_bar.showMessage("Section updated successfully")
                    self.loadSections()
                else:
                    QMessageBox.critical(self, "Error", "Failed to update section")
                    
    def deleteSection(self):
        section_data = self.sections_table.getSelectedRowData()
        if section_data:
            student_count = section_data.get('Students', 0)
            warning = f"Are you sure you want to delete {section_data['Section']}?"
            if int(student_count) > 0:
                warning += f"\nThis section has {student_count} students that will also be deleted!"
                
            reply = QMessageBox.question(
                self, "Confirm Delete",
                warning,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                result = self.db.delete_section(int(section_data['ID']))
                if result:
                    self.status_bar.showMessage("Section deleted successfully")
                    self.loadSections()
                    self.loadStudents()
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete section")
                    
    # ============================================================
    # REPORTS TAB
    # ============================================================
    
    def initReportsTab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Statistics group
        stats_group = QGroupBox("School Statistics")
        stats_layout = QFormLayout()
        
        self.total_students_label = QLabel("0")
        self.total_subjects_label = QLabel("0")
        self.total_grades_label = QLabel("0")
        self.avg_grade_label = QLabel("0.00")
        
        stats_layout.addRow("Total Students:", self.total_students_label)
        stats_layout.addRow("Total Subjects:", self.total_subjects_label)
        stats_layout.addRow("Total Grades:", self.total_grades_label)
        stats_layout.addRow("Average Grade:", self.avg_grade_label)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Summary tables
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Level summary
        level_widget = QWidget()
        level_layout = QVBoxLayout()
        level_layout.addWidget(QLabel("Levels Summary"))
        self.level_summary_table = DataTable()
        level_layout.addWidget(self.level_summary_table)
        level_widget.setLayout(level_layout)
        splitter.addWidget(level_widget)
        
        # Subject summary
        subject_widget = QWidget()
        subject_layout = QVBoxLayout()
        subject_layout.addWidget(QLabel("Subjects Summary"))
        self.subject_summary_table = DataTable()
        subject_layout.addWidget(self.subject_summary_table)
        subject_widget.setLayout(subject_layout)
        splitter.addWidget(subject_widget)
        
        layout.addWidget(splitter)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Reports")
        refresh_btn.clicked.connect(self.loadReports)
        layout.addWidget(refresh_btn)
        
        tab.setLayout(layout)
        self.tabs.addTab(tab, "Reports")
        
    def loadReports(self):
        # Load statistics
        stats = self.db.get_school_statistics()
        if stats:
            self.total_students_label.setText(str(stats.get('total_students', 0)))
            self.total_subjects_label.setText(str(stats.get('total_subjects', 0)))
            self.total_grades_label.setText(str(stats.get('total_grades', 0)))
            avg = stats.get('overall_average', 0)
            self.avg_grade_label.setText(f"{avg:.2f}" if avg else "N/A")
            
        # Load level summary
        level_summary = self.db.get_levels_summary() or []
        level_headers = ['Level', 'Category', 'Sections', 'Students', 'Subjects', 'Grades', 'Avg Grade']
        self.level_summary_table.setData(level_summary, level_headers)
        
        # Load subject summary
        subject_summary = self.db.get_subjects_summary() or []
        subject_headers = ['Subject', 'Advisor', 'Level', 'Grades', 'Students', 'Avg', 'Min', 'Max']
        self.subject_summary_table.setData(subject_summary, subject_headers)
        
    # ============================================================
    # UTILITY FUNCTIONS
    # ============================================================
    
    def loadAllData(self):
        """Load all data into tabs"""
        self.loadLevels()
        self.loadSections()
        self.loadStudents()
        self.loadSubjects()
        self.loadGrades()
        self.loadReports()
        self.status_bar.showMessage("All data loaded successfully")
        
    def backupDatabase(self):
        """Backup the database"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Backup Database", 
            os.path.expanduser("~/school_backup.db"),
            "SQLite Database (*.db)"
        )
        if filename:
            if self.db.backup_database(filename):
                QMessageBox.information(self, "Success", "Database backed up successfully")
                self.status_bar.showMessage(f"Database backed up to {filename}")
            else:
                QMessageBox.critical(self, "Error", "Failed to backup database")
                
    def showAbout(self):
        QMessageBox.about(
            self, "About School Management System",
            "School Management System v1.0\n\n"
            "A comprehensive system for managing students, subjects, and grades.\n\n"
            "Built with PyQt6 and SQLite3"
        )


# ============================================================
# MAIN
# ============================================================

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = SchoolManagementSystem()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()