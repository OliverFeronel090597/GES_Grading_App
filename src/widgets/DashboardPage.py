from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QLabel, QGroupBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QSizePolicy, QPushButton,
    QScrollArea, QProgressBar, QComboBox, QLineEdit
)
from PyQt6.QtCore import Qt, QUrl, QTimer, QDateTime, QSize
from PyQt6.QtGui import QFont, QColor, QIcon, QPixmap, QPainter, QBrush, QPen
from PyQt6.QtWebEngineWidgets import QWebEngineView

from src.Database.Database import Database
import os

class DashboardPage(QWidget):
    """Dashboard page content with grid layout"""
    def __init__(self, parent=None, db:Database=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_date)
        self.timer.start(1000)  # Update every second

    def update_date(self):
        """Update the current date label"""
        now = QDateTime.currentDateTime()
        date_str = now.toString("dddd, MMMM d, yyyy hh:mm AP")
        for child in self.findChildren(QLabel):
            if child.objectName() == "currentDateLabel":
                child.setText(date_str)
                break

    def init_ui(self):
        """Initialize the user interface"""
        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)

        # ============================================================
        # MAIN CARD FRAME
        # ============================================================
        card_frame = QFrame()
        card_frame.setObjectName("cardFrame")
        self.main_layout.addWidget(card_frame)

        # Card layout
        card_layout = QVBoxLayout(card_frame)
        card_layout.setSpacing(15)
        card_layout.setContentsMargins(30, 25, 30, 30)

        # ============================================================
        # CARD STYLESHEET
        # ============================================================
        card_frame.setStyleSheet("""
            /* ============================================================
               MAIN CARD FRAME
               ============================================================ */
            QFrame#cardFrame {
                background-color: #ffffff;
                border-radius: 40px 40px 32px 32px;
                border: 1px solid rgba(255, 255, 255, 0.4);
                padding: 0px;
                max-width: 1200px;
                min-height: 600px;
                /* Prevent text selection */
            }
            
            /* Decorative top bar - shimmer effect */
            QFrame#cardFrame::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 6px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #001eff, stop:0.5 #4a6fff, stop:1 #001eff);
                border-radius: 40px 40px 0 0;
            }
            
            /* ============================================================
               HEADER SECTION
               ============================================================ */
            QFrame#headerContainer {
                background: transparent;
                border: none;
                padding: 0px;
            }
            
            /* School name */
            QLabel#schoolName {
                font-size: 60px;
                font-weight: 700;
                letter-spacing: -0.02em;
                color: #001eff;
                padding: 0px;
                margin: 0px;
            }
            
            QLabel#schoolSubtitle {
                font-size: 20px;
                font-weight: 500;
                color: #001eff;
                opacity: 0.8;
                letter-spacing: 2px;
                text-transform: uppercase;
                padding: 0px;
                margin: 0px;
            }
            
            /* School icon */
            QLabel#schoolIcon {
                font-size: 42px;
                color: #001eff;
                padding: 0px;
                margin: 0px;
            }
            
            /* Image */
            QLabel#schoolImage {
                border-radius: 12px;
                background: white;
                min-width: 100px;
                min-height: 100px;
                max-width: 120px;
                max-height: 120px;
            }
            
            /* ============================================================
               LOCATION BLOCK
               ============================================================ */
            QFrame#locationBlock {
                background: transparent;
                border-top: 2px dashed #d7e6e0;
                padding-top: 12px;
                margin-top: 8px;
            }
            
            QLabel#locationIcon {
                font-size: 18px;
                color: #001eff;
                padding: 0px;
                margin: 0px;
            }
            
            QLabel#locationText {
                font-size: 22px;
                font-weight: 500;
                color: #1d4237;
                background: rgba(0, 30, 255, 0.05);
                padding: 4px 12px 4px 8px;
                border-radius: 40px;
            }
            
            /* ============================================================
               TABLE DATA ITEMS
               ============================================================ */
            QFrame#dataItem {
                background: #f8faff;
                border: 1px solid #dce3ff;
                border-radius: 12px;
                padding: 12px 18px;
            }
            
            QFrame#dataItem:hover {
                background: #eef3ff;
                border-color: #001eff;
            }
            
            QLabel#dataIcon {
                font-size: 20px;
                color: #001eff;
                padding: 0px;
                margin: 0px;
                min-width: 30px;
                text-align: center;
            }
            
            QLabel#dataLabel {
                font-size: 10px;
                color: #7c9f91;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-weight: 600;
            }
            
            QLabel#dataValue {
                font-size: 14px;
                font-weight: 600;
                color: #0d3329;
            }
            
            QLabel#dataValue strong {
                color: #001eff;
            }
            
            /* ============================================================
               SCHOOL TAG
               ============================================================ */
            QFrame#schoolTag {
                background: #f0f4ff;
                border: 1px solid rgba(0, 30, 255, 0.15);
                border-radius: 60px;
                padding: 10px 20px;
                margin-top: 10px;
            }
            
            QLabel#tagItem {
                font-size: 13px;
                color: #1b4f3f;
                font-weight: 460;
                padding: 0px 8px;
            }
            
            QLabel#tagItem strong {
                color: #001eff;
                font-weight: 600;
            }
            
            QLabel#tagIcon {
                font-size: 14px;
                color: #001eff;
                padding: 0px;
                margin: 0px;
                min-width: 18px;
                text-align: center;
            }
            
            /* ============================================================
               FUTURE GRID ITEMS
               ============================================================ */
            QFrame#futureGridItem {
                background: #f8faff;
                border: 2px dashed #dce3ff;
                border-radius: 12px;
                padding: 5px 5px;
                min-height: 120px;
            }
            
            QFrame#futureGridItem:hover {
                border-color: #001eff;
                background: #eef3ff;

                

            }
            
            QLabel#placeholderIcon {
                font-size: 32px;
                color: #dce3ff;
                padding: 0px;
                margin: 0px 0px 8px 0px;
            }
            
            QLabel#placeholderText {
                font-size: 12px;
                color: #a0b4c8;
                font-weight: 500;
                letter-spacing: 0.5px;
                text-transform: uppercase;
                opacity: 0.6;
                text-align: center;
                line-height: 1.5;
            }
            
            /* ============================================================
               ATTRIBUTION
               ============================================================ */
            QLabel#attribution {
                font-size: 10px;
                color: #7c9f91;
                background: #f0f4ff;
                letter-spacing: 0.3px;
                padding-top: 8px;
                margin-top: 10px;
                border-top: 1px solid #e0ede7;
                text-align: right;
            }
            
        """)

        # ============================================================
        # HEADER CONTAINER - School Name + Image
        # ============================================================
        header_frame = QFrame()
        header_frame.setObjectName("headerContainer")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setSpacing(20)
        header_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.addWidget(header_frame)

        # Left side - School name
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(0)
        left_layout.setContentsMargins(0, 0, 0, 0)

        # School name with icon
        name_layout = QHBoxLayout()
        name_layout.setSpacing(12)
        name_layout.setContentsMargins(0, 0, 0, 0)

        # icon_label = QLabel("🏫")
        # icon_label.setObjectName("schoolIcon")
        # name_layout.addWidget(icon_label)

        name_text_layout = QVBoxLayout()
        name_text_layout.setSpacing(0)

        school_name = QLabel("Guintas")
        school_name.setObjectName("schoolName")
        name_text_layout.addWidget(school_name)

        school_subtitle = QLabel("Elementary School")
        school_subtitle.setObjectName("schoolSubtitle")
        name_text_layout.addWidget(school_subtitle)

        name_layout.addLayout(name_text_layout)
        name_layout.addStretch(1)
        left_layout.addLayout(name_layout)

        header_layout.addWidget(left_widget, 1)

        # Right side - Image
        image_widget = QLabel()
        image_widget.setObjectName("schoolImage")
        image_widget.setMinimumHeight(300)
        image_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Load image
        image_path = r"C:\Users\O.Feronel\OneDrive - ams OSRAM\Documents\PYTHON_EXTERN_PROJ\GUINTAS_ELEM_GRADING_SYSTEM\img\image.png"
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                image_widget.setPixmap(pixmap)
        else:
            image_widget.setText("📸")
            image_widget.setStyleSheet("font-size: 40px;")
        
        header_layout.addWidget(image_widget)

        # ============================================================
        # LOCATION BLOCK
        # ============================================================
        location_frame = QFrame()
        location_frame.setObjectName("locationBlock")
        location_layout = QHBoxLayout(location_frame)
        location_layout.setSpacing(8)
        location_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.addWidget(location_frame)

        # loc_icon = QLabel("📍")
        # loc_icon.setObjectName("locationIcon")
        # location_layout.addWidget(loc_icon)

        location_text = QLabel("Guintas, Leganes, Iloilo")
        location_text.setObjectName("locationText")
        location_layout.addWidget(location_text)
        location_layout.addStretch()

        # ============================================================
        # TABLE DATA - Grid Layout
        # ============================================================
        data_grid = QGridLayout()
        data_grid.setSpacing(12)
        data_grid.setContentsMargins(0, 0, 0, 0)
        card_layout.addLayout(data_grid)

        # Data items
        data_items = [
            ("🕐", "School Hours", "7:00 AM - 5:00 PM"),
            ("📅", "Current Date", QDateTime.currentDateTime().toString("dddd, MMMM d, yyyy hh:mm AP")),
            ("📆", "School Year", "<strong>2026-2027</strong>"),
            ("👨‍🏫", "Faculty In-Charge", "<span style='color:#001eff; font-weight:700;'>Prof. Oliver D. Feronel</span>")
        ]

        # for i, (icon, label, value) in enumerate(data_items):
        #     item_frame = QFrame()
        #     item_frame.setObjectName("dataItem")
        #     item_layout = QHBoxLayout(item_frame)
        #     item_layout.setSpacing(12)
        #     item_layout.setContentsMargins(0, 0, 0, 0)

        #     icon_label = QLabel(icon)
        #     icon_label.setObjectName("dataIcon")
        #     item_layout.addWidget(icon_label)

        #     text_layout = QVBoxLayout()
        #     text_layout.setSpacing(2)
            
        #     label_text = QLabel(label)
        #     label_text.setObjectName("dataLabel")
        #     text_layout.addWidget(label_text)
            
        #     value_text = QLabel(value)
        #     value_text.setObjectName("dataValue")
        #     value_text.setTextFormat(Qt.TextFormat.RichText)
        #     if label == "Current Date":
        #         value_text.setObjectName("currentDateLabel")
        #     text_layout.addWidget(value_text)
            
        #     item_layout.addLayout(text_layout)
        #     item_layout.addStretch()
            
        #     data_grid.addWidget(item_frame, i // 2, i % 2)

        # ============================================================
        # SCHOOL TAG
        # ============================================================
        tag_frame = QFrame()
        tag_frame.setObjectName("schoolTag")
        tag_layout = QHBoxLayout(tag_frame)
        tag_layout.setSpacing(16)
        tag_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.addWidget(tag_frame)

        tags = [
            ("🏳️", "<strong>Region VI</strong> · Western Visayas"),
            ("📅", "established <strong>1968</strong>"),
            ("🏫", "Public Elementary")
        ]

        for icon, text in tags:
            tag_widget = QWidget()
            tag_widget_layout = QHBoxLayout(tag_widget)
            tag_widget_layout.setSpacing(6)
            tag_widget_layout.setContentsMargins(0, 0, 0, 0)
            
            tag_icon = QLabel(icon)
            tag_icon.setObjectName("tagIcon")
            tag_widget_layout.addWidget(tag_icon)
            
            tag_label = QLabel(text)
            tag_label.setObjectName("tagItem")
            tag_label.setTextFormat(Qt.TextFormat.RichText)
            tag_widget_layout.addWidget(tag_label)
            
            tag_layout.addWidget(tag_widget)

        tag_layout.addStretch()

        # ============================================================
        # FUTURE GRID CONTAINER
        # ============================================================
        future_grid = QGridLayout()
        future_grid.setSpacing(12)
        future_grid.setContentsMargins(0, 0, 0, 0)
        card_layout.addLayout(future_grid)

        future_items = [
            ("➕", "Future Feature\nComing Soon"),
            ("➡️", "Future Feature\nComing Soon"),
            ("⭐", "Future Feature\nComing Soon"),
            ("⚙️", "Future Feature\nComing Soon")
        ]

        for i, (icon, text) in enumerate(future_items):
            item_frame = QFrame()
            item_frame.setObjectName("futureGridItem")
            item_layout = QVBoxLayout(item_frame)
            item_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            item_layout.setSpacing(6)

            icon_label = QLabel(icon)
            icon_label.setObjectName("placeholderIcon")
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            item_layout.addWidget(icon_label)

            text_label = QLabel(text)
            text_label.setObjectName("placeholderText")
            text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            text_label.setWordWrap(True)
            item_layout.addWidget(text_label)

            future_grid.addWidget(item_frame, i // 2, i % 2)

        # ============================================================
        # ATTRIBUTION
        # ============================================================
        attribution = QLabel("📍 Guintas, Leganes, Iloilo · Philippines")
        attribution.setObjectName("attribution")
        card_layout.addWidget(attribution)

        # Start timer for date updates
        self.update_date()