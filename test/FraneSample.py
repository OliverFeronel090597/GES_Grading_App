import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QFrame, QLabel, QComboBox, QPushButton,
    QGroupBox, QSpinBox, QColorDialog, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor

class FrameTester(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QFrame Tester with QSS - PyQt6")
        self.setGeometry(100, 100, 700, 650)
        
        # Default colors
        self.bg_color = "#f0f4f8"
        self.border_color = "#2c3e50"
        self.border_radius = 5
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        
        # Control panel
        controls = QGroupBox("Frame Controls")
        controls.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: #ecf0f1;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background-color: #3498db;
                color: white;
                border-radius: 4px;
            }
        """)
        controls_layout = QVBoxLayout(controls)
        controls_layout.setSpacing(10)
        
        # Row 1: Shape selector
        shape_layout = QHBoxLayout()
        shape_label = QLabel("Shape:")
        shape_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        shape_layout.addWidget(shape_label)
        
        self.shape_combo = QComboBox()
        self.shape_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 2px solid #3498db;
                border-radius: 4px;
                background-color: white;
                min-width: 150px;
            }
            QComboBox:hover {
                border-color: #2980b9;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #3498db;
                margin-right: 5px;
            }
        """)
        shapes = [
            ("No Frame", QFrame.Shape.NoFrame),
            ("Box", QFrame.Shape.Box),
            ("Panel", QFrame.Shape.Panel),
            ("Styled Panel", QFrame.Shape.StyledPanel),
            ("H Line", QFrame.Shape.HLine),
            ("V Line", QFrame.Shape.VLine),
            ("Win Panel", QFrame.Shape.WinPanel)
        ]
        for name, shape in shapes:
            self.shape_combo.addItem(name, shape)
        self.shape_combo.currentIndexChanged.connect(self.update_frame)
        shape_layout.addWidget(self.shape_combo)
        shape_layout.addStretch()
        controls_layout.addLayout(shape_layout)
        
        # Row 2: Shadow selector
        shadow_layout = QHBoxLayout()
        shadow_label = QLabel("Shadow:")
        shadow_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        shadow_layout.addWidget(shadow_label)
        
        self.shadow_combo = QComboBox()
        self.shadow_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 2px solid #e67e22;
                border-radius: 4px;
                background-color: white;
                min-width: 150px;
            }
            QComboBox:hover {
                border-color: #d35400;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #e67e22;
                margin-right: 5px;
            }
        """)
        shadows = [
            ("Plain", QFrame.Shadow.Plain),
            ("Raised", QFrame.Shadow.Raised),
            ("Sunken", QFrame.Shadow.Sunken)
        ]
        for name, shadow in shadows:
            self.shadow_combo.addItem(name, shadow)
        self.shadow_combo.currentIndexChanged.connect(self.update_frame)
        shadow_layout.addWidget(self.shadow_combo)
        shadow_layout.addStretch()
        controls_layout.addLayout(shadow_layout)
        
        # Row 3: Line width and Mid line width
        width_layout = QHBoxLayout()
        width_label = QLabel("Line Width:")
        width_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        width_layout.addWidget(width_label)
        
        self.width_spin = QSpinBox()
        self.width_spin.setRange(0, 10)
        self.width_spin.setValue(3)
        self.width_spin.setStyleSheet("""
            QSpinBox {
                padding: 5px;
                border: 2px solid #27ae60;
                border-radius: 4px;
                background-color: white;
            }
            QSpinBox:hover {
                border-color: #229954;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #27ae60;
                border: none;
                border-radius: 2px;
                color: white;
            }
        """)
        self.width_spin.valueChanged.connect(self.update_frame)
        width_layout.addWidget(self.width_spin)
        
        mid_label = QLabel("Mid Line Width:")
        mid_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-left: 20px;")
        width_layout.addWidget(mid_label)
        
        self.mid_width_spin = QSpinBox()
        self.mid_width_spin.setRange(0, 10)
        self.mid_width_spin.setValue(1)
        self.mid_width_spin.setStyleSheet("""
            QSpinBox {
                padding: 5px;
                border: 2px solid #8e44ad;
                border-radius: 4px;
                background-color: white;
            }
            QSpinBox:hover {
                border-color: #7d3c98;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #8e44ad;
                border: none;
                border-radius: 2px;
                color: white;
            }
        """)
        self.mid_width_spin.valueChanged.connect(self.update_frame)
        width_layout.addWidget(self.mid_width_spin)
        width_layout.addStretch()
        controls_layout.addLayout(width_layout)
        
        # Row 4: Color controls
        color_layout = QHBoxLayout()
        
        # Background color
        bg_label = QLabel("BG Color:")
        bg_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        color_layout.addWidget(bg_label)
        
        self.bg_color_btn = QPushButton("Choose")
        self.bg_color_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.bg_color};
                border: 2px solid #2980b9;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.bg_color};
                border-color: #1a5276;
            }}
        """)
        self.bg_color_btn.clicked.connect(self.choose_bg_color)
        color_layout.addWidget(self.bg_color_btn)
        
        # Border color
        border_label = QLabel("Border Color:")
        border_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-left: 20px;")
        color_layout.addWidget(border_label)
        
        self.border_color_btn = QPushButton("Choose")
        self.border_color_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.border_color};
                border: 2px solid #2980b9;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
                color: white;
            }}
            QPushButton:hover {{
                background-color: {self.border_color};
                border-color: #1a5276;
            }}
        """)
        self.border_color_btn.clicked.connect(self.choose_border_color)
        color_layout.addWidget(self.border_color_btn)
        
        # Border radius
        radius_label = QLabel("Radius:")
        radius_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin-left: 20px;")
        color_layout.addWidget(radius_label)
        
        self.radius_spin = QSpinBox()
        self.radius_spin.setRange(0, 20)
        self.radius_spin.setValue(5)
        self.radius_spin.setStyleSheet("""
            QSpinBox {
                padding: 5px;
                border: 2px solid #f39c12;
                border-radius: 4px;
                background-color: white;
            }
            QSpinBox:hover {
                border-color: #e67e22;
            }
        """)
        self.radius_spin.valueChanged.connect(self.update_frame)
        color_layout.addWidget(self.radius_spin)
        
        color_layout.addStretch()
        controls_layout.addLayout(color_layout)
        
        # Row 5: Show Frame Shadow checkbox
        shadow_check_layout = QHBoxLayout()
        self.show_shadow_check = QCheckBox("Show Frame Shadow Effect")
        self.show_shadow_check.setStyleSheet("""
            QCheckBox {
                font-weight: bold;
                color: #2c3e50;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border: 2px solid #3498db;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db;
                border-color: #2980b9;
            }
        """)
        self.show_shadow_check.setChecked(True)
        self.show_shadow_check.stateChanged.connect(self.update_frame)
        shadow_check_layout.addWidget(self.show_shadow_check)
        shadow_check_layout.addStretch()
        controls_layout.addLayout(shadow_check_layout)
        
        main_layout.addWidget(controls)
        
        # Frame display
        display_group = QGroupBox("Frame Preview")
        display_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #2c3e50;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 10px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background-color: #2c3e50;
                color: white;
                border-radius: 4px;
            }
        """)
        display_layout = QVBoxLayout(display_group)
        
        # Create frame with visible QSS
        self.frame = QFrame()
        self.frame.setMinimumHeight(250)
        display_layout.addWidget(self.frame)
        
        # Info label
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("""
            QLabel {
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                color: #2c3e50;
            }
        """)
        display_layout.addWidget(self.info_label)
        
        # Current QSS display - MOVED BEFORE update_frame_qss()
        self.qss_label = QLabel()
        self.qss_label.setWordWrap(True)
        self.qss_label.setStyleSheet("""
            QLabel {
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 10px;
                background-color: #2c3e50;
                color: #ecf0f1;
                border-radius: 4px;
            }
        """)
        display_layout.addWidget(self.qss_label)
        
        main_layout.addWidget(display_group)
        
        # Initial update - NOW AFTER qss_label is created
        self.update_frame()
    
    def choose_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.bg_color = color.name()
            self.bg_color_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.bg_color};
                    border: 2px solid #2980b9;
                    border-radius: 4px;
                    padding: 5px 15px;
                    font-weight: bold;
                    color: {'black' if self.is_light_color(self.bg_color) else 'white'};
                }}
                QPushButton:hover {{
                    background-color: {self.bg_color};
                    border-color: #1a5276;
                }}
            """)
            self.update_frame()
    
    def choose_border_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.border_color = color.name()
            self.border_color_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.border_color};
                    border: 2px solid #2980b9;
                    border-radius: 4px;
                    padding: 5px 15px;
                    font-weight: bold;
                    color: {'black' if self.is_light_color(self.border_color) else 'white'};
                }}
                QPushButton:hover {{
                    background-color: {self.border_color};
                    border-color: #1a5276;
                }}
            """)
            self.update_frame()
    
    def is_light_color(self, color_hex):
        """Determine if a color is light or dark"""
        color = QColor(color_hex)
        brightness = (color.red() * 299 + color.green() * 587 + color.blue() * 114) / 1000
        return brightness > 128
    
    def update_frame_qss(self):
        """Apply QSS to the frame with current settings"""
        qss = f"""
            QFrame {{
                background-color: {self.bg_color};
                border: {self.width_spin.value()}px solid {self.border_color};
                border-radius: {self.radius_spin.value()}px;
                padding: 10px;
            }}
        """
        
        # Add shadow effect if enabled
        if self.show_shadow_check.isChecked():
            qss += f"""
                QFrame {{
                    border: {self.width_spin.value()}px solid {self.border_color};
                    border-radius: {self.radius_spin.value()}px;
                }}
            """
            # Add box shadow based on shadow style
            shadow = self.shadow_combo.currentData()
            if shadow == QFrame.Shadow.Raised:
                qss += f"""
                    QFrame {{
                        border: {self.width_spin.value()}px solid {self.border_color};
                        border-radius: {self.radius_spin.value()}px;
                        border-top-color: {self.lighten_color(self.border_color, 40)};
                        border-left-color: {self.lighten_color(self.border_color, 40)};
                        border-bottom-color: {self.darken_color(self.border_color, 40)};
                        border-right-color: {self.darken_color(self.border_color, 40)};
                    }}
                """
            elif shadow == QFrame.Shadow.Sunken:
                qss += f"""
                    QFrame {{
                        border: {self.width_spin.value()}px solid {self.border_color};
                        border-radius: {self.radius_spin.value()}px;
                        border-top-color: {self.darken_color(self.border_color, 40)};
                        border-left-color: {self.darken_color(self.border_color, 40)};
                        border-bottom-color: {self.lighten_color(self.border_color, 40)};
                        border-right-color: {self.lighten_color(self.border_color, 40)};
                    }}
                """
        
        self.frame.setStyleSheet(qss)
        self.qss_label.setText("Current QSS:\n" + qss.strip())
    
    def lighten_color(self, hex_color, amount):
        """Lighten a hex color by amount"""
        color = QColor(hex_color)
        h, s, l, a = color.getHsl()
        l = min(l + amount, 255)
        color.setHsl(h, s, l, a)
        return color.name()
    
    def darken_color(self, hex_color, amount):
        """Darken a hex color by amount"""
        color = QColor(hex_color)
        h, s, l, a = color.getHsl()
        l = max(l - amount, 0)
        color.setHsl(h, s, l, a)
        return color.name()
    
    def update_frame(self):
        # Get values from controls
        shape = self.shape_combo.currentData()
        shadow = self.shadow_combo.currentData()
        width = self.width_spin.value()
        mid_width = self.mid_width_spin.value()
        
        # Apply to frame (these work with QFrame's built-in drawing)
        self.frame.setFrameShape(shape)
        self.frame.setFrameShadow(shadow)
        self.frame.setLineWidth(width)
        self.frame.setMidLineWidth(mid_width)
        
        # Update QSS
        self.update_frame_qss()
        
        # Update info
        shape_name = self.shape_combo.currentText()
        shadow_name = self.shadow_combo.currentText()
        self.info_label.setText(
            f"Shape: {shape_name} | Shadow: {shadow_name} | "
            f"Line Width: {width} | Mid Line Width: {mid_width} | "
            f"Radius: {self.radius_spin.value()}px"
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application-wide style
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f6fa;
        }
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #1a5276;
        }
        QLabel {
            color: #2c3e50;
        }
        QGroupBox {
            background-color: white;
        }
    """)
    
    window = FrameTester()
    window.show()
    sys.exit(app.exec())