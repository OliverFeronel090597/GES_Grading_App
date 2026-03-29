# layouts/Home.py
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtGui import QFontDatabase, QFont
from layouts.BackgroundImage import PixmapBgWidget
from layouts.DragAndDropImages import DragAndDropImage


class HomeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ---------------- Background ----------------
        self.bg_widget = PixmapBgWidget(0.5, self)
        self.bg_widget.setAutoFillBackground(False)

        # ---------------- Main Layout ----------------
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # ---------------- Digital Font ----------------
        font_path = r"img\digital-7 (mono).ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print(f"Failed to load font: {font_path}")
        family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.digital_font = QFont(family, 50)
        self.digital_font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 100)

        # ---------------- School Info ----------------
        self._init_school_layout()

        # ---------------- Date & Time ----------------
        self._init_datetime_layout()

        # ---------------- Adviser Details ----------------
        self._about_details_layout()

        # ---------------- Timer ----------------
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)
        self.update_datetime()

    # ------------------- Helper Layouts -------------------
    def _init_school_layout(self):
        """School name and location layout."""
        self.school_layout = QVBoxLayout()
        self.school_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.school_layout.setSpacing(0)

        self.school_name = QLabel("Paaralang Elemetarya ng Guintas")
        self.school_name.setObjectName("schoolName")
        self.school_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.school_name.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.school_layout.addWidget(self.school_name)

        self.school_location = QLabel("Guintas, Leganes, Iloilo")
        self.school_location.setObjectName("schoolLocation")
        self.school_location.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.school_location.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.school_layout.addWidget(self.school_location)

        self.main_layout.addLayout(self.school_layout)

    def _init_datetime_layout(self):
        """Date and time layout with digital font."""
        self.date_time_layout = QHBoxLayout()
        self.date_time_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.date_time_layout.setSpacing(0)

        # Date
        self.date_label = QLabel()
        self.date_label.setObjectName("date")
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.date_label.setFont(self.digital_font)
        self.date_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.date_time_layout.addWidget(self.date_label)

        # Time
        self.time_label = QLabel()
        self.time_label.setObjectName("time")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.time_label.setFont(self.digital_font)
        self.time_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.date_time_layout.addWidget(self.time_label)

        self.main_layout.addLayout(self.date_time_layout)

    def _about_details_layout(self):
        """Adviser drag & drop image layout."""
        self.details_layout = QHBoxLayout()
        # self.details_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
    
        # left area of the details
        # self.adviser_details = QVBoxLayout()
        # self.adviser_details.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        # self.details_layout.addLayout(self.adviser_details)

        # # Drag & Drop Image Widget
        # self.drag_widget = DragAndDropImage(logo_type="Adviser" ,size=300, parent=self)
        # self.adviser_details.addWidget(self.drag_widget)


        # right ares of details
        self.school_details = QVBoxLayout()
        self.school_details.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.details_layout.addLayout(self.school_details)

        self.drag_widget = DragAndDropImage(logo_type="SchoolLogo" ,size=300, parent=self)
        self.school_details.addWidget(self.drag_widget)
        
        self.main_layout.addLayout(self.details_layout)

    # ------------------- Events -------------------
    def resizeEvent(self, event):
        """Ensure background widget always fills HomeWidget."""
        self.bg_widget.resize(self.size())
        super().resizeEvent(event)

    # ------------------- Updates -------------------
    def update_datetime(self):
        """Update date and time labels every second."""
        now = QDateTime.currentDateTime()
        self.date_label.setText(now.toString("yyyy-MM-dd"))
        self.time_label.setText(now.toString("hh:mm:ss"))
